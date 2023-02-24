import multiprocessing as mp
import os
import threading
import time

import uploader
from project import Project

from . import util

IGNORE_PROJECTS = ["process"]


class AnnotationScraper:
    def __init__(
        self,
    ):
        self.manager = mp.Manager()
        self.queue = self.manager.Queue()
        self.results = self.manager.Queue()
        self.done = self.manager.Value("all_done", False)
        self.pool = None
        self.pool_args = []
        self.handled_projects = {}
        self.handled_anno_requests = {}
        self.projects = [
            pro for pro in uploader.listProjects() if pro not in IGNORE_PROJECTS
        ]
        self.annotations = {}

    def init_pool(self, n=None):
        if n is None:
            n = len(self.projects)
        if n > os.cpu_count() - 1:
            n = os.cpu_count() - 1
        if n < 1:
            n = 1
        bg_args = (
            self.queue,
            self.results,
            self.done,
        )
        self.pool = mp.Pool(n)
        for _ in range(n):
            self.pool.apply_async(worker_task, bg_args)
        # for _ in range(n):
        #     worker_task(*bg_args)

    def update_annotations(self, project):
        for data_type in ["node", "link"]:
            self.add_to_queue(project, data_type, force=True)

    def add_to_queue(self, project, data_type, force=False):
        if not self.is_processing(project, data_type) or force:
            print("Adding to queue..", project, data_type, end="\r")
            all_jobs = []
            while not self.queue.empty():
                all_jobs.append(self.queue.get())
            if (project, data_type) in all_jobs:
                all_jobs.remove((project, data_type))
            all_jobs = [(project, data_type)] + all_jobs

            for job in all_jobs:
                self.queue.put(job)

            self.annotations[project] = {}
            if project not in self.handled_projects:
                self.handled_projects[project] = []

            self.handled_projects[project].append(data_type)

    def add_result_to_global_data(self, res):
        if res is None:
            return
        res = res[0]
        project = res["project"]
        data_type = res["type"]
        if project in self.annotations:
            if data_type not in self.annotations[project]:
                # print("Adding result to global data..", project, data_type)
                self.annotations[project][data_type] = res

    def start(self):
        for project in self.projects:
            for data_type in ["node", "link"]:
                self.add_to_queue(project, data_type)
        self.init_pool()
        waiter = ["/", "\\"]  # noqa
        i = 0
        while True:
            print(waiter[i], end="\r")
            if self.results.empty():
                time.sleep(1)
                continue
            res = self.results.get()
            self.add_result_to_global_data(res)
            if self.queue.empty() and self.all_projects_processed():
                break
            i = (i + 1) % 2

        self.done.value = True
        print("\nAll annotations scraped!")

        self.pool.close()
        self.pool.join()
        while not self.all_projects_processed() and not self.queue.empty():
            print("Annotation scraper idling...", end="\r")
            time.sleep(5)
        self.start()

    def all_projects_processed(self):
        for project in self.projects:
            for data_type in ["node", "link"]:
                processing, origin = self.is_processing(project, data_type)
                if processing:
                    if origin:
                        project = origin
                    if data_type not in self.annotations[project]:
                        return False
        return True

    def is_processing(self, project, data_type):
        project = Project(project)
        origin = project.origin
        if origin:
            project = project.origin
        else:
            project = project.name

        if project not in self.handled_projects:
            return False
        for data_type in ["node", "link"]:
            if data_type not in self.handled_projects[project]:
                return False
        return True, origin

    def wait_for_annotation(self, message):
        project = Project(message.get("project"), False)

        if project in IGNORE_PROJECTS:
            return

        requested_project = project.name
        data_type = message.get("type")
        if not project.exists():
            return
        # Handle copies of project to only process annotations once
        if project.get_origin():
            project = find_data_origin(project, data_type)
        # Reject multiple anno request for the same project and data type, e.g. multiple clients request while already processing.
        project = project.name
        if project in self.handled_anno_requests:
            if data_type in self.handled_anno_requests[project]:
                return
            self.handled_anno_requests[project].append(data_type)
        else:
            self.handled_anno_requests[project] = [data_type]

        arg = (project, data_type)
        while True:
            # print("Waiting for annotation", project, data_type)
            if project in self.handled_projects:
                if data_type in self.annotations[project]:
                    print("Annotation processed", project, data_type, end="\r")
                    break
                self.add_to_queue(*arg)
            else:
                self.add_to_queue(*arg)
            time.sleep(1)

        message = self.annotations[project][data_type]
        message["project"] = requested_project
        if project in self.handled_anno_requests:
            if data_type in self.handled_anno_requests[project]:
                self.handled_anno_requests[project].remove(data_type)
        # print("Sending annotation result for ", project, data_type)
        return message


class Worker(threading.Thread):
    def __init__(self, queue, results, all_done):
        threading.Thread.__init__(self)
        self.queue = queue
        self.results = results
        self.all_done = all_done

    def run(self):
        # print("Starting worker")
        while True and not self.queue.empty() or self.all_done.get():
            self.collect_annotations()
        # print("Worker done:")

    def collect_annotations(self):
        """Collects all the annotations of every project and stores them in the GlobalData."""
        project, data_type = self.queue.get()
        print("Collecting Anntoation for:", project, data_type, end="\r")
        message = {"project": project, "type": data_type}
        message = util.get_annotation(message, {})
        self.results.put(message)
        print("Done collecting annotation for:", project, data_type, end="\r")

    def collect_args(self, project, data_type):
        project = Project(project)
        tmp = Project(project.name)
        if project.origin:
            project = self.find_data_origin(tmp, data_type)
        return project.name, data_type


def find_data_origin(project, data_type):
    function_call = {
        "node": project.has_own_nodes,
        "link": project.has_own_links,
    }
    if data_type in function_call:
        if not function_call[data_type]():
            origin = Project(project.origin, check_exists=True)
            if origin.exists():
                project = origin
    return project


def worker_task(queue, results, all_done):
    worker = Worker(queue, results, all_done)
    worker.run()
