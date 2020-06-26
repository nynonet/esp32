import dht
import machine


d = dht.DHT22(machine.pin(4))

d.measure()

t = d.temperature()

d = d.humidity()


print( "temperatura")
print( t )

print( "humidade" )
print( d)  
