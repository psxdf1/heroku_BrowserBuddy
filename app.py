# # app.py
# from flask import Flask, request, jsonify
# app = Flask(__name__)

# @app.route('/getmsg/', methods=['GET'])
# def respond():
#     # Retrieve the name from url parameter
#     name = request.args.get("name", None)

#     # For debugging
#     print(f"got name {name}")

#     response = {}

#     # Check if user sent a name at all
#     if not name:
#         response["ERROR"] = "no name found, please send a name."
#     # Check if the user entered a number not a name
#     elif str(name).isdigit():
#         response["ERROR"] = "name can't be numeric."
#     # Now the user entered a valid name
#     else:
#         response["MESSAGE"] = f"Welcome {name} to our awesome platform!!"

#     # Return the response in json format
#     return jsonify(response)

# @app.route('/post/', methods=['POST'])
# def post_something():
#     param = request.form.get('name')
#     print(param)
#     # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
#     if param:
#         return jsonify({
#             "Message": f"Welcome {name} to our awesome platform!!",
#             # Add this option to distinct the POST request
#             "METHOD" : "POST"
#         })
#     else:
#         return jsonify({
#             "ERROR": "no name found, please send a name."
#         })

# # A welcome message to test our server
# @app.route('/')
# def index():
#     return "<h1>Welcome to our server !!</h1>"

# if __name__ == '__main__':
#     # Threaded option to enable multiple instances for multiple user access support
#     app.run(threaded=True, port=5000)

from flask import Flask, request, jsonify
import base64
import os
from twilio.rest import Client
from twilio.rest import TwilioRestClient
from datetime import datetime
from datetime import datetime, timedelta
from flask_cors import CORS, cross_origin
import csv
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

def OA(_url):

    response = openai.Completion.create(
    engine="text-davinci-001",
    prompt=f" What is the content of the website : {_url}?",
    temperature=0,
    max_tokens=65,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response.choices[0].text


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
mydict = {}

# USERS = {
#     "Sanskruti": "+447879907243",
#     "Ryan": "+447579065474"
# }

# with open('csv_file.csv', mode='r') as inp:
#     reader = csv.reader(inp)
#     USERS = {rows[0]:rows[1] for rows in reader}


@app.route('/')
def index():
    app.logger.info('test message')
    return 'Hello world'  

@app.route('/request', methods=["POST"])
def add_guide():
    print(request.json)
    if("content" in request.json):
         content = request.json['content']
         print(content)     
    
    username = request.json['username']
    pn = request.json["number"]
    url=request.json['url']
    message = request.json["message"]
    message=message+ " \n Site Summary: " + OA(url)

    # url=base64.b64decode(url).decode("utf-8")
    print(url)
        # msg= "Watching Youtube :" + url
    print(username)
    print(pn)
    send_text(message, pn)
    return ""

@app.route('/login',methods = ['POST'])  
def login():  
      uname=request.form['uname']  
      passwrd=request.form['pass']  
      if uname=="Ryan" and passwrd=="google1":  
          print(uname)
          return "Welcome %s" %uname 
      else:
          return "Ask Ryan for access"

def send_text(msg,phonenumber):
    print(msg)
    account_sid = os.environ['T_AccountSID']
    auth_token = os.environ['T_auth_token']
    
    client = Client(account_sid, auth_token) 

    message = client.messages.create(
                              messaging_service_sid=os.environ['T_messaging_service_sid'], 
                              body=msg,
                              to= phonenumber
                              #send_at=send_when.isoformat() + 'Z',
                                #schedule_type='fixed'
                          )
    print(message.sid)

if __name__ == '__main__':
    app.run(host='http://0.0.0.0:7214')
    # app.run(host='https://browsermate.herokuapp.com/')


