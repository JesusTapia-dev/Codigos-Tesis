import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

MQTT_SERVER="10.10.10.102"
MQTT_PORT = 1883 

publishTopic="tesis/test"
broker_address = "localhost"
mensaje = "[10,20,30,40,50,60,70,80]"
# Publicar el mensaje en el tópico
publish.single(publishTopic, mensaje, hostname=MQTT_SERVER)