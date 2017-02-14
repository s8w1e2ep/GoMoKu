#!/usr/bin/env python
#-*- coding: utf-8 -*-

import numpy as np
class Step_Record:
    def __init__(self, count):
        """
        紀錄步數
        先走的1是黑
        後走的2是白
        """
        self.count = count
        self.color = (self.count+1) % 2 + 1;

class Step_Record_Chess_Board:
    def __init__(self):
        #初始化
        self.count = 1;
        self.records = [[None for i in range(15)] for j in range(15)]
        #15x15,如果沒有落子則值是None
    	#value[1]:player1	value[2]:player2	value[0]:player1+player2
    	self.value = np.array([[[0] * 15] * 15] * 3)
    	self.state = np.array([[0] * 15] * 15)
    	#eight direction
    	self.dir = np.array([[1,1,0,-1,-1,-1,0,1],[0,1,1,1,0,-1,-1,-1]])

    def insert_record(self, x, y):
        '''
        根據步數落子判斷是黑子還是白子
        步數加1
        '''
        self.records[x][y] = Step_Record(self.count)	#紀錄下子
    	self.state[x][y] = self.records[x][y].color
    	self.value[1][x][y] = self.records[x][y].color	#
    	self.value[2][x][y] = self.records[x][y].color	#
    	#print '{0}'.format('black' if ((self.count+1) % 2 + 1) == 1 else 'white') ,'< x:', x, ', y:', y,'>'
    	#print x
    	#print y
    	#print self.state
    	for i in range(-5,6):
    		for j in range(-5,6):
    			if(not self.checkState(x+i,y+j) == None):
    				continue;
    			#重新計算player1 value
    			type = self.checkType(x+i,y+j,1)
    			value = self.evaluate(type)
    			self.setValue(x+i,y+j,1,value)
    			#重新計算player2 value
    			type = self.checkType(x+i,y+j,2)
    			value = self.evaluate(type)
    			self.setValue(x+i,y+j,2,value)

    	self.value[0] = (self.value[1] + self.value[2])/2
    	"""
    	print "combine value"
    	print self.value[0]
    	"""
        self.count += 1;

    def who_to_play(self):
        '''
        判斷該誰走了
        '''
        return (self.count+1) % 2 + 1

    def checkState(self,x,y):
    	#out bound
    	if (x < 0 or y < 0 or x > 14 or y > 14):
    		return -1;
    	if(self.count == 1 and (x > 2 and x < 12) and (y > 2 and y < 12)):
    		return -1
    	if(self.records[x][y] == None):
    		return None
    	return self.records[x][y].color

    def setValue(self,x,y,player,value):
	       self.value[player][x][y] = value

    def checkType(self,x,y,player):
    	dir = self.dir
    	type = np.array([0] * 8)

    	for i in range(0,8):
    		# 12 		(0)
    		if(self.checkState(x+dir[0][i],y+dir[1][i]) != player and self.checkState(x+dir[0][i],y+dir[1][i]) != None):
    			type[i] = 0
    		# 102 		(1)
    		if(self.checkState(x+dir[0][i],y+dir[1][i]) == None and self.checkState(x+dir[0][i]*2,y+dir[1][i]*2) != player):
    			type[i] = 1
    		# 112 		(2)
    		if(self.checkState(x+dir[0][i],y+dir[1][i]) == player and self.checkState(x+dir[0][i]*2,y+dir[1][i]*2) != player and self.checkState(x+dir[0][i]*2,y+dir[1][i]*2) != None):
    			type[i] = 2
    		# 1102 		(3)
    		if(self.checkState(x+dir[0][i],y+dir[1][i]) == player and self.checkState(x+dir[0][i]*2,y+dir[1][i]*2) == None and self.checkState(x+dir[0][i]*3,y+dir[1][i]*3) != player):
    			type[i] = 3
    		# 1012		(4)
    		if(self.checkState(x+dir[0][i],y+dir[1][i]) == None and self.checkState(x+dir[0][i]*2,y+dir[1][i]*2) == player and self.checkState(x+dir[0][i]*3,y+dir[1][i]*3) != player and self.checkState(x+dir[0][i]*3,y+dir[1][i]*3) != None):
    			type[i] = 4
    		# 10102		(5)
    		if(self.checkState(x+dir[0][i],y+dir[1][i]) == None and self.checkState(x+dir[0][i]*2,y+dir[1][i]*2) == player and self.checkState(x+dir[0][i]*3,y+dir[1][i]*3) == None and self.checkState(x+dir[0][i]*4,y+dir[1][i]*4) != player):
    			type[i] = 5
    		# 1112		(6)
    		if(self.checkState(x+dir[0][i],y+dir[1][i]) == player and self.checkState(x+dir[0][i]*2,y+dir[1][i]*2) == player and self.checkState(x+dir[0][i]*3,y+dir[1][i]*3) != player and self.checkState(x+dir[0][i]*3,y+dir[1][i]*3) != None):
    			type[i] = 6
    		# 11102		(7)
    		if(self.checkState(x+dir[0][i],y+dir[1][i]) == player and self.checkState(x+dir[0][i]*2,y+dir[1][i]*2) == player and self.checkState(x+dir[0][i]*3,y+dir[1][i]*3) == None and self.checkState(x+dir[0][i]*4,y+dir[1][i]*4) != player):
    			type[i] = 7
    		# 11012		(8)
    		if(self.checkState(x+dir[0][i],y+dir[1][i]) == player and self.checkState(x+dir[0][i]*2,y+dir[1][i]*2) == None and self.checkState(x+dir[0][i]*3,y+dir[1][i]*3) == player and self.checkState(x+dir[0][i]*4,y+dir[1][i]*4) != player):
    			type[i] = 8
    		# 10112		(9)
    		if(self.checkState(x+dir[0][i],y+dir[1][i]) == None and self.checkState(x+dir[0][i]*2,y+dir[1][i]*2) == player and self.checkState(x+dir[0][i]*3,y+dir[1][i]*3) == player and self.checkState(x+dir[0][i]*4,y+dir[1][i]*4) != player):
    			type[i] = 9
    		# 10101		(10)
    		if(self.checkState(x+dir[0][i],y+dir[1][i]) == None and self.checkState(x+dir[0][i]*2,y+dir[1][i]*2) == player and self.checkState(x+dir[0][i]*3,y+dir[1][i]*3) == None and self.checkState(x+dir[0][i]*4,y+dir[1][i]*4) == player):
    			type[i] = 10
    		# 11112		(11)
    		if(self.checkState(x+dir[0][i],y+dir[1][i]) == player and self.checkState(x+dir[0][i]*2,y+dir[1][i]*2) == player and self.checkState(x+dir[0][i]*3,y+dir[1][i]*3) == player and self.checkState(x+dir[0][i]*4,y+dir[1][i]*4) != player):
    			type[i] = 11
    		# 11110		(12)
    		if(self.checkState(x+dir[0][i],y+dir[1][i]) == player and self.checkState(x+dir[0][i]*2,y+dir[1][i]*2) == player and self.checkState(x+dir[0][i]*3,y+dir[1][i]*3) == player and self.checkState(x+dir[0][i]*4,y+dir[1][i]*4) == None):
    			type[i] = 12
    		# 11101		(13)
    		if(self.checkState(x+dir[0][i],y+dir[1][i]) == player and self.checkState(x+dir[0][i]*2,y+dir[1][i]*2) == player and self.checkState(x+dir[0][i]*3,y+dir[1][i]*3) == None and self.checkState(x+dir[0][i]*4,y+dir[1][i]*4) == player):
    			type[i] = 13
    		# 11011		(14)
    		if(self.checkState(x+dir[0][i],y+dir[1][i]) == player and self.checkState(x+dir[0][i]*2,y+dir[1][i]*2) == None and self.checkState(x+dir[0][i]*3,y+dir[1][i]*3) == player and self.checkState(x+dir[0][i]*4,y+dir[1][i]*4) == player):
    			type[i] = 14
    		# 10111		(15)
    		if(self.checkState(x+dir[0][i],y+dir[1][i]) == None and self.checkState(x+dir[0][i]*2,y+dir[1][i]*2) == player and self.checkState(x+dir[0][i]*3,y+dir[1][i]*3) == player and self.checkState(x+dir[0][i]*4,y+dir[1][i]*4) == player):
    			type[i] = 15
    		# 11111		(16)
    		if(self.checkState(x+dir[0][i],y+dir[1][i]) == player and self.checkState(x+dir[0][i]*2,y+dir[1][i]*2) == player and self.checkState(x+dir[0][i]*3,y+dir[1][i]*3) == player and self.checkState(x+dir[0][i]*4,y+dir[1][i]*4) == player):
    			type[i] = 16

        return type

    def evaluate(self,type):
    	value = 0
    	for i in range(0,8):
    		#five 11111
    		if(type[i] == 16):
    			value += 99999
    		#five 1111 + 11
    		elif( (type[i] == 11 or type[i] == 12) and (type[(i+4)%8] == 2 or type[(i+4)%8] == 3 or type[(i+4)%8] == 6 or type[(i+4)%8] == 7 or type[(i+4)%8] == 8 or type[(i+4)%8] == 11 or type[(i+4)%8] == 12 or type[(i+4)%8] == 13 or type[(i+4)%8] == 14)):
    			value += 99999
    		#five 111 + 111
    		elif( (type[i] == 6 or type[i] == 7 or type[i] == 11 or type[i] == 12 or type[i] == 13) and (type[(i+4)%8] == 6 or type[(i+4)%8] == 7 or type[(i+4)%8] == 11 or type[(i+4)%8] == 12 or type[(i+4)%8] == 13)):
    			value += 99999

    		#live four 11110 + 10
    		elif( (type[i] == 12) and (type[(i+4)%8] == 1 or type[(i+4)%8] == 4 or type[(i+4)%8] == 5 or type[(i+4)%8] == 9 or type[(i+4)%8] == 10 or type[(i+4)%8] == 15)):
    			value += 10000
    		#live four 1110 + 110
    		elif( (type[i] == 7 or type[i] == 13) and (type[(i+4)%8] == 3 or type[(i+4)%8] == 8 or type[(i+4)%8] == 14)):
    			value += 10000
    		#die four a 11110 + 12
    		elif( (type[i] == 12) and (type[(i+4)%8] == None) ):
    			value += 2500
    		#die four a 1110 + 112
    		elif( (type[i] == 7 or type[i] == 13) and (type[(i+4)%8] == 2) ):
    			value += 2500
    		#die four a 110 + 1112
    		elif( (type[i] == 3 or type[i] == 8 or type[i] == 14) and (type[(i+4)%8] == 6) ):
    			value += 2500
    		#die four a 10 + 11112
    		elif( (type[i] == 1 or type[i] == 4 or type[i] == 5 or type[i] == 9 or type[i] == 10 or type[i] == 15) and (type[(i+4)%8] == 11) ):
    			value += 2500
    		#die four b 11101
    		elif(type[i] == 13):
    			value += 3000

    		#die four b 1101+11
    		elif( (type[i] == 8 or type[i] == 14) and (type[(i+4)%8] == 2 or type[(i+4)%8] == 3 or type[(i+4)%8] == 6 or type[(i+4)%8] == 7 or type[(i+4)%8] == 8 or type[(i+4)%8] == 11 or type[(i+4)%8] == 12 or type[(i+4)%8] == 13 or type[(i+4)%8] == 14) ):
    			value += 3000

    		#die four b 101 + 111
    		elif( (type[i] == 4 or type[i] == 5 or type[i] == 9 or type[i] == 10 or type[i] == 15) and (type[(i+4)%8] == 6 or type[(i+4)%8] == 7 or type[(i+4)%8] == 11 or type[(i+4)%8] == 12 or type[(i+4)%8] == 13) ):
    			value += 3000

    		#die four b 10111
    		elif(type[i] == 15):
    			value += 3000

    		#die four c 11011
    		elif(type[i] == 14):
    			value += 2600

    		#die four c 1101 + 11
    		elif( (type[i] == 9 or type[i] == 15) and (type[(i+4)%8] == 2 or type[(i+4)%8] == 3 or type[(i+4)%8] == 6 or type[(i+4)%8] == 7 or type[(i+4)%8] == 8 or type[(i+4)%8] == 11 or type[(i+4)%8] == 12 or type[(i+4)%8] == 13 or type[(i+4)%8] == 14) ):
    			value += 2600

    		#live three 1110 + 10
    		elif( (type[i] == 7 or type[i] == 13) and (type[(i+4)%8] == 1 or type[(i+4)%8] == 4 or type[(i+4)%8] == 5 or type[(i+4)%8] == 9 or type[(i+4)%8] == 10 or type[(i+4)%8] == 15) ):
    			value += 3000

    		#live three 110 110
    		elif( (type[i] == 3 or type[i] == 8 or type[i] == 14) and (type[(i+4)%8] == 3 or type[(i+4)%8] == 8 or type[(i+4)%8] == 14) ):
    			value += 1500	#count 2 times

    		#die three a 1110 + 12
    		elif( (type[i] == 7 or type[i] == 13) and (type[(i+4)%8] == None) ):
    			value += 500

    		#die three a 110 + 112
    		elif( (type[i] == 3 or type[i] == 8 or type[i] == 14) and (type[(i+4)%8] == 2) ):
    			value += 500

    		#die three a 10 + 1112
    		elif( (type[i] == 1 or type[i] == 4 or type[i] == 5 or type[i] == 9 or type[i] == 10 or type[i] == 15) and (type[(i+4)%8] == 6) ):
    			value += 500

    		#die three b 10110 + 10
    		elif( (type[i] == 9 or type[i] == 15) and (type[(i+4)%8] == 1 or type[(i+4)%8] == 4 or type[(i+4)%8] == 5 or type[(i+4)%8] == 9 or type[(i+4)%8] == 10 or type[(i+4)%8] == 15) ):
    			value += 800

    		#die three b 110 + 101
    		elif( (type[i] == 3 or type[i] == 8 or type[i] == 14) and (type[(i+4)%8] == 4 or type[(i+4)%8] == 5 or type[(i+4)%8] == 9 or type[(i+4)%8] == 10 or type[(i+4)%8] == 15) ):
    			value += 800

    		#die three b 10 + 11010
    		elif( (type[i] == 1 or type[i] == 4 or type[i] == 5 or type[i] == 9 or type[i] == 10 or type[i] == 15) and (type[(i+4)%8] == 8 or type[(i+4)%8] == 14) ):
    			value += 800

    		#die three c 10101
    		elif(type[i] == 10):
    			value += 550

    		#die three c 101 + 101
    		elif( (type[i] == 4 or type[i] == 5 or type[i] == 9 or type[i] == 15) and (type[(i+4)%8] == 4 or type[(i+4)%8] == 5 or type[(i+4)%8] == 9 or type[(i+4)%8] == 15) ):
    			value += 550

    		#live two 110 + 10
    		elif(type[i] == 3 and type[(i+4)%8] == 1):
    			value += 650

    		#die two a 110 + 12
    		elif(type[i] == 3 and type[(i+4)%8] == None):
    			value += 150

    		#die two a 10 + 112
    		elif(type[i] == 1 and type[(i+4)%8] == 2):
    			value += 150

    		#die two b 1010 + 10
    		elif(type[i] == 5 and type[(i+4)%8] == 1):
    			value += 250

        return value
