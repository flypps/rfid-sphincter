# RFID sphincter

Use cheap standard RFID reader to trigger [OpenLabs sphincter](https://github.com/openlab-aux/sphincter).
Uses Flask and JQuery and stores everything to json file.


#### install

(tested on Raspberry Pi and odroid c1+ and BananaPi)

-> clone repo and __change__ *config.py*

-> install pyserial: *pip install pyserial*

-> install flask: *pip install flask*

-> run *app.py*

-> go to *https://[device]:[port]*

#### howto

It is very simple. If you put a known (in token list) token in front of RFID reader it will trigger the GPIO, if the token is unknown it will save it and you can add it.

So to add tokens you just need to put them in front of the reader and __after this__ you click the "Add RFID Token", submit a name and save it.

![webinterface](https://raw.githubusercontent.com/flypps/rfid-sphincter/master/static/sphincter.png)

![add token](https://raw.githubusercontent.com/flypps/rfid-sphincter/master/static/sphincter-add-token.png)

#### TLS cert
By default your app will create a new ssl cert on every run. If you want to have a permanent one change last line of _app.py_ from __ssl_context='adhoc'__ to __ssl_context=('cert.pem', 'key.pem')__

#### LOGS:
By default logs opening action with timestamp and token to __/tmp/RFID_log.txt__. You can disable this in config file.

#### TBD:
* redirect http to https
* add option for token deletion
* make tokens appear live
