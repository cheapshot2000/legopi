
import time
import buildhat
from datetime import datetime

# # TWEAKS GO HERE
# LIGHTS_PORT = 'C'
CONVEYOR_PORT = 'A'
CONVEYOR_MOTOR_SPEED = 10
# Speed 10 moves two technic treads per 1/10th of a second.

conveyor = buildhat.Motor(CONVEYOR_PORT)

# conveyor.start(-10)
# conveyor.coast()
# time.sleep(10)
# conveyor.run_for_degrees(45)
# conveyor.run_for_rotations(.5)
# time.sleep(.4)
# conveyor.reverse()
# conveyor.plimit(1)
# conveyor.run_for_seconds(4, 100)
# conveyor.coast()
# conveyor.release == True
# time.sleep(10)
# motor_a.stop()

def handle_motor(speed, pos, apos):
    """Motor data

    :param speed: Speed of motor
    :param pos: Position of motor
    :param apos: Absolute position of motor
    """
    d = datetime.utcnow()
    # print("Motor", speed, pos, apos, cds.get_distance(), d.strftime('%Y-%m-%d %H:%M:%S.%f')[:-5])
    print("Motor Speed ()", speed, cds.get_distance(), cds.get_distance(), cds.get_reflected_light(), cds.get_ambient_light(), cds.get_color_rgb(), d.strftime('%Y-%m-%d %H:%M:%S.%f')[:-5])

conveyor.when_rotated = handle_motor


# Spit out the distance sensor information:
# cds = buildhat.ColorDistanceSensor('D')

conveyor.plimit(1)
conveyor.set_default_speed(10)

# print("Run for degrees 360")
# conveyor.run_for_degrees(360)
# time.sleep(3)

# print("Run for degrees -360")
# conveyor.run_for_degrees(-360)
# time.sleep(3)
# print("Accelerating motor...")
# for i in range(8, 10, 1):
#     conveyor.start(speed=i)
#     time.sleep(.1)
print("Start motor")
# conveyor.start()

toggle = False
print("Press any key to toggle (Ctrl+C to quit).")

# while True:
#     keyboard.read_event()  # waits for a key event
#     toggle = not toggle
#     print(f"Toggled state: {toggle}")
#     if toggle:
#         conveyor.start(speed=10)
#     else:
#         conveyor.stop()

# # conveyor.stop()
# conveyor.float()
# time.sleep(1)

# while True:
#     time.sleep(1)
#     print("Distance", cds.get_distance(), cds.get_reflected_light(), cds.get_ambient_light(), cds.get_color_rgb())