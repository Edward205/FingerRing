# FingerRing alpha beta (very early acces)
# for pc with python and FingerRing wifi mode

import socket
import struct
import time
from pythonosc import udp_client

client = udp_client.SimpleUDPClient("127.0.0.1", 9000)

# ip adress your FingerRing
IP = "192.168.0.193" 
ESP_PORT = 1234
BUTTON_COUNT = 4

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 0))
sock.settimeout(2.0)
conected = False
print("conecting FingerRing " + IP)
sock.sendto(b"CONECT", (IP, ESP_PORT))
print("conection waiting to FingerRing...")

js_x_val = 0
js_y_val = 0
b = []
aux_b = []
btns = [
    "/input/Jump",
    "/input/UseLeft",
    "/input/DropLeft",
    "/input/Voice",
    "/input/QuickMenuToggleLeft",
]

fmt = '<ii' + ('?' * BUTTON_COUNT)
while True:
    try:
        if not conected:
            print("conected FingerRing")
            conected = True
        data, addr = sock.recvfrom(255)
        
        unpacked = struct.unpack(fmt, data)
        
        js_x_val = unpacked[0]
        js_y_val = unpacked[1]
        b = unpacked[2:]
        client.send_message("/input/Vertical", -js_x_val / 32767)
        client.send_message("/input/Horizontal", js_y_val / 32767)
        
        if len(b) == len(aux_b):
            for i in range(len(b)):
                if b[i] != aux_b[i]:
                    if b[i]:
                        client.send_message(btns[i], 1)
                    else:
                        client.send_message(btns[i], 0)              
        aux_b = b
    except socket.timeout:
        if conected:
            print("FingerRing disconected... reconection")
            conected = False
        sock.sendto(b"CONECT", (IP, ESP_PORT))
        time.sleep(1)