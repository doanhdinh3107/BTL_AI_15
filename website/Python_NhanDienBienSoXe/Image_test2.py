import math

import cv2
import numpy as np

# import Preprocess

from website.Python_NhanDienBienSoXe import Preprocess



def xuly(filename):
    ADAPTIVE_THRESH_BLOCK_SIZE = 19
    ADAPTIVE_THRESH_WEIGHT = 9

    n = 1
    list_plate=set()
    Min_char = 0.01
    Max_char = 0.09

    RESIZED_IMAGE_WIDTH = 20
    RESIZED_IMAGE_HEIGHT = 30

    # img = cv2.imread("data/image/20.jpg")
    # img = cv2.imread("D:/Study/LaptrinhPython/BackendWebsite/website/static/video/20.jpg")
    img = cv2.imread(filename)
    # img = cv2.resize(img, dsize=(1920, 1080))
    img = cv2.resize(img, dsize=(1420, 1280))




    # npaClassifications = np.loadtxt("classifications.txt", np.float32)
    # npaFlattenedImages = np.loadtxt("flattened_images.txt", np.float32)
    npaClassifications = np.loadtxt("D:/Study/LaptrinhPython/BackendWebsite/website/Python_NhanDienBienSoXe/classifications.txt", np.float32)
    npaFlattenedImages = np.loadtxt("D:/Study/LaptrinhPython/BackendWebsite/website/Python_NhanDienBienSoXe/flattened_images.txt", np.float32)
    npaClassifications = npaClassifications.reshape(
        (npaClassifications.size, 1))
    kNearest = cv2.ml.KNearest_create()
    kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)


    ################ Image Preprocessing #################
    imgGrayscaleplate, imgThreshplate = Preprocess.preprocess(img)
    canny_image = cv2.Canny(imgThreshplate, 250, 255)  # Canny Edge
    kernel = np.ones((3, 3), np.uint8)
    dilated_image = cv2.dilate(canny_image, kernel, iterations=1)  # Dilation



    ###### Draw contour and filter out the license plate  #############
    contours, hierarchy = cv2.findContours(dilated_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]  # Lấy 10 contours có diện tích lớn nhất


    screenCnt = []
    for c in contours:
        peri = cv2.arcLength(c, True)  # Tính chu vi
        approx = cv2.approxPolyDP(c, 0.06 * peri, True)  # làm xấp xỉ đa giác, chỉ giữ contour có 4 cạnh
        [x, y, w, h] = cv2.boundingRect(approx.copy())
        ratio = w / h

        if (len(approx) == 4):
            screenCnt.append(approx)

            cv2.putText(img, str(len(approx.copy())), (x, y), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 0), 3)

    if screenCnt is None:
        detected = 0
        print("No plate detected")
    else:
        detected = 1

    if detected == 1:

        for screenCnt in screenCnt:
            cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)  # Khoanh vùng biển số xe

            ############## Find the angle of the license plate #####################
            (x1, y1) = screenCnt[0, 0]
            (x2, y2) = screenCnt[1, 0]
            (x3, y3) = screenCnt[2, 0]
            (x4, y4) = screenCnt[3, 0]
            array = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
            array.sort(reverse=True, key=lambda x: x[1])
            sorted_array = array
            (x1, y1) = sorted_array[0]
            (x2, y2) = sorted_array[1]
            doi = abs(y1 - y2)
            ke = abs(x1 - x2)
            angle = math.atan(doi / ke) * (180.0 / math.pi)

            ####################################

            ########## Crop out the license plate and align it to the right angle ################

            mask = np.zeros(imgGrayscaleplate.shape, np.uint8)
            new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1, )
            # cv2.imshow("new_image",new_image)

            # Cropping
            (x, y) = np.where(mask == 255)
            (topx, topy) = (np.min(x), np.min(y))
            (bottomx, bottomy) = (np.max(x), np.max(y))

            roi = img[topx:bottomx, topy:bottomy]
            imgThresh = imgThreshplate[topx:bottomx, topy:bottomy]
            ptPlateCenter = (bottomx - topx) / 2, (bottomy - topy) / 2

            if x1 < x2:
                rotationMatrix = cv2.getRotationMatrix2D(ptPlateCenter, -angle, 1.0)
            else:
                rotationMatrix = cv2.getRotationMatrix2D(ptPlateCenter, angle, 1.0)

            roi = cv2.warpAffine(roi, rotationMatrix, (bottomy - topy, bottomx - topx))
            imgThresh = cv2.warpAffine(imgThresh, rotationMatrix, (bottomy - topy, bottomx - topx))
            roi = cv2.resize(roi, (0, 0), fx=3, fy=3)
            imgThresh = cv2.resize(imgThresh, (0, 0), fx=3, fy=3)

            #################### Prepocessing and Character segmentation ####################
            kerel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            thre_mor = cv2.morphologyEx(imgThresh, cv2.MORPH_DILATE, kerel3)
            cont, hier = cv2.findContours(thre_mor, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            cv2.imshow(str(n + 20), thre_mor)
            cv2.drawContours(roi, cont, -1, (100, 255, 255), 2)  # Vẽ contour các kí tự trong biển số

            ##################### Filter out characters #################
            char_x_ind = {}
            char_x = []
            height, width, _ = roi.shape
            roiarea = height * width

            for ind, cnt in enumerate(cont):
                (x, y, w, h) = cv2.boundingRect(cont[ind])
                ratiochar = w / h
                char_area = w * h

                if (Min_char * roiarea < char_area < Max_char * roiarea) and (0.25 < ratiochar < 0.7):
                    if x in char_x:  # Sử dụng để dù cho trùng x vẫn vẽ được
                        x = x + 1
                    char_x.append(x)
                    char_x_ind[x] = ind


            ############ Character recognition ##########################

            char_x = sorted(char_x)
            strFinalString = ""
            first_line = ""
            second_line = ""

            for i in char_x:
                (x, y, w, h) = cv2.boundingRect(cont[char_x_ind[i]])
                cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)

                imgROI = thre_mor[y:y + h, x:x + w]

                imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))
                #lam phang mang de co cung kich co voi diem anh (1,600) trong mang flattend_image(moi anh lam phang tuong ung 1 hnag trong mang 2d do)
                npaROIResized = imgROIResized.reshape(
                    (1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))

                npaROIResized = np.float32(npaROIResized)
                #600 diem anh voi moi diem anh tim k lan can de  bau phieu xet xem no thuoc lable nao
                _, npaResults, neigh_resp, dists = kNearest.findNearest(npaROIResized,k=3)
                strCurrentChar = str(chr(int(npaResults[0][0])))

                cv2.putText(roi, strCurrentChar, (x, y + 50), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 255, 0), 3)

                if (y < height / 3):  # decide 1 or 2-line license plate
                    first_line = first_line + strCurrentChar
                else:
                    second_line = second_line + strCurrentChar
            if(len(first_line+second_line)>=8):
                print("\n License Plate " + str(n) + " is: " + first_line + second_line + "\n")
                n = n + 1


            plate=first_line  + second_line
            if( plate not in list_plate and len(plate)>=8):
                list_plate.add(plate)
            roi = cv2.resize(roi, None, fx=0.75, fy=0.75)
            cv2.imshow(str(n), cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))
             # cv2.putText(img, first_line + "-" + second_line ,(topy ,topx),cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 255), 2)


    img = cv2.resize(img, None, fx=0.5, fy=0.5)
    cv2.imshow('License plate', img)

    # cv2.waitKey(0)
    return list_plate