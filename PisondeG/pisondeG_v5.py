# SPDX-FileCopyrightText: 2018 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
Example for using the RFM9x Radio with Raspberry Pi.

Learn Guide: https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi
Author: Brent Rubell for Adafruit Industries
"""
# Import Python System Libraries
import time
# Import Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the SSD1306 module.
import adafruit_ssd1306
# Import RFM9x
import adafruit_rfm9x

# Set up 
datafile = "range_test.txt"

# Button A
btnA = DigitalInOut(board.D5)
btnA.direction = Direction.INPUT
btnA.pull = Pull.UP

# Button B
btnB = DigitalInOut(board.D6)
btnB.direction = Direction.INPUT
btnB.pull = Pull.UP

# Button C
btnC = DigitalInOut(board.D12)
btnC.direction = Direction.INPUT
btnC.pull = Pull.UP

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# 128x32 OLED Display
reset_pin = DigitalInOut(board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
# Clear the display.
display.fill(0)
display.show()
width = display.width
height = display.height

# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power = 23
prev_packet = None

now = datetime.now()
current_time = now.strftime("%x %X")
timeold = time.time()
pathnum = 0
while True:
        path = "".join(("/home/pi/loratest/",current_time,"_",str(pathnum)))
        if not os.path.isdir(path):
            os.mkdir(path)
            print("dir made")
            print(path)
            datafolder = path
            break
        pathnum+=1
file1 = open(datafile, "w") 
file1.close() 
while True:
    packet = None
    # draw a box to clear the image
    display.text('RasPi LoRa', 35, 0, 1)
    # check for packet rx
    packet = rfm9x.receive()
    if packet is None:
        display.fill(0)
        display.show()
        display.text('- Waiting for PKT -', 15, 20, 1)
    else:
        # Display the packet text and rssi
        try:
            file1 = open(datafile, "a")
            display.fill(0)
            prev_packet = packet
            packet_text = str(prev_packet, "utf-8")
            display.text(packet_text, 0, 0, 1)
            rssi = (" %0.1f" % rfm9x.last_rssi) 
            display.text(rssi, 25, 15, 1)
            print(rfm9x.last_rssi)
            dataw = packet_text+rssi+"\n"
            file1.write(dataw)
            file1.close() 
            cells = packet_text.strip().split(',')
            time.sleep(1)
        except:
            print(rfm9x.last_rssi)
            print("bad packet")
            display.text("bad packet", 15, 15, 1)
        

    if not btnA.value:
        display.fill(0)
        display.text(cells[0]+" "+rssi, 0, 0, 1)
        display.text(cells[1], 0, 10, 1)
        rxsens = cells[2]+", "+cells[3]+", "+cells[4]
        display.text(datasens+datasens2, 0, 20, 1)
    elif not btnB.value:
        display.fill(0)
        display.text(cells[5], 0, 0, 1)
        display.text(cells[6], 25, 0, 1)
        display.text(cells[7], 0, 10, 1)
        display.text(cells[8], 0, 20, 1)
        display.text(cells[9], 25, 20, 1)
    elif not btnC.value:
        # Send Button C
        display.fill(0)
        button_c_data = bytes("Button C!\r\n","utf-8")
        rfm9x.send(button_c_data)
        display.text('Sent Button C!', 25, 15, 1)
        
    # if (time.time() - timeold)>=5:
        # data = "rssi test"
        # datas = bytes(data,"utf-8")
        # rfm9x.send(datas)
        # timeold = time.time()

    display.show()
    time.sleep(0.1)
