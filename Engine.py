#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from ctypes import *
import random
import threading
from win32com import client
from time import sleep
from Classes import Border, Ship, Bullet, Enemy, EnemyBullet



class Engine(Border, Ship, Bullet):
    
    def __init__(self):
        settings = client.Dispatch("Settings")
        self.border = Border()
        self.ship = client.Dispatch("Ship")
        self.bullets = []
        self.enemies = []
        self.enemybombs = []
        self.level = settings.level
        self.num = 0
        self.score = 0
        self.flag = True
        self.die = True
        self.hp = settings.hp

    def PressLeft(self):
        self.border.border[len(self.border.border)-1][self.ship.pos] = ' '
        self.ship.MoveLeft()
        self.border.border[len(self.border.border) -
                           1][self.ship.pos] = self.ship.name
        sleep(0.1)

    def PressRight(self):
        self.border.border[len(self.border.border)-1][self.ship.pos] = ' '
        self.ship.MoveRight()
        self.border.border[len(self.border.border) -
                           1][self.ship.pos] = self.ship.name
        sleep(0.1)

    def Shoot(self):
        bullet = client.Dispatch("Bullet")
        bullet.x = self.ship.pos
        self.bullets.append(bullet)
        sleep(0.1)

    def MoveShoot(self):
        if self.bullets != 0:
            for bullet in self.bullets:
                if bullet.y == 0:
                    self.border.border[bullet.y][bullet.x] = ' '
                    self.bullets.remove(bullet)
                else:
                    bullet.MoveUp()
                    self.border.border[bullet.y][bullet.x] = bullet.name
                    if bullet.y != 23:
                        self.border.border[bullet.y+1][bullet.x] = ' '

                    for enemy in self.enemies:
                        if (enemy.x == bullet.x) and (enemy.y == bullet.y):
                            # print('Kill')
                            self.score += 10
                            self.border.border[bullet.y][bullet.x] = ' '
                            self.enemies.remove(enemy)
                            self.bullets.remove(bullet)
                            break
        if (self.flag) and (self.die):
            threading.Timer(0.1, self.MoveShoot).start()

    def paint(self):

        os.system('cls')
        time1 = time()
        self.border.print_Border()
        print('Score:', self.score, 28*' '+'Your level:', self.level)
        print('Hp:', self.hp)
        if (self.flag) and (self.die):
            threading.Timer(0.01, self.paint).start()

    def MoveEnemy(self):
        for i in self.enemies:
            self.border.border[i.y][i.x] = ' '
        if self.enemies != []:
            for i in self.enemies:
                i.MoveDown()
                if i.y == 24:
                    self.die = False
                    self.GameOver()

        for i in self.enemies:
            self.border.border[i.y][i.x] = i.name

    def SpawnEnemy(self):
        if (self.num == 3*self.level):
            if self.enemies == []:
                self.border.clean_Border()
                sleep(2)
                self.num = 0
                self.level += 1
        else:
            mas = []
            for i in range(random.randint(1*self.level, 15)):
                mas.append(random.randint(0, 49))
            mas = list(set(mas))
            for x in mas:
                enemy = client.Dispatch("Enemy")
                enemy.x = x
                self.enemies.append(enemy)
            self.num += 1
        self.MoveEnemy()
        if (self.flag) and (self.die):
            threading.Timer((4 - self.level * 0.3), self.SpawnEnemy).start() # может уйти но не уйдёт!!!

    def CreateBomb(self):
        for enemy in self.enemies:
            if enemy.y == self.enemies[0].y and enemy.y < 21:
                enemy_bullet = client.Dispatch("EnemyBullet")
                enemy_bullet.x = enemy.x
                enemy_bullet.y = enemy.y+2
                #self.enemybombs.append(EnemyBullet(x = enemy.x, y = enemy.y+1))
                self.enemybombs.append(enemy_bullet)
                sleep(5)
            else:
                break
        if (self.flag) and (self.die):
            threading.Timer((12//self.level), self.CreateBomb).start()

    def MoveBomb(self):
        for bomb in self.enemybombs:
            self.border.border[bomb.y][bomb.x] = bomb.name
            if bomb.y != self.enemies[0].y+1:
                self.border.border[bomb.y-1][bomb.x] = ' '
                if bomb.y == 24:
                    self.border.border[bomb.y][bomb.x] = ' '
                    if bomb.x == self.ship.pos:
                        self.hp -= 1
                        if self.hp == 0:
                            self.die = False
                            self.GameOver()
                        else:
                            self.border.border[24][self.ship.pos] = ' '
                            sleep(0.15)
                            self.border.border[24][self.ship.pos] = 'A'
                            sleep(0.15)
                            self.border.border[24][self.ship.pos] = ' '
                            sleep(0.15)
                            self.border.border[24][self.ship.pos] = 'A'
                            sleep(0.15)
                            self.border.border[24][self.ship.pos] = ' '
                            sleep(0.15)
                            self.border.border[24][self.ship.pos] = 'A'
                    self.enemybombs.remove(bomb)
            bomb.MoveDown()
        if (self.flag) and (self.die):
            threading.Timer((0.5), self.MoveBomb).start()

    def MoveKeybord(self):
        directiry = r'C:\Users\Antoska\Desktop\tmp\Space_Invaders'
        lib = CDLL(f'{directiry}\Megalab.dll')
        strcat = lib.TheFunc
        strcat.restype = c_int
        input_key = lib.TheFunc()
        # print(input_key)
        if input_key == 113 or input_key == 81:

            self.flag = False
            sleep(1)
            os.system('cls')
            print('Good luck')

        elif input_key == 97 or input_key == 65:
            self.PressLeft()
        elif input_key == 100 or input_key == 68:
            self.PressRight()
        elif input_key == 119 or input_key == 87:
            self.Shoot()

        if (self.flag) and (self.die):
            threading.Timer((0.1), self.MoveKeybord).start()

    def GameOver(self):
        sleep(1)
        # sys.exit()
        os.system('cls')
        print('Your die')
        if self.score == 0:
            print('Bad Game!!!\nMission Failed. Okey next time\nYour score:', self.score)
        else:
            print('Good Game!!!\nYour score:', self.score)

    def run(self):
        # назначение клавишам

        # изменяю поле и рисую там караблик
        self.border.border[len(self.border.border) -
                           1][self.ship.pos] = self.ship.name

        self.paint()  # процесс отрисовки
        self.SpawnEnemy()  # процесс спавна противников
        self.MoveShoot()  # процесс движение выстрелов
        self.MoveBomb()  # процесс движения бомб
        self.CreateBomb()  # процесс создания бомб
        self.MoveKeybord()
    #     while True:
    # #strcat.argtypes = [c_int]
    #         input_key = lib.TheFunc()
    #         #print(input_key)
    #         if input_key == 113 or input_key == 81:
    #             print('Good luck')
    #             sys.exit()
    #             break
    #         elif input_key == 97 or input_key == 65:
    #             self.MoveLeft()
    #         elif input_key == 100 or input_key == 68:
    #             self.MoveRight()
    #         elif input_key == 119 or input_key == 87:
    #             self.Shoot()
        # keyboard.unhook_all() #отключаю все бинды
        # keyboard.add_hotkey('a', self.PressLeft) #добавляю бинд на движение влево
        # keyboard.add_hotkey('d', self.PressRight) #добавляю бинд на движение вправо
        # keyboard.add_hotkey('q', self.GameOver) #добавляю бинд на выход из игры
        # keyboard.add_hotkey('w', self.Shoot) #добавляю бинд на выстрел


if __name__ == '__main__':
    myEngine = Engine()  # создаём класс Engine
    myEngine.run()  # запуск игры
