# -*- coding: UTF-8 -*-
from random import choice
from math import log, sqrt
import numpy as np
import os
import ast
import time

class Board:
    def __init__(self):
        self.state = np.array([[0] * 15] * 15)
    # 判斷是否有贏家
    def isWin(self, state, action, player):
        i, j = action[0], action[1]
        count = np.array([1] * 4)
        state = np.array(state).reshape(15, 15)
        # 直線 |
        for shift in xrange(1, 5):
            if (i + shift) < 15:
                if(state[i + shift][j] == player):
                    count[0] += 1
                else:
                    break
        for shift in xrange(1, 5):
            if (i - shift) > -1:
                if(state[i - shift][j] == player):
                    count[0] += 1
                else:
                    break
        # 橫線 -
        for shift in xrange(1, 5):
            if (j + shift) < 15:
                if (state[i][j + shift] == player):
                    count[1] += 1
                else:
                    break
        for shift in xrange(1, 5):
            if (j + shift) < 15:
                if (state[i][j - shift] == player):
                    count[1] += 1
                else:
                    break
        # 斜線 /
        for shift in xrange(1, 5):
            if (i - shift) > -1 and (j + shift) < 15:
                if (state[i - shift][j + shift] == player):
                    count[2] += 1
                else:
                    break
        for shift in xrange(1, 5):
            if (i + shift) < 15 and (j - shift) > -1:
                if (state[i + shift][j - shift] == player):
                    count[2] += 1
                else:
                    break
        # 反斜線 \
        for shift in xrange(1, 5):
            if (i + shift) < 15 and (j + shift) < 15:
                if (state[i + shift][j + shift] == player):
                    count[3] += 1
                else:
                    break
        for shift in xrange(1, 5):
            if (i - shift) > -1 and (j - shift) > -1:
                if (state[i - shift][j - shift] == player):
                    count[3] += 1
                else:
                    break
        # check 是否五子連線
        if len([val for val in count if (val > 4)]) > 0:
            return True
        else:
            return False
    # 顯示盤面
    def display(self):
        for i in xrange(17):
            if(i == 0 or i == 1):
                print ' ',
            for j in xrange(16):
                if(i == 0 and j != 15):
                    print ' ' + format(j, 'x'),
                elif(i == 1 and j != 15):
                    print '{:>2}'.format('='),
                elif(j == 0):
                    print format((i - 2), 'x') + '|',
                elif(i != 0 and i != 1):
                    if(self.state[(i - 2)][(j -1)] == 0):
                        print '{:2}'.format('-'),
                    elif(self.state[(i - 2)][(j -1)] == 1):
                        print '{:2}'.format('X'),
                    else:
                        print '{:2}'.format('O'),
            print ''
    # 回傳此回合玩家
    def currentPlayer(self, state):
        state = np.array(state)
        state = state.reshape(1, 225)[0]
        p1 = len([v for v in state if (v == 1)])
        p2 = len([v for v in state if (v == 2)])
        if (p1 == p2):
            return 2
        elif(p1 > p2):
            return 1
    # 回傳下回合玩家
    def nextPlayer(self, state):
        state = np.array(state)
        state = state.reshape(1, 225)[0]
        p1 = len([v for v in state if (v == 1)])
        p2 = len([v for v in state if (v == 2)])
        if (p1 == p2):
            return 1
        elif(p1 > p2):
            return 2
class MonteCarlo(object):
    def __init__(self, board, player):
        # C: UCB1常數, MAX_TIME: 模擬時間, MAX_MOVE: 最大移動步數
        # board: 目前盤面 player: 代表玩家
        # states: 狀態表
        # wins, plays: 贏棋的次數, 模擬的次數
        self.board = board
        self.player = player
        self.C = 1.4
        self.MAX_TIME = 3
        self.MAX_MOVE = 100
        self.MAX_DEPTH = 0
        self.states = []
        self.value = np.array([[[0] * 15] * 15])
        self.update(board.state)
        self.wins = {}
        self.plays = {}
        self.before = (-1, -1)
    # 更新狀態
    def update(self, state):
        # 添加新狀態
        self.states.append(state)
    # 回傳合法的走法
    def legalMoves(self, state, pos, flag = 1):
        if(flag == 0):
            tem_value = list(self.value.reshape(1, 225)[0])
            temp_value = []
            for i in xrange(len(tem_value)):
                temp_value.append((tem_value[i], i))
            temp_value = sorted(temp_value, key=lambda s : s[0],reverse=True)
            move = []
            if(temp_value[0][0] > 40000):
                index = temp_value[0][1]
                move.append((index/15, index%15))
            else:
                temp = [(index/15, index%15) for (val, index) in temp_value]
                if(temp_value[0][0] > 3000 and temp_value[0][0] / float(temp_value[1][0]) > 1.5):
                    move.append(temp[0])
                elif(temp_value[0][0] > 3000 and temp_value[0][0] / float(temp_value[2][0]) > 1.5):
                    move.append(temp[0])
                    move.append(temp[1])
                else:
                    move.append(temp[0])
                    move.append(temp[1])
                    move.append(temp[2])
            return move
        else:
            i, j = pos
            if(i != -1 and j != -1):
                state = np.array(state).reshape(1, 225)[0]
                temp = [(pos / 15, pos % 15) for pos in np.where(state == 0)[0]]
                moves = []
                for (x, y) in temp:
                    if x == i and abs(y - j) < 5:
                        moves.append((x, y))
                    elif y == j and abs(x - j) < 5:
                        moves.append((x, y))
                    elif abs(x - i) == abs(y - j) and abs(x - i) < 5:
                        moves.append((x, y))
                if len(moves) == 0:
                    return temp
                else:
                    return moves
            else:
    			state = np.array(state).reshape(1, 225)[0]
    			moves = [(pos / 15, pos % 15) for pos in np.where(state == 0)[0]]

    			if (len(moves) == 225):
    				return ([(pos / 15, pos % 15) for pos in np.where(state == 0)[0] if (pos / 15 < 2 or pos / 15 > 12) or (pos % 15 < 2 or pos % 15 > 12)])
    			else:
    				return moves
    # 找出最好的走法
    def bestAction(self):
        # 找出最佳下法
        self.MAX_DEPTH = 0
        state = self.states[-1]
        moves = self.legalMoves(state,None,0)
        # 判斷是否有很多種走法
        if not moves:
            return
        elif len(moves) == 1:
            return moves[0]
        # 如果很多走法，找一個最好的
        game = 0
        begin = time.time()

        while (time.time() - begin) < self.MAX_TIME:
            self.simulation()
            game += 1

        moves_states = [(pos, self.updateState(state, pos, self.player).reshape(1, 225)[0]) for pos in moves]
        # 確認模擬次數，時間
        #print 'Turn: {0},
	print 'Time: {0}(s)'.format(time.time() - begin)
        # print 'Play: {}, Win: {}'.format(self.plays.values(), self.wins.values())
        # 選擇最大勝率的走法
        totalMoves = []
        for item in moves_states:
            t1 = float(self.wins.get((self.player, tuple(item[1])), 0))
            t2 = self.plays.get((self.player, tuple(item[1])), 1)
            if t2 != 0:
                totalMoves.append(((t1 / t2), item[0]))
            else:
                totalMoves.append((0.0, item[0]))

        max = -1
        best_move = moves_states
        for p, move in totalMoves:
            if (p > max):
                max = p
                del best_move[:]
                best_move.append((max, move))
            elif (p == max):
                best_move.append((max, move))

        if len(best_move) == 1:
            rate_wins, bmove = best_move[0]
        elif len(best_move) != 0:
            rate_wins, bmove = choice(best_move)

        #print 'The probability of win: {}, the best action: {}'.format(rate_wins, bmove)

        #print "Maximum depth searched:", self.MAX_DEPTH
        return bmove
    # 模擬
    def simulation(self):
        # MonteCarloSearch
        plays, wins = self.plays, self.wins
        # 紀錄拜訪過的狀態
        visited = set()
        states_copy = self.states[:]
        # 取得最後一個狀態
        state = np.copy(states_copy[-1])
        player = self.player

        expand = True
	pos = (-1,-1)
        for t in xrange(1, self.MAX_MOVE + 1):
            # player = 1 << ((t + 1) % 2)
            moves = self.legalMoves(state,pos)
            if len(moves) == 0:
                return
            # 取得每個走法的狀態
            moves_state = [(pos, self.updateState(state, pos, player).reshape(1, 225)[0]) for pos in moves]
            # 取得目前玩家在每個狀態的模擬次數
            play = [plays.get((player, tuple(item[1]))) for item in moves_state]
            # 確保每個步驟都有初始值，而不是None
            # print 'play:{}'.format(play)
            if all(play):
                # total log(模擬總次數)
                total = log(np.sum(play))
                # 取得最大UCB1值state的action
                ucb = [((wins[(player, tuple(s))] / plays[(player, tuple(s))]) + self.C * np.sqrt(total / plays[(player, tuple(s))]), (pos, s)) for pos, s in moves_state]
		print ucb
                val, move_s = max(ucb)
                pos, state = move_s[0], move_s[1]
            else:
                pos, state = choice(moves_state) #self.valueNet(moves, state, player)#choice(moves)
                # state = self.updateState(state, pos, player)
	    print state
            # 設定初始值
            if (expand and (player, tuple(state)) not in plays):
                expand = False
                plays[(player, tuple(state))] = 0
                wins[(player, tuple(state))] = 0
                if (t > self.MAX_DEPTH):
                    self.MAX_DEPTH = t
            # 更新拜訪集合
            visited.add((player, tuple(state)))

            winner = self.board.isWin(state, pos, player)
            if winner:
                break
            player = self.board.nextPlayer(state)

        for player, state in visited:
            # print state
            if (player, state) not in plays.keys():
                continue
            plays[(player, state)] += 1
            # print 'Sim: {}'.format(plays.values())
            # print 'player {}, winner {}'.format(player, winner)
            if player == winner:
                wins[(player, state)] += 1
                # print '{}: {}'.format(player, wins[(player, state)])
    # 回傳模擬的state
    def updateState(self, state, action, player):
        temp = np.copy(state)
        temp = np.array(temp).reshape(15, 15)
        temp[action[0]][action[1]] = player
        return temp

"""if __name__=="__main__":
    board = Board()
    STATE = np.copy(board.state)
    p1 = MonteCarlo(board, 1)
    p2 = MonteCarlo(board, 2)

    board.display()

    turn = 0
    action2 = (-1, -1)
    while True:
        # Player 1
        p1.update(board.state)
        action1 = p1.bestAction(turn, action2)
        print 'Turn: {}, p1: {}'.format(turn, action1)
        STATE[action1[0]][action1[1]] = p1.player
        board.state = np.copy(STATE)
        board.display()
        if board.isWin(STATE, action1, p1.player):
            break
        turn += 1
        p2.update(board.state)
        # Player 2
        action2 = p2.bestAction(turn, action1)
        print 'Turn: {}, p2: {}'.format(turn, action2)
        STATE[action2[0]][action2[1]] = p2.player
        board.state = np.copy(STATE)
        board.display()
        turn += 1
        if board.isWin(STATE, action2, p2.player):
            break

    win = board.currentPlayer(STATE)
    if (win == 1):
        print 'Black is win.'
    elif (win == 2):
        print 'White is win.'"""
