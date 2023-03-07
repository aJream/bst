from PyQt5 import QtCore, QtGui, QtWidgets
from ui import Ui_Form
import sys
import os
import cv2
import numpy as np
import bst


class MyWidget(QtWidgets.QWidget, Ui_Form):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.spinBoxK.stepBy = lambda steps: self.spinBoxK.setValue(
            self.spinBoxK.value() * (2 ** steps))  # 指数型步长
        self.logBrowser.append("注意：建议图片大小不超过500*500，bayer不超过4，图片越大，bayer矩阵越大，转换耗时越长")
        self.img = None
        self.filepath = None

    def btnInputClick(self):
        self.filepath, filetype = QtWidgets.QFileDialog.getOpenFileName(
            self,  # 父窗口对象
            "选择一张图片",  # 窗口标题
            r"../resources",  # 自定义起始目录
            # r"D:\Users\74452\Desktop\avatars",
            # 选择类型过滤，过滤内容再括号中，如果要有多个过滤器的话，可以用 ;; 分割
            "文件类型(*.jpg;*.png;*.bmp;)"
        )
        if not self.filepath:
            self.logBrowser.append("-- 未选择图片，请重新选择")
            return
        self.lineEditFilePath.setText(self.filepath)
        self.logBrowser.append("-- 读取了一张图片")

        img = cv2.imdecode(np.fromfile(
            self.filepath, dtype=np.uint8), cv2.IMREAD_COLOR)  # 解决中文路径
        # imgGray = cv2.imread(self.filepath, 0)
        self.img = img
        imgGray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        imgGray = self.imgResize(imgGray, self.grayImgLabel)
        img = self.imgResize(img, self.rgbImgLabel)

        imgh, imgw = imgGray.shape  # 获取图片大小
        qimgGray = QtGui.QImage(
            imgGray, imgw, imgh, imgw, QtGui.QImage.Format_Grayscale8)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        qimg = QtGui.QImage(img.data, imgw, imgh,
                            imgw*3, QtGui.QImage.Format_RGB888)
        self.grayImgLabel.setPixmap(QtGui.QPixmap(qimgGray))  # 将 QPixmap 对象设置为 QLabel 的内容
        self.rgbImgLabel.setPixmap(QtGui.QPixmap(qimg))

    def btnConvertClick(self):
        k = self.spinBoxK.value()
        outImg = bst.convertImg(self.img, k, f=False, useGray=False)
        imgShow = self.imgResize(outImg, self.outImgLabel)
        qimgShow = QtGui.QImage(
            imgShow, imgShow.shape[1], imgShow.shape[0], imgShow.shape[1], QtGui.QImage.Format_Grayscale8)
        self.outImgLabel.setPixmap(QtGui.QPixmap(qimgShow))

        filename = self.filepath.split('/')[-1].split('.')[0]
        filetype = self.filepath.split('/')[-1].split('.')[1]
        savepath = f"../out/b_{filename}.{filetype}"
        if(cv2.imwrite(savepath, outImg)):
            self.logBrowser.append(
                f"转换{self.filepath}并保存成功，保存路径是：\n{savepath}\n================\n")

    def imgResize(self, img, imgLabel):
        labelW, labelH = imgLabel.width(), imgLabel.height()
        if(len(img.shape)==3):
            imgh, imgw, _ = img.shape
        else:
            imgh, imgw = img.shape
        if imgh > imgw:
            scale = labelH/imgh
        else:
            scale = labelW/imgw
        img = cv2.resize(img, dsize=None, fx=scale, fy=scale)
        return img

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MyWidget()
    w.show()
    sys.exit(app.exec_())
