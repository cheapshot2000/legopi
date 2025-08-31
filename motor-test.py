
import time
import buildhat
from datetime import datetime


motor_a = buildhat.Motor('A')

motor_a.start(100)

time.sleep(120)

# motor_a.stop()
