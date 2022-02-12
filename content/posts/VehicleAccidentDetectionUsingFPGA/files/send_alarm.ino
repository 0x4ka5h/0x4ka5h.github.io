#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"

#define AIO_SERVER      "io.adafruit.com"
#define AIO_SERVERPORT  1883
#define AIO_USERNAME    "g00g1y5p4"
#define AIO_KEY         "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  // Obtained from account info on io.adafruit.com          
int i=0;
int s=0;
int k=0;
int n=0;
/* Set these to your desired credentials. */
const char *ssid = "vivo 1610"; //Enter your WIFI ss
const char *password = "12345678"; //Enter your WIFI password


ESP8266WebServer server(80);
void handleRoot() {
      server.send(200, "text/html", "");
}


void handleSave() {
  if (server.arg("pass") != "") {
    Serial.println(server.arg("pass"));
  }
}

WiFiClient client;
 
// Setup the MQTT client class by passing in the WiFi client and MQTT server and login details.
Adafruit_MQTT_Client mqtt(&client, AIO_SERVER, AIO_SERVERPORT, AIO_USERNAME, AIO_KEY);
 
Adafruit_MQTT_Publish Attendance = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/iot");


void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  delay(3000);
  Serial.begin(115200);
  
  pinMode(0, INPUT_PULLUP);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  pinMode(4, INPUT);
  
  server.on("/Python", handleRoot);
  server.on ("/save", handleSave);
  server.begin();
  connect();
}
void connect() {
  Serial.print(F("Connecting to Adafruit IO... "));
  int8_t ret;
  while ((ret = mqtt.connect()) != 0) {
    switch (ret) {
      case 1: Serial.println(F("Wrong protocol")); break;
      case 2: Serial.println(F("ID rejected")); break;
      case 3: Serial.println(F("Server unavail")); break;
      case 4: Serial.println(F("Bad user/pass")); break;
      case 5: Serial.println(F("Not authed")); break;
      case 6: Serial.println(F("Failed to subscribe")); break;
      default: Serial.println(F("Connection failed")); break;
    }
 
    if(ret >= 0)
      mqtt.disconnect();
 
    Serial.println(F("Retrying connection..."));
    delay(5000);
  }
  Serial.println(F("Adafruit IO Connected!"));
  if (! Attendance.publish("g00g1y")){
          Serial.println(F("Failed"));
            } else {
              Serial.println(F("Sent!"));
  }
}
void loop() {
  server.handleClient();

  if (digitalRead(0)== HIGH){
      i=0;
      Serial.println("LOW");
  }else if(digitalRead(0)==LOW && i==0 ){
    k=0;
    if (s==0){
          if (! Attendance.publish("reset")) {    
          //Publish to Adafrui
              Serial.println(F("Failed"));
            } else {
              i+=1;
              Serial.println(F("Sent!"));
          }
    }
  
  }
  delay(1000);
  if (analogRead(4)>=250 && k==0){
      if (n==0){
         n+=1;
          if (! Attendance.publish("g00g1yg00g1y")) {    
          //Publish to Adafrui
              Serial.println(F("Failed"));
            } else {
              k+=1;
              Serial.println(F("Sent!"));
          }
    }
  }else if(analogRead(4)<=200 && k!=0){
      n=0;
      
  }
}
