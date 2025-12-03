import network
import socket
from machine import Pin, SPI
import time

# ---- WiFi ----
SSID = "TVA_WIFI"
PASSWORD = "TVE_HESLO"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    time.sleep(0.1)

print("Connected:", wlan.ifconfig())

# ---- MAX7219 INIT ----

spi = SPI(0, baudrate=10000000, polarity=0, phase=0,
          sck=Pin(2), mosi=Pin(3))
cs = Pin(5, Pin.OUT)

def max7219_write(reg, data):
    cs.value(0)
    spi.write(bytearray([reg, data]))
    cs.value(1)

# MAX7219 registers
DECODE_MODE = 0x09
INTENSITY = 0x0A
SCAN_LIMIT = 0x0B
SHUTDOWN = 0x0C
DISPLAY_TEST = 0x0F

# Initialize matrix
max7219_write(SCAN_LIMIT, 7)
max7219_write(DECODE_MODE, 0)
max7219_write(INTENSITY, 8)
max7219_write(SHUTDOWN, 1)
max7219_write(DISPLAY_TEST, 0)

# Framebuffer: 8×8
matrix = [[0]*8 for _ in range(8)]

def refresh_matrix():
    for row in range(8):
        byte = 0
        for col in range(8):
            byte |= (matrix[row][col] << col)
        max7219_write(row+1, byte)

# ---- HTTP SERVER ----
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(5)
print("HTTP server running")

def handle_request(request):
    try:
        path = request.split(" ")[1]
        print("Path:", path)

        # Example: /set/3/5/1  (row=3, col=5, value=1)
        if path.startswith("/set/"):
            _, _, r, c, v = path.split("/")
            r = int(r)
            c = int(c)
            v = int(v)
            matrix[r][c] = v
            refresh_matrix()
            return "OK"
        return "INVALID"
    except:
        return "ERR"

while True:
    client, addr = s.accept()
    req = client.recv(1024).decode()
    print("Client:", addr)

    response = handle_request(req)

    client.send("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n")
    client.send(response)
    client.close()
