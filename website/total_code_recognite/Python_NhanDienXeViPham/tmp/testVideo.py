import cv2
import numpy as np
import os
# Load pre-trained model
net = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')

# Load các lớp của mô hình
with open('coco.names', 'r') as f:
    classes = f.read().strip('\n').split('\n')

# Đọc video đầu vào
video = cv2.VideoCapture('images/Ngã Tư Đường Phố.mp4')
output_dir = 'detected_images'
print("Attempting to create directory:", output_dir)
os.makedirs(output_dir, exist_ok=True)
print("Directory created successfully:", output_dir)
while True:
    ret, frame = video.read()
    if not ret:
        break

    height, width = frame.shape[:2]
    # Tạo blob từ frame và truyền vào mạng
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    # Thực hiện phát hiện đối tượng
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    outputs = net.forward(output_layers)

    # Xác định và vẽ hộp giới hạn cho các đối tượng được phát hiện
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                bottom_center_x = center_x
                bottom_center_y = y + h

                if bottom_center_y >= bottom_center_x * 67/472 + 337.6:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255))
                    # Lưu hình ảnh vào thư mục
                    filename = os.path.join(output_dir, f"detected_{class_id}_{confidence:.2f}.jpg")
                    cv2.imwrite(filename, frame)
                else:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0))

                cv2.putText(frame, classes[class_id], (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    cv2.imshow('Object Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()