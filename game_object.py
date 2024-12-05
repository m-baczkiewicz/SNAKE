#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 01:38:25 2024

@author: michalbaczkiewicz
"""
# game_object.py
from tkinter import *

class GameObject:
    def __init__(self, x, y, color, tag):
        self.coordinates = [x, y]
        self.color = color
        self.tag = tag

    def draw(self, canvas, space_size):
        return canvas.create_rectangle(self.coordinates[0], self.coordinates[1],
                                       self.coordinates[0] + space_size, self.coordinates[1] + space_size,
                                       fill=self.color, tag=self.tag)
