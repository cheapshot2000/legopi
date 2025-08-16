
import time
import buildhat
from datetime import datetime


motor_a = buildhat.Motor('A')

motor_a.start(-20)

time.sleep(15)

motor_a.stop()
