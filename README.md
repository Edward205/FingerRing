# FingerRing

One-handed VR/gaming controller in a ring form factor which can be made with off the shelf parts and can be used as a standard Bluetooth controller or via Wi-Fi for better flexibility. 

## Make your own

Minimal programming experience is required, and the hardware part requires some creative DIY design skills.

### Hardware
Check the hardware reference design below for our version of the finished product. This is a rough outline for you to take creative liberty in building it:
* Connect the joystick and the buttons to the GPIO pins to your ESP32 board
    * You may add as many buttons as you wish, but only one joystick
    * Avoid using pins 2, 13, 12
* Attach the peripherals to your finger using your preferred mounting method
* Use a cut USB cable or 5 core cable for tidy wire management
* Paint the ring with a color similar to your skin to improve hand tracking performance

### Programming

First, ensure your ESP32 board is working properly by flashing the LED blink example. Afterwards, you will need to edit the following things per your design:
* By default the program operates in Wi-Fi mode. Comment out `#define WIFI` (by adding `//` at the start of the line) to switch to Bluetooth.
    * If you choose Wi-Fi, you will have to enter your SSID (Wi-Fi network name) and password below
* Set the number of buttons you have connected in `#define BUTTON_COUNT`
    * This includes push buttons and the joystick's push button but not the joystick's X and Y axis pins, or other modules
* Set the pins the joystick is connected to in the `JS_X_PIN` and `JS_Y_PIN` `#define`s
* Set the pins you connected the buttons to in the `b_pins` variable 

Once you upload the program onto the microcontroller, you're now ready to connect it as a games controller to your computer. 

## Functionality

The functionality difers based on the selected configuration.

### Bluetooth

Simply add a device in your computer's Bluetooth settings, and the FingerRing should appear as an available device. Once it's connected, it shows up as a generic games controller. You can check that it's working properly in Control Panel > View devices and printers > FingerRing > Right click > Game controller settings > Properties.

Depending on the game, you might want to use Steam Input to map its buttons to standard controller buttons. Open Steam > Settings > Controller > click to set up the FingerRing. Note: It might seem unresponsive during setup, but that seems to be a problem on Steam's side. 

### Wi-Fi

We have provided two Python scripts which connect to the FingerRing and allow it to work in different ways:

1. `fingerring_wifi.py` connects the device as a virtual Xbox controller. The buttons will be automatically mapped in the order they were defined in the ESP32's code (`b_pins`). For example, Button 1 -> A, Button 2 -> B, Button 3 -> X, etc.
2. `fingerring_osc.py` sends OSC events on localhost. You will need to install pythonosc for it to work: `pip install pythonosc`. The script is currently set to work with VRChat, but it can be easily modified.

For both scripts, you will need to set the ESP32's IP. It prints its IP to the serial monitor when it connects. 

### Limitations

For those who want to use it as a VR controller, the FingerRing currently isn't a complete VR controller replacement. That is a more complex problem which might require a custom OpenVR driver. For now, you can only use it as a standard game controller or to send data/events to games which support inputs like this either officially or through mods.

## Hardware reference design

BOM
| Component                              | Pcs | Price  |
|----------------------------------------|-----|--------|
| ESP32-C3 Development Board             | 1   | £1.6   |
| TP4056 lithium battery charging module | 1   | £0.5   |
| KY-023 joystick module                 | 1   | £1     |
| Momentary tactile switch 6x6x5mm       | 4   | £0.5   |
| Li-po or li-ion battery                | 1   | £2.8   |
| Hose clamps                            | 2   | £1     |
| 20cm 5 core wire                       | 2   | £1     |
| Wristband                              | 1   | £0.5   |
| Toggle switch                          | 1   | £0.5   |

Grand Total: £9.4

Prices are in GBP, and might change in time or depending on the region.

ESP32-C3 Super Mini with a Li-Po charging board, a battery and a power switch. 
<img width="576" height="506" alt="image" src="https://github.com/user-attachments/assets/a9133934-d464-4257-a544-19dd9341325c" />

Generic off the shelf joystick and buttons hot glued to hose clamps. 
<img width="576" height="480" alt="image" src="https://github.com/user-attachments/assets/b327b3c8-8198-4013-adda-7eb38ce6e6ae" />

4 6x6x5 momentary switches which can be mapped to A/B/X/Y in games.
<img width="576" height="501" alt="image" src="https://github.com/user-attachments/assets/23ced573-493a-4230-9391-93245d8583cc" />

## License
    FingerRing, open source one-handed VR/gaming controller in a ring form factor
    Copyright (C) 2025  Edward205
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.