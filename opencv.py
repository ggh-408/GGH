import math
import cv2
import numpy as np


def image_identify(image):

    return int()


def open_cv(file_name):
    demo_open_cv = [[0 for _ in range(9)] for _ in range(9)]
    img = cv2.imread(file_name)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    contour_max = [0, 0]
    counters = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    for contour in counters:
        if cv2.contourArea(contour) > contour_max[0] and np.all(contour):
            contour_max = [cv2.contourArea(contour), contour]
    approx = cv2.approxPolyDP(contour_max[1], 100, closed=True)
    src_list = [[]]*4
    point_list = [[point[0][0], point[0][1]] for point in list(approx)]
    centre = sum([point[0][0] for point in list(approx)]) / 4, sum([point[0][1] for point in list(approx)]) / 4
    for point in point_list:
        index = [[0, 2], [1, 3]][int(point[0] > centre[0])][int(point[1] > centre[1])]
        src_list[index] = point
    width = max(src_list[1][0] - src_list[0][0], src_list[3][0] - src_list[2][0])
    high = max(src_list[2][1] - src_list[0][1], src_list[3][1] - src_list[1][1])
    src_list = np.float32(src_list)
    dst = np.float32([[0, 0], [width, 0], [0, high], [width, high]])
    m = cv2.getPerspectiveTransform(src_list, dst)
    img = cv2.warpPerspective(img, m, (width, high))
    offset = int(math.sqrt(img.shape[0]*img.shape[1])/81)
    cv2.imshow("123", img)
    cv2.waitKey(0)
    for col in range(9):
        for row in range(9):
            img_part = img[int(row * img.shape[0] / 9) + offset:int((row + 1) * img.shape[0] / 9) - offset:,
                           int(col * img.shape[1] / 9) + offset:int((col + 1) * img.shape[1] / 9) - offset]

            string = image_identify(img_part)
            if string:
                demo_open_cv[row][col] = string
    return demo_open_cv
