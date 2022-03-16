from flask import Flask, jsonify, request,g, render_template
from flask import Flask, flash, request, redirect, url_for
from flask import Flask, session
import json
import requests

def sendUE4(adress, data):
    # The POST request to our node server
    res = requests.post('http://127.0.0.1:3000/in', json=data) 
    # Convert response data to json
    #returned_data = res.json() 
    #print(returned_data)

idata = {'mes': 'dfhdfhfh', 'usr': 'NaS7QA89nxLg9nKQAAAn', 'tag': 'flask'}

app = Flask(__name__)

@app.route('/')
def index():
    
    return render_template("index.html")

###RECEIVE INCOMING WEBSOCKET MSG FROM NODE.JS 
@app.route('/flask', methods=['GET', 'POST'])
def wsreceiver():
    if request.method == 'POST':
        #data = request.form
        data =request.get_json()
    else:
        data = request.args

    global idata
    idata = data
    #print(idata)


    #data["tag"] = "flask"
    #astring = data["usr"]
    #print(data)

    sendUE4.send('http://127.0.0.1:3000/in', data)


    return 
    
@app.route('/chat')
def chat():
    
    return render_template("chat.html")  #, data=idata


if __name__ == "__main__":
    app.run(port=5000, debug=True)


