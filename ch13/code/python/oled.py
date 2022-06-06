from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306

import time

# rev.1 users set port=0
# substitute spi(device=0, port=0) below if using that interface
serial = i2c(port=1, address=0x3C)

# substitute ssd1331(...) or sh1106(...) below if using that device
device = ssd1306(serial)  #change to ssd1306, ssd1325, ssd1331, sh1106

import serial
import time
import string
import pynmea2
import requests

from geopy.geocoders import Nominatim
# Import module

# Initialize Nominatim API
geolocator = Nominatim(user_agent="geoapiExercises")

import os
import sys

while True:
   device_gps = os.environ['DEVICE']
   ser=serial.Serial(device_gps, baudrate=9600, timeout=0.5)
   dataout = pynmea2.NMEAStreamReader()
   newdata=ser.readline().decode('utf-8')

   if newdata[0:6] == "$GPRMC":
      try:
         newmsg=pynmea2.parse(newdata)
         lat = newmsg.latitude
         lng = newmsg.longitude

         with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="black", fill="black")
         with canvas(device) as draw:
            draw.text((10, 4),"next:", fill="white")
            draw.text((10, 16),"nextXYZ", fill="white")
         time.sleep(2)
         with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="black", fill="black")
         with canvas(device) as draw:
            location = geolocator.geocode(str(lat)+","+str(lng))
            draw.text((10, 4),"current:", fill="white")
            print(location,file=sys.stderr)
            draw.text((10, 16),"lat:"+str(lat), fill="white")
            draw.text((10, 28),"lng:"+str(lng), fill="white")
         time.sleep(2)

      except:
         print("No GPS data to send",file=sys.stderr)
         with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="black", fill="black")
         with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="black", fill="black")
            draw.text((10, 4),"No GPS signal", fill="white")