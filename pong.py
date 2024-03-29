#!/usr/bin/env python
import sys
from PySimpleGUI import Canvas, Popup, Button, T, Window, Image
import random
import time
from sys import exit as exit


"""
    Pong code supplied by Daniel Young (Neonzz)
    Modified.  Original code: https://www.pygame.org/project/3649/5739
    THIS IS A JOKE EDIT
"""

class Ball:
    def __init__(self, canvas, bat, bat2, color):
        self.canvas = canvas
        self.bat = bat
        self.bat2 = bat2
        self.playerScore = 0
        self.player1Score = 0
        self.drawP1 = None
        self.drawP = None
        self.id = self.canvas.create_oval(10, 10, 35, 35, fill=color)
        self.canvas.move(self.id, 327, 220)
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.x = random.choice([-2.5, 2.5])
        self.y = 2.5

    def checkwin(self):
        winner = None
        if self.playerScore >= 3:
            winner = 'Player'
        if self.player1Score >= 3:
            winner = 'Bot'
        return winner


    def updatep(self, val):
        self.canvas.delete(self.drawP)
        self.drawP = self.canvas.create_text(170, 50, font=('freesansbold.ttf', 40), text=str(val), fill='white')

    def updatep1(self, val):
        self.canvas.delete(self.drawP1)
        self.drawP1 = self.canvas.create_text(550, 50, font=('freesansbold.ttf', 40), text=str(val), fill='white')

    def hit_bat(self, pos):
        bat_pos = self.canvas.coords(self.bat.id)
        if pos[2] >= bat_pos[0] and pos[0] <= bat_pos[2]:
            if pos[3] >= bat_pos[1] and pos[3] <= bat_pos[3]:
                return True
            return False

    def hit_bat2(self, pos):
        bat_pos = self.canvas.coords(self.bat2.id)
        if pos[2] >= bat_pos[0] and pos[0] <= bat_pos[2]:
            if pos[3] >= bat_pos[1] and pos[3] <= bat_pos[3]:
                return True
            return False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 4
        if pos[3] >= self.canvas_height:
            self.y = -4
        if pos[0] <= 0:
            self.player1Score += 1
            self.canvas.move(self.id, 327, 220)
            self.x = 4
            self.updatep1(self.player1Score)
        if pos[2] >= self.canvas_width:
            self.playerScore += 1
            self.canvas.move(self.id, -327, -220)
            self.x = -4
            self.updatep(self.playerScore)
        if self.hit_bat(pos):
            self.x = 4
        if self.hit_bat2(pos):
            self.x = -4

class pongbat():
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = self.canvas.create_rectangle(40, 200, 25, 310, fill=color)
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.y = 0

    def up(self, evt):
        self.y = -5

    def down(self, evt):
        self.y = 5

    def draw(self):
        self.canvas.move(self.id, 0, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 0
        if pos[3] >= 400:
            self.y = 0


class pongbat2():
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = self.canvas.create_rectangle(680, 200, 660, 310, fill=color)
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.y = 0

    def up(self, evt):
        self.y = -5

    def down(self, evt):
        self.y = 5

    def draw(self, ballPos):
        self.canvas.move(self.id, 0, self.y)
        pos = self.canvas.coords(self.id)
        if ballPos[1] > pos[1]:
            self.y = 10
        if ballPos[3] <= pos[3]:
            self.y = -10

def pong():
    # ------------- Define GUI layout -------------
    layout = [[Image('image.png', size=(700, 400), visible=False, key = 'gno')],
              [Canvas(size=(700, 400), background_color='black', key='canvas')],
              [T(''), Button('Quit')]]
    # ------------- Create window -------------
    window = Window('The Classic Game of Pong', return_keyboard_events=True).Layout(layout).Finalize()
    # window.Finalize()                  # TODO Replace with call to window.Finalize once code released

    # ------------- Get the tkinter Canvas we're drawing on -------------
    canvas = window.FindElement('canvas').TKCanvas

    # ------------- Create line down center, the bats and ball -------------
    canvas.create_line(350, 0, 350, 400, fill='white')
    bat1 = pongbat(canvas, 'white')
    bat2 = pongbat2(canvas, 'white')
    ball1 = Ball(canvas, bat1, bat2, 'white')

    # ------------- Event Loop -------------
    while True:
        # ------------- Draw ball and bats -------------
        ball1.draw()
        bat1.draw()
        bat2.draw(ball1.canvas.coords(ball1.id))

        # ------------- Read the form, get keypresses -------------
        # pylint: disable=W0612
        event, values = window.Read(timeout=0)
        # ------------- If quit  -------------
        if event is None or event == 'Quit':
            exit(69)
        # ------------- Keypresses -------------
        if event is not None:
            if event.startswith('Up'):
                bat1.up(1)

            elif event.startswith('Down'):
                bat1.down(1)
            

        if ball1.checkwin():
            break

        canvas.after(10)

if __name__ == '__main__':
    pong()