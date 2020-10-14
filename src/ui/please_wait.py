import tkinter as tk
import time

class PleaseWait():
    def __init__(self, root :tk.Frame, canvas :tk.Canvas):
        self.canvas = canvas
        self.root = root

        self.percent_done = 0
        self.widgets = []
        self.title = ""

    def start(self, title):
        self.stop()
        self.root.config(cursor="watch")
        self.title = title
        self.redraw()

    def stop(self, pause_seconds=0):
        time.sleep(pause_seconds)
        self.remove_previous_widgets()
        self.root.update()
        self.percent_done = 0
        self.root.config(cursor="")

    def set_progress(self, percent_done):
        if percent_done < 0:
            percent_done = 0
        if percent_done > 100:
            percent_done = 100
        if int(round(percent_done)) != self.percent_done:
            self.percent_done = int(round(percent_done))
            self.redraw()

    def redraw(self):
        self.remove_previous_widgets()

        x = self.canvas.winfo_width() / 2
        y = self.canvas.winfo_height() / 2

        total_width = 200
        outline_width = 6

        self.widgets.append(self.canvas.create_rectangle(
            x - total_width/2, y - 30,
            x + total_width/2, y + 30,
            fill="black", outline="grey", width=outline_width))

        if self.percent_done > 0:
            percent_width = (total_width - 2 * outline_width) * self.percent_done / 100
            percent_left = x - total_width / 2 + outline_width
            self.widgets.append(self.canvas.create_rectangle(
                percent_left, y - 30 + outline_width,
                percent_left + percent_width, y + 30 - outline_width,
                fill="grey", width=0))

        self.widgets.append(self.canvas.create_text(
            x, y, text=self.title,
            fill="Blue", font=("", 16)))

        self.root.update()

    def remove_previous_widgets(self):
        for w in self.widgets:
            self.canvas.delete(w)

        self.widgets = []











