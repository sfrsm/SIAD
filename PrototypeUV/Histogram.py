# import the necessary packages
import cv2
import numpy as np
from matplotlib import pyplot as plt

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
cropping = False


def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping, drawing

    drawing = False
    cropping = False
    ix,iy = -1,-1

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE + cv2.EVENT_LBUTTONDOWN:
        if drawing == True:
            cv2.line(image, (ix, iy), (ix, y), (0, 255, 0), 1, 8, 0)
            cv2.line(image, (ix, iy), (x, iy), (0, 255, 0), 1, 8, 0)

            cv2.line(image, (ix, y), (x, y), (0, 255, 0), 1, 8, 0)
            cv2.line(image, (x, iy), (x, y), (0, 255, 0), 1, 8, 0)

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x, y))
        cropping = False
        drawing = False


        # draw a rectangle around the region of interest
        cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow("image", image)

image = cv2.imread('images/corona-2.jpg')
clone = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)

# keep looping until the 'q' key is pressed
while True:
    # display the image and wait for a keypress
    cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF

    # if the 'r' key is pressed, reset the cropping region
    if key == ord("r"):
        image = clone.copy()

    # if the 'c' key is pressed, break from the loop
    elif key == ord("c"):
        break

# close all open windows
cv2.destroyAllWindows()
# if there are two reference points, then crop the region of interest
# from teh image and display it
if len(refPt) == 2:
    roi = gray[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    cv2.imshow("ROI", roi)

    plt.subplot(221), plt.imshow(roi, 'gray')
    plt.subplot(222), plt.hist(roi.ravel(),256,[0,256])
    plt.subplot(223), plt.imshow(roi, 'gray')
    plt.subplot(224), plt.hist(roi.ravel(),256,[0,256])

    plt.show()