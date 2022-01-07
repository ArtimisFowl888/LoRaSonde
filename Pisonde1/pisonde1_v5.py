# SPDX-FileCopyrightText: 2018 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
Example for using the RFM9x Radio with Raspberry Pi.

Learn Guide: https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi
Author: Brent Rubell for Adafruit Industries
"""
import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
from datetime import datetime
import adafruit_ssd1306
import adafruit_rfm9x
import adafruit_ahtx0
import adafruit_gps
import serial

# Sonde MetaData
SN ="1"

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

# Setup sensors
AHT = adafruit_ahtx0.AHTx0(i2c)


# GPS
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(uart, debug=False)
gps.send_command(b"PMTK101")
time.sleep(2)
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
time.sleep(2)
gps.send_command(b"PMTK220,100")
gps.update()

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

timeold = time.time()
pnum = 1
while True:
    packet = None
    # update GPS and listen for Messages
    gps.update()
    packet = rfm9x.receive()
    # draw a box to clear the image
    display.fill(0)
    # Display GPS fix data
    if not gps.has_fix:
        display.text("Waiting for fix...", 20, 0, 1)
    else:
        display.text("GPS fix", 35, 0, 1)
        datan = ("SAT: %0.1f" % (gps.satellites))
        display.text(datan, 15, 10, 1)
    # Check for package and diplay if one is recived
    if packet is None:
        display.text('- Waiting for PKT -', 15, 20, 1)
    else:
        # Display the packet text and rssi
        try:
            display.fill(0)
            prev_packet = packet
            packet_text = str(prev_packet, "utf-8")
            display.text('RX: ', 0, 0, 1)
            display.text(packet_text, 25, 0, 1)
        except:
            print(rfm9x.last_rssi)
            print("bad packet")
            display.text("bad packet", 15, 15, 1)
    # Read sensor data and write data package
    now = datetime.now()
    current_time = now.strftime("%x %X")
    data = SN+", "+str(pnum)+", "+current_time+", "
    try:
        datasens = ("T: %0.1f, H: %0.1f, " % (AHT.temperature,AHT.relative_humidity))
        data = data+datasens
    except:
        datasens = ("T: nan, H: nan, ")
        data = data+datasens
    try:
        datalat = ("Lat: %0.6f, " % (gps.latitude))
        data = data+datalat
        datalon = ("Lon: %0.6f, " % (gps.longitude))
        data = data+datalon
        dataalt = ("ALT: %0.3f, " % (gps.altitude_m))
        data = data+dataalt
    except:
        datalat = ("Lat: nan, ")
        data = data+datalat
        datalon = ("Lon: nan, ")
        data = data+datalon
        dataalt = ("ALT: nan, ")
        data = data+dataalt
    # Display Data
    if not btnA.value:
        # Send Button A
        display.fill(0)
        display.text('Ready', 0, 0, 1)
    elif not btnB.value:
        # Send Button B
        display.fill(0)
        data = str(pnum)
        display.text(data, 0, 0, 1)
        display.text(current_time, 0, 10, 1)
        display.text(datasens, 0, 20, 1)
    elif not btnC.value:
        # Send Button C
        display.fill(0)
        display.text(datalat, 0, 0, 1)
        display.text(datalon, 0, 10, 1)
        display.text(dataalt, 0, 20, 1)
 
    if (time.time() - timeold)>=3:
        datas = bytes(data,"utf-8")
        rfm9x.send(datas)
        timeold = time.time()
        pnum+=1
    display.show()
