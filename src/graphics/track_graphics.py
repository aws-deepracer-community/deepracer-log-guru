from tkinter import *
import math

class TrackGraphics:
    def __init__(self, canvas:Canvas):
        self.canvas = canvas
        self.scale = 100.0
        self.min_x = 0
        self.max_y = 0

        self.ring_highlight_widgets = []
        self.angle_line_highlight_widgets = []
        self.car_widgets = []
        self.old_car_widgets = []

    def reset_to_blank(self):
        self.canvas.delete("all")

    def set_track_area(self, min_x, min_y, max_x, max_y):
        assert max_x > min_x
        assert max_y > min_y

        x_size = max_x - min_x
        y_size = max_y - min_y

        x_scale = self.canvas.winfo_width() / x_size
        y_scale = self.canvas.winfo_height() / y_size

        self.scale = min(x_scale, y_scale)

        x_border = (1 - self.scale / x_scale) / 2 * x_size
        y_border = (1 - self.scale / y_scale) / 2 * y_size

        self.min_x = min_x - x_border
        self.max_y = max_y + y_border

    def plot_dot(self, point, r, fill_colour):
        (x, y) = point

        x = (x - self.min_x) * self.scale
        y = (self.max_y - y) * self.scale

        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=fill_colour, width=0)

    def plot_line(self, point1, point2, width, fill_colour, dash_pattern=None):
        (x, y) = point1
        (x2, y2) = point2

        x = (x - self.min_x) * self.scale
        y = (self.max_y - y) * self.scale

        x2 = (x2 - self.min_x) * self.scale
        y2 = (self.max_y - y2) * self.scale

        return self.canvas.create_line(x, y, x2, y2, fill=fill_colour, width=width, dash=dash_pattern)

    def plot_angle_line(self, start_point, heading, distance, width, fill_colour):
        (x, y) = start_point

        radians_to_target = math.radians(heading)

        x2 = x + math.cos(radians_to_target) * distance
        y2 = y + math.sin(radians_to_target) * distance

        end_point = (x2, y2)

        return self.plot_line(start_point, end_point, width, fill_colour)

    def plot_text(self, point, text_string, font_size, colour: str):
        (x, y) = point

        x = (x - self.min_x) * self.scale
        y = (self.max_y - y) * self.scale

        self.canvas.create_text(x, y, text=text_string, fill=colour, font=("", font_size))

    def plot_box(self, x, y, x2, y2, colour):

        x = (x - self.min_x) * self.scale
        y = (self.max_y - y) * self.scale

        x2 = (x2 - self.min_x) * self.scale
        y2 = (self.max_y - y2) * self.scale

        return self.canvas.create_rectangle(x, y, x2, y2, fill=colour, width=0)

    def plot_polygon(self, points, colour):

        points_as_array = []
        for p in points:
            (x, y) = p
            points_as_array.append((x - self.min_x) * self.scale)
            points_as_array.append((self.max_y - y) * self.scale)

        self.canvas.create_polygon(points_as_array, fill=colour, width=2)

    def get_real_point_for_widget_location(self, x, y):
        return (x / self.scale) + self.min_x, self.max_y - (y / self.scale)

    def plot_ring_highlight(self, point, r, colour, line_width):

        (x, y) = point
        x = (x - self.min_x) * self.scale
        y = (self.max_y - y) * self.scale

        self.ring_highlight_widgets.append(self.canvas.create_oval(
            x - r, y - r, x + r, y + r, fill="", width=line_width, outline=colour))

    def plot_angle_line_highlight(self, start_point, heading, distance, width, fill_colour):
        self.angle_line_highlight_widgets.append(self.plot_angle_line(start_point, heading, distance, width, fill_colour))

    def remove_highlights(self):
        for w in self.ring_highlight_widgets + self.angle_line_highlight_widgets:
            self.canvas.delete(w)

    def draw_car(self, x: float, y: float, colour: str, heading: float):
        self.car_widgets.append(self.plot_box(x - 0.15, y - 0.15, x + 0.15, y + 0.15, colour))
        self.car_widgets.append(self.plot_angle_line((x, y), heading, 1, 3, colour))

    def prepare_to_remove_old_cars(self):
        self.old_car_widgets = self.car_widgets.copy()
        self.car_widgets = []

    def remove_cars(self):
        for w in self.old_car_widgets:
            self.canvas.delete(w)
        self.old_car_widgets = []
