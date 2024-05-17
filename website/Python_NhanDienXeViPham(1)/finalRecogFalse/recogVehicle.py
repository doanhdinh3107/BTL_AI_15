import cv2
import numpy as np
import os

# output_dir = 'detected_images'
# print("Attempting to create directory:", output_dir)
# os.makedirs(output_dir, exist_ok=True)
# print("Directory created successfully:", output_dir)
def recognize(image_path, name):
    # Load pre-trained model
    net = cv2.dnn.readNetFromDarknet('D:/Study/LaptrinhPython/BackendWebsite/website/Python_NhanDienXeViPham/finalRecogFalse/yolov3.cfg', 'D:/Study/LaptrinhPython/BackendWebsite/website/Python_NhanDienXeViPham/finalRecogFalse/yolov3.weights')

    # Load các lớp của mô hình
    with open('D:/Study/LaptrinhPython/BackendWebsite/website/Python_NhanDienXeViPham/finalRecogFalse/coco.names', 'r') as f:
        classes = f.read().strip('\n').split('\n')


    # image = cv2.imread('images/t2.png')
    image = cv2.imread(image_path)
    height, width = image.shape[:2]
    top_left = (820, 5)
    bottom_right = (850, 60)
    roi = image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    # Tạo blob từ ảnh và truyền vào mạng
    blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    # Thực hiện phát hiện đối tượng
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    outputs = net.forward(output_layers)

    # Tạo mask để chỉ giữ lại các pixel có giá trị màu đỏ
    lower_red = np.array([0, 0, 100])
    upper_red = np.array([80, 80, 255])
    red_mask = cv2.inRange(roi, lower_red, upper_red)

    # Tìm contours từ mask
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)

    bounding_boxes = []

    # Xác định bounding box cho mỗi phương tiện
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

                bounding_boxes.append([x, y, x + w, y + h, confidence])

    #loại bỏ các bounding box trùng lắp
    # chuyển thành mảng
    bounding_boxes = np.array(bounding_boxes)
    # Apply non-maximum suppression
    indices = cv2.dnn.NMSBoxes(bounding_boxes[:, :4], bounding_boxes[:, 4], score_threshold=0.5, nms_threshold=0.4)

    list_vehicle = list()
    cnt = 1
    for i in indices.flatten():
        bbox = bounding_boxes[i]
        x, y, x2, y2 = map(int, bbox[:4])  # Đưa toạ độ về kiểu int
        cv2.rectangle(image, (x, y), (x2, y2), (0, 0, 255), 2)
        roi_vp = image[y + 20:y2 - 20, x + 20:x2 - 20]

        try:
            cv2.imwrite(f'D:/Study/LaptrinhPython/BackendWebsite/website/static/video/{name}_{cnt}.png', roi_vp)
            list_vehicle.append(name + "_" + str(cnt) + ".png")
            cnt += 1
        except:
            continue
        # else:
        #     cv2.rectangle(image, (x, y), (x2, y2), (0, 255, 0), 2)


    cv2.line(image, (500, 770), (1800, 700), (0, 255, 255), 2)  # y= −7/130 * x + 10360/13
    cv2.line(image, (500, 420), (1800, 360), (0, 255, 255), 2)  # y= −7/130 * x + 10360/13 - 40

    # Tạo cửa sổ hiển thị với kích thước tự động
    cv2.namedWindow('Rectangle', cv2.WINDOW_NORMAL)
    cv2.imshow('Rectangle', image)

    # cv2.waitKey(0)
    cv2.destroyAllWindows()

    return list_vehicle