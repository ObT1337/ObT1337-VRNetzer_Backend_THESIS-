from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
from GlobalData import *
from flask import jsonify
from engineio.payload import Payload
from PIL import Image
import csv
from io import StringIO




def makeProjectFolders(name):
    path = "static/projects/" + name
    pfile = {}
    pfile["name"] = name
    pfile["layouts"] = []
    pfile["layoutsRGB"] = []
    pfile["links"] = []
    pfile["linksRGB"] = []
    pfile["selections"] = []
    

    try:
        os.mkdir(path)
        os.mkdir(path + '/layouts')
        os.mkdir(path + '/layoutsl')
        os.mkdir(path + '/layoutsRGB')
        os.mkdir(path + '/links')
        os.mkdir(path + '/linksRGB')

        with open(path + '/pfile.json', 'w') as outfile:
            json.dump(pfile, outfile)

    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

def loadProjectInfo(name):
    folder = 'static/projects/' + name + '/'
    layoutfolder = folder + "layouts"
    layoutRGBfolder = folder + "layoutsRGB"
    linksRGBfolder = folder + "linksRGB"
    linkfolder = folder + "links"

    if os.path.exists(folder):

        layouts = [name for name in os.listdir(layoutfolder)]
        layoutsRGB = [name for name in os.listdir(layoutRGBfolder)]
        links = [name for name in os.listdir(linkfolder)]
        linksRGB = [name for name in os.listdir(linksRGBfolder)]

        return jsonify(
            layouts=layouts,
            layoutsRGB=layoutsRGB,
            links = links,
            linksRGB = linksRGB 
        )
    else:
        return 'no such project'
def loadAnnotations(name):
    namefile = 'static/projects/' + name + '/names.json'
    f = open(namefile)
    data = json.load(f)
    return data

def listProjects():
    folder = 'static/projects'
    sub_folders = [name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))]
    print(sub_folders)
    return sub_folders


def makeNodeTex(project, name, file):

    f = StringIO(file)
    csvreader = csv.reader(f, delimiter=',')
    elem = sum(1 for x in csvreader)
    f.seek(0)
    csvreader = csv.reader(f, delimiter=',')
    hight = 128 * (int(elem / 16384) + 1)

    print ("hight is " + str(hight))
    size = 128 * hight 
    path = 'static/projects/' + project 
    
    texh = [(0,0,0)] * size
    texl = [(0,0,0)] * size
    texc = [(0,0,0,0)] * size

    new_imgh = Image.new('RGB', (128, hight))
    new_imgl = Image.new('RGB', (128, hight))
    new_imgc = Image.new('RGBA', (128, hight))
    
    i = 0
    attrlist = {}
    attrlist['names'] = []

    try:
        for row in csvreader:
            #print(row[7])
            my_list = row[7].split(";")
            attrlist['names'].append(my_list)
            
            x = int(float(row[0])*65280)
            y = int(float(row[1])*65280)
            z = int(float(row[2])*65280)
            r = int(row[3])
            g = int(row[4])
            b = int(row[5])
            a = int(row[6])
            xh = int(x / 255)
            yh = int(y / 255)
            zh = int(z / 255)
            xl = x % 255
            yl = y % 255
            zl = z % 255
            pixelh = (xh,yh,zh)
            pixell = (xl,yl,zl)
            pixelc = (r,g,b,a)
            texh[i] = pixelh
            texl[i] = pixell
            texc[i] = pixelc
            #print(row)
            i += 1

    except (IndexError, ValueError):
        return '<a style="color:red;">ERROR </a>' + name + " nodefile malformated?" 
    
    with open(path + '/names.json', 'w') as outfile:
        json.dump(attrlist, outfile)

    new_imgh.putdata(texh)
    new_imgl.putdata(texl)
    new_imgc.putdata(texc)
        
    pathXYZ = path + '/layouts/' +  name + 'XYZ.bmp'
    pathXYZl = path + '/layoutsl/' +  name + 'XYZl.bmp' 
    pathRGB = path + '/layoutsRGB/' +  name +  'RGB.png'

    if os.path.exists(pathXYZ):
        return '<a style="color:red;">ERROR </a>' +  name + " Nodelist already in project"
    else:
        new_imgh.save(pathXYZ)
        new_imgl.save(pathXYZl)
        new_imgc.save(pathRGB, "PNG")
        return '<a style="color:green;">SUCCESS </a>' + name + " Node Textures Created"
    
    
    
def makeLinkTex(project, name, file):
    
    f = StringIO(file)
    csvreader = csv.reader(f, delimiter=',')
    elem = sum(1 for x in csvreader)
    f.seek(0)
    csvreader = csv.reader(f, delimiter=',')
    hight = 512 #int(elem / 512)+1
    path = 'static/projects/' + project 

    #with open('static/csv/'+ name +'.csv', newline='') as csvfile:
    #csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
 
    texl = [(0,0,0)] * 1024 * hight
    texc = [(0,0,0,0)] * 512 * hight
    new_imgl = Image.new('RGB', (1024, hight))
    new_imgc = Image.new('RGBA', (512, hight))
    i = 0
    try:
        for row in csvreader:

            sx = int(row[0]) % 128
            syl = int(int(row[0]) / 128) % 128
            syh = int(int(row[0]) / 16384)

            ex = int(row[1]) % 128
            eyl = int(int(row[1]) / 128) % 128
            eyh = int(int(row[1]) / 16384)

            if len(row) == 6:

                r = int(row[2])
                g = int(row[3])
                b = int(row[4])
                a = int(row[5])

            if len(row) == 2:
                r = 0
                g = 100
                b = 255
                a = 90

            pixell1 = (sx,syl,syh)
            pixell2 = (ex,eyl,eyh)
            pixelc = (r,g,b,a)

            if i < 262144:

                texl[i*2] = pixell1
                texl[i*2+1] = pixell2
                texc[i] = pixelc

            i += 1

    except (IndexError, ValueError):
        return '<a style="color:red;">ERROR </a>'  +  name + " Linkfile malformated?" 

    new_imgl.putdata(texl)
    new_imgc.putdata(texc)
    pathl = path + '/links/' +  name + 'XYZ.bmp'
    pathRGB = path + '/linksRGB/' +  name +  'RGB.png'

    if os.path.exists(pathl):
        return '<a style="color:red;">ERROR </a>' +  name  + " linklist already in project"
    else:
        new_imgl.save(pathl, "PNG")
        new_imgc.save(pathRGB, "PNG")
        return '<a style="color:green;">SUCCESS </a>' +  name +  " Link Textures Created"
    return "successfully created node textures and names file"

def upload_files(request):
    #print("namespace", request.args.get("namespace"))
    form = request.form.to_dict()
    #print(request.files)
    #print(form)
    prolist = listProjects()
    namespace = ''
    if form["namespace"] == "New":
        namespace = form["new_name"]
        
    else:
        namespace = form["existing_namespace"]
    if not namespace:
        return "namespace fail"
    
    # GET LAYOUT
    
    if namespace in prolist:
        print('project exists')
    else:
        # Make Folders
        makeProjectFolders(namespace)


    folder = 'static/projects/' + namespace + '/'
    pfile = {}

    with open(folder + 'pfile.json', 'r') as json_file:
        pfile = json.load(json_file)
    json_file.close()


    state = ''
    layout_files = request.files.getlist("layouts")

    if len(layout_files) > 0 and len(layout_files[0].filename) > 0:
        print("loading layouts", len(layout_files))
        print(layout_files[0])
        for file in layout_files:
            # TODO: fix the below line to account for dots in filenames
            name = file.filename.split(".")[0]
            contents = file.read().decode('utf-8')
            state = state + ' <br>'+  makeNodeTex(namespace, name, contents)
            pfile["layouts"].append(name + "XYZ")
            pfile["layoutsRGB"].append(name + "RGB")

            
            # print(contents)
            #x = validate_layout(contents.split("\n"))
            #print("layout errors are", x)
            #if x[1] == 0:
            
        #Upload.upload_layouts(namespace, layout_files)


    # GET EDGES
    edge_files = request.files.getlist("links")
    if len(edge_files) > 0 and len(edge_files[0].filename) > 0:
        print("loading links", len(edge_files))
        #Upload.upload_edges(namespace, edge_files)
        for file in edge_files:
            name = file.filename.split(".")[0]
            contents = file.read().decode('utf-8')
            pfile["links"].append(name + "XYZ")
            pfile["linksRGB"].append(name + "RGB")
            state = state + ' <br>'+ makeLinkTex(namespace, name, contents)
            
    #update the projects file
    with open(folder + 'pfile.json', 'w') as json_file:
        json.dump(pfile, json_file)

    global sessionData
    sessionData["proj"] = listProjects()

    return state
    

sessionData["proj"] = listProjects()
