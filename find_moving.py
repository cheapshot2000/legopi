# Stop libcamera output annoyance - 3 is error level only.
import os
os.environ["LIBCAMERA_LOG_LEVELS"] = "*:3"

import cv2
import time
import buildhat
import numpy as np
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




filename = f"tmp/image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"


# Capture the first frame
frame1 = picam2.capture_array("main")
gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)

# Wait and capture the second frame
print('sleeping for second frame')
time.sleep(5)
frame2 = picam2.capture_array("main")
gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)

# Compute difference and threshold
delta = cv2.absdiff(gray1, gray2)
thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
thresh = cv2.dilate(thresh, None, iterations=2)

# Find contours of moving objects
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw bounding boxes
for c in contours:
    if cv2.contourArea(c) < 500:  # Skip small changes
        continue
    (x, y, w, h) = cv2.boundingRect(c)
    cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Save or preview result
cv2.imwrite(filename, frame2)



print(f"Saved image as {filename}")


light.off()
