import network

def do_connect(wifi_sid, wifi_pas):
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(wifi_sid, wifi_pas)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())