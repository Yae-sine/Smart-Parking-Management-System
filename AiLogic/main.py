import cv2
import json
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
from ultralytics import YOLO
import time

# YOLOv8 pré-entraîné
model = YOLO("yolov8s.pt")

cap = cv2.VideoCapture(0)

target_width = 821
target_height = 400

px_per_cm = 37.8
spot_height = int(5.5 * px_per_cm)     
spot_width = int(4.2 * px_per_cm)      
spot_spacing = int(0.4 * px_per_cm)    

parking_zones = []
start_x = 20
start_y = 100

for i in range(4):
    x = start_x + i * (spot_width + spot_spacing)
    y = start_y
    zone = {
        "points": [
            [x, y],
            [x + spot_width, y],
            [x + spot_width, y + spot_height],
            [x, y + spot_height]
        ]
    }
    parking_zones.append(zone)

window = tk.Tk()
status_dict = {}

def is_box_in_zone(box, zone_pts):
    x1, y1, x2, y2 = box
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    return cv2.pointPolygonTest(np.array(zone_pts, dtype=np.int32), (cx, cy), False) >= 0

def update_frame():
    ret, frame = cap.read()
    if not ret:
        return

    frame_resized = cv2.resize(frame, (target_width, target_height))
    results = model(frame_resized)[0]
    all_boxes = [box.xyxy[0].cpu().numpy() for box in results.boxes]

    for zone_index, zone in enumerate(parking_zones):
        zone_id = zone_index + 1
        pts = np.array(zone["points"], dtype=np.int32)
        occupied = False

        for box in all_boxes:
            if is_box_in_zone(box, pts):
                occupied = True
                break

        color = (0, 0, 255) if occupied else (0, 255, 0)
        status_dict[f"spot{zone_id}"] = "occupied" if occupied else "available"

        cv2.polylines(frame_resized, [pts], isClosed=True, color=color, thickness=2)
        cv2.putText(frame_resized, f"Spot {zone_id}: {status_dict[f'spot{zone_id}']}", tuple(pts[0]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)

    with open("status.json", "w") as f:
        json.dump(status_dict, f)

    print("Updated:", status_dict)

    for box in all_boxes:
        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(frame_resized, (x1, y1), (x2, y2), (255, 255, 0), 2)

    image = Image.fromarray(cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB))
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.image = photo
    window.geometry(f"{image.width}x{image.height}")
    window.after(1, update_frame)

label = tk.Label(window)
label.pack()
update_frame()
window.mainloop()
cap.release()
with open("status.json", "w") as f:
    json.dump(status_dict,f)