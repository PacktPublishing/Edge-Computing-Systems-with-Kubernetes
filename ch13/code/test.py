import serial
import time
import string
import pynmea2

from geopy.geocoders import Nominatim
# Import module
 
# Initialize Nominatim API
geolocator = Nominatim(user_agent="geoapiExercises")


while True:
	port="/dev/cu.usbmodem144301"
#	print("1")
	ser=serial.Serial(port, baudrate=9600, timeout=0.5)
#	print("2")
	dataout = pynmea2.NMEAStreamReader()
#	print("3")
	newdata=ser.readline().decode('utf-8')
#	print("4",newdata[0:6],newdata[0:6]=="$GPRMC",newdata)

	if newdata[0:6] == "$GPRMC":
#		print("5")
		newmsg=pynmea2.parse(newdata)
		print(newmsg)
#		print("6")
		lat=newmsg.latitude
		lng=newmsg.longitude
#		alt=newmsg.altitude
#		print("7")
		gps = "Latitude=" + str(lat) + ", Longitude=" + str(lng)
		print(gps)

		# Get location with geocode
		location = geolocator.geocode(str(lat)+","+str(lng))
 
		# Display location
		print("\nLocation of the given Latitude, Longitude and Altitude:")
		print(location)
