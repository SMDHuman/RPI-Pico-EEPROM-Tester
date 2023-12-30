from machine import Pin

def disable():
    WE.on()
    OE.on()
    CE.on()
    
WE  = Pin(0, Pin.OUT, value = 1)
OE  = Pin(5, Pin.OUT, value = 1)
CE  = Pin(7, Pin.OUT, value = 1)

disable()