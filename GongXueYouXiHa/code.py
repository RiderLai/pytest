import cv2 as cv


def hello_gongxue():
    img = cv.imread('test.png')
    cv.namedWindow('Image')
    cv.imshow('Image', img)
    cv.waitKey(0)
    cv.destroyAllWindows()


hello_gongxue()