import cv2
import time
import pygame
import os
import urllib.request
from ultralytics import YOLO

# 1. Automatically download the eye detection model if missing
cascade_path = "haarcascade_eye.xml"
if not os.path.exists(cascade_path):
    url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_eye.xml"
    urllib.request.urlretrieve(url, cascade_path)

# Load models
model = YOLO("yolov8n.pt")
eye_cascade = cv2.CascadeClassifier(cascade_path)

# Initialize sound
pygame.mixer.init()
sound = pygame.mixer.Sound("alaram.mp3")
last_sound = 0
sound_delay = 5

CLOSED_FRAMES_THRESHOLD = 15
closed_frames_count = 0

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Phone Detection
    results = model(frame, verbose=False)
    phone_detected = False

    for result in results:
        for box in result.boxes:
            if int(box.cls[0]) == 67 and float(box.conf[0]) > 0.5:
                phone_detected = True
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)

    # Eye Detection (Sleep detection)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # The cascade detects OPEN eyes. 
    eyes = eye_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)
    sleeping = False

    if len(eyes) == 0:
        closed_frames_count += 1
    else:
        closed_frames_count = 0
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(frame, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)

    if closed_frames_count >= CLOSED_FRAMES_THRESHOLD:
        sleeping = True

    # Warnings
    warning_text = ""
    if phone_detected and sleeping:
        warning_text = "PHONE AWAY & WAKE UP!"
    elif phone_detected:
        warning_text = "PADHLE! PUT THE PHONE AWAY!"
    elif sleeping:
        warning_text = "WAKE UP! EYES CLOSED!"

    if warning_text:
        cv2.putText(frame, warning_text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
        
        current_time = time.time()
        if current_time - last_sound > sound_delay:
            sound.play()
            last_sound = current_time

    cv2.imshow("Smart Study Monitor", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()