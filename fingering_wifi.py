# FingerRing alpha beta (very early acces)
# for pc with python and FingerRing wifi mode

import socket
import struct
import time
import vgamepad as vg

gamepad = vg.VX360Gamepad()

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
    vg.XUSB_BUTTON.XUSB_GAMEPAD_A,              
    vg.XUSB_BUTTON.XUSB_GAMEPAD_B,              
    vg.XUSB_BUTTON.XUSB_GAMEPAD_X,              
    vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,              
    vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,  
    vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER, 
    vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,           
    vg.XUSB_BUTTON.XUSB_GAMEPAD_START,          
    vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,     
    vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,    
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
        gamepad.left_joystick(x_value=js_x_val, y_value=js_y_val)
        
        if len(b) == len(aux_b):
            for i in range(len(b)):
                if b[i] != aux_b[i]:
                    if b[i]:
                        gamepad.press_button(button=btns[i])
                    else:
                        gamepad.release_button(button=btns[i])                
        aux_b = b
        gamepad.update()
    except socket.timeout:
        if conected:
            print("FingerRing disconected... reconection")
            conected = False
        sock.sendto(b"CONECT", (IP, ESP_PORT))
        time.sleep(1)