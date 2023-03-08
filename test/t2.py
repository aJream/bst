from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QTransform, QPainter
from PyQt5.QtCore import Qt, QRectF
import sys



class ImageViewer(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.image_item = QGraphicsPixmapItem()
        self.scene.addItem(self.image_item)
        self.setRenderHint(QPainter.Antialiasing, True)
        self.setRenderHint(QPainter.SmoothPixmapTransform, True)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setInteractive(True)
        self._zoom = 0

    def setImage(self, image_path):
        pixmap = QPixmap(image_path)
        self.image_item.setPixmap(pixmap)
        self.setSceneRect(QRectF(pixmap.rect()))

    def wheelEvent(self, event):
        zoom_step = 1
        scale = 1.1 ** self._zoom
        

        if event.angleDelta().y() > 0:
            self._zoom += zoom_step
            transform = QTransform().scale(scale, scale)
            self.setTransform(transform)
            # self.updateTransform()
        else:
            self._zoom -= zoom_step
            transform = QTransform().scale(scale, scale)
            self.setTransform(transform)
            # self.updateTransform()

    def updateTransform(self):
        scale = 1.1 ** self._zoom
        transform = QTransform().scale(scale, scale)
        self.setTransform(transform)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageViewer()
    window.setImage('../resources/t.jpg')
    window.show()
    sys.exit(app.exec_())
