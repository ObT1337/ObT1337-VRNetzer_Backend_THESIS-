import json
import re
from GlobalData import *

def search(term):
    project = sessionData["actPro"]
    if project != "none":
        folder = 'static/projects/' + project + '/'
        

        results = []
        i = 0
        with open(folder + 'names.json', 'r') as json_file:
            names = json.load(json_file)
            for name in names["names"]:
                for attr in name:
                    #contains: 
                    match = re.search(term, attr, re.IGNORECASE)
                    #match = re.match(term, attr, re.IGNORECASE)
                    if match:
                        res = {"id": i, "name": attr}
                        results.append(res)
                        break

                i += 1

        json_file.close()
    
    return results