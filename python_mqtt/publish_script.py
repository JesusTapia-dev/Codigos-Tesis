import paho.mqtt.publish as publish

# Especificar la dirección del broker MQTT como localhost
broker_address = "localhost"

# Especificar el tópico al que deseas publicar
topico = "tu_topico_aqui"

# Mensaje que deseas publicar
mensaje = "Hola, mundo MQTT!"

# Publicar el mensaje en el tópico
publish.single(topico, mensaje, hostname=broker_address)
