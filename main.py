import time
from machine import Pin

wifi_essid = 'NAME WIFI'
wifi_pass = 'password wifi'

#Url do FireBase
urlFireBase = "https://name_project.firebaseio.com/esp32.json"

led = Pin(13, Pin.OUT)    # led no pin 13 do ESP32

#Ler dados do FireBase
def lerdados():
    import urequests as ureq
    req = ureq.get( urlFireBase )
    return req.json()

#Conecta no WiFi
def conectarwifi():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect( wifi_essid, wifi_pass)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

#controla o led
def lampada( status ):
    led.value( status )

def ativar():
    while True:
            print('Lendo fireBase')
            dados = lerdados()
            
            print('Atribuindo os valores')
            lampada( dados['led'] )
            
            print('Espera 5 seg')
            time.sleep(5)