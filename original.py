
import time
import buildhat
from datetime import datetime

# # TWEAKS GO HERE
COLOR_DISTANCE_SENSOR_PORT = 'D'
MOTOR_PORT = 'A'
MOTOR_MOTOR_SPEED = 20
# Speed 10 moves two technic treads per 1/10th of a second.

last_color = None

# motor.start(-10)
# motor.coast()
# time.sleep(10)
# motor.run_for_degrees(45)
# motor.run_for_rotations(.5)
# time.sleep(.4)
# motor.plimit(1)



def handle_motor(speed, pos, apos):
    d = datetime.utcnow()

    distance = cds.get_distance()
    reflected = cds.get_reflected_light()
    ambient = cds.get_ambient_light()
    rgb = cds.get_color_rgb()
    color = cds.get_color()

    print(
        "Motor Speed",
        speed,
        distance,
        reflected,
        ambient,
        rgb,
        color,
        d.strftime('%Y-%m-%d %H:%M:%S.%f')[:-5]
    )

def classify_rgb(rgb):
    r, g, b = rgb
    brightness = r + g + b

    if brightness < 60:
        return "black"
    if g > r * 1.7 and g > b * 1.5:
        return "green"
    if r > g * 1.5 and r > b * 1.5:
        return "red"
    if b > r * 1.5 and b > g * 1.5:
        return "blue"
    return "unknown"

class ColorWatcher:
    def __init__(self, sensor):
        self.sensor = sensor
        self.last_color = None

    def handle_cds(self, data):
        rgb = self.sensor.get_color_rgb()
        color = classify_rgb(rgb)
        distance = self.sensor.get_distance()

        if color != self.last_color:
            print("COLOR CHANGED:", self.last_color, "->", color, rgb, "distance:", distance)
            self.last_color = color

            if color == "green":
                print("GREEN ACTION")
            elif color == "red":
                print("RED ACTION")
            elif color == "black":
                print("BLACK ACTION")


# Spit out the distance sensor information:
cds = buildhat.ColorDistanceSensor(COLOR_DISTANCE_SENSOR_PORT)
watcher = ColorWatcher(cds)
cds.callback(watcher.handle_cds)


motor = buildhat.Motor(MOTOR_PORT)
motor.when_rotated = handle_motor
info = motor.get()
print(info)
motor.float()


# Positive equals raising
# Negative equals lowering
motor.run_for_seconds(1, -100)
motor.run_for_seconds(2, 100)
motor.run_for_seconds(3, -100)
motor.run_for_seconds(2, 100)
motor.run_for_seconds(3, -100)
motor.run_for_seconds(2, 100)
motor.run_for_seconds(3, -100)
motor.run_for_seconds(2, 100)
motor.run_for_seconds(3, -100)


motor.when_rotated = None
motor.coast()
motor.release = True
motor.stop()

os._exit(0)

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
# print("Start motor")
# motor.start()

# toggle = False
# print("Press any key to toggle (Ctrl+C to quit).")

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