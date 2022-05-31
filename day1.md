# Day 1

## Introduction to Raspberry Pi

A Raspberry Pi is a simple, mini computer. It is a "single-board computer" because it is a single circuit board. On it, there is a microprocessor that computes logical and arithmetic operations (just like any computer). Then, there are also ports for you to plug in any I/O (input or out) devices.

![parts of a Raspberry Pi](pi_parts.png "parts of a Raspberry Pi")

Exmaples of input devices are the standard keyboard and mouse, or external sensors like camera or microphone. Output devices are anything coming from the computer in a human-perceptible form. This can include a monitor (which visualizes the state of the computer), or a speaker (which provides auditory feedback).

### GPIO

GPIO stands for "general-purpose input/output". These are the two rows of pins along the side of the Raspberry Pi.

![GPIO pinout](gpio_pinout.png "GPIO pinout")

Each pin has different different uses:

#### Standard GPIO Pins
These pins can be used for sending and receiving any input/output. Each pin has only 2 voltage states: high or low. Think of this as 1 or 0, or on or off. You can send a on or off signal to the connected peripheral device. The device can also communicate back by sending the same signal or a series of signals.

#### Power Pins
These pins transmit power as output to power attached peripherals. There are several 3.3V and 5V output pins, depending on what the external device requires.

#### Ground
And if we’re going to be rigging up electrical circuits here with power, then we’ll need a ground. 

#### Communication Pins
Some of the standard GPIO pins are used for communication purposes. Here are some common communication protocols.

* SPI pins – The Serial Peripheral Interface (SPI) is a communication protocol used to transfer data between micro-computers like the Raspberry Pi and peripheral devices. The MISO pin receives data, and the MOSI pin sends data from the Raspberry Pi. Furthermore, the serial clock pin sends pulses at a regular frequency between the Raspberry Pi and the SPI device at the same speed in which the devices to transfer data to each other.
* UART pins – UART stands for universal asynchronous receiver-transmitter, which is a physical circuit designed to send and recieve data.
* PWM pins – PWM means “pulse width modulation,” which is a communication protocol best used with stuff that moves and lights up: motors, LEDs, and so on.
* I2C pins – I2C is short for inter-integrated circuit (two “inters” or I"squared"C). It works similarly to SPI, but it doesn’t force you to use nearly so many pins.

## Introduction to the Project

Over the course of the next few days, you will complete a project that replicates a smart doorbell system.

Imaging you want to create a doorbell alarm system where the visitor doesn't have to press a button for you to be notified. The doorbell system will know when a person approaches the door and alert you.

We will achieve this in several parts. Today, you will begin by learning about how to interface with the camera module using a Python script.

## 1. Take a picture

To take a picture, we will use the builtin library `libcamera`. It is a software library aimed at supporting complex camera systems directly from the Linux operating system.

Let's check to make sure everything is working. Run
``` bash
$ libcamera-hello
```
in the terminal. You should see a camera preview window for about 5 seconds.

To play around with how many seconds the preview window is shown, we can add a tag `-t <duration>` to specify the number of milliseconds. We can also show the preview indefinitely by running

``` bash
$ libcamera-hello -t 0
```
To exit out of this preview, click the window's close button, or use `Ctrl-C` in the terminal.

Now, lets capture a photo. To accomplish this, we can use the builtin `libcamera-still` application.

To capture a full resolution JPEG images, run
``` bash
$ libcamera-still -o test.jpg
```

This will display a preview for about 5 seconds, and then capture a full resolution JPEG image to the file `test.jpg`.

The `-t <duration>` option can be used to alter the length of time the preview shows, and the `--width` and `--height` options will change the resolution of the captured still image. For example
``` bash
$ libcamera-still -o test.jpg -t 2000 --width 640 --height 480
```

`libcamera-still` allows files to be saved in a number of different formats. 
``` bash
$ libcamera-still -e png -o test.png
$ libcamera-still -e bmp -o test.bmp
$ libcamera-still -e rgb -o test.data
$ libcamera-still -e yuv420 -o test.data
```
Note that the format in which the image is saved depends on the `-e` (equivalently `--encoding`) option and is not selected automatically based on the output file name.

## Automate Picture Taking

Now that we know we can use the builtin `libcamera-still` application to take images, lets wrap it up in a Bash script.

Anything you can run normally on the command line can be put into a Bash script and it will do exactly the same thing. Similarly, anything you can put into a Bash script can also be run normally on the command line and it will do exactly the same thing.

Bash scripts help us automate tasks by allowing us to run a set of terminal commands all at once.

To start, lets create a `capture.sh` file. This will be the Bash script where we will automate taking images. Once created, it is important to note that the first line of the script must be 
``` bash
#!/bin/bash
```
in order to signify that this is in fact a Bash script. This is referred to as the `Shebang`. The hash exclamation mark `(#!)` character sequence is referred to as the Shebang. Following it is the path to the interpreter (or program) that should be used to run (or interpret) the rest of the lines in the text file. For Bash scripts it will be the path to Bash, but there are many other types of scripts and they each have their own interpreter.

In the following lines, we can run any terminal commands we want! For example: 
``` bash
#!/bin/bash

echo Hello
sleep 1
echo World
sleep 1
echo !
```

is a script that will print 
``` bash
Hello
World
!
```
into the terminal with 1 second between each print out statement.

For our purpose, we will create a script called `capture.sh` with the following:
``` bash
#!/bin/bash

libcamera-still -o test.jpg
```

Can you guess what this script will do?

You'd be correct if you said that it would do the exact same thing as running the `libcamera-still -o test.jpg` command directly in the terminal!

Now, to execute this script, we can go back to the terminal and run
``` bash
./capture.sh
```

## To Push Some Buttons

What if the monitor suddenly went black... or if the keyboard just randomly decided to stop taking input? How will we take pictures then??

This is where we will take what we've learned about GPIO pins and put them to good use.

# TODO:

``` python
import sys
import os
import time
import RPi.GPIO as GPIO

button_pin = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    if (GPIO.input(button_pin) == GPIO.LOW):
        print("Button pressed--Take picture")
        timestamp = time.time_ns()
        os.system("./capture.sh " + timestamp + ".jpg")
        time.sleep(0.5)

        if (GPIO.input(button_pin) == GPIO.HIGH):
            print("Button released")
```