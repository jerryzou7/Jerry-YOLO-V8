import cv2
import torch
from ultralytics import YOLO
import random


model_heavy = YOLO('yolov8s.pt')  # 較慢
model_light = YOLO('yolov8n.pt')  # 快速

battery_level = 100
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 模擬 battery 消耗
    battery_level -= random.uniform(0.5, 1.0)
    if battery_level < 20:
        battery_level = 100  # 模擬充電

    # 選擇模型
    if battery_level > 50:
        model = model_heavy
        model_name = "YOLOv8s (Heavy)"
    else:
        model = model_light
        model_name = "YOLOv8n (Light)"

    # YOLOv8 推論
    results = model.predict(frame, verbose=False)

    # 畫出偵測結果
    annotated_frame = results[0].plot()

    # 顯示 Battery 和模型名稱
    cv2.putText(annotated_frame, f"Battery: {int(battery_level)}%", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    cv2.putText(annotated_frame, f"Model: {model_name}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Edge AI Demo (YOLOv8)", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()