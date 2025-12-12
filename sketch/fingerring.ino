// FingerRing alpha beta (very early acces) version
// install esp32-ble-gamepad librarie

// !!!!!!! WIFI ORE BLEUTOOTH MODE
// chainge for wifi ore bleutooth modes (comennt it out for bleutooth mode)
#define WIFI

// buttons
#define BUTTON_COUNT 4

#ifdef WIFI 
  #include <WiFi.h>
  #include <WiFiUdp.h>
  const char* ssid = "";
  const char* password = "";
  WiFiUDP udp;
  struct packet {
    int x;
    int y;
    bool b[BUTTON_COUNT];
  };
  packet data;
  const int port = 1234;
  int pc_port;
  IPAddress ip;
  bool conected = false;
#else
  #include <BleGamepad.h>
  BleGamepad bleGamepad("FingerRing", "FingerRing");
#endif

// conectt joystick to 3.3V and any pins
// avoid pins 2, 13, 12
#define JS_X_PIN 32
#define JS_Y_PIN 33
const int b_pins[BUTTON_COUNT] = {14, 27, 26, 25};



void setup() {
  Serial.begin(115200);
  pinMode(JS_X_PIN, INPUT);
  pinMode(JS_Y_PIN, INPUT);
  analogSetAttenuation(ADC_11db); // ADC atanuattion for ~3.3V input

  for(int i = 0; i < BUTTON_COUNT; ++i)
    pinMode(b_pins[i], INPUT_PULLUP);

  #ifdef WIFI
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    Serial.println("\nconection to wi fi..");
 
    while(WiFi.status() != WL_CONNECTED){
        Serial.print(".");
        delay(100);
    }
 
    Serial.println("conected to wi fi");
    Serial.print("got ip: ");
    Serial.println(WiFi.localIP());
    udp.begin(port);
    Serial.print("waiting to conect on port....");
    Serial.println(port);
  #else
    bleGamepad.begin();
    Serial.println("waiting bleutooth conecttion...");
  #endif
}
int js_x, js_y, js_x_val, js_y_val;
bool b_pressed[BUTTON_COUNT], aux_b_pressed[BUTTON_COUNT];
void loop() {
  #ifdef WIFI
    if (udp.parsePacket()) 
    {
      char incoming[255];
      int len = udp.read(incoming, 255);
      if (len > 0) 
        incoming[len] = 0;
      
      if (strstr(incoming, "CONECT") != NULL) 
      {
        ip = udp.remoteIP();
        pc_port = udp.remotePort();
        conected = true;
        Serial.print("conected pc ");
        Serial.println(ip);
      }
    }
  #else
    if(!bleGamepad.isConnected())
      return;
  #endif

  for(int i = 0; i < BUTTON_COUNT; ++i)
    b_pressed[i] = !digitalRead(b_pins[i]);
  
  for(int i = 0; i < BUTTON_COUNT; ++i)
  {
    if(b_pressed[i] != aux_b_pressed[i])
      {
        #ifdef WIFI
        #else
          if(b_pressed[i])
            bleGamepad.press(i + 1);
          else
            bleGamepad.release(i + 1);
        #endif
      }
      aux_b_pressed[i] = b_pressed[i];
  }

  js_x = analogRead(JS_X_PIN);
  js_y = analogRead(JS_Y_PIN);

  #ifdef WIFI
    if (conected) 
    {
      js_x_val = map(js_x, 4095, 0, -32768, 32767);
      js_y_val = map(js_y, 0, 4095, -32768, 32767);

      data.x = js_x_val;
      data.y = js_y_val;
      for(int i = 0; i < BUTTON_COUNT; ++i)
        data.b[i] = b_pressed[i];

      udp.beginPacket(ip, pc_port);
      udp.write((const uint8_t*)&data, sizeof(packet));
      udp.endPacket();
      delay(10); 
    }
  #else
    js_x_val = map(js_x, 4095, 0, 0, 32737);
    js_y_val = map(js_y, 0, 4095, 0, 32737);
    bleGamepad.setX(js_x_val);
    bleGamepad.setY(js_y_val);
    bleGamepad.sendReport();
  #endif
}
