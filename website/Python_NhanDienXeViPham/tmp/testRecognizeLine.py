import cv2
import numpy as np


img = cv2.imread('images/t1.jpg')
# cv2.imshow("Display window", img)
# cv2.waitKey(0)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   
# # Phát hiện cạnh bằng phương pháp Canny
edges = cv2.Canny(gray, 50, 150, apertureSize=3)
cv2.imshow("Display window gray", edges)
cv2.waitKey(0)

# Tìm các đường thẳng bằng biến đổi Hough Line
lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=200, maxLineGap=10)
cv2.imshow( "Hough lines", edges)
cv2.waitKey(0)

# Vẽ các đường thẳng tìm được lên ảnh gốc
# if lines is not None:
#     for line in lines:
#         x1, y1, x2, y2 = line[0]
#         cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
#         # In toạ độ của điểm đầu
#         cv2.putText(img, f'({x1}, {y1})', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
#         # In tọa độ của điểm cuối
#         cv2.putText(img, f'({x2}, {y2})', (x2, y2), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,0,0), 1)
cv2.line(img,(38,343),(510,410),(0,255,0),1) # y = 167/372 x + 326
cv2.putText(img, f'({38}, {343})', (38,343 ), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,0,0), 1)
cv2.putText(img, f'({510}, {410})', (510,410 ), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,0,0), 1)
# cv2.line(img,(80,400),(500,200),(0,255,0),1)
# cv2.putText(img, f'({80}, {400})', (80, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
# cv2.putText(img, f'({500}, {200})', (500,200, ), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,0,0), 1)

# Hiển thị ảnh
cv2.imshow('Detected Lane Lines', img)
cv2.waitKey(0)
# cv2.destroyAllWindows()

