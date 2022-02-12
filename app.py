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

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

USERS = {
    "Sanskruti": "+447879907243",
    "Ryan": "+447579065474"
}


@app.route('/')
def index():
    app.logger.info('test message')
    return 'Hello world'  

@app.route('/request', methods=["POST"])
def add_guide():
    #title = request.json['title']
    if("content" in request.json):
         content = request.json['content']
         print(content)     

    global username     
    username = request.json['userame']
    app.logger.info('test message')
    print(request.json)

    url=request.json['url']
    # url=base64.b64decode(url).decode("utf-8")
    print(url)
    if "youtube" in url:
        msg= "Watching Youtube :" + url
        send_text(msg)
    return ""

@app.route('/login',methods = ['POST'])  
def login():  
      uname=request.form['uname']  
      passwrd=request.form['pass']  
      if uname=="Ryan" and passwrd=="google1":  
          print(uname)
          return "Welcome %s" %uname 

def send_text(msg):
    print(msg)
    account_sid = 'ACec171a119c791c205c71a012fa72e967' 
    auth_token = '54192993a1830feed6ae781983befc23' 
    client = Client(account_sid, auth_token) 

    message = client.messages.create(
                              messaging_service_sid='MG16ab7d1555d148d28d80fbff12722672', 
                              body=msg,
                              to= USERS[username]
                              #send_at=send_when.isoformat() + 'Z',
                                #schedule_type='fixed'
                          )
    print(message.sid)

if __name__ == '__main__':
    app.run(host='http://0.0.0.0:7214')
    # app.run(host='https://browsermate.herokuapp.com/')


