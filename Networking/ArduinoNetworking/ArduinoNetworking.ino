// Some Libraries
#include <SPI.h>
#include <WiFiNINA.h>
#include <ArduinoMqttClient.h>

// Initialize the Wifi client
WiFiClient wifiClient;

// WiFi Credentials 
char ssid[] = "WiFi-19BE";      // Wifi SSID
char pass[] = "29806768";       // Wifi password

// Network status
int status = WL_IDLE_STATUS;

// Initialise MQTT
MqttClient mqttClient(wifiClient);

// MQTT server 
int port = 1883; 
char broker[] = "192.168.1.110";

// Show detailed log
bool detailed = true; 

// Control state
int thrust = 0; 
int pitch = 0;
int roll = 0;
int yaw = 0; 
int button = 0; 
int state[5] = {thrust, pitch, roll, yaw, button};

// Connecting to network function
void connectToAP() {
  
  while ( status != WL_CONNECTED) {
    
    Serial.println("[INFO] Starting UAV connection processes");
    
    Serial.print("[INFO] Attempting to connect to Network: ");
    Serial.print(ssid);
    Serial.println("...");
    
    // Connect to WPA/WPA2 network
    status = WiFi.begin(ssid, pass);
 
    // wait 1 second for connection:
    delay(1000);

    // status of three means connected
    if(status == WL_CONNECTED){
      Serial.println("[INFO] Successfully connected to the network");
      
      // Connection details
      if(detailed){
        // Network SSID  
        Serial.print("[INFO] SSID: ");
        Serial.println(WiFi.SSID());
  
        // Device IP address
        IPAddress ip = WiFi.localIP(); 
        Serial.print("[INFO] IP Address: ");
        Serial.println(ip);
        }
        
      }else{
        Serial.print(".");
    }
  }
} 

// Connecting to MQTT Broker
void connectToMQTT(){

  Serial.println("[INFO] Attempting to connect to MQTT Broker...");
  
  while(!mqttClient.connect(broker, port)) {
  
    Serial.print("[ERROR] MQTT connection failed! Error code = ");
    Serial.println(mqttClient.connectError());
    
    // wait 1 second for connection:
    //delay(1000);
  }
  Serial.println("[INFO] Successfully connected to MQTT Broker");
}
  
// Setup function
void setup() {

  // Initialise and wait for port to open 
  Serial.begin(9600); 
  while(!Serial){
  }

  // Checking for wifi module
  if(WiFi.status() == WL_NO_MODULE){
    Serial.println("[ERROR] Wifi module failed");
    while(true);    
  }
  
  Serial.println("[INFO] UAV init begin ");
  
  // Connecting to network 
  connectToAP();  

  // Connecting to MQTT
  connectToMQTT(); 

  // Subscribing to topics
  mqttClient.subscribe("~/heartbeat");
  mqttClient.subscribe("~/control/thrust");
  mqttClient.subscribe("~/control/pitch");
  mqttClient.subscribe("~/control/roll");
  mqttClient.subscribe("~/control/yaw");
  mqttClient.subscribe("~/control/button");
}

void loop() {
  
  int messageSize = mqttClient.parseMessage();
  
  if (messageSize) {

    String topic = mqttClient.messageTopic();
    
    int i = 0; 
    char buffer[4];
    
    // use the Stream interface to print the contents
    while (mqttClient.available()) {
      buffer[i] = (char)mqttClient.read();
      i++;
    }
    buffer[i + 1] = '\0'; 
    
    if(topic == "~/control/thrust"){
      thrust = atoi(buffer);
    }
    if(topic == "~/control/pitch"){
      pitch = atoi(buffer);
    }
    if(topic == "~/control/roll"){
      roll =  atoi(buffer);
    }
    if(mqttClient.messageTopic() == "~/control/yaw"){
      yaw =  atoi(buffer);
    }
    if(mqttClient.messageTopic() == "~/control/button"){
      button =  atoi(buffer);
    }
  }
}
