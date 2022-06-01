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
``` Bash
$ libcamera-hello
```
in the terminal. You should see a camera preview window for about 5 seconds.

To play around with how many seconds the preview window is shown, we can add a tag `-t <duration>` to specify the number of milliseconds. We can also show the preview indefinitely by running

``` Bash
$ libcamera-hello -t 0
```
To exit out of this preview, click the window's close button, or use `Ctrl-C` in the terminal.

Now, lets capture a photo. To accomplish this, we can use the builtin `libcamera-still` application.

To capture a full resolution JPEG images, run
``` Bash
$ libcamera-still -o test.jpg
```

This will display a preview for about 5 seconds, and then capture a full resolution JPEG image to the file `test.jpg`.

The `-t <duration>` option can be used to alter the length of time the preview shows, and the `--width` and `--height` options will change the resolution of the captured still image. For example
``` Bash
$ libcamera-still -o test.jpg -t 2000 --width 640 --height 480
```

`libcamera-still` allows files to be saved in a number of different formats. 
``` Bash
$ libcamera-still -e png -o test.png
$ libcamera-still -e bmp -o test.bmp
$ libcamera-still -e rgb -o test.data
$ libcamera-still -e yuv420 -o test.data
```
Note that the format in which the image is saved depends on the `-e` (equivalently `--encoding`) option and is not selected automatically based on the output file name.

## 2. Automate Picture Taking

Now that we know we can use the builtin `libcamera-still` application to take images, lets wrap it up in a Bash script.

Anything you can run normally on the command line can be put into a Bash script and it will do exactly the same thing. Similarly, anything you can put into a Bash script can also be run normally on the command line and it will do exactly the same thing.

Bash scripts help us automate tasks by allowing us to run a set of terminal commands all at once.

To start, lets create a `capture.sh` file. This will be the Bash script where we will automate taking images. Once created, it is important to note that the first line of the script must be 
``` Bash
#!/bin/Bash
```
in order to signify that this is in fact a Bash script. This is referred to as the `Shebang`. The hash exclamation mark `(#!)` character sequence is referred to as the Shebang. Following it is the path to the interpreter (or program) that should be used to run (or interpret) the rest of the lines in the text file. For Bash scripts it will be the path to Bash, but there are many other types of scripts and they each have their own interpreter.

In the following lines, we can run any terminal commands we want! For example: 
``` Bash
#!/bin/Bash

echo Hello
sleep 1
echo World
sleep 1
echo !
```

is a script that will print 
``` Bash
Hello
World
!
```
into the terminal with 1 second between each print out statement.

For our purpose, we will create a script called `capture.sh` with the following:
``` Bash
#!/bin/Bash

libcamera-still -o test.jpg
```

Can you guess what this script will do?

You'd be correct if you said that it would do the exact same thing as running the `libcamera-still -o test.jpg` command directly in the terminal!

Now, to execute this script, we can go back to the terminal and run
``` Bash
./capture.sh
```

You'll notice that a new `test.jpg` file was created on the `Desktop`. It's the image that was just captured! Try running the command again. You'll see that `test.jpg` was replaced with a new image. Lets fix this.

Inside `capture.sh` replace the existing line with
``` bash
libcamera-still -o $1.jpg
```
instead. Instead of storing the image in the file `test.jpg`, we've replaced it with `$1.jpg`. What does this mean?

`$1` is the first command-line argument passed to the shell script. Go back to the terminal and run the following
``` Bash
./capture.sh image1.jpg
```

Now, the new image is stored in `image1.jpg`. Run it again but replace `image1.jpg` with anything (ending in `.jpg`). As you can see, our bash script reads in whatever is passed in when you run the script and uses that as the name of the file. Very cool stuff! Now you can run our `./capture.sh` script and store the image to any filename of your choosing.

## 3. To Push Some Buttons

What if the monitor suddenly went black... or if the keyboard just randomly decided to stop taking input? How will we take pictures then??

This is where we will take what we've learned about GPIO pins and put them to good use.

Let's write a Python script that takes a photo using the camera module whenever a push button is pressed.

### a) Hardware Setup

We will use a breadboard, a push pin (or a switch), a resistor, and two jumper wires.

We connect one side of the switch to an input pin on the Raspberry Pi, in this case we use pin 10. The other side of the switch we connect to 3.3V on pin 1 using a resistor. The resistor is used as a current limiting resistor to protect our input pin by limiting the amount of current that can flow.

It should look like the following:

![Push Button Circuit](pushbutton_circuit.jpeg "Push Button Circuit")

The idea is that the input pin will be low (0V) when the button is not pushed. When the button is pushed it will connect the pin to 3.3V and change the state to high (3.3V).

In the diagram above, pin 10 is used. Notice how the physical pin 10 is the 5th pin from the edge along the first row of pins. You can use any available GPIO pin on the board, it does not have to be pin 10 specifically.

### b) Python Script to read GPIO Input

We will need to use the `RPi.GPIO` module. This package provides a Python module to control the GPIO on a Raspberry Pi. But first, we must download the package locally by running 
```Bash
$ sudo apt-get install Python-rpi.gpio Python3-rpi.gpio
```
in the terminal.

Now, create a Python file, lets call it `push_botton_capture.py`.

Our initial script will initialize the GPIO port and then continuously read the status of the pin until we exit the program.

First we import the GPIO library and then setup the library to use board numbering. We then initialize pin 10 as an input pin, and instruct the Raspberry Pi to pull the pin low using the `pull_up_down` parameters.

The initialization code looks as follows:

``` Python
import RPi.GPIO as GPIO
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
```
The `pull_up_down` parameter in the `GPIO.setup` call tells the Raspberry Pi which state the pin should be in when there is nothing connected to the pin. This is important since we want our program to read a low state when the button is not pushed and a high state when the button is pushed.

With the port initialized we can write the code that continuously reads the port and outputs a message when the button is pressed. We use the GPIO.input function to read the state of the port.
```Python
while True: # Run forever
    if GPIO.input(10) == GPIO.HIGH:
        print("Button was pushed!")
```

Let's try executing this Python program by running the following in the terminal:
```Bash
$ Python3 push_botton_capture.py
```

You’ll notice that when you push the button the script outputs `Button was pushed!` many times. This is because we are continuously reading the state of the button. 

If the program does not work, or continuously outputs `Button was pushed!` without the button being pressed down, try rotating the button 90 degrees.

### c) Switching to Event-based GPIO Input

We want the program to only print out `Button was pushed!` once everytime the button is pushed. After all, it is quiet strange for there to be multiple `Button was pushed!` prints when you have only pressed the button once.

We want to rewrite our program to output a single message whenever the button is pressed rather than continuously outputting a message. To do this we need to use GPIO events.

A GPIO event in the Raspberry Pi Python GPIO library works by calling a Python function whenever an event is triggered. Such a function is called a callback function.

An event can be an input pin being low or high, but it could also be when the pin changes from low to high – called rising – or when the pin changes from high to low – called falling.

In our case we want to detect when the button is being pressed, that is going from low to high also called the rising edge.

Before we setup the event we must however first write the callback function to be executed when the event is detected. The callback function is a regular Python function and as such can contain any Python code, it could send out a tweet or as we do in our case simply print `Button was pushed!`.

In the top of `push_botton_capture.py`, lets add
```Python
def button_callback(channel):
    print("Button was pushed!")
```

Next, we will initalize the pin
``` Python
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
```

Finally, lets define the wanted behavior for when a specific event occurs
```
GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback) # Setup event on pin 10 rising edge
```

Lastly, we should instruct Python to wait for keyboard input and when someone presses enter cleanup the GPIO input library resources and finish the program.
``` Python
message = input("Press enter to quit\n\n") # Run until someone presses enter
GPIO.cleanup() # Clean up
```

In summary, your `push_button_capture.py` should now look like the following
``` Python
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
def button_callback(channel):
    print("Button was pushed!")
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback) # Setup event on pin 10 rising edge
message = input("Press enter to quit\n\n") # Run until someone presses enter
GPIO.cleanup() # Clean up
```

Lets try executing this file again by running the following in the terminal
``` Bash
$ python3 push_button_capture.py
```
You now see that the program only outputs one `Button was pushed!` everytime the button is pushed.

### d) What To Do When the Button is Pushed?

There is now visual indication in the terminal whenever the button is pushed. Our next task is to capture an image whenever this event occurs. Can you think of how this can be accomplished?

We already have a callback function, `button_callback`, that is called whenever the button is pushed. Don't believe me? Change the print statement inside `button_callback` to anything you want and run the program again. You'll see that whenever the button is pushed, your new print statement is outputed in the terminal!

So, we will need to add something inside of this callback function in order to accomplish our mission.

We already wrote a Bash script that takes a photo. Lets use that! When we wanted to take a photo, we would simply run the Bash script in the terminal. We need a way to run the same script in our Python program.

This is where the Python `os` module comes into place. This module provides a portable way of using operating system dependent functionality. Some popular functions includes creating and deleting directories/files, and of course, executing other programs.

To do this, we will first need to import the module in our Python file
``` Python 
import os
```

In order to run a terminal command in Python, we will use the funciton `os.system`. Meaning we can add the following line in `button_callback`
``` Python
os.system("./capture.sh test_capture.jpg")
```

Try running the Python program again. As you can see, whenever you press the button, `test_capture.jpg` is created with the photo. But we still face the same issue as before... If you press the button again, the photo is replaced with a new photo. What if we wanted to save all of the photos everytimg we press the button instead of just the most recent?

### e) Unique Files for Each Image

We can try naming the images something unique. Lets try using the timestamp for this purpose! 

To do this, lets import the `datetime` package in Python.
``` Python
import datetime
```

To get the time, we can use the builtin function `datetime.datetime.now` to get the current time. We will then format the timestamp into something humans can easily read and understand. To do this, we will use `strftime` to format the `datetime` object.

``` Python
current_time = datetime.datetime.now()
time_formatted = current_time.strftime("%m_%d_%Y--%H_%M_%S")
```

Can you find a way to use the timestamp in your existing code?

We can replace the `os.system` call with the following.

``` Python
os.system("./capture.sh " + time_formatted + ".jpg")
```

This line uses string concatenation, which basically just adds different strings together to form a longer string. For example, if the `time_formatted` was `6_20_2022--10_03_02`, then Python would interpret the above line as 
``` Python
os.system("./capture.sh 6_20_2022--10_03_02.jpg")
```

### f) Putting It All Together

The final version of `push_button_capture.py` should be the following.

``` Python
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
def button_callback(channel):
    print("Button was pushed!")
    os.system("./capture.sh " + time_formatted + ".jpg")

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback) # Setup event on pin 10 rising edge
message = input("Press enter to quit\n\n") # Run until someone presses enter
GPIO.cleanup() # Clean up
```

Try running it in the terminal
``` bash
$ python3 push_button_capture.py
```

See that a new `.jpg` file is created everytime you push the button and that each file is an image captured from the camera module.