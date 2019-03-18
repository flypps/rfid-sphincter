name="Sphincter RFID Admin Panel"
database = "rfid_list.json"
webuser = "admin"
webpass = "admin"
secret = b'benutz1gescheitesSecret!'
serialport = "/dev/ttyUSB0"
baudrate = 9600
doorpin = 1 #GPIO which the door is connected to
host = '0.0.0.0' #if you want to have this listen only on localhost change to '127.0.0.1'
port = 2342
backups = 1 #create a backup of the json token file in /save, disable with 0.
log = 1 #create temporary log file in: /tmp/RFID_log.txt