import cv2
import numpy as np

# Load pre-trained model
net = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')

# Lấy danh sách các chỉ số đầu ra không kết nối trong mạng
unconnected_out_layers = net.getUnconnectedOutLayers()

# In giá trị trả về
print("Giá trị trả về của hàm net.getUnconnectedOutLayers():", unconnected_out_layers)

# Kiểm tra kiểu dữ liệu của biến unconnected_out_layers
print("Kiểu dữ liệu của biến unconnected_out_layers:", type(unconnected_out_layers))

