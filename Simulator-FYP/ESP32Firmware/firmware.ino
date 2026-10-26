#include <Wire.h>
#include <LSM6.h>
#include <LIS3MDL.h>
#include <LPS.h>
#include <ArduinoJson.h>
#include <WiFi.h>
#include <WiFiUdp.h>

LSM6 acc_giroscopio;
LIS3MDL magnetometro;
LPS altimetro;
WiFiUDP udp;

// Datos sobre la red.
const char* ssid = "SSID_NAME";
const char* contrasenna = "PASSWORD"; 
const char* IPdestino = "DESTINATIONIP";

// Puertos escucha Aplicaciones.
const int PUERTOIV = 65000; const int PUERTOSC = 5005;

// Conexiones Pines ESP32.
const int PINPOTENCIOMETRO = 34; const int VRX_PIN = 35;
const int VRY_PIN = 36;
const int SW_PIN = 25;

// Paquete UDP enviado al Simulador de Instrumentos de Vuelo.
struct PaqueteIV{
  float Mx, My, Mz;
  float Ax, Ay, Az;
  float Gx, Gy, Gz;
  float Altitud;
  float ValPot;
  // CUIDADO CON EL OVERFLOW EN EL CALCULO DEL DT.
  uint32_t Tiempo;
};

// Paquete UDP enviado al Simulador de Superficies de Control.
struct PaqueteSC{
  int x;
  int y;
  int sw;
};

PaqueteIV datosIV;
PaqueteSC datosSC;

void setup() {
  Serial.begin(9600);

  // Probamos el funcionamiento de los módulos de la IMU.
  WiFi.begin(ssid, contrasenna);

  // Pines IMU.
  Wire.begin(21, 22);      // SDA = 21; SCL = 22.

  // Conectamos a red WiFi.
  while (WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.println("Conectando a la red WiFi...");
  }

  // Verificamos funcionamiento módulos IMU.
  if (!acc_giroscopio.init()){
    Serial.println(("Módulo LSM5DS33 no detectado."));
    while(1);
  }
  if (!magnetometro.init()){
    Serial.println("Módulo LIS3MDL no detectado.");
    while(1);
  }
  if (!altimetro.init()){
    Serial.println("Módulo LPS25H no detectado.");
    while(1);
  }

  // Iniciamos puerto UDP de la ESP32.
  udp.begin(5000);

  // Pin Potenciómetro y Switch del Joystick como entrada.
  pinMode(PINPOTENCIOMETRO, INPUT);
  pinMode(SW_PIN, INPUT_PULLUP);

  acc_giroscopio.enableDefault();
  magnetometro.enableDefault();
  altimetro.enableDefault();

  // Configuramos Acelerómetro y Giroscopio.
  acc_giroscopio.writeReg(LSM6::CTRL1_XL, 0x60);
  acc_giroscopio.writeReg(LSM6::CTRL2_G, 0x60);

  Serial.println("Conectado a la red WiFi.");
  Serial.println("Módulo LSM5DS33 detectado, leyendo datos...");
  Serial.println("Módulo LIS3MDL detectado, leyendo datos...");
  Serial.println("Modulo LPS25H detectado, leyendo datos...");
}

void loop() {
  // Leemos datos del Acelerómetro y Giroscopio.
  acc_giroscopio.read();

  // Valores en g/seg.
  float ax = acc_giroscopio.a.x * 0.061 / 1000;
  float ay = acc_giroscopio.a.y * 0.061 / 1000;
  float az = acc_giroscopio.a.z * 0.061 / 1000;

  // Valores en grados/seg.
  float gx = acc_giroscopio.g.x * 8.75 / 1000;
  float gy = acc_giroscopio.g.y * 8.75 / 1000;
  float gz = acc_giroscopio.g.z * 8.75 / 1000;

  // Leemos datos Magnetómetro.
  magnetometro.read();
  float mx = magnetometro.m.x;
  float my = magnetometro.m.y;
  float mz = magnetometro.m.z;

  // Obtenemos la presión medida por el Altímetro / Barómetro.
  float presion = altimetro.readPressureInchesHg();
  // Calculamos altitud a partir de la presión barométrica.
  float altitud = altimetro.pressureToAltitudeFeet(presion,
     30.17);

  // Leemos datos del Potenciómetro  0 - 4095.
  float valPotenciometro = (float) analogRead(PINPOTENCIOMETRO); 

  // Leemos datos del Joystick.
  int x = analogRead(VRX_PIN);
  int y = analogRead(VRY_PIN);
  int sw = digitalRead(SW_PIN);

  uint32_t tiempo = millis();

  // Añadimos datos al paquete de IV.
  datosIV.Mx = mx; datosIV.My = my; datosIV.Mz = mz;
  datosIV.Ax = ax; datosIV.Ay = ay; datosIV.Az = az;
  datosIV.Gx = gx; datosIV.Gy = gy; datosIV.Gz = gz;
  datosIV.Altitud = altitud; datosIV.ValPot = valPotenciometro;
  datosIV.Tiempo = tiempo;

  // Añadimos datos al paquete de SC.
  datosSC.x = x; datosSC.y = y; datosSC.sw = sw;

  // Enviamos el paquete a través de UDP al Simulador (MATLAB).
  udp.beginPacket(IPdestino, PUERTOIV);
  udp.write((uint8_t*)&datosIV, sizeof(datosIV));
  udp.endPacket();

  // Enviamos el paquete a través de UDP a ECAM (Python).
  udp.beginPacket(IPdestino, PUERTOSC);
  udp.write((uint8_t*)&datosSC, sizeof(datosSC));
  udp.endPacket();
}
