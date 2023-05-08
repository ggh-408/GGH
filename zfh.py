import os
import cv2
import numpy as np

ascii_char = r"@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'"
path_image = "/Users/ggh/Desktop/python/zfh/image"
path_txt = "/Users/ggh/Desktop/python/zfh/txt"

if os.path.exists(path_txt):
    for file in os.listdir(path_txt):
        os.remove(path_txt + "/" + file)
else:
    os.makedirs(path_txt)
files = os.listdir(path_image)
files.sort(key=lambda x: int(x[:-4]))
for file in files:
    text = str()
    img = cv2.imread(path_image + "/" + file)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (100, 100 * img.shape[0] // img.shape[1]))
    img = np.array(img)
    for row in range(img.shape[0]):
        for col in range(img.shape[1]):
            text += ascii_char[img[row][col] // 67]
        text += '\n'
    with open(path_txt + "/" + file[:-3] + "txt", 'w') as f:
        f.write(text)

files = os.listdir(path_image)
height, width = cv2.imread(path_image + "/" + files[0]).shape[:2]
height, width = int(height * 0.75), int(width * 0.6)
files = os.listdir(path_txt)
files.sort(key=lambda x: int(x[:-4]))
image = np.full((height, width), fill_value=255, dtype=np.uint8)

for file in files:
    img = image.copy()
    with open(path_txt + "/" + file, 'r') as f:
        for i, txt in enumerate(f.read().split('\n')):
            y = 10 * (i + 1)
            cv2.putText(img, txt, (0, y), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 0, 0))
    cv2.imshow('cxk', img)
    cv2.waitKey(100)
