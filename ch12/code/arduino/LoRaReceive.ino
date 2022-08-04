#include "heltec.h"
#include "WiFi.h"
#include <HTTPClient.h>
#define BAND    915E6
#define METRICS_IP "192.168.0.241"

void setup()
{
  Heltec.begin(false, true, true, true, BAND);
  Serial.begin(9600);
  LoRa.setSyncWord(0xF3);
  Serial.println("LoRa started");
  WIFISetUp();
}

void WIFISetUp(void)
{
  WiFi.disconnect(true);
  delay(100);
  WiFi.mode(WIFI_STA);
  WiFi.setAutoConnect(true);
  WiFi.begin("NET_NAME","PASSWORD");
  delay(100);

  byte count = 0;
  while(WiFi.status() != WL_CONNECTED && count < 10)
  {
    count ++;
    delay(500);
    Serial.println("Connecting...");
  }
  if(WiFi.status() == WL_CONNECTED)
    Serial.println("Connected OK");
  else
    Serial.println("Failed");
}


void callURL(String data)
{
  String postData = data;
  Serial.println("Sending: " + postData);

  WiFiClient client;
  HTTPClient http;
  http.begin(client, "http://"+((String)METRICS_IP)+":3000/device");
  http.addHeader("Content-Type","application/json");
       
  int httpResponseCode = http.POST(postData);
  Serial.println("HTTP Response code xyz: "+(String)httpResponseCode);
  http.end();
}

void loop()
{
  onReceive(LoRa.parsePacket());
}

void onReceive(int packetSize)
{
  String incoming = "";
  if (packetSize == 0) return;

  while (LoRa.available())
    incoming += (char)LoRa.read();

  Serial.println("Received: " + incoming);
  callURL(incoming);
}