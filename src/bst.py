# 该文件实现半色调技术的代码

import cv2
import numpy as np


def getBayerMat(k):
    '''
    函数作用：获取bayer矩阵
    return：numpy类型的矩阵
    k: 是bayer矩阵的阶数，取值一般为1 2 4 8 16
    '''
    if k & (k-1) != 0:
        return False, None
    if k == 1:
        return True, np.array([[0.5]])
    m = [[0, 2], [3, 1]]
    m = np.array(m)
    while(m.shape[0] != k):
        m1 = np.zeros((m.shape[0]*2, m.shape[1]*2))
        m1[:m.shape[0], :m.shape[1]] += 4*m
        m1[:m.shape[0], m.shape[1]:] += 4*m+2
        m1[m.shape[0]:, :m.shape[1]] += 4*m+3
        m1[m.shape[0]:, m.shape[1]:] += 4*m+1
        m = m1
    return True, m


def convertImg(img, k=4, f=False, useGray=False):
    '''
    k：bayer矩阵大小
    f：由于转换后图像尺寸会变大k倍，f表示是否先缩小k倍
    useGray：传入的img是否为灰度图
    '''
    if not useGray:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if f:
        img = cv2.resize(img, dsize=None, fx=1/k, fy=1/k)
    ret, bayers = getBayerMat(k)
    if not ret:
        print(f"矩阵阶数k={k}非2的倍数")
        return
    # div = 256/(k*k)
    # img = img/div
    bayers = bayers * (256/(k*k))
    h, w = img.shape
    newImg = np.zeros((k*h, k*w), dtype='uint8')
    
    for i in range(0, h, 1):
        for j in range(0, w, 1):
            for p in range(k):
                for q in range(k):
                    if img[i][j] > bayers[p][q]:
                        newImg[k*(i)+p][k*(j)+q] = 255
                    else:
                        newImg[k*(i)+p][k*(j)+q] = 0
#     newImg = np.array(newImg, dtype='uint8')
    return newImg


def newImgWin(img):
    h, w = img.shape
    cv2.namedWindow("img", flags=cv2.WINDOW_NORMAL)
#     cv2.resizeWindow((w,h))
    cv2.imshow("img", img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    imgPath = r'D:\Users\74452\Desktop\avatars\ecy\1-1.jpg'
    # imgPath = r'D:\Users\74452\Desktop\avatars\me.jpg'
    img = cv2.imread(imgPath, 0)

    nimg = convertImg(img, k=1, f=False, useGray=True)
    # nimg = cv2.cvtColor(nimg, cv2.COLOR_GRAY2BGR)
    cv2.imwrite("../out/b2.png", nimg)
    # newImgWin(nimg)

