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

# Set camera configuration
picam2.set_controls({
    "AeEnable": False,          # Disable auto exposure
    "AfMode": 2,                # 1 = Auto. # 2 = Continuous
    "AfTrigger": 0,             # 0 = Start single autofocus scan
    "ExposureTime": 20000,       # in microseconds (e.g., 20000 = 1/50s)
    "AnalogueGain": 6.0         # Higher = brighter (range 1.0–~16.0)
})

time.sleep(5) # Allow autofocus to settle

# picam2.set_controls({"AfMode": 0})  # 0 = Manual
# picam2.set_controls({"LensPosition": 0.0})  # Adjust from ~90 to 160 for close objects

filename = f"tmp/image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
picam2.capture_file(filename)

print(f"Saved image as {filename}")


light.off()
