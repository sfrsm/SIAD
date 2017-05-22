# Standard imports
import cv2
import numpy as np;

def findCorona(image):
    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    params.minThreshold = 220;
    params.maxThreshold = 255;

    # Minimal distance between blobs
    params.minDistBetweenBlobs = 20

    # Filter by Area.
    params.filterByArea = True
    params.minArea = 20
    #params.maxArea = 200

    params.filterByColor = True
    params.blobColor = 255

    # Filter by Circularity
    params.filterByCircularity = False
    params.minCircularity = 0.1

    # Filter by Convexity
    params.filterByConvexity = False
    params.minConvexity = 0.87

    # Filter by Inertia
    params.filterByInertia = False
    params.minInertiaRatio = 0.2

    # Create a detector with the parameters
    detector = cv2.SimpleBlobDetector_create(params)

    imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img2 = cv2.bilateralFilter(imgGray, 15, 75, 75)

    keypoints = detector.detect(img2)
    return keypoints


# Read image
im = cv2.imread('images/corona-13.jpg')

# Detect blobs.
keypoints = findCorona(im)

print 'Deteccoes: ' + str(len(keypoints))


# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0, 0, 255),
                                      cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)