import sys
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsRectItem, QApplication, QGraphicsPixmapItem, \
    QMainWindow, QLabel, QAbstractGraphicsShapeItem
from PyQt6.QtGui import QBrush, QPen, QPixmap, QPainter
from PyQt6.QtCore import Qt


class Canvas(QGraphicsView):
    def __init__(self, width: int, height: int, background_colour: Qt.GlobalColor):
        super().__init__(None)
        self._background_colour = background_colour
        self._width = self.geometry().width()
        self._height = self.geometry().height()
        self._recreate_scene()

    def paintEvent(self, event):
        new_width = self.geometry().width()
        new_height = self.geometry().height()
        if self._width != new_width or self._height != new_height:
            self._width = new_width
            self._height = new_height
            self._recreate_scene()

        super().paintEvent(event)

    def _recreate_scene(self):
        # print("REDRAW***", self._width, self._height)

        pixmap = QPixmap(self._width, self._height)
        pixmap.fill(self._background_colour)
        painter = QPainter(pixmap)
        self._paint(painter)
        painter.end()

        scene = QGraphicsScene(0, 0, self._width, self._height)
        scene.addItem(QGraphicsPixmapItem(pixmap))
        for i in self._get_scene_items():
            scene.addItem(i)
        self.setScene(scene)

    # Hardcoded examples for now - these will be abstract shortly
    def _paint(self, painter: QPainter):
        painter.fillRect(0, 0, round(self._width / 2), round(self._height / 2), Qt.GlobalColor.darkYellow)

    # Hardcoded examples for now - these will be abstract shortly
    def _get_scene_items(self) -> list[QAbstractGraphicsShapeItem]:
        rect = QGraphicsRectItem(0, 0, self._width / 3, self._height / 3)
        rect.setPos(self._width / 10, self._height / 10)
        brush = QBrush(Qt.GlobalColor.red)
        rect.setBrush(brush)
        pen = QPen(Qt.GlobalColor.cyan)
        pen.setWidth(10)
        rect.setPen(pen)

        return [rect]


