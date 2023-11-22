#include <WiFi.h>
#include <PubSubClient.h>

const char *ssid = "HUAWEI P smart";
const char *password = "12345678";
const char *mqtt_server = "192.168.43.149";
const int mqtt_port = 1883;
const char *mqtt_client_id = "ESP32_Client";
const char *subscribe_topic = "tesis/potenciaNominal";
const char *publish_topic = "tesis/potencia";
const char *publish_topic_voltage = "tesis/ReferenceVoltage";

WiFiClient espClient;
PubSubClient client(espClient);
float Vpk=0,Vout=0;
void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Conectando a ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("Conectado a la red WiFi");
  Serial.println("Dirección IP: ");
  Serial.println(WiFi.localIP());
}

void callback(char *topic, byte *payload, unsigned int length) {
  Serial.print("Mensaje recibido en el tópico: ");
  Serial.println(topic);
  // Convierte el payload a una cadena de caracteres
  char receivedValue[length + 1];
  strncpy(receivedValue, (char *)payload, length);
  receivedValue[length] = '\0';
  // Convierte la cadena a un número (en este caso, asume que es un float)
  float potenciaNominal = atof(receivedValue);
  // Realiza cálculos basados en la potencia nominal recibida (sustituye con tu lógica)
  Vpk= sqrt(10*potenciaNominal)/5;
  Vout=175.19*Vpk-101;

  // Publica el resultado en el tópico de voltaje
  char result[10];
  snprintf(result, sizeof(result), "%.2f", Vout);
  client.publish(publish_topic_voltage, result);
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Intentando conexión MQTT...");

    if (client.connect(mqtt_client_id)) {
      Serial.println("Conectado al servidor MQTT");
      client.subscribe(subscribe_topic);
    } else {
      Serial.print("Falló, rc=");
      Serial.print(client.state());
      Serial.println(" Intentando de nuevo en 5 segundos");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  char str[16];
  sprintf(str, "%u", random(100));
  client.publish(publish_topic, str);
  delay(500);
}
