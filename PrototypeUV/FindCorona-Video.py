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
    params.minArea = 50
    # params.maxArea = 3000

    params.filterByColor = True
    params.blobColor = 255

    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = 0.5

    # Filter by Convexity
    params.filterByConvexity = False
    params.minConvexity = 0.87

    # Filter by Inertia
    params.filterByInertia = False
    params.minInertiaRatio = 0.01

    # Create a detector with the parameters
    detector = cv2.SimpleBlobDetector_create(params)

    imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img = cv2.bilateralFilter(image, 15, 75, 75)

    keypoints = detector.detect(img)
    return keypoints


# Read image
#im = cv2.imread('images/corona-6.jpg')
cap = cv2.VideoCapture('videos/corona-1.mp4')

frameCount = 0

monitor1 = 'Original Video'
cv2.namedWindow(monitor1)
cv2.moveWindow(monitor1, 2000, 100)

monitor2 = 'Corona Video'
cv2.namedWindow(monitor2)
cv2.moveWindow(monitor2, 300, 100)

while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:
        frameCount += 1
        res = cv2.resize(frame, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        cv2.imshow(monitor1, res)


        # Detect blobs.
        keypoints = findCorona(res)

        im_with_keypoints = cv2.drawKeypoints(res, keypoints * 4, np.array([]), (0, 0, 255),
                                              cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        res2 = cv2.resize(im_with_keypoints, None, fx=1, fy=1, interpolation=cv2.INTER_CUBIC)
        cv2.imshow(monitor2, res2)
        detections = str(len(keypoints))
        #print 'Deteccoes: ' + detections

        '''
        if detections > 0:
            filename = 'detections/corona-1-frame-' + str(frameCount) + '.png'
            cv2.imwrite(filename, im_with_keypoints)
        '''
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cv2.waitKey(0)