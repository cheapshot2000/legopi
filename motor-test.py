import time
from datetime import UTC, datetime

import buildhat
from buildhat import BuildHATError


# Hardware ports
COLOR_DISTANCE_SENSOR_PORT = "D"
MOTOR_PORT = "A"

# Motor behavior
WHITE_MOTOR_SPEED = -25
GREEN_MOTOR_SPEED = 25
MOTOR_POWER_LIMIT = 1.0

# Color behavior
STOP_COLORS = ("red", "blue")

# Load protection
STARTUP_GRACE_SECONDS = 1.5
STUCK_TIMEOUT_SECONDS = 1.5
STRAIN_ARM_SPEED = max(abs(WHITE_MOTOR_SPEED), abs(GREEN_MOTOR_SPEED))
STRAIN_MIN_SPEED = 15
STRAIN_TIMEOUT_SECONDS = 0.5
MOTOR_LOG_INTERVAL_SECONDS = 0.5

# Speed 10 moves two technic treads per 1/10th of a second.


def timestamp():
    return datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S.%f")[:-5]


def classify_rgb(rgb):
    r, g, b = rgb
    brightness = r + g + b

    if brightness > 220 and max(r, g, b) - min(r, g, b) < 45:
        return "white"
    if brightness < 60:
        return "black"
    if g > r * 1.7 and g > b * 1.5:
        return "green"
    if r > g * 1.5 and r > b * 1.5:
        return "red"
    if b > r * 1.5 and b > g * 1.5:
        return "blue"
    return "unknown"


class MotorColorController:
    def __init__(self, sensor, motor):
        self.sensor = sensor
        self.motor = motor
        self.last_color = None
        self.motor_running = False
        self.current_motor_speed = None
        self.motor_started_at = None
        self.last_motor_moved_at = None
        self.latest_motor_speed = None
        self.strain_armed = False
        self.strain_started_at = None
        self.last_motor_log_at = 0
        self.stuck_armed = False
        self.shutting_down = False

    def start_motor(self, speed, reason):
        now = time.monotonic()
        print(reason)
        self.motor.start(speed)
        self.motor_running = True
        self.current_motor_speed = speed
        self.motor_started_at = now
        self.last_motor_moved_at = now
        self.latest_motor_speed = None
        self.strain_armed = False
        self.strain_started_at = None
        self.last_motor_log_at = 0
        self.stuck_armed = False

    def stop_motor(self, reason):
        if not self.motor_running:
            return

        print(reason)
        self.motor.stop()
        self.motor_running = False
        self.current_motor_speed = None
        self.motor_started_at = None
        self.last_motor_moved_at = None
        self.latest_motor_speed = None
        self.strain_armed = False
        self.strain_started_at = None
        self.last_motor_log_at = 0
        self.stuck_armed = False

    def handle_color_sensor(self, data):
        if self.shutting_down:
            return

        rgb = self.sensor.get_color_rgb()
        color = classify_rgb(rgb)
        distance = self.sensor.get_distance()
        previous_color = self.last_color

        if color != self.last_color:
            print("COLOR:", self.last_color, "->", color, "rgb:", rgb, "distance:", distance)
            self.last_color = color

        if color == "white":
            if previous_color != "white":
                self.start_motor(WHITE_MOTOR_SPEED, "START: white detected; starting motor forward")
            return

        if color == "green":
            if previous_color != "green":
                self.start_motor(GREEN_MOTOR_SPEED, "START: green detected; starting motor reverse")
            return

        if color in STOP_COLORS:
            self.stop_motor("STOP: " + color + " detected; stopping motor")
            return

    def handle_motor_rotation(self, speed, position, absolute_position):
        if self.shutting_down:
            return

        if not self.motor_running:
            return

        now = time.monotonic()
        current_speed = abs(speed)
        self.latest_motor_speed = current_speed
        self.last_motor_moved_at = now
        self.stuck_armed = True

        if now - self.last_motor_log_at >= MOTOR_LOG_INTERVAL_SECONDS:
            print(
                "MOTOR:",
                "speed",
                speed,
                "position",
                position,
                "absolute position",
                absolute_position,
                timestamp(),
            )
            self.last_motor_log_at = now

        if self.in_startup_grace(now):
            return

        if not self.strain_armed:
            if current_speed >= STRAIN_ARM_SPEED:
                self.strain_armed = True
                self.strain_started_at = None
                print("STRAIN: armed after motor reached speed", current_speed)
            return

        if current_speed >= STRAIN_MIN_SPEED:
            self.strain_started_at = None
            return

        if self.strain_started_at is None:
            self.strain_started_at = now
            return

        if now - self.strain_started_at >= STRAIN_TIMEOUT_SECONDS:
            self.stop_motor(
                "STRAIN: speed stayed below "
                + str(STRAIN_MIN_SPEED)
                + " for "
                + str(STRAIN_TIMEOUT_SECONDS)
                + "s; stopping motor"
            )

    def check_for_stuck_motor(self):
        if self.shutting_down or not self.motor_running:
            return

        now = time.monotonic()
        if self.in_startup_grace(now):
            return

        if not self.stuck_armed:
            return

        if self.last_motor_moved_at is None:
            self.last_motor_moved_at = now
            return

        if now - self.last_motor_moved_at >= STUCK_TIMEOUT_SECONDS:
            if self.strain_armed and self.latest_motor_speed is not None and self.latest_motor_speed < STRAIN_MIN_SPEED:
                self.stop_motor(
                    "STRAIN: motor slowed below "
                    + str(STRAIN_MIN_SPEED)
                    + " then stopped moving; stopping motor"
                )
            else:
                self.stop_motor(
                    "STUCK: no motor position changes for "
                    + str(STUCK_TIMEOUT_SECONDS)
                    + "s; stopping motor"
                )

    def in_startup_grace(self, now):
        return (
            self.motor_started_at is not None
            and now - self.motor_started_at < STARTUP_GRACE_SECONDS
        )

    def shutdown(self):
        self.shutting_down = True
        self.motor_running = False
        self.sensor.callback(None)
        self.motor.callback(None)
        self.motor.stop()
        self.motor.coast()


def main():
    try:
        sensor = buildhat.ColorDistanceSensor(COLOR_DISTANCE_SENSOR_PORT)
        motor = buildhat.Motor(MOTOR_PORT)
    except BuildHATError as exc:
        print("ERROR: Build HAT is not responding:", exc)
        print("Power-cycle the Build HAT if this happened after Ctrl+C or a forced quit.")
        return

    motor.plimit(MOTOR_POWER_LIMIT)
    motor.float()

    controller = MotorColorController(sensor, motor)
    motor.when_rotated = controller.handle_motor_rotation
    sensor.callback(controller.handle_color_sensor)

    try:
        print(
            "Watching colors. White starts forward; green starts reverse; red/blue, strain, or stuck stops. "
            "Press Ctrl+C to quit."
        )
        while True:
            controller.check_for_stuck_motor()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Stopping.")
    finally:
        controller.shutdown()


if __name__ == "__main__":
    main()
