import sys
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsRectItem, QApplication, QGraphicsPixmapItem, \
    QMainWindow, QLabel
from PyQt6.QtGui import QBrush, QPen, QPixmap, QPainter
from PyQt6.QtCore import Qt


class Canvas(QGraphicsView):
    def __init__(self, width: int, height: int, background_colour: Qt.GlobalColor):
        super().__init__(None)
        self._background_colour = background_colour
        self._recreate_scene(width, height)
        self._last_drawn_width = self.geometry().width()
        self._last_drawn_height = self.geometry().height()

    def paintEvent(self, event):
        width = self.geometry().width()
        height = self.geometry().height()
        if self._last_drawn_width != width or self._last_drawn_height != height:
            self._recreate_scene(width, height)
            self._last_drawn_width = width
            self._last_drawn_height = height

        super().paintEvent(event)

    def _recreate_scene(self, width: int, height: int):
        print("REDRAW***", width, height)
        pixmap = QPixmap(width, height)
        pixmap.fill(self._background_colour)

        painter = QPainter(pixmap)
        painter.fillRect(0, 0, round(width / 2), round(height / 2), Qt.GlobalColor.green)
        painter.end()

        scene = QGraphicsScene(0, 0, width, height)
        rect = QGraphicsRectItem(0, 0, width/3, height/3)
        rect.setPos(width/10, height/10)
        brush = QBrush(Qt.GlobalColor.red)
        rect.setBrush(brush)
        pen = QPen(Qt.GlobalColor.cyan)
        pen.setWidth(10)
        rect.setPen(pen)

        scene.addItem(QGraphicsPixmapItem(pixmap))
        scene.addItem(rect)

        self.setScene(scene)


