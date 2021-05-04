#AWS MQTT Broker "Mosquito" ESP32 "IOT" CONTROLLER REMOTE
#Andeson de Jesus de Menezes

#26/04/2021
#andeson@fasb.edu.br

from machine import Pin, PWM
import config
import wifi
import machine
from umqttsimple import MQTTClient
import ubinascii
import time
import struct

#use porta controller LED: ON/OFF
led = Pin( 4, Pin.OUT, value=0 )      #Publiced: pin1
Ok = Pin(2, Pin.OUT, value=0)
#use ports RGB PWM
red = PWM(Pin(5), duty=1023 ) #Publiced: red
gre = PWM(Pin(18), duty=1023) #Publiced: green
blu = PWM(Pin(19), duty=1023) #Publiced: blue

#connect to wifi
wifi.do_connect( config.wifi_ssid, config.wifi_pass )

#Id unique machine
client_id = ubinascii.hexlify(machine.unique_id())

#controller LED
def setLed( valor ):
    led.value(valor)
    if led.value() == 1:
        print("Led On")
    else:
        print("Led Off")
        
def setValor( porta, valor ):
    #print('valor = ', valor)
    porta.duty(1023-valor)

def sub_cb(topic, msg): #the action you want to happen, when you receive a msg
    print((topic, msg))
    #valor = msg.replace( 'b', '' )
    #print(type(msg))
    if topic == b'esp32/pin1':
        setLed( int(msg) )
    if topic == b'esp32/red':
        setValor( red, int(msg) )
    if topic == b'esp32/green':
        setValor( gre, int(msg) )
    if topic == b'esp32/blue':
        setValor( blu, int(msg) )
    
    
def ler():
    Ok.on()
    try:        
        mqtt = MQTTClient(client_id, config.aws_ip, user=config.mqtt_user, password=config.mqtt_pass)
        mqtt.set_callback( sub_cb )
        mqtt.connect()
        mqtt.subscribe("esp32/pin1")
        mqtt.subscribe("esp32/red")
        mqtt.subscribe("esp32/green")
        mqtt.subscribe("esp32/blue")
        while True:
            mqtt.wait_msg()
            time.sleep(1)
            
        mqtt.disconnect()
    except Exception as e:
        print("Falha!", e)
        Ok.off()
        time.sleep(10)
        machine.reset()

#Power led esp32 is runing
ler()