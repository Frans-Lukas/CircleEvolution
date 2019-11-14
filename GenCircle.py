import math
import random


class GeneticCircles:
    def __init__(self, width, height, radius, number_of_circles, gen_size, mutation_amount):
        self.w = width
        self.h = height
        self.r = radius
        self.num_circ = number_of_circles
        self.gen_size = gen_size
        self.mut = mutation_amount
        self.curr_gen = []

    def distance(self, c1, c2):
        return math.sqrt((c1.x - c2.x) ** 2 + (c1.y - c2.y) ** 2)

    def intersecting(self, c1, c2):
        d = self.distance(c1, c2)
        return d < (c1.r + c2.r)

    def intersecting_amount(self, c1, c2):
        d = self.distance(c1, c2)
        if d > (c1.r + c2.r):
            return 0
        else:
            return abs(d - c1.r)

    def evaluate_generation(self, generation):
        score = 0
        for circle in generation:
            for sub_circle in generation:
                if circle == sub_circle:
                    continue
                else:
                    i_amnt = self.intersecting_amount(circle, sub_circle)
                    if i_amnt > 0:
                        score += i_amnt
        return score

    def mark_overlapping(self, circles):
        for circle in circles:
            for sub_circle in circles:
                if circle == sub_circle:
                    continue
                elif self.intersecting_amount(circle, sub_circle) > 0:
                    circle.lap = True

    def initial_generation(self):
        self.curr_gen.clear()
        for i in range(self.gen_size):
            self.curr_gen.append(
                [Circle(random.randint(0, self.w), random.randint(0, self.h), self.r) for i in range(self.num_circ)])

    def get_top_circles(self):
        index = 0
        min_val = 100000
        for i in range(len(self.curr_gen)):
            result = self.evaluate_generation(self.curr_gen[i])
            if result < min_val:
                min_val = result
                index = i
        return self.curr_gen[index]

    def breed(self):
        pass

    def select_breeders(self):
        pass


class Circle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.lap = False
