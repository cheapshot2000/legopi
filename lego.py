# Initial Configuration Notes:::
# Configure the serial connection on the raspberry pi to see the buildhat
# sudo raspi-config
#
# Interface Options → Serial Port →
# - "Would you like a login shell to be accessible over serial?" → No
# - "Would you like the serial port hardware to be enabled?" → Yes
# Reboot the Pi
#
# Get the system updated.
# sudo apt update
# sudo apt full-upgrade
#
# Validate git already installed:
# sudo apt install git -y
# git clone https://github.com/cheapshot2000/legopi.git
# cd legopi/
#
# Install full python, virtual environments, and camera:
# sudo apt install python3-full python3-venv python3-picamera2 -y
# sudo reboot
#
# Create and activate a virtual environment to install modules:
# python3 -m venv ~/buildhat-venv
# source ~/buildhat-venv/bin/activate
#
# Install Lego Buildhat module:
# pip  install buildhat
#

import datetime
import time
import buildhat
from picamera2 import Picamera2

# Lights, Camera, Action!
light = buildhat.Light('A')
light.on()
time.sleep(2)

picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())
picam2.start()

# Optional delay to allow camera to adjust exposure
picam2.sleep(2)

filename = f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
picam2.capture_file(filename)

print(f"Saved image as {filename}")

light.off()

color = buildhat.ColorDistanceSensor('B')
print("Waiting for color white")
color.wait_until_color("white")
print("Got white")

motor_c = buildhat.Motor('C')
motor_d = buildhat.Motor('D')

motor_c.start(5)
motor_d.start(100)

time.sleep(2)

motor_c.stop()
motor_d.stop()


def handle_distance(val):
    if 50 < val < 150:
        print(f"Object detected at {val}mm")
    else:
        print("Out of range")


# print("Distance", color.get_distance())
# print("RGBI", color.get_color_rgb())
# print("Ambient", color.get_ambient_light())
# print("Reflected", color.get_reflected_light())
# print("Color", color.get_color())

# print("Waiting for color black")
# color.wait_until_color("black")
# print("Found color black")

# print("Waiting for color white")
# color.wait_until_color("white")
# print("Found color white")

# while True:
#     c = color.wait_for_new_color()
#     print("Found new color", c)


# while True:
#     time.sleep(1)