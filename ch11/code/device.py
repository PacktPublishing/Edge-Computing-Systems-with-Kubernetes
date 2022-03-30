import time
import board
import adafruit_dht
import psutil
import paho.mqtt.client as mqtt
import sys

# We first check if a libgpiod process is running. If yes, we kill it!
for proc in psutil.process_iter():
   if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
        proc.kill()
sensor = adafruit_dht.DHT11(board.D22)

mqhost="192.168.0.243"
client = mqtt.Client()
client.connect(mqhost, 1883, 60)

client.loop_start()

def main():
   while True:
      temperature = sensor.temperature
      humidity = sensor.humidity
      client.publish("sensor1",str({"temperature":int(temperature),"humidity":int(humidity)}))
      print({"temperature":int(temperature),"humidity":int(humidity)},file=sys.stderr)
      time.sleep(2)
try:
  main()
except KeyboardInterrupt:
  pass
finally:
  sensor.exit()
