
import time
import buildhat
from datetime import datetime

# # TWEAKS GO HERE
COLOR_DISTANCE_SENSOR_PORT = 'B'
MOTOR_PORT = 'A'
MOTOR_MOTOR_SPEED = 20
# Speed 10 moves two technic treads per 1/10th of a second.

motor = buildhat.Motor(MOTOR_PORT)

# motor.start(-10)
# motor.coast()
# time.sleep(10)
# motor.run_for_degrees(45)
# motor.run_for_rotations(.5)
# time.sleep(.4)
# motor.plimit(1)



def handle_motor(speed, pos, apos):
    """Motor data

    :param speed: Speed of motor
    :param pos: Position of motor
    :param apos: Absolute position of motor
    """
    d = datetime.utcnow()
    # print("Motor", speed, pos, apos, cds.get_distance(), d.strftime('%Y-%m-%d %H:%M:%S.%f')[:-5])
    print("Motor Speed ()", speed, cds.get_distance(), cds.get_distance(), cds.get_reflected_light(), cds.get_ambient_light(), cds.get_color_rgb(), d.strftime('%Y-%m-%d %H:%M:%S.%f')[:-5])



# Positive equals raising
# Negative equals lowering


# Spit out the distance sensor information:
cds = buildhat.ColorDistanceSensor(COLOR_DISTANCE_SENSOR_PORT)

motor.when_rotated = handle_motor
info = motor.get()
print(info)
motor.float()
motor.run_for_seconds(10, 100)
motor.run_for_seconds(10, -100)
motor.run_for_seconds(10, 100)
motor.run_for_seconds(10, -100)
motor.run_for_seconds(10, 100)
motor.run_for_seconds(10, -100)
motor.run_for_seconds(10, 100)
motor.run_for_seconds(10, -100)
motor.run_for_seconds(10, 100)
motor.run_for_seconds(10, -100)
motor.run_for_seconds(10, 100)
motor.run_for_seconds(10, -100)
motor.run_for_seconds(10, 100)
motor.run_for_seconds(10, -100)
motor.run_for_seconds(10, 100)
motor.run_for_seconds(10, -100)



motor.coast()
motor.release == True
time.sleep(1)
motor.stop()


# motor.plimit(1)
# motor.set_default_speed(10)

# print("Run for degrees 360")
# motor.run_for_degrees(360)
# time.sleep(3)

# print("Run for degrees -360")
# motor.run_for_degrees(-360)
# time.sleep(3)
# print("Accelerating motor...")
# for i in range(8, 10, 1):
#     motor.start(speed=i)
#     time.sleep(.1)
print("Start motor")
motor.start()

toggle = False
print("Press any key to toggle (Ctrl+C to quit).")

# while True:
#     keyboard.read_event()  # waits for a key event
#     toggle = not toggle
#     print(f"Toggled state: {toggle}")
#     if toggle:
#         motor.start(speed=10)
#     else:
#         motor.stop()

# # motor.stop()
# motor.float()
# time.sleep(1)

# while True:
#     time.sleep(1)
#     print("Distance", cds.get_distance(), cds.get_reflected_light(), cds.get_ambient_light(), cds.get_color_rgb())