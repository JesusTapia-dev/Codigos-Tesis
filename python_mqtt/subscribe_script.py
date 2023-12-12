import matplotlib.pyplot as plt
import matplotlib.animation as animation
import paho.mqtt.client as mqtt
import numpy as np
subscribe_topic="tesis/AnalogRaw"
broker_address = "192.168.43.149"
analogRawMatriz=[]
contador = 0
data=[]
def init():
    ax.set_ylim(900, 1800)  # Ajusta los límites de la gráfica según tus necesidades
    ax.set_xlim(0,30)
    line.set_data([], [])
    return line,
def update(frame):
    y_data = np.array(data)
    x_data = np.arange(len(y_data))
    line.set_data(x_data, y_data)
    return line,
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
    global analogRawMatriz
    global contador
    global data
    mensaje = float(msg.payload.decode())
    analogRawMatriz.append(mensaje)
    contador=contador+1
    if contador==500:
        contador=0
        valor_promedio = sum(analogRawMatriz) / len(analogRawMatriz)
        # potencia=1.5476*valor_promedio-91.898
        data.append(valor_promedio)
        data[:] = data[-30:]
        analogRawMatriz=[]
        print(valor_promedio)    
# Configurar el cliente MQTT
client = mqtt.Client()
# Configurar los callbacks
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port=1883, keepalive=60)
# Configuración de la gráfica
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_xlabel('Tiempo')
ax.set_ylabel('Analog Raw')
ax.grid(True) 
# Configuración de la animación
ani = animation.FuncAnimation(fig, update, frames=None, init_func=init, blit=True)
# Mantener la ejecución del programa para recibir mensajes
#client.loop_forever()
client.loop_start()
plt.show()
client.loop_stop()
""""
PARA UN IPP DE 10MS Y 10 US DE ANCHO, la ecuación sera:PotLinea= 1.5476*AnalogRaw-91.898
"""