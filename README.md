# LoRaSonde

Project to develop an opensource LoRa based radiosonde system.

The system should firstly be able to behave just like a standard radiosonde that
can transmit meteorological data with out the need to be recovered, additionally
the system will need to record data locally for missions in which distance and
or time make it impossible for the sonde to communicate with the ground station
over LoRa.

The LoRa sonde system will comprise of a ground station, LoRa radiosondes, and
repeater stations (if possible).

**Sondes**

**Pi-sonde-1**

| Raspberry pi zero w  | 1 | https://www.adafruit.com/product/3400 | 10    |
|----------------------|---|---------------------------------------|-------|
| LoRa Radio           | 1 | https://www.adafruit.com/product/4074 | 32.5  |
| 915mhz antenna       | 1 |                                       |       |
| Temp/humidity sensor | 1 | https://www.adafruit.com/product/4566 | 4.50  |
| gps                  | 1 | https://www.adafruit.com/product/4415 | 29.95 |

Comparable to a standard radiosonde in which only one sonde can be used with one
ground station each operation on a single frequency.

Do to not needing buffer multiple messages from other sondes the Pi-sonde-1 will
have a higher transmission rate for a higher temporal resolution.

Raspberry pi could be replaced with Arduino see Ardu-sonde.

**Pi-sonde-S (Swarm sonde)**

| Raspberry pi zero 2 w | 1 | https://www.adafruit.com/product/5291 | 15    |
|-----------------------|---|---------------------------------------|-------|
| LoRa Radio            | 1 | https://www.adafruit.com/product/4074 | 32.5  |
| 915mhz antenna        | 1 |                                       |       |
| Temp/humidity sensor  | 1 | https://www.adafruit.com/product/4566 | 4.50  |
| gps                   | 1 | https://www.adafruit.com/product/4415 | 29.95 |

A swarm of radiosondes can be launched or dropped together all of which will
operate on the same channel to minimize interference with other 915mhz systems,
to do this these sondes will leverage mesh communication to relay messages
between each other reach the ground station.

Lower transmission rate to accommodate data buffer for mesh communication.   
resulting in lower temporal resolution with the benefit of a higher spatial
resolution.

**All Pi-sondes are capable of local data logging for missions where radio
coverage is uncertain and field recoveries are possible.**

**Ardu-sonde-1**

| LoRa Radio/Arduino   | 1 | https://www.adafruit.com/product/3078 | 34.95 |
|----------------------|---|---------------------------------------|-------|
| 915mhz antenna       | 1 |                                       |       |
| Temp/humidity sensor | 1 | https://www.adafruit.com/product/4566 | 4.50  |
| gps                  | 1 | https://www.adafruit.com/product/4415 | 29.95 |

Same as Pi sonde at a lower cost, but will not have a ability to do local
logging of data.

**Ardu-sonde-s?**

| LoRa Radio/Arduino   | 1 | https://www.adafruit.com/product/3078 | 34.95 |
|----------------------|---|---------------------------------------|-------|
| 915mhz antenna       | 1 |                                       |       |
| Temp/humidity sensor | 1 | https://www.adafruit.com/product/4566 | 4.50  |
| gps                  | 1 | https://www.adafruit.com/product/4415 | 29.95 |

*  
*research required to see if Arduino have enough memory buffer to operate in a
mesh configuration

**Ground station**

| Raspberry pi 4                                | 1 | https://www.adafruit.com/product/4296 | 55    |
|-----------------------------------------------|---|---------------------------------------|-------|
| LoRa Radio                                    | 1 | https://www.adafruit.com/product/4074 | 32.5  |
| High gain 915mhz antenna                      | 1 |                                       |       |
| Ultra Low-Noise Variable Gain Amplifier (VGA) | 1 | https://amzn.to/3eTXoka               | 49.95 |
| screen                                        | 1 |                                       |       |
| Mouse and keyboard                            | 1 |                                       |       |
| gps                                           | 1 | https://www.adafruit.com/product/4415 | 29.95 |
| 9DOF IMU                                      | 1 | https://www.adafruit.com/product/4554 | 14.95 |
| 2axis gimbal                                  | 1 |                                       |       |
| Servo controller                              | 1 | https://www.adafruit.com/product/3416 | 9.95  |

Ground station for LoRa sonde

-   2axis gimbal for high gain directional antenna or portable with Omni antenna

-   GUI for initializing and plotting data from LoRa sonde

-   Minimum plot(s): SkewT, time trace, sonde track

-   Additional plot(s): map of all sondes relative to each other.

-   Will create data files for each sonde that the ground station receives data
    from.

**Other uses for LoRa on balloons**

Balloons recovery.

A LoRa can be added to a balloon cutdown for remotely triggered cut down, along
with is low power consumption it can be used to assist in recovery by
transmitting its location to a ground recovery team for easier orientation, (a
secondary cutdown can be used to cut the payload from the line to if it is stuck
in a tree)

