#!/usr/bin/python3
# coding=utf-8
__author__ = "flypps"
__credits__ = "dwhagawhdgajwgd"
__license__ = "GPL"
__version__ = "1.0"

from flask import Flask, flash, render_template, request, Response
from functools import wraps
import RPi.GPIO as GPIO
import threading
import serial
import json
import time
import config

# Set some defaults and values from config
app = Flask(__name__)
app.secret_key = config.secret
lasttoken = "None"
lastseen = 0
title = config.name

# Read json file
def jsondata():
    with open(config.database) as file:
        data = json.load(file)
    return data

# Open the door
# reinitialize the GPIO every time because we share it with Sphincter
def openup(rfid):
    if config.log == 1:
      file = open('/tmp/RFID_log.txt','a')
      file.write(time.ctime()+" Opening Door with token: "+rfid+"\n")
      file.close()
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(config.doorpin, GPIO.OUT)
    GPIO.output(config.doorpin, GPIO.HIGH)
    time.sleep(0.15)
    GPIO.output(config.doorpin, GPIO.LOW)
#    GPIO.cleanup()

# Check if tokens are valid
def rfid_checker(rfid):
  json_object = jsondata()
  for tokens in json_object:
    for mail, token in tokens.items():
      if token == rfid:
        openup(rfid)
      else:
          #print ("Unknown: "+rfid)
          global lasttoken
          global lastseen
          lasttoken = rfid
          lastseen = int(time.time())


#open serial port, read tokens and sanitize them
def read_rfid():
  rfid=""
  while True:
    try:
      ser = serial.Serial(config.serialport)
      ser.baudrate = config.baudrate
      rfid = ser.read(14)
      ser.close()
      rfid = rfid.replace("\x02", "" )
      rfid = rfid.replace("\x03", "" )
      #print(rfid)
      rfid_checker(rfid)
    except serial.serialutil.SerialException:
      return


#start rfid reader as daemon in background
try:
    RFIDreader = threading.Thread(target=read_rfid)
    RFIDreader.daemon=True
    RFIDreader.start()
except (KeyboardInterrupt, SystemExit):
    print ('\n! Killing RFID Reader!\n')


#create json for the javascript table
columns = [
  {
    "field": "mail",
    "title": "Name / E-Mail",
    "sortable": True,
  },
  {
    "field": "token",
    "title": "Token",
    "sortable": True,
  }
]


# Authentication for web frontend
# Using basic auth so you can use curl or something
def check_auth(username, password):
    return username == config.webuser and password == config.webpass

def authenticate():
    return Response(
    'Sorry you dont have access here.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# Create the default route
@app.route('/', methods=['GET', 'POST'])
@requires_auth
def index():
    if "addtoken" in request.form:
      if lastseen == 0:
        mins = "never before"
      else:
        mins = (int(time.time()) - lastseen)/60
      return render_template("add.html", lasttoken = lasttoken, minutes = mins, title=config.name)

    # form to add tokens and save them
    elif "user" in request.form:
	    text = request.form['user']
	    data=jsondata()
	    data.append({'mail':text, 'token':lasttoken})
	    #print(data)
	    with open(config.database, 'w') as outfile:
        	json.dump(data, outfile)
	    if config.backups == 1:
                save = 'tokensave/tokensave.json.' + str(time.time())
                with open(save, 'w') as savefile:
                    json.dump(data, savefile)
    else:
        pass
    return render_template("table.html",
        data=jsondata(),
        columns=columns,
        title=config.name)

if __name__ == '__main__':
    app.run(debug=True,host=config.host, port=config.port,ssl_context='adhoc')

