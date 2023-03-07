import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QPen, QPainter
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene


class CustomGraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Custom GraphicsView')

        # 创建场景和项
        scene = QGraphicsScene(self)
        scene.setSceneRect(0, 0, 300, 300)
        rect_item = scene.addRect(50, 50, 100, 100, QPen(
            Qt.black), QBrush(QColor(255, 0, 0)))
        ellipse_item = scene.addEllipse(
            150, 150, 100, 100, QPen(Qt.black), QBrush(QColor(0, 255, 0)))

        # 设置场景和视图
        self.setScene(scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CustomGraphicsView()
    sys.exit(app.exec_())
