# v4 UI STATUS - BRAND NEW
# ************************

from abc import ABC

from graphics.canvas import Canvas
from PyQt6.QtWidgets import QAbstractGraphicsShapeItem
from PyQt6.QtGui import QPen, QPainter, QBrush, QColor, QFont
from PyQt6.QtCore import Qt

from utils import geometry

Point = (float | int, float | int)     # Typedef which we will use a lot for graphics


class CanvasItem(ABC):
    pass


class FixedShape(CanvasItem):
    pass


class FloatingShape(CanvasItem):
    pass


class TrackArea:
    def __init__(self, min_x, min_y, max_x, max_y):
        assert max_x > min_x
        assert max_y > min_y

        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y


class Scale:
    def __init__(self, min_x, max_y, scale_factor):
        self._min_x = min_x
        self._max_y = max_y
        self._scale_factor = scale_factor

    def apply(self, point: Point) -> Point:
        (x, y) = point

        x = (x - self._min_x) * self._scale_factor
        y = (self._max_y - y) * self._scale_factor

        return round(x), round(y)


class TrackAnalysisCanvas(Canvas):
    def __init__(self):
        self._track_area = TrackArea(0, 0, 100, 100)

        self._fixed_shapes = []

        # self._ring_highlight_widgets = []
        # self._angle_line_highlight_widgets = []
        # self._car_widgets = []
        # self._old_car_widgets = []

        super().__init__(Qt.GlobalColor.black)

    def reset_to_blank(self):
        self._fixed_shapes = []

    def set_track_area(self, track_area: TrackArea):
        self._track_area = track_area

    def _get_current_scale(self):
        min_x = self._track_area.min_x
        min_y = self._track_area.min_y
        max_x = self._track_area.max_x
        max_y = self._track_area.max_y

        x_size = max_x - min_x
        y_size = max_y - min_y

        x_scale = self.geometry().width() / x_size
        y_scale = self.geometry().height() / y_size

        scale = min(x_scale, y_scale)

        x_border = (1 - scale / x_scale) / 2 * x_size
        y_border = (1 - scale / y_scale) / 2 * y_size

        return Scale(min_x - x_border, max_y + y_border, scale)

    def _paint(self, painter: QPainter):
        scale = self._get_current_scale()
        for f in self._fixed_shapes:
            f.paint(painter, scale)

    def _get_scene_items(self) -> list[QAbstractGraphicsShapeItem]:
        # rect = QGraphicsRectItem(0, 0, self._width / 20, self._height / 20)
        # rect.setPos(self._width / 10, self._height / 10)
        # brush = QBrush(Qt.GlobalColor.red)
        # rect.setBrush(brush)
        # pen = QPen(Qt.GlobalColor.cyan)
        # pen.setWidth(10)
        # rect.setPen(pen)
        #
        # return [rect]
        return []

    def add_fixed_shape(self, item: FixedShape):
        self._fixed_shapes.append(item)


# plot_dot() in v3

class FilledCircle(FixedShape):
    def __init__(self, point: Point, diameter: int, colour: QColor):
        self._point = point
        self._pen = QPen(colour)
        self._diameter = diameter
        self._brush = QBrush()
        self._brush.setColor(colour)
        self._brush.setStyle(Qt.BrushStyle.SolidPattern)

    def paint(self, painter: QPainter, scale: Scale):
        x, y = scale.apply(self._point)
        painter.setPen(self._pen)
        painter.setBrush(self._brush)
        radius = self._diameter / 2
        if self._diameter >= 3:
            painter.drawEllipse(round(x - radius), round(y - radius), self._diameter, self._diameter)
        else:
            painter.drawPoint(round(x), round(y))


# def plot_line(self, point1, point2, width, fill_colour, dash_pattern=None)    in v3

class Line(FixedShape):
    def __init__(self, start: Point, finish: Point, width: int, colour: QColor, dash_pattern: (int, int) = None):
        self._start = start
        self._finish = finish
        self._pen = QPen(colour)
        self._pen.setWidth(width)
        if dash_pattern:
            self._pen.setDashPattern(dash_pattern)

    def paint(self, painter: QPainter, scale: Scale):
        x1, y1 = scale.apply(self._start)
        x2, y2 = scale.apply(self._finish)
        painter.setPen(self._pen)
        painter.drawLine(x1, y1, x2, y2)


# The point given is the approximate CENTRE of the text

class Text(FixedShape):
    last_non_overlapping_text_position = None

    def __init__(self, position: Point, text: str, font_size: int, colour: QColor, offset_x: int = 0, offset_y: int = 0):
        self._position = position
        self._text = text
        self._offset_x = offset_x
        self._offset_y = offset_y
        self._centering_x_offset = 0.4 * font_size * len(text)
        self._centering_y_offset = 0.5 * font_size
        self._spacing = 2.3 * font_size

        self._pen = QPen(colour)
        self._font = QFont()
        self._font.setPointSize(font_size)
        # self._font.setStyleStrategy(QFont.StyleStrategy.NoAntialias)

    def paint(self, painter: QPainter, scale: Scale):
        x, y = scale.apply(self._position)

        x = round(x + self._offset_x - self._centering_x_offset)
        y = round(y + self._offset_y + self._centering_y_offset)

        if Text.last_non_overlapping_text_position:
            dist = geometry.get_distance_between_points(self.last_non_overlapping_text_position, (x, y))
            if dist < self._spacing:
                return

        painter.setPen(self._pen)
        painter.setFont(self._font)
        painter.drawText(x, y, self._text)

        Text.last_non_overlapping_text_position = (x, y)
