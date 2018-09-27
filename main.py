#!/usr/bin/env python
#-*- coding: utf-8 -*-

import GUI
import tkinter
import os
from tkinter import Button

def callback():
    cmd = 'python main.py'
    os.system(cmd)
    exit(0)

if __name__ == '__main__':
    window = tkinter.Tk()
    gui_chess_board = GUI.Chess_Board_Frame(window)

    b = Button(window, text="Restart", command=callback)

    gui_chess_board.pack()
    b.pack()
    window.mainloop()
