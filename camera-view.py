# Stop libcamera output annoyance - 3 is error level only.
import os
os.environ["LIBCAMERA_LOG_LEVELS"] = "*:3"

import time
import buildhat
from datetime import datetime
from picamera2 import Picamera2

# Lights, Camera, Action!
light = buildhat.Light('A')
light.on()
# time.sleep(2)

picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())
picam2.start()

# Wait briefly for camera to warm up
time.sleep(2)

# Trigger autofocus
picam2.set_controls({"AfMode": 2})       # 1 = Auto. # 2 = Continuous
picam2.set_controls({"AfTrigger": 0})    # 0 = Start single autofocus scan
time.sleep(2) # Allow autofocus to settle

# picam2.set_controls({"AfMode": 0})  # 0 = Manual
# picam2.set_controls({"LensPosition": 0.0})  # Adjust from ~90 to 160 for close objects

filename = f"tmp/image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
picam2.capture_file(filename)

print(f"Saved image as {filename}")


light.off()
