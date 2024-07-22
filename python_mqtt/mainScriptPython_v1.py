import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from datetime import datetime, timezone, timedelta
import numpy as np
import json
import time
subscribe_topic="tesis/analogRaw"
publish_topic="atrad/test3"#"tesis/potencia"
broker_address = "10.10.10.102"#10.10.10.102"#"192.168.43.149"
analogRawMatriz=[[],[],[],[],[],[],[],[]]#guardamos los valores del 
numMaxdatos=1000 #definimos el numero máximo de datos a promediar
contador = 0
interval_start_time = time.time()
interval_duration=30 #duracion del intervalo (en segundos) para el envio de datos
def potenciaAncho10us(AnalogRaw):
    potencia=[0,0,0,0,0,0,0,0]
    m=1.5476
    b=-91.898
    for i in range(8):
        potencia[i]=m*AnalogRaw[i]+b
    return potencia

def potenciaAncho20us(AnalogRaw):
    potencia=[0,0,0,0,0,0,0,0]
    m=0.6233
    b=62.891
    for i in range(8):
        potencia[i]=m*AnalogRaw[i]+b
    return potencia
#la potencia default considera en general valores mayores a 100 us
def potenciaDefault(AnalogRaw):
    potencia=[0,0,0,0,0,0,0,0]
    m=0.6233
    b=62.891
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
        average_raw=[0,0,0,0,0,0,0,0]
        for i in range(8):
            average_raw[i] = sum(analogRawMatriz[i]) / len(analogRawMatriz[i])  
        if(ancho<15):
            potencia=potenciaAncho10us(average_raw)      
        if ancho>15 and ancho<25:
            potencia=potenciaAncho20us(average_raw)
        timestamp_actual = int(time.time())
        fecha_utc=datetime.utcfromtimestamp(timestamp_actual)
        zona_horaria_utc_menos_5 = timezone(timedelta(hours=-5))
        fecha_utc_menos_5 = fecha_utc.replace(tzinfo=timezone.utc).astimezone(zona_horaria_utc_menos_5)   
        fecha_legible=fecha_utc_menos_5.strftime('%d-%m-%Y %H:%M:%S')
        estado=[1 if x > 0 else 0 for x in potenciaNominal]
        processed_data = {"Ancho_us":IPP,"pow": potencia, "time": fecha_legible,"potenciaNominal":potenciaNominal,"status":estado,"threshold":threshold}
        client.publish(publish_topic, json.dumps(processed_data))
        print("---------------------------------------")
        print(average_raw)
        print(processed_data)
        print(type(processed_data["pow"]))

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
#Leo los datos de la configuracion y halla el ancho
archivo_txt = 'commandPotencia.txt' 
datos_numericos = leer_datos_desde_txt(archivo_txt)
if len(datos_numericos)!=11:
    print("Hay más(o menos) valores de los que debería")
else:
    IPP_km=datos_numericos[0]
    IPP=IPP_km*1/150#IPP en ms
    Dutty=datos_numericos[1]
    threshold=datos_numericos[2]
    ancho=IPP*Dutty*pow(10,3)/100
    potenciaNominal=datos_numericos[3:]
# Configurar el cliente MQTT
client = mqtt.Client()
# Configurar los callbacks
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port=1883, keepalive=60)

client.loop_start()
try:
    while True:
        # Verifica si ha pasado el intervalo de tiempo
        current_time = time.time()
        elapsed_time = current_time - interval_start_time
        if elapsed_time >= interval_duration:
            procesamiento_data(analogRawMatriz)  # Calcula la potencia y envía los datos
            interval_start_time = current_time  # Reinicia el temporizador del intervalo
            analogRawMatriz=[[],[],[],[],[],[],[],[]]
        time.sleep(1)

except KeyboardInterrupt:
    print("Programa detenido por el usuario.")
    client.disconnect()
    client.loop_stop()
#client.loop_forever()