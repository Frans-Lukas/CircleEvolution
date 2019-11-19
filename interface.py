import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *

from GenCircle import GeneticCircles


class Window():
    def __init__(self, width, height):
        self.master = Tk()
        self.btn_setup()
        self.counter = 0
        self.w = Canvas(self.master, width=width, height=height)
        self.w.pack()
        rad = 30
        num_circs = 100
        gen_size = 100
        mut_amt = 1
        self.gc = GeneticCircles(width, height, rad, num_circs, gen_size, mut_amt)
        self.gc.initial_generation()
        self.draw_gc_circles()
        self.score = [self.gc.evaluate_generation(self.gc.get_top_circles(1)[0])]

    def done(self):
        df = pd.DataFrame(self.score, columns=['score'])
        df.plot(y="score", use_index=True)
        plt.show()

    def btn_setup(self):
        btn_next = Button(self.master, text="Next", command=self.next)
        btn_next_10 = Button(self.master, text="Next 10", command=self.next_10)
        btn_next_100 = Button(self.master, text="Next 100", command=self.next_100)
        btn_done = Button(self.master, text="Graph", command=self.done)
        btn_next.pack()
        btn_next_10.pack()
        btn_next_100.pack()
        btn_done.pack()



    def next_100(self):
        for _ in range(100):
            self.clear_drawings()
            self.gc.new_generation()
            self.score.append(self.gc.evaluate_generation(self.gc.get_top_circles(1)[0]))
            self.draw_gc_circles()

    def next_10(self):
        for _ in range(10):
            self.clear_drawings()
            self.gc.new_generation()
            self.score.append(self.gc.evaluate_generation(self.gc.get_top_circles(1)[0]))
            self.draw_gc_circles()

    def next(self):
        self.clear_drawings()
        self.gc.new_generation()
        self.score.append(self.gc.evaluate_generation(self.gc.get_top_circles(1)[0]))
        self.draw_gc_circles()

    def clear_drawings(self):
        self.w.delete("all")

    def create_circle(self, x, y, r, **kwargs):
        self.w.create_oval(x - r, y - r, x + r, y + r, kwargs)

    def add_circles(self, circles):
        for circle in circles:
            self.create_circle(circle[0], circle[1], circle[2])

    def show(self):
        mainloop()

    def draw_gc_circles(self):
        top_circles = self.gc.get_top_circles(1)[0]
        self.gc.mark_overlapping(top_circles)
        for circle in top_circles:
            if circle.lap:
                self.create_circle(circle.x, circle.y, circle.r, fill="red")
            else:
                self.create_circle(circle.x, circle.y, circle.r)



window = Window(800,800)
window.show()
