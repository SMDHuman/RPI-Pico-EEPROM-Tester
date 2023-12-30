from machine import Pin
from time import sleep
from random import randint

def int2binlist(data, lenght):
    data = max(min(2**lenght-1, data), 0)
    
    b = bin(data)[2:]
    b = "0"*(lenght - len(b)) + b
    return([int(i) for i in list(b)][::-1])

def goto(address):
    address = max(min(2**15-1, address), 0)
    address = int2binlist(address, 15)
    for i in range(15):
        addressPins[i].value(address[i])
    sleep(0.001)
    
def disable():
    WE.on()
    OE.on()
    CE.on()
    sleep(0.01)
    
def enable():
    WE.on()
    OE.on()
    CE.off()
    sleep(0.01)

def pushData(data):
    WE.on()
    OE.on()
    sleep(0.001)
    
    data = int2binlist(data, 8)
    for i in range(8):
        dataPins[i].init(dataPins[i].OUT)
        dataPins[i].value(data[i])
    sleep(0.001)
    
    WE.off()
    sleep(0.005)
    WE.on()
    sleep(0.001)
    
def pullData():
    WE.on()
    OE.off()
    sleep(0.001)
    
    data = 0
    for i in range(8):
        dataPins[i].init(dataPins[i].IN, dataPins[i].PULL_DOWN)
        data += dataPins[i].value() * 2**i
        
    sleep(0.001)
    OE.on()
    
    return(data)

A14      = Pin(28, Pin.OUT, value = 0)
A12, WE  = Pin(27, Pin.OUT, value = 0),  Pin(0, Pin.OUT, value = 1)
A7,  A13 = Pin(26, Pin.OUT, value = 0),  Pin(1, Pin.OUT, value = 0)
A6,  A8  = Pin(22, Pin.OUT, value = 0),  Pin(2, Pin.OUT, value = 0)
A5,  A9  = Pin(21, Pin.OUT, value = 0),  Pin(3, Pin.OUT, value = 0)
A4,  A11 = Pin(20, Pin.OUT, value = 0),  Pin(4, Pin.OUT, value = 0)
A3,  OE  = Pin(19, Pin.OUT, value = 0),  Pin(5, Pin.OUT, value = 1)
A2,  A10 = Pin(18, Pin.OUT, value = 0),  Pin(6, Pin.OUT, value = 0)
A1,  CE  = Pin(16, Pin.OUT, value = 0),  Pin(7, Pin.OUT, value = 1)
A0,  IO7 = Pin(17, Pin.OUT, value = 0),  Pin(8, Pin.IN, value = 0)
IO0, IO6 = Pin(11, Pin.IN, value = 0), Pin(9, Pin.IN, value = 0)
IO1, IO5 = Pin(12, Pin.IN, value = 0), Pin(10, Pin.IN, value = 0)
IO2, IO4 = Pin(13, Pin.IN, value = 0), Pin(14, Pin.IN, value = 0)
IO3      =                              Pin(15, Pin.IN, value = 0)

addressPins = [A0, A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14]
dataPins = [IO0, IO1, IO2, IO3, IO4, IO5, IO6, IO7]

disable()
enable()

randomData = [randint(0, 255) for i in range(2**7)]

#Write random data list into EEPROM
logged = 0
for a, data in enumerate(randomData):
    if(((a*100)//(len(randomData)-1)) % 2 == 0):
        if(not logged):
            print(f"Writing to: {a}")
            logged = 1
    else:
        logged = 0
        
    goto(a)
    pushData(data)

sleep(0.2)


#Read and check all data that writed
score = 0
logged = 0
for a, data in enumerate(randomData):
    if(((a*100)//(len(randomData)-1)) % 2 == 0):
        if(not logged):
            print(f"Reading from: {a}")
            logged = 1
    else:
        logged = 0
        
    goto(a)
    if(pullData() == data):
        score += 1
    
print(f"Score : {score}/{len(randomData)}")


disable()