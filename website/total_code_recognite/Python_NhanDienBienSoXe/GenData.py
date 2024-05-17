# GenData.py

import numpy as np
import cv2
import sys


# module level variables ##########################################################################
MIN_CONTOUR_AREA = 40


RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 30

###################################################################################################
def main():
    imgTrainingNumbers = cv2.imread("training_chars.png")           
    imgGray = cv2.cvtColor(imgTrainingNumbers, cv2.COLOR_BGR2GRAY)          
    imgBlurred = cv2.GaussianBlur(imgGray, (5,5), 0)                       

                                                        
    imgThresh = cv2.adaptiveThreshold(imgBlurred,                         
                                      255,                                 
                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C,       
                                      cv2.THRESH_BINARY_INV,                
                                      11,                                
                                      2)                                  

    cv2.imshow("imgThresh", imgThresh)      # show threshold image for reference

    imgThreshCopy = imgThresh.copy()        # make a copy of the thresh image, this in necessary b/c findContours modifies the image

    npaContours, hierarchy = cv2.findContours(imgThreshCopy,       
                                                 cv2.RETR_EXTERNAL,            
                                                 cv2.CHAIN_APPROX_SIMPLE)          

    npaFlattenedImages =  np.empty((0, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))
   

    intClassifications = []         # declare empty classifications list, this will be our list of how we are classifying our chars from user input, we will write to file at the end

                                    # possible chars we are interested in are digits 0 through 9, put these in list intValidChars
    intValidChars = [ord('0'), ord('1'), ord('2'), ord('3'), ord('4'), ord('5'), ord('6'), ord('7'), ord('8'), ord('9'),
                     ord('A'), ord('B'), ord('C'), ord('D'), ord('E'), ord('F'), ord('G'), ord('H'), ord('I'), ord('J'),
                     ord('K'), ord('L'), ord('M'), ord('N'), ord('O'), ord('P'), ord('Q'), ord('R'), ord('S'), ord('T'),
                     ord('U'), ord('V'), ord('W'), ord('X'), ord('Y'), ord('Z')] #Là mã ascii của mấy chữ này

    for npaContour in npaContours:                         
        if cv2.contourArea(npaContour) > MIN_CONTOUR_AREA:          
            [intX, intY, intW, intH] = cv2.boundingRect(npaContour)         

                                                
            cv2.rectangle(imgTrainingNumbers,           
                          (intX, intY),                
                          (intX+intW,intY+intH),       
                          (0, 0, 255),                  
                          2)                            

            imgROI = imgThresh[intY:intY+intH, intX:intX+intW]                                 
            imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))    

            cv2.imshow("imgROI", imgROI)                   
            cv2.imshow("imgROIResized", imgROIResized)    
            
            cv2.imshow("training_numbers.png", imgTrainingNumbers)      

            intChar = cv2.waitKey(0)                     # get key press

            if intChar == 27:                
                sys.exit()                    
            elif intChar in intValidChars:      # else if the char is in the list of chars we are looking for . . .

                intClassifications.append(intChar)      
                #Là file chứa label của tất cả các ảnh mẫu, tổng cộng có 32 x 5 = 160 mẫu.
                npaFlattenedImage = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT)) 
                
                npaFlattenedImages = np.append(npaFlattenedImages, npaFlattenedImage, 0)                    
                
          

    fltClassifications = np.array(intClassifications, np.float32)                  
    
    npaClassifications = fltClassifications.reshape((fltClassifications.size, 1))  
    print ("\n\ntraining complete !!\n")

    np.savetxt("classifications.txt", npaClassifications)           # write flattened images to file
    np.savetxt("flattened_images.txt", npaFlattenedImages)          #

    cv2.destroyAllWindows()             # remove windows from memory

    return

###################################################################################################
if __name__ == "__main__":
    main()
    

