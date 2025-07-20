# Initial Configuration Notes:::
# Configure the serial connection on the raspberry pi to see the buildhat
# sudo raspi-config
#
# Interface Options → Serial Port →
# - "Would you like a login shell to be accessible over serial?" → No
# - "Would you like the serial port hardware to be enabled?" → Yes
# Reboot the Pi
#
# Install python stuff now:
# sudo apt update
#
# Validate git already installed:
# sudo apt install git -y
#
# Install full python and virtual environments:
# sudo apt install python3-full python3-venv
#
# Create and activate a virtual environment to install modules:
# python3 -m venv ~/buildhat-venv
# source ~/buildhat-venv/bin/activate
#
# Install Lego Buildhat module:
# pip  install buildhat
#



from buildhat import Motor
from buildhat import ColorDistanceSensor
import time

motor_c = Motor('C')
motor_d = Motor('D')
# sensor = ColorDistanceSensor('B')
color = ColorDistanceSensor('B')

def handle_distance(val):
    if 50 < val < 150:
        print(f"Object detected at {val}mm")
    else:
        print("Out of range")

motor_c.start(5)
motor_d.start(100)

time.sleep(4)

motor_c.stop()
motor_d.stop()

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