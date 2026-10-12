from ultralytics import YOLO
import os

# Auto-download safe model loading
model = YOLO("yolov8n.pt")

def detect(frame):
    return model(frame, verbose=False)