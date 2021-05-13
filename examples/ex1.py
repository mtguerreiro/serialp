import serialp

# --- Input ---
COM = 'COM4'
baud = 115200
to = 1

ser = serialp.serial.Serial(COM, baud, to)

data = [0, 200]

#ser.send(0x01, data)
