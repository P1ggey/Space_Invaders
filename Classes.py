#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os

def Border_grid():
    border = []
    for j in range(25):
        border_line=[]
        for i in range(50):
            border_line.append(' ')
        border.append(border_line)
    return border

#класс игрового поля
class Border(object):
    def __init__ (self, border = Border_grid()):
        self.border  = border
    
    def print_Border(self):
        for i in self.border:
            print(''.join(i)+'|')
        print('_'*51)
    
    def clean_Border(self):
        for i in range(len(self.border)-1):
            for j in range(len(self.border[i])):
                self.border[i][j]=' '

#класс бомбы
class EnemyBullet(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.name = '*'

    def moveDown(self):
        self.y = self.y+1

#класс пули от тачанки
class Bullet(object):

    def __init__(self, x):
        self.x = x
        self.y = 24
        self.name = 'i'

    def moveUp(self):
        self.y = self.y-1

#класс противника
class Enemy(object):

    def __init__(self,x):
        self.x = x
        self.y = 0
        self.name = 'O'

    def moveDown(self):
        self.y = self.y+1

#класс кораблика
class Ship(object):
    
    def __init__(self):
        self.pos = 12
        self.name = 'A'

    def MoveLeft(self):
        self.pos-=1
        if self.pos <= 0:
            self.pos = 0
        #print('MoveLeft')
        
    def MoveRight(self):
        self.pos+=1
        if self.pos >= 49:
            self.pos = 49
        #print('MoveRight')