import paho.mqtt.client as mqtt

subscribe_topic="tesis/potencia"
broker_address = "192.168.43.149"
potenciaReal=[]
contador = 0
# Callback cuando se establece la conexión con el broker MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conexión exitosa con el broker")
        # Suscribirse a un tópico después de la conexión exitosa
        client.subscribe(subscribe_topic)
    else:
        print("Error de conexión. Código de retorno =", rc)
# Callback cuando se recibe un mensaje en el tópico suscrito
def on_message(client, userdata, msg):
    global potenciaReal
    global contador
    mensaje = float(msg.payload.decode())
    potenciaReal.append(mensaje)
    contador=contador+1
    if contador==20:
        contador=0
        valor_promedio = sum(potenciaReal) / len(potenciaReal)
        potenciaReal=[]
        print(valor_promedio)    
# Configurar el cliente MQTT
client = mqtt.Client()
# Configurar los callbacks
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port=1883, keepalive=60)
# Mantener la ejecución del programa para recibir mensajes
client.loop_forever()
