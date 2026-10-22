# smart-study-monitor

# Smart Study Monitor

I built this project during a hackathon to tackle a problem almost every student deals with: getting distracted by a phone or falling asleep while trying to study. 

It uses your webcam to monitor your study session in real time, catching you when you pick up your phone or close your eyes, and playing an alarm to force you back to work.

---

## What it does

The script runs a live webcam feed and continuously checks for two main distraction triggers:

- **Phone Detection:** Uses YOLOv8 (`yolov8n.pt`) to scan each frame for cell phones. If a phone appears in front of the camera, a bounding box pops up with a warning text.
- **Sleep/Drowsiness Detection:** Uses OpenCV eye cascades to track whether your eyes are open. If your eyes stay closed for more than 15 consecutive frames, it assumes you're dozing off.
- **Audio Alarm:** When either distraction is detected, it triggers `alaram.mp3` via Pygame to wake you up or tell you to put the phone away.

---

## Tech Stack & Dependencies

You'll need Python 3.10+ and the following libraries:

- `ultralytics` (YOLOv8 model engine)
- `opencv-python` (Webcam handling & eye detection)
- `pygame` (Playing the audio warning)

---

## How to Set It Up

1. **Clone this repository:**
   ```bash
   git clone [https://github.com/faridiasad19/smart-study-monitor.git](https://github.com/faridiasad19/smart-study-monitor.git)
   cd smart-study-monitor
