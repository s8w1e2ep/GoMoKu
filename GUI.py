#!/usr/bin/env python
#-*- coding: utf-8 -*-
import Tkinter
import math
import Point
import Record
import time
import MCTS
import numpy as np

class Chess_Board_Canvas(Tkinter.Canvas):
    #棋盤繪製
    def __init__(self, master=None, height=0, width=0):
        Tkinter.Canvas.__init__(self, master, height=height, width=width)
        self.step_record_chess_board = Record.Step_Record_Chess_Board()
        #初始化記步器
        self.init_chess_board_points()    #畫點
        self.init_chess_board_canvas()    #畫棋盤
        self.board = MCTS.Board()
        self.AI = MCTS.MonteCarlo(self.board, 2)
        self.clicked = 0

    def init_chess_board_points(self):
        '''
        生成棋盤點,並且對應到像素座標
        保存到 chess_board_points 屬性
        '''
        self.chess_board_points = [[None for i in range(15)] for j in range(15)]


        for i in range(15):
            for j in range(15):
                self.chess_board_points[i][j] = Point.Point(i, j); #轉換棋盤座標像素座標

    def init_chess_board_canvas(self):
        '''
        初始化棋盤
        '''

        for i in range(15):  #直線
            self.create_line(self.chess_board_points[i][0].pixel_x, self.chess_board_points[i][0].pixel_y, self.chess_board_points[i][14].pixel_x, self.chess_board_points[i][14].pixel_y)

        for j in range(15):  #橫線
            self.create_line(self.chess_board_points[0][j].pixel_x, self.chess_board_points[0][j].pixel_y, self.chess_board_points[14][j].pixel_x, self.chess_board_points[14][j].pixel_y)
        #邊界
        self.create_line(self.chess_board_points[2][2].pixel_x, self.chess_board_points[2][2].pixel_y, self.chess_board_points[2][12].pixel_x, self.chess_board_points[2][12].pixel_y,fill="red")
        self.create_line(self.chess_board_points[12][2].pixel_x, self.chess_board_points[12][2].pixel_y, self.chess_board_points[12][12].pixel_x, self.chess_board_points[12][12].pixel_y,fill="red")
        self.create_line(self.chess_board_points[2][12].pixel_x, self.chess_board_points[2][12].pixel_y, self.chess_board_points[12][12].pixel_x, self.chess_board_points[12][12].pixel_y,fill="red")
        self.create_line(self.chess_board_points[2][2].pixel_x, self.chess_board_points[2][2].pixel_y, self.chess_board_points[12][2].pixel_x, self.chess_board_points[12][2].pixel_y,fill="red")

        for i in range(15):  #交點橢圓
            for j in range(15):
                r = 1
                self.create_oval(self.chess_board_points[i][j].pixel_x-r, self.chess_board_points[i][j].pixel_y-r, self.chess_board_points[i][j].pixel_x+r, self.chess_board_points[i][j].pixel_y+r);

    def click1(self, event): #click關鍵字重複
        '''
        監聽滑鼠事件,根據滑鼠位置判斷落點
        '''
    	if(self.clicked != 1):

    		for i in range(15):
    		    for j in range(15):
    		        square_distance = math.pow((event.x - self.chess_board_points[i][j].pixel_x), 2) + math.pow((event.y - self.chess_board_points[i][j].pixel_y), 2)
    		        #計算滑鼠的位置和點的距離
    		        #距離小於14的點

    		        if (square_distance <= 200) and (self.step_record_chess_board.checkState(i, j) == None): #合法落子位置
    			    self.clicked = 1
    		            if self.step_record_chess_board.who_to_play() == 1:
    		                #奇數次，黑落子
    		                self.create_oval(self.chess_board_points[i][j].pixel_x-10, self.chess_board_points[i][j].pixel_y-10, self.chess_board_points[i][j].pixel_x+10, self.chess_board_points[i][j].pixel_y+10, fill='black')
    				Tkinter.Canvas.update(self)
    				#偶數次，白落子
    		            elif self.step_record_chess_board.who_to_play() == 2:
    		                self.create_oval(self.chess_board_points[i][j].pixel_x-10, self.chess_board_points[i][j].pixel_y-10, self.chess_board_points[i][j].pixel_x+10, self.chess_board_points[i][j].pixel_y+10, fill='white')


    			    result = 0
    		            if(self.step_record_chess_board.value[1][i][j] >= 90000):
    				result = 1
    				self.clicked = 0
    		            self.step_record_chess_board.insert_record(i, j)
    		            #落子，最多225

    		            #######result = self.step_record_chess_board.check()
    		            #判斷是否有五子連珠


    		            if result == 1:
    		                self.create_text(240, 475, text='the black wins')
    		                #解除左键绑定
    		                self.unbind('<Button-1>')
    		                # """Unbind for this widget for event SEQUENCE  the
    		                #     function identified with FUNCID."""

    		            elif result == 2:
    		                self.create_text(240, 475, text='the white wins')
    		                #解除左键绑定
    		                self.unbind('<Button-1>')
    		#根據價值網路落子
    		if(self.clicked == 1):
    			x = 0
    			y = 0
    			max_value = 0
    			for i in range(0,15):
    				for j in range(0,15):
    					if(self.step_record_chess_board.value[2][i][j] >= 90000):
    						x = i
    						y = j
    						max_value = 99999
    						break;
    					elif(self.step_record_chess_board.value[0][i][j] >= max_value):
    						x = i
    						y = j
    						max_value = self.step_record_chess_board.value[0][i][j]
    			if(self.step_record_chess_board.value[2][x][y] >= 90000):
    				result = 2

    			self.board.state = np.copy(self.step_record_chess_board.state)
    			self.AI.value = self.step_record_chess_board.value[0]
    			self.AI.update(self.board.state)
    			action = self.AI.bestAction()
    			x,y = action

    			self.step_record_chess_board.insert_record(x, y)
    			self.create_oval(self.chess_board_points[x][y].pixel_x-10, self.chess_board_points[x][y].pixel_y-10, self.chess_board_points[x][y].pixel_x+10, self.chess_board_points[x][y].pixel_y+10, fill='white')
    			#######result = self.step_record_chess_board.check()
    			#判斷是否有五子連珠


    			if result == 1:
    				self.create_text(240, 475, text='the black wins')
    				#解除左键绑定
    				self.unbind('<Button-1>')
    				# """Unbind for this widget for event SEQUENCE  the
    				#     function identified with FUNCID."""

    			elif result == 2:
    				self.create_text(240, 475, text='the white wins')
    				#解除左键绑定
    				self.unbind('<Button-1>')
    			self.clicked = 0

class Chess_Board_Frame(Tkinter.Frame):
    def __init__(self, master=None):
        Tkinter.Frame.__init__(self, master)
        self.create_widgets()

    def create_widgets(self):
        self.chess_board_label_frame = Tkinter.LabelFrame(self, text="Chess Board", padx=5, pady=5)
        self.chess_board_canvas = Chess_Board_Canvas(self.chess_board_label_frame, height=500, width=480)

        self.chess_board_canvas.bind('<Button-1>', self.chess_board_canvas.click1)

        self.chess_board_label_frame.pack();
        self.chess_board_canvas.pack();
