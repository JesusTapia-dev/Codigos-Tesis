import paho.mqtt.client as mqtt
from datetime import datetime
import numpy as np
import json
import time
subscribe_topic="tesis/test"
publish_topic="tesis/potencia"
broker_address = "localhost"#"192.168.43.149"
analogRawMatriz=[[],[],[],[],[],[],[],[]]
numMaxdatos=1000
contador = 0
data=[]
interval_start_time = time.time()
interval_duration=15 #duracion del intervalo en segundos para el envio de datos
def potenciaAncho10us(AnalogRaw):
    potencia=[0,0,0,0,0,0,0,0]
    m=1.5476
    b=-91.898
    for i in range(8):
        potencia[i]=m*AnalogRaw[i]+b
    return potencia

def potenciaAncho20us(AnalogRaw):
    potencia=[0,0,0,0,0,0,0,0]
    m=1.5476
    b=-91.898
    for i in range(8):
        potencia[i]=m*AnalogRaw[i]+b
    return potencia

def leer_datos_desde_txt(archivo):
    try:
        with open(archivo, 'r') as file:
            lineas = file.readlines()
            # Obtiene la segunda línea (índice 1)
            segunda_linea = lineas[1]
            datos = segunda_linea.strip().split()
            datos_numericos = [float(dato) for dato in datos]
            return datos_numericos
    except FileNotFoundError:
        print(f"El archivo '{archivo}' no fue encontrado.")
    except Exception as e:
        print(f"Error al leer el archivo: {e}")

def procesamiento_data(analogRawMatriz):
    if analogRawMatriz[0]:
        average_raw=[0,0,0,0,0,0,0,0,0]
        for i in range(8):
            average_raw[i] = sum(analogRawMatriz[i]) / len(analogRawMatriz[i])  
        if(ancho<15):
            potencia=potenciaAncho10us(average_raw)      
        if ancho>15 and ancho<25:
            potencia=potenciaAncho20us(average_raw)
        processed_data = {"Ancho_us":IPP,"average_potencia": potencia, "timestamp": datetime.now()}
        #client.publish(publish_topic, json.dumps(processed_data))
        print("---------------------------------------")
        print(average_raw)
        print(processed_data)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conexión exitosa con el broker")
        client.subscribe(subscribe_topic)
    else:
        print("Error de conexión. Código de retorno =", rc)
# Callback cuando se recibe un mensaje en el tópico suscrito
def on_message(client, userdata, msg):
    global analogRawMatriz
    global contador
    mensaje = msg.payload.decode()
    lista=json.loads(mensaje)
    if contador<numMaxdatos:
        for i in range(8):
            analogRawMatriz[i].append(lista[i])
            contador=contador+1
#Leo los datos de la configuracion
archivo_txt = 'commandPotencia.txt' 
datos_numericos = leer_datos_desde_txt(archivo_txt)
if len(datos_numericos)!=10:
    print("Hay más(o menos) valores de los que debería")
else:
    IPP_km=datos_numericos[0]
    IPP=IPP_km*1/150#IPP en ms
    Dutty=datos_numericos[1]
    ancho=IPP*Dutty*pow(10,3)/100
    potenciaNominal=datos_numericos[2:]
    
# Configurar el cliente MQTT
client = mqtt.Client()
# Configurar los callbacks
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port=1883, keepalive=60)
#client.loop_forever()

client.loop_start()
try:
    while True:
        # Verifica si ha pasado el intervalo de tiempo
        current_time = time.time()
        elapsed_time = current_time - interval_start_time
        if elapsed_time >= interval_duration:
            procesamiento_data(analogRawMatriz)  # Calcula la potencia y envía los datos al nuevo tópico
            interval_start_time = current_time  # Reinicia el temporizador del intervalo
            analogRawMatriz=[[],[],[],[],[],[],[],[]]
        # Puedes ajustar el tiempo de espera según tus necesidades
        time.sleep(1)

except KeyboardInterrupt:
    print("Programa detenido por el usuario.")
    #procesamiento_data()  # Asegúrate de enviar los datos acumulados antes de salir
    client.disconnect()
    client.loop_stop()
