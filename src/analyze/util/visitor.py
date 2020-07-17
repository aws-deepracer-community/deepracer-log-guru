from src.graphics.track_graphics import TrackGraphics
import math

class VisitorMap:

    def __init__(self, min_x, min_y, max_x, max_y, granularity):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y

        self.granularity = granularity

        x_size = self.get_x_index(max_x) + 1
        y_size = self.get_y_index(max_y) + 1

        self.visits = [[0] * x_size for _ in range(y_size)]
        self.last_visitor = [[None] * x_size for _ in range(y_size)]

    def get_x_index(self, value):
        value = max(min(value, self.max_x), self.min_x)
        return round((value - self.min_x - self.granularity/2) / self.granularity)

    def get_y_index(self, value):
        value = max(min(value, self.max_y), self.min_y)
        return round((value - self.min_y - self.granularity/2) / self.granularity)

    def visit(self, x, y, visitor):
        x_index = self.get_x_index(x)
        y_index = self.get_y_index(y)

        if visitor != self.last_visitor[y_index][x_index]:
            self.last_visitor[y_index][x_index] = visitor
            self.visits[y_index][x_index] += 1

    def draw(self, track_graphics :TrackGraphics, extra_bright :bool):
        # self.print_debug()

        max_visits = max(max(x) for x in self.visits)

        if max_visits == 0:
            return

        colour_multiplier = 255 / max_visits / max_visits * 2
        min_visits = max_visits / 10

        if extra_bright:
            colour_multiplier *= 2
            min_visits /= 2

        for yy, visits in enumerate(self.visits):
            for xx, visit in enumerate(visits):
                if visit >= min_visits:
                    x = self.min_x + self.granularity * xx
                    y = self.min_y + self.granularity * yy

                    h = hex(round(min(255, 30 + colour_multiplier * visit * visit)))[2:]

                    if len(h) == 1:
                        h = "0" + h

                    colour = "#" + h*3

                    track_graphics.plot_box(x, y, x + self.granularity, y + self.granularity, colour)



    def print_debug(self):
        for v in reversed(self.visits):
            s = ""
            for w in v:
                if w == 0:
                    s += "  "
                else:
                    s += str(w) + " "
            print(s)

def multi_draw(track_graphics :TrackGraphics, visitors, colours, threshold):
    assert len(colours) == len(visitors)
    assert threshold >= 1

    min_x = visitors[0].min_x
    min_y = visitors[0].min_y
    granularity = visitors[0].granularity


    for yy in range(0, len(visitors[0].visits)):
        for xx in range(0, len(visitors[0].visits[0])):
            visits = []
            for v in range(0, len(visitors)):
                visits.append(visitors[v].visits[yy][xx])

            if sum(visits) >= threshold:
                target = max(visits)
                colour = ""
                for i, v in enumerate(visits):
                    if v >= target:
                        colour = colours[i]

                x = min_x + granularity * xx
                y = min_y + granularity * yy

                track_graphics.plot_box(x, y, x + granularity, y + granularity, colour)

def test_it():
    map = VisitorMap(1, 1, 5.99, 7.99, 0.5)

    print(map.get_x_index(1))
    print(map.get_x_index(1.24))
    print(map.get_x_index(1.25))
    print(map.get_x_index(1.49))
    print(map.get_x_index(1.51))


    map.visit(1, 1, "aaa")
    map.visit(6, 7, "bbb")
    map.visit(6, 7, "ccc")

    # map.print_debug()

    map.visit(5.9, 6.9, "zzz")

    map.visit(1.26, 1.26, "a")
    map.visit(1.4, 1.4, "b")
    map.visit(1.6, 1.6, "c")
    map.visit(1.8, 1.8, "d")

    map.visit(3, 3, "d")
    map.visit(4, 4, "d")
    map.visit(5, 5, "d")

    map.print_debug()




# RUN TEST
#test_it()



