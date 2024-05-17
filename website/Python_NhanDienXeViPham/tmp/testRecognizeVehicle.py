import cv2
import numpy as np

# Load pre-trained model
net = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')

# Load các lớp của mô hình
with open('coco.names', 'r') as f:
    classes = f.read().strip('\n').split('\n')

# Đọc ảnh đầu vào
image = cv2.imread('images/f1.jpg')
height, width = image.shape[:2]
# Tạo blob từ ảnh và truyền vào mạng
blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
net.setInput(blob)

print(blob)

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
             # trung điểm cạnh dưới
            bottom_center_x = center_x
            bottom_center_y = y + h
            # Vẽ dấu chấm đỏ
            cv2.circle(image, (bottom_center_x, bottom_center_y), 3, (0, 0, 255), -1)
            cv2.putText(image, classes[class_id], (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            if  bottom_center_y >= bottom_center_x * 67/472 + 337.6:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255) )  
            else:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0))

cv2.line(image,(38,343),(510,410),(0,255,255),2)
cv2.putText(image, f'({38}, {343})', (38,343 ), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,0,0), 1)
cv2.putText(image, f'({510}, {410})', (510,410 ), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,0,0), 1)

# Hiển thị ảnh đã được nhận diện
cv2.imshow('CHECK VAR', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
