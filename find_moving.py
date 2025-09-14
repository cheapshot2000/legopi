# Stop libcamera output annoyance - 3 is error level only.
import os
os.environ["LIBCAMERA_LOG_LEVELS"] = "*:3"

import cv2
import time
import buildhat
import json
import numpy as np
import requests
from datetime import datetime
from picamera2 import Picamera2

# # TWEAKS GO HERE
# LIGHTS_PORT = 'D'
# CONVEYOR_PORT = 'A'
# CONVEYOR_MOTOR_SPEED = 10
# BASE_FILENAME = f"tmp/image_{datetime.now().strftime('%Y%m%d_%H%M%S_')}"
# MIN_AREA_BOUNDING_BOX = 12000   # Skip little movemenents
# MAX_AREA_BOUNDING_BOX = 500000  # Skip large movemenents

# # Initialization stuff

# # Lights, Camera, Action!
# light = buildhat.Light(LIGHTS_PORT)
# light.on()

# # Camera
# picam2 = Picamera2()
# picam2.configure(picam2.create_still_configuration())
# picam2.set_controls({
#     "AeEnable": False,          # Disable auto exposure
#     "AfMode": 2,                # 1 = Auto. # 2 = Continuous
#     "AfTrigger": 0,             # 0 = Start single autofocus scan
#     "ExposureTime": 20000,      # in microseconds (e.g., 20000 = 1/50s)
#     "AnalogueGain": 7.0         # Higher = brighter (range 1.0–~16.0)
# })
# picam2.start()
# time.sleep(2) # Wait briefly for camera to warm up

# # Action
# conveyor = buildhat.Motor(CONVEYOR_PORT)
# conveyor.start(CONVEYOR_MOTOR_SPEED)



# def capture_image() -> np.ndarray:
#     conveyor.stop()
#     time.sleep(.2)
#     frame = picam2.capture_array("main")
#     time.sleep(.2)
#     conveyor.start(CONVEYOR_MOTOR_SPEED)
#     return frame

# def blur_image(frame: np.ndarray) -> np.ndarray:
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     blurred = cv2.GaussianBlur(gray, (21, 21), 0)
#     return blurred





# # Capture the first frame
# frame1 = capture_image()
# cv2.imwrite(BASE_FILENAME + "frame1.jpg", frame1)

# # Making grey scale and blurring//softening
# blur1 = blur_image(frame1)
# cv2.imwrite(BASE_FILENAME + "blur1.jpg", blur1)



# # Wait and capture the second frame
# time.sleep(.33)


# frame2 = capture_image()
# cv2.imwrite(BASE_FILENAME + "frame2.jpg", frame2)

# blur2 = blur_image(frame2)
# cv2.imwrite(BASE_FILENAME + "blur2.jpg", blur2)


# # Compute difference and threshold
# delta = cv2.absdiff(blur1, blur2)
# cv2.imwrite(BASE_FILENAME + "absdiff.jpg", delta)

# thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
# cv2.imwrite(BASE_FILENAME + "thresh.jpg", thresh)

# dilate = cv2.dilate(thresh, None, iterations=2)
# cv2.imwrite(BASE_FILENAME + "dilate.jpg", dilate)

# # Find contours of moving objects
# contours, _ = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


# Draw bounding boxes
# for c in contours:
#     area = cv2.contourArea(c)
#     if area < MIN_AREA_BOUNDING_BOX: # or area > MAX_AREA_BOUNDING_BOX:
#         continue
#     (x, y, w, h) = cv2.boundingRect(c)
#     cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)


# # Save result
# cv2.imwrite(BASE_FILENAME + "diff.jpg", frame2)



# print(f"Saved images as {BASE_FILENAME}")

# Call Brickognize:

def recognize_brick(frame: np.ndarray) -> dict:
    # Convert the frame to JPEG format
    _, img_encoded = cv2.imencode('.jpg', frame)
    img_bytes = img_encoded.tobytes()

    # Prepare the API endpoint and headers
    url = "https://api.brickognize.com/predict/"
    headers = {'accept': 'application/json'}

    # Prepare the image file for the POST request
    files = {'query_image': ('image.jpg', img_bytes, 'image/jpeg')}

    # Send the POST request to the Brickognize API
    response = requests.post(url, headers=headers, files=files)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()  # Return the JSON response
    else:
        response.raise_for_status()  # Raise an exception for HTTP errors


# Recognize the LEGO brick
frame3 = cv2.imread('tmp/image_20250831_154219_frame1.jpg')
result = recognize_brick(frame3)
print(json.dumps(result, indent=4))

# # Turn things off
# light.off()
# conveyor.stop()
# del conveyor
