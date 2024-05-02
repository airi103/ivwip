import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap, QPainter, QTransform

class ImageViewer(QMainWindow):
    def __init__(self, image_path):
        super().__init__()
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)  
        self.setAttribute(Qt.WA_TranslucentBackground)  
        self.label = QLabel(self)
        self.setCentralWidget(self.label)
        self.image_path = image_path
        self.load_image()

    def load_image(self):
        self.pixmap = QPixmap(self.image_path)
        self.image_scaled = self.pixmap
        self.label.setPixmap(self.image_scaled)
        self.resize(self.image_scaled.width(), self.image_scaled.height())
        self.center_window()

    def center_window(self):
        frame_geometry = self.frameGeometry()
        center_point = QApplication.desktop().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.close()
        elif event.button() == Qt.LeftButton:
            self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_start_position)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.resize_image(1.1)
        else:
            self.resize_image(0.9)

    def resize_image(self, factor):
        width = int(self.image_scaled.width() * factor)
        height = int(self.image_scaled.height() * factor)
        self.image_scaled = self.pixmap.scaled(width, height, Qt.KeepAspectRatio)
        self.label.setPixmap(self.image_scaled)
        self.resize(self.image_scaled.width(), self.image_scaled.height())
        self.center_window()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python imageviewer.py <image_file>")
        sys.exit(1)

    app = QApplication(sys.argv)
    image_path = sys.argv[1]
    viewer = ImageViewer(image_path)
    viewer.show()
    sys.exit(app.exec_())