import cv2
import numpy as np
import imutils as im
import pytesseract
from PIL import Image

# Specifying the Path
input1 = 'car4.jpg'

# Reading the Image
img = cv2.imread(input1)

# Resizing the image to Standard Size
newwidth = 500
img = im.resize(img, width=newwidth)

# Converting the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Image Smoothing
d, sigmaColor, sigmaSpace = 10, 15, 15
flitered_img = cv2.bilateralFilter(gray, d, sigmaColor, sigmaSpace)

# Canny Edge Detection
# If intensity of pixel is greater than the upper threshold then pixel is accepted
# If intensity of pixel is less than the lower threshold then pixel is rejected
# If intensity of pixel is between lower threshold and upper threshold then pixel is accepted, only of it is connected to upper threshold
lower, upper = 170, 200
edged = cv2.Canny(flitered_img, lower, upper)

# Finding Contours
contour, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Sorting contours according to there area
contour = sorted(contour, key=cv2.contourArea, reverse=True)[:10]
print('Number of Contours found: ' + str(len(contour)))

# Iterating through all the contours
count = 0
for c in contour:
    perimeter = cv2.arcLength(c, True)
    epsilon = 0.01 * perimeter   # Epsilon is basically the maximum distance from contour to approximated contour. It is an accuracy parameter.
    # This function below is used to find the approximate shape. Eg. If we want to find a square but we are not getting it so by using this func we can find the approx shape as of the square.
    approx = cv2.approxPolyDP(c, epsilon, True)
    if len(approx) == 4: # If approx has 4 corners
        print(approx)
        NumberPlateContour = approx
        count = 1
        break

if count == 0:
    print('No License Plate Detected')
else:
    # Drawing all contours
    cv2.drawContours(img, [NumberPlateContour], -1, (0, 255, 0), 2)

# # Now as the remaining image is not useful for us so we will mask that image
# mask = np.zeros(gray.shape, np.uint8)
# new_image = cv2.drawContours(mask, [NumberPlateContour], 0, 255, -1)
# new_image = cv2.bitwise_and(img, img, mask=mask)
#
# # Now cropping this number plate from the masked image and recognising character from it using raspberry-pi
# # Now Crop
# (x, y) = np.where(mask == 255)
# (topx, topy) = (np.min(x), np.min(y))
# (bottomx, bottomy) = (np.max(x), np.max(y))
# cropped = gray[topx:bottomx+1, topy:bottomy+1]
#
# # Now Character recognition using pytesseract it is a google based OCR
# text = pytesseract.image_to_string(cropped, config='--psm 11')
# print('Detected number on the License Plate is: ' + text)

cv2.imshow('Result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()