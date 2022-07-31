#include "heltec.h"
#define BAND    915E6

//Sensor libraries
#include "DHT.h"
#define DHTPIN 17     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

#define DEVICE 1
#define DELAY 3000 //Delay for 3 seconds

void setup()
{
  Heltec.begin(false,true,true,true,BAND);
  Serial.begin(9600);
  LoRa.setSyncWord(0xF3);
  Serial.println("LoRa started");
  dht.begin();
}

void sendTH()
{
  String values = "";
  LoRa.beginPacket();
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(h) || isnan(t)) {
    Serial.println(F("Failed to get data from sensor"));
    return;
  } 
  String hS = (String)h;
  String tS = (String)t;
  String dS = (String)DEVICE;
  values = "{\"t\":"+tS+",\"h\":"+hS+",\"d\":"+dS+"}";
  Serial.println(values);
  LoRa.print(values);
  LoRa.endPacket();
}

void loop()
{
  delay(DELAY);
  sendTH();
}
