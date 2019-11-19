import copy
import math
import random
from itertools import chain


class GeneticCircles:
    def __init__(self, width, height, radius, number_of_circles, gen_size, mutation_amount):
        self.w = width
        self.h = height
        self.r = radius
        self.num_circ = number_of_circles
        self.gen_size = gen_size
        self.mut = mutation_amount
        self.curr_gen = []

    def evaluate_generation(self, generation):
        score = 0
        for circle in generation:
            for sub_circle in generation:
                if circle == sub_circle:
                    continue
                else:
                    i_amnt = circle.intersecting_amount(sub_circle)
                    if i_amnt > 0:
                        score += i_amnt
        return score

    def mark_overlapping(self, circles):
        for circle in circles:
            for sub_circle in circles:
                if circle == sub_circle:
                    continue
                elif circle.intersecting_amount(sub_circle) > 0:
                    circle.lap = True

    def initial_generation(self):
        self.curr_gen.clear()
        for i in range(self.gen_size):
            self.curr_gen.append(
                [Circle(random.randint(0, self.w), random.randint(0, self.h), self.r) for i in range(self.num_circ)])

    def new_generation(self):
        # Selection step
        top_circles = self.get_top_circles(2)
        print(self.evaluate_generation(top_circles[0]))

        # Reproduction step
        new_generation_base = self.reproduce_top_two(top_circles)
        self.create_generation(new_generation_base)

    def create_generation(self, new_generation_base):
        self.curr_gen.clear()
        for i in range(self.gen_size):
            mutated_circles = copy.deepcopy(new_generation_base)
            for new_circle in mutated_circles:
                # Mutation step
                if random.randint(0, 100) < self.mut:
                    new_circle.x = random.randint(0, self.w)
                    new_circle.y = random.randint(0, self.h)
                new_circle.lap = False
            self.curr_gen.append(mutated_circles)

    def reproduce_top_two(self, top_circles):
        first_half = math.floor(len(top_circles[0]) / 2)
        second_half = math.ceil(len(top_circles[1]) / 2)
        return [circle for circle in chain((circle for circle in top_circles[0][first_half:]),
                                           (circle for circle in top_circles[1][:second_half]))]

    def get_top_circles(self, num):
        if num >= len(self.curr_gen):
            raise ValueError("num can't be bigger than length of generation.")
        min_vals = [[i, self.evaluate_generation(self.curr_gen[i])] for i in range(num)]
        for i in range(1, len(self.curr_gen)):
            result = self.evaluate_generation(self.curr_gen[i])
            if result < min_vals[0][1]:
                min_vals.append([i, result])
                min_vals.sort(key=lambda x: x[1])
                min_vals = min_vals[:num]
        return [self.curr_gen[min_val[0]] for min_val in min_vals]

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

    @property
    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def convert_to_unit_vector(self):
        if not self.magnitude == 0:
            self.x = self.x / self.magnitude
            self.y = self.y / self.magnitude
        else:
            self.x = 0
            self.y = 0

    def distance(self, target):
        return math.sqrt((self.x - target.x) ** 2 + (self.y - target.y) ** 2)

    def intersecting(self, target):
        d = self.distance(target)
        return d < (self.r + target.r)

    def circle_edge_to(self, unit_direction):
        return Circle(unit_direction.x * self.r, unit_direction.y * self.r, 0)

    def intersecting_amount(self, target):

        d = self.distance(target)
        if d > (self.r + target.r):
            return 0
        else:
            uv_to_target = self.find_unit_vector_to_circle(target)
            uv_from_target = target.find_unit_vector_to_circle(self)
            circle_edge_to_target = uv_to_target.circle_edge_to(uv_to_target)
            circle_edge_from_target = uv_from_target.circle_edge_to(uv_from_target)
            return circle_edge_to_target.distance(circle_edge_from_target)

    def find_unit_vector_to_circle(self, target):
        x = self.x - target.x
        y = self.y - target.y
        uv = Circle(x, y, 1)
        uv.convert_to_unit_vector()
        return uv
