import serialp
import time
import datetime
import matplotlib.pyplot as plt
plt.ion()

# --- Input ---
COM = 'COM4'
baud = 115200
to = 1

# --- Connection ---
ser = serialp.serial.Serial(COM, baud, to)

T = []
t = []

plt.figure()
plt.grid()

while True:
    ser.send(0x02, None)
    d = list(ser.read(0x02))[0]

    T.append(d)
    t.append(datetime.datetime.now())

    plt.cla()
    plt.plot(t, T, '--o')

    plt.pause(5)
    
    
