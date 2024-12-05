#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 01:13:45 2024

@author: michalbaczkiewicz
"""

from tkinter import *
import random


# Ustawienia gry
game_width = 700
game_height = 700
speed = 90
space_size = 50
body_parts = 3
snake_color = "#088343"
background_color = "#000000"

class Snake:
    def __init__(self):
        self.body_size = body_parts
        self.coordinates = []
        self.squares = []

        # Inicjalizacja początkowych współrzędnych węża
        for i in range(0, body_parts):
            self.coordinates.append([250, 250])

        # Tworzenie prostokątów reprezentujących ciało węża
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + space_size, y + space_size, fill=snake_color, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        self.change_color()
        self.spawn_food()

    def change_color(self):
        self.color = random.choice(["#AE0964", "#FF5733", "#33FF57", "#3366FF", "#FFFF33", "#AA44AA", '#0994A6', '#FCE503', '#D34810'])

    def spawn_food(self):
        x = random.randint(0, int((game_width / space_size) - 1)) * space_size
        y = random.randint(0, int((game_height / space_size) - 1)) * space_size
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + space_size, y + space_size, fill=self.color, tag="food")

def start_game(event):
    global game_started
    if not game_started:
        game_started = True
        next_turn(snake, food)
        

def restart_game(event):
    global game_started, score
    game_started = False  # Ustawienie stanu gry na nieuruchomiony po restarcie
    score = 0
    label.config(text="Score:{}".format(score))
    canvas.delete("all")
    snake.__init__()
    food.__init__()
    window.update()

def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= space_size
    elif direction == "down":
        y += space_size
    elif direction == "left":
        x -= space_size
    elif direction == "right":
        x += space_size

    # Dodanie nowej głowy węża
    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + space_size, y + space_size, fill=snake_color)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        # Jeżeli wąż zjada jedzenie, zwiększ wynik i stwórz nowe jedzenie
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        # Jeżeli wąż nie zjada jedzenia, usuń ostatni segment węża
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(speed, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    # Sprawdzenie kolizji z granicami planszy
    if x < 0 or x >= game_width or y < 0 or y >= game_height:
        print(f'Uzyskany wynik {score}')
        return True

    # Sprawdzenie kolizji z samym sobą
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print(f'Uzyskany wynik {score}')
            return True

    return False

def game_over():
    global game_started
    game_started = False
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       font=('consolas', 70), text="      GAME OVER    \n  Press 'r' to restart", fill="red", tag="gameover")

# Inicjalizacja okna
window = Tk()
window.title("Snake game")
window.resizable(False, False)

# Inicjalizacja zmiennych
score = 0
direction = 'down'
game_started = False  # Zmienna kontrolująca, czy gra została uruchomiona

# Utworzenie etykiety na wynik
label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

# Utworzenie płótna do rysowania węża i jedzenia
canvas = Canvas(window, bg=background_color, height=game_height, width=game_width)
canvas.pack()

# Aktualizacja okna
window.update()

# Ustawienia położenia okna
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))  # położenie w połowie ekranu oś x
offset_y = 50  # wartość w celu podwyższenia okna 
y = int((screen_height/2) - (window_height/2)) - offset_y  # if system operacyjny != macOS należy usunąć offset

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Przypisanie kierunków ruchu do przycisków
directions = {"<Left>": "left", "<Right>": "right", "<Up>": "up", "<Down>": "down", "a": "left", "d": "right", "w": "up", "s": "down"}
for key, value in directions.items():
    window.bind(key, lambda event, d=value: change_direction(d))  # utworzenie sterowania 'wsad'

# Dodanie obsługi zdarzenia dla przycisku start i restart
window.bind("<Return>", start_game)
window.bind("<space>", start_game)
window.bind("<`>", start_game)
window.bind("<q>", start_game)
window.bind("</>", start_game)
window.bind("<r>", restart_game) 
window.bind("<.>", restart_game) # Dodano restart na klawisze

# Inicjalizacja obiektów węża i jedzenia
snake = Snake()
food = Food()

# Uruchomienie pętli głównej
window.mainloop()
