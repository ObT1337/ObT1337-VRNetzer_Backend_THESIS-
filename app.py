from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, emit
#from flask_session import Session
import requests
import json
import os
from flask import jsonify
from engineio.payload import Payload
from PIL import Image
import string
import random
import csv
from io import StringIO
from uploader import *
from websocket_functions import *
from GlobalData import *
import logging
import re
from search import *
import random
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

#Payload.max_decode_packets = 50


app = Flask(__name__)
app.debug = False
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'



socketio = SocketIO(app, manage_session=False)

### HTML ROUTES ###

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# note to self: 
# - only include 100% working code in releases
# - have homies commit stuff and star the git
# - make a webscraper for git and display contributors for a spec software in vr

@app.route('/search', methods=['GET'])
def searchR():
    term = request.args.get("term")
    return jsonify(search(term))


@app.route('/upload', methods=['GET'])
def upload():
    prolist = listProjects()
    return render_template('upload.html', namespaces=prolist)

@app.route('/Examples/CustomElements1')
def CustomElements1R():
    return render_template('geneElement.html')

@app.route('/Examples/ServerSideVar')
def ServerSideVarR():
    return render_template('scroll.html', data = scb1Data)

@app.route('/Examples/CustomElements2')
def test3():
    return render_template('test.html')






### DATA ROUTES###

###RECEIVE INCOMING WEBSOCKET MSG FROM NODE.JS 
@app.route('/flask', methods=['GET', 'POST'])
def ws_receiver():
    wsreceiver(socketio)
    return 

@app.route('/uploadfiles', methods=['GET', 'POST'])
def uploadR():
    return upload_files(request)

@app.route('/load_all_projects', methods=['GET', 'POST'])
def loadAllProjectsR():
    return jsonify(projects=listProjects())

@app.route('/load_project/<name>', methods=['GET', 'POST'])
def loadProjectInfoR(name):
    return loadProjectInfo(name)

@app.route('/projectAnnotations/<name>', methods=['GET'])
def loadProjectAnnotations(name):
    return loadAnnotations(name)

@app.route('/main', methods=['GET'])
def main():
    username = request.args.get("usr")
    project = request.args.get("project")
    if username is None:
        username = str(random.randint(1001,9998))
    else:
        username = username + str(random.randint(1001,9998))
        print(username)
    
    if project is None:
        project = "none"
    else:
        print(project)

    if(request.method=='GET'):

        room = 1
        #Store the data in session
        session['username'] = username
        session['room'] = room
        #prolist = listProjects()
        if project != "none":
            folder = 'static/projects/' + project + '/'
            with open(folder + 'pfile.json', 'r') as json_file:
                global pfile
                pfile = json.load(json_file)
                #print(pfile)
            json_file.close()

            with open(folder + 'names.json', 'r') as json_file:
                global names
                names = json.load(json_file)
                #print(names)
            json_file.close()
        return render_template('main.html', session = session, sessionData = json.dumps(sessionData), pfile = json.dumps(pfile))
    else:
        return "error"    

@app.route('/login/<usr>', methods=['GET'])
def loginR(usr):
    if(request.method=='GET'):
        username = usr 
        room = 1
        #Store the data in session
        session['username'] = username
        session['room'] = room
        return render_template('geneElement.html', session = session)
    else:
        return "error"
    

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if(request.method=='POST'):
        username = request.form['username'] 
        room = request.form['room']
        #Store the data in session
        session['username'] = username
        session['room'] = room
        return render_template('chat.html', session = session)
    else:
        if(session.get('username') is not None):
            session['username'] = 'reee'
            session['room'] = '2'
            return render_template('chat.html', session = session)
        else:
            return redirect(url_for('index'))


@app.route('/Test')
def test():
    return render_template('test.html')


@app.route('/nodepanel',methods=['GET'])
def nodepanel():
    #try:
    #    id = int(request.args.get("id"))
    #    if id is None:
    #        print("ID is none.")
    #        id=0
    #except:
    #    pass 

    if pfile:
        
        if "ppi" in pfile["name"].lower():
            try:
                id = int(request.args.get("id"))
            except:
                print("ID is none - ppi.")
                id=0
                    
            data = names['names'][id]
            print("C_DEBUG: PPI nodepanel")
        
            return render_template('nodepanelppi.html', data=data) 
        else:
            try:
                id = int(request.args.get("id"))
            except:
                print("ID is none.")
                id=0
                
            data = names['names'][id]
            print("C_DEBUG: general nodepanel")
        
            return render_template('nodepanel.html',data=data)
    else:
        try:
            id = int(request.args.get("id"))
            data = {'names':[id]} 
        except:
            print("ID is none - in outer if.")
            data = {'names':[0]}
        print("C_DEBUG: general nodepanel")
        
        return render_template('nodepanel.html',data=data)

###SocketIO ROUTES###


@socketio.on('join', namespace='/chat')
def join(message):
    room = session.get('room')
    join_room(room)
    print(bcolors.WARNING + session.get('username') + ' has entered the room.' + bcolors.ENDC)
    emit('status', {'msg':  session.get('username') + ' has entered the room.'}, room=room)


@socketio.on('ex', namespace='/chat')
def ex(message):
    room = session.get('room')
    print(bcolors.WARNING + session.get('username') + "ex: " + json.dumps(message) + bcolors.ENDC)
    message['usr'] = session.get('username')
    
    if message['id'] == 'projects':
        global sessionData
        sessionData['actPro'] = message['opt']

        print("changed activ project " + message['opt'])

    if message['id'] == 'search':
        if len(message["val"]) > 1:
            x = '{"id": "sres", "val":[], "fn": "sres"}'
            results = json.loads(x)
            results["val"] = search(message["val"])
            
            emit('ex',results, room=room)

    if message['id'] == 'nl':
        message['names'] = []
        message['fn'] = 'cnl'
        message['prot'] = []
        message['protsize'] = []
        for id in message['data']:
            message['names'].append(names['names'][id][0])
            
            if len(names['names'][id]) == 5:
                message['prot'].append(names['names'][id][3])
                message['protsize'].append(names['names'][id][4])
            else:
                message['prot'].append("x")
                message['protsize'].append(-1)
            
        print(message)
        emit('ex', message, room=room)
    
    else:
        emit('ex', message, room=room)
    #sendUE4('http://127.0.0.1:3000/in',  {'msg': session.get('username') + ' : ' + message['msg']})

@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    username = session.get('username')
    leave_room(room)
    session.clear()
    emit('status', {'msg': username + ' has left the room.'}, room=room)
    print(bcolors.WARNING + session.get('username') + ' has left the room.' + bcolors.ENDC)


if __name__ == '__main__':
    socketio.run(app)

