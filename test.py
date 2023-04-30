import tkinter as tk
import random

# constants
WIDTH = 500
HEIGHT = 500
SEG_SIZE = 20
IN_GAME = True

# classes
class Segment(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake(object):
    def __init__(self, segments):
        self.segments = segments
        self.mapping = {"Down": (0, 1), "Right": (1, 0), "Up": (0, -1), "Left": (-1, 0)}
        self.vector = self.mapping["Down"]

    def move(self):
        for i in range(len(self.segments)-1, 0, -1):
            self.segments[i].x = self.segments[i-1].x
            self.segments[i].y = self.segments[i-1].y
        self.segments[0].x += self.vector[0] * SEG_SIZE
        self.segments[0].y += self.vector[1] * SEG_SIZE

    def change_direction(self, event):
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]

    def add_segment(self):
        x = self.segments[-1].x
        y = self.segments[-1].y
        self.segments.append(Segment(x, y))

class Game(tk.Canvas):
    def __init__(self):
        super().__init__(width=WIDTH, height=HEIGHT, background="black", highlightthickness=0)
        self.snake = self.create_snake()
        self.food = self.create_food()
        self.score = 0
        self.text_score = self.create_text(50, 10, text=f"Score: {self.score}", font=("TkDefaultFont", 14), fill="white", anchor="nw")
        self.bind_all("<Key>", self.snake.change_direction)
        self.pack()

    def create_snake(self):
        segments = [Segment(SEG_SIZE, SEG_SIZE), Segment(SEG_SIZE*2, SEG_SIZE), Segment(SEG_SIZE*3, SEG_SIZE)]
        return Snake(segments)

    def create_food(self):
        x = random.randint(SEG_SIZE, WIDTH-SEG_SIZE)
        y = random.randint(SEG_SIZE, HEIGHT-SEG_SIZE)
        return self.create_oval(x, y, x+SEG_SIZE, y+SEG_SIZE, outline="red", fill="red")

    def check_collisions(self):
        head = self.snake.segments[0]
        if head.x < 0 or head.x > WIDTH-SEG_SIZE or head.y < 0 or head.y > HEIGHT-SEG_SIZE:
            return True
        for segment in self.snake.segments[1:]:
            if head.x == segment.x and head.y == segment.y:
                return True
        return False

    def check_food(self):
        if self.snake.segments[0].x == self.coords(self.food)[0] and self.snake.segments[0].y == self.coords(self.food)[1]:
            self.score += 1
            self.itemconfig(self.text_score, text=f"Score: {self.score}")
            self.snake.add_segment()
            self.delete(self.food)
            self.food = self.create_food()

    def game_over(self):
        self.create_text(WIDTH/2, HEIGHT/2, text="Game Over", fill="white
