import serial
import time
import string
import pynmea2
import os
import requests
import sys

while True:
	device = os.environ['DEVICE']
	ser=serial.Serial(device, baudrate=9600, timeout=0.5)
	dataout = pynmea2.NMEAStreamReader()
	newdata=ser.readline().decode('utf-8')

	if newdata[0:6] == "$GPRMC":
		newmsg=pynmea2.parse(newdata)
		lat = newmsg.latitude
		lng = newmsg.longitude
        data = {'lat': lat,'lng':lng
                ,'id':os.environ['CLIENT_ID']}
        r = requests.post(os.environ['ENDPOINT'],data=data)
        data['status'] = r.status
        print(str(data),file=sys.stderr)
