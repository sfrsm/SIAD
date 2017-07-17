# Standard imports
import sys
import os.path
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

def help():
    print '################### Usage Example ####################'
    print '##                                                  ##'
    print '## FindCorona-Video-presentation.py [videoFilePath] ##'
    print '##                                                  ##'
    print '######################################################'

if (len(sys.argv) != 2):
    help()
    exit(0)

if (os.path.exists(sys.argv[1]) == False):
    print 'Wrong video file path!!'
    exit(0)

filePath = sys.argv[1]

# Open video file
cap = cv2.VideoCapture(filePath)

frameCount = 0

monitor1 = 'Original Video'
cv2.namedWindow(monitor1)
cv2.moveWindow(monitor1, 80, 200)

monitor2 = 'Corona Video'
cv2.namedWindow(monitor2)
cv2.moveWindow(monitor2, 880, 200)

FPS = 15.0
combinedSize = (1566, 522) #h=522 w=783
videoWriter = cv2.VideoWriter('videos/videoWriter.avi', cv2.VideoWriter_fourcc('D','I','V','3'), FPS, combinedSize, True)

while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:
        frameCount += 1
        res = cv2.resize(frame, None, fx=1.45, fy=1.45, interpolation=cv2.INTER_CUBIC)
        cv2.imshow(monitor1, res)

        # Detect blobs.
        keypoints = findCorona(res)

        im_with_keypoints = cv2.drawKeypoints(res, keypoints * 4, np.array([]), (0, 0, 255),
                                              cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        res2 = cv2.resize(im_with_keypoints, None, fx=1, fy=1, interpolation=cv2.INTER_CUBIC)
        cv2.imshow(monitor2, res2)
        detections = str(len(keypoints))
        #print 'Deteccoes: ' + detections

        cv2.putText(res, "Original", (330, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(res2, "Detection", (315, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        res3 = np.concatenate((res, res2), axis=1)
        videoWriter.write(res3)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
videoWriter.release()
cv2.destroyAllWindows()