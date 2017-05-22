import cv2
import numpy as np


def nothing(x):
    pass


def ContourMethod(image):
    _, contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnt = contours
    big_contour = []
    max = 0
    for i in cnt:
        area = cv2.contourArea(i)  # --- find the contour having biggest area ---
        if (area > max):
            max = area
            big_contour = i
    return big_contour


imgPath = 'images/corona-7.jpg'

# Criando Janela
windowImg = 'Imagem Original'
cv2.namedWindow(windowImg)

# cria trackbar na janela windowImg
cv2.createTrackbar('dp', windowImg, 2, 1000, nothing)
cv2.createTrackbar('minDist', windowImg, 40, 1000, nothing)
cv2.createTrackbar('param_1', windowImg, 1000, 10000, nothing)
cv2.createTrackbar('param_2', windowImg, 20, 1000, nothing)

# lendo a imagem
img = cv2.imread(imgPath)
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow(windowImg, img)

# img2 = cv2.GaussianBlur(imgGray, (5, 5), 5)
img2 = cv2.bilateralFilter(imgGray, 15, 75, 75)
# cv2.imshow('Bilateral Filter', img2)

# imagem filtrada
retval, threshold = cv2.threshold(img2, 220, 255, cv2.THRESH_BINARY)
# cv2.imshow('binary', threshold)

# CONTOUR METHOD
big_contour = ContourMethod(threshold)
final = cv2.drawContours(img, big_contour, -1, (0, 255, 0), 3)
cv2.imshow('Contour Method Result', final)

# CONNECTED COMPONENTS METHOD
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(threshold, 8, cv2.CV_32S)
# Get the results
# The first cell is the number of labels
print 'Num labels: ' + str(num_labels)
for i in range(0, num_labels):
    cv2.imshow('Deteccao' + str(i), labels[i])
    print 'Deteccao: ' + str(i)
    print 'Area: ' + str(stats[i, cv2.CC_STAT_AREA])

while True:
    cimg = cv2.imread(imgPath)
    dp = cv2.getTrackbarPos('dp', windowImg);
    minDist = cv2.getTrackbarPos('minDist', windowImg);
    param1 = cv2.getTrackbarPos('param_1', windowImg);
    param2 = cv2.getTrackbarPos('param_2', windowImg);
    circles = None
    print 'PROCESSA'
    print 'dp' + str(dp)
    print 'minDist ' + str(minDist)
    print 'param1 ' + str(param1)
    print 'param2 ' + str(param2)

    canny = cv2.Canny(threshold, param1 / 2, param1)
    # cv2.imshow('Canny', canny)

    circles = cv2.HoughCircles(canny, cv2.HOUGH_GRADIENT, dp, minDist, param1=param1, param2=param2, minRadius=0,
                               maxRadius=30)
    # circles = cv2.HoughCircles(img2, cv2.HOUGH_GRADIENT, dp, minDist, param1=param1, param2=param2, minRadius=0, maxRadius=30)
    print 'DESENHA'
    if circles is not None:
        circles = np.uint16(np.around(circles))
        print 'Deteccoes: ' + str(circles.size / 3)
        for i in circles[0, :]:
            cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
    # cv2.circle(cimg, (30, 30), 30, (0, 255, 0), 2)
    cv2.imshow('detected circles', cimg)
    if cv2.waitKey(0) == 27:
        break
    else:
        print 'Proximo ciclo'
        cv2.waitKey(500)

cv2.waitKey(0)
cv2.destroyAllWindows()
