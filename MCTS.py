# -*- coding: UTF-8 -*-
from random import choice
from math import log, sqrt
import numpy as np
import ast
import time

class Node():
    def __init__(self, state, action=None):
        self.state = state
        self.parent = None
        self.visited = []
        self.children = []
        self.action = action
        self.win = 0
        self.play = 0
    # add child node
    def addChild(self, child):
        self.children.append(child)
    # add parent
    def addParent(self, parent):
        self.parent = parent
    # get the posibility of win
    def getWP(self):
        return (self.win, self.play)
    # visited
    def isVisit(self, pos):
        if pos in self.visited:
            return True
        else:
            return False


class Board:
    def __init__(self):
        self.state = np.array([[0] * 15] * 15)
    # 下子
    def play(self, pos, player):
        i, j = pos[0], pos[1]
        self.state[i][j] = player
    # 判斷是否有贏家
    def winner(self, state):
        state = np.array(state)
        state = state.reshape(15, 15)
        empty = 225
        for i in xrange(15):
            for j in xrange(15):
                if(state[i][j] == 1):
                    count = np.array([1] * 4)
                    for shift in xrange(1, 5):
                        if (i + shift) < 15 and (state[i + shift][j] == 1):
                            count[0] += 1
                        if (j + shift) < 15 and (state[i][j + shift] == 1):
                            count[1] += 1
                        if (i - shift) > 0 and (j + shift) < 15 and (state[i - shift][j + shift] == 1):
                            count[2] += 1
                        if (i + shift) < 15 and (j + shift) < 15 and (state[i + shift][j + shift] == 1):
                            count[3] += 1
                    # check 是否五子連線
                    if len([val for val in count if (val > 4)]) > 0:
                        return 1
                elif(state[i][j] == 2):
                    count = np.array([1] * 4)
                    for shift in xrange(1, 5):
                        if (i + shift) < 15 and (state[i + shift][j] == 2):
                            count[0] += 1
                        if (j + shift) < 15 and (state[i][j + shift] == 2):
                            count[1] += 1
                        if (i - shift) > 0 and (j + shift) < 15 and (state[i - shift][j + shift] == 2):
                            count[2] += 1
                        if (i + shift) < 15 and (j + shift) < 15 and (state[i + shift][j + shift] == 2):
                            count[3] += 1
                    # check 是否五子連線
                    if len([val for val in count if (val > 4)]) > 0:
                        return 2
                else:
                    empty -= 1
        # 判斷棋盤是否已滿
        if (empty == 225):
            return 3
        else:
            return False
    def isWin(self, state, action, player):
        i, j = action[0], action[1]
        count = np.array([1] * 4)
        for shift in xrange(1, 5):
            # 直線 |
            if (i + shift) < 15 and (state[i + shift][j] == 1):
                count[0] += 1
            elif (i - shift) > -1 and (state[i + shift][j] == 1):
                count[0] += 1
            # 橫線 -
            if (j + shift) < 15 and (state[i][j + shift] == 1):
                count[1] += 1
            elif (j - shift) > -1 and (state[i][j - shift] == 1):
                count[1] += 1
            # 斜線 /
            if (i - shift) > -1 and (j + shift) < 15 and (state[i - shift][j + shift] == 1):
                count[2] += 1
            elif (i + shift) < 15 and (j - shift) > -1 and (state[i + shift][j - shift] == 1):
                count[2] += 1
            # 反斜線 \
            if (i + shift) < 15 and (j + shift) < 15 and (state[i + shift][j + shift] == 1):
                count[3] += 1
            elif (i - shift) > -1 and (j - shift) > -1 and (state[i - shift][j - shift] == 1):
                count[3] += 1
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
    # 回傳目前玩家
    def currentPlayer(self, state):
        state = np.array(state)
        state = state.reshape(1, 225)[0]
        p1 = len([v for v in state if (v == 1)])
        p2 = len([v for v in state if (v == 2)])
        if (p1 == p2):
            return 2
        else:
            return 1

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
        self.update(board.state)
        # dict
        self.wins = {}
        self.plays = {}
    # 更新狀態
    def update(self, state):
        # 添加新狀態
        self.states.append(state)
    # 回傳合法的走法
    def legalMoves(self, state):
        state = np.array(state).reshape(1, 225)[0]
        moves = [(pos / 15, pos % 15) for pos in np.where(state == 0)[0]]
        if (len(moves) == 225):
            return ([(pos / 15, pos % 15) for pos in np.where(state == 0)[0] if (pos / 15 < 2 or pos / 15 > 12) or (pos % 15 < 2 or pos % 15 > 12)])
        else:
            return moves

    # 找出最好的走法
    def bestAction(self, turn, f):
        # 找出最佳下法
        self.MAX_DEPTH = 0
        state = self.states[-1]
        moves = self.legalMoves(state)
        # 判斷是否有很多種走法
        if not moves:
            return
        elif len(moves) == 1:
            return moves[0]
        # 如果很多走法，找一個最好的
        game = 0
        begin = time.time()

        while (time.time() - begin) < self.MAX_TIME:
            self.simulation(turn)
            game += 1

        moves_states = [(pos, self.updateState(state, pos, self.player).reshape(1, 225)[0]) for pos in moves]
        # 確認模擬次數，時間
        print 'Turn: {0}, Time: {1}(s)'.format(game, time.time() - begin)
        # print 'Play: {}, Win: {}'.format(self.plays.values(), self.wins.values())
        # 選擇最大勝率的走法
        totalMoves = [(float(self.wins.get((self.player, tuple(item[1])), 0)) / self.plays.get((self.player, tuple(item[1])), 1), item[0])
                      for item in moves_states]
        max = -1
        best_move = []
        for p, move in totalMoves:
            if (p > max):
                max = p
                del best_move[:]
                best_move.append((max, move))
            elif (p == max):
                best_move.append((max, move))

        if len(best_move) == 1:
            rate_wins, best_move = best_move[0]
        else:
            rate_wins, best_move = choice(best_move)

        # f.write(str(totalMoves) + '\n')

        # rate_wins, best_move = max(
        #     (float(self.wins.get((self.player, tuple(s)), 0)) / self.plays.get((self.player, tuple(s)), 1), pos)
        #     for pos, s in moves_states
        # )
        # 顯示所有走法勝率
        # for x in sorted(
        #     ((100 * self.wins.get((self.player, tuple(s)), 0) / float(self.plays.get((self.player, tuple(s)), 1)),
        #       self.wins.get((self.player, tuple(s)), 0), self.plays.get((self.player, tuple(s)), 0), pos, self.player)
        #       for pos, s in moves_states),
        #     reverse=True
        # ):
        #     f.write("{4} - {3}: {0:.2f}% ({1} / {2}) \n".format(*x))
            # print "{4} - {3}: {0:.2f}% ({1} / {2})".format(*x)

        print "Maximum depth searched:", self.MAX_DEPTH

        return best_move
    # 模擬
    def simulation(self, turn):
        # MonteCarloSearch
        plays, wins = self.plays, self.wins
        # 紀錄拜訪過的狀態
        visited = set()
        states_copy = self.states[:]
        # 取得最後一個狀態
        state = np.copy(states_copy[-1])
        player = self.board.currentPlayer(state)

        expand = True
        for t in xrange(1, self.MAX_MOVE + 1):
            # player = 1 << ((t + 1) % 2)
            moves = self.legalMoves(state)
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
                ucb = [((wins[(player, s)] / plays[(player, s)]) + self.C * np.sqrt(total / plays[(player, s)]), move_s) for move_s in moves_state]
                value, move_s = max(ucb)
                pos, state = move_s[0], move_s[1]
            else:
                pos, state = choice(moves_state) #self.valueNet(moves, state, player)#choice(moves)
                # state = self.updateState(state, pos, player)

            # 設定初始值
            if (expand and (player, tuple(state)) not in plays):
                expand = False
                plays[(player, tuple(state))] = 0
                wins[(player, tuple(state))] = 0
                if (t > self.MAX_DEPTH):
                    self.MAX_DEPTH = t
            # 更新拜訪集合
            visited.add((player, tuple(state)))

            player = self.board.currentPlayer(state)
            winner = self.board.winner(state)
            if winner != False:
                break

        for player, state in visited:
            # print state
            if (player, state) not in plays:
                continue
            plays[(player, state)] += 1
            # print 'Sim: {}'.format(plays.values())
            # print 'player {}, winner {}'.format(player, winner)
            if player == winner:
                wins[(player, state)] += 1
                # print '{}: {}'.format(player, wins[(player, state)])
    # 回傳模擬的state
    def updateState(self, state, pos, player):
        temp = np.copy(state)
        temp = np.array(temp).reshape(15, 15)
        i, j = pos[0], pos[1]
        temp[i][j] += player
        return temp

if __name__=="__main__":
    board = Board()
    STATE = np.copy(board.state)
    rp1 = open('p1.txt', 'r');
    rp2 = open('p2.txt', 'r');
    rw1 = open('w1.txt', 'r');
    rw2 = open('w2.txt', 'r');

    p1 = MonteCarlo(board, 1)
    p1.plays = ast.literal_eval(rp1.read())
    p1.wins = ast.literal_eval(rw1.read())
    p2 = MonteCarlo(board, 2)
    p2.plays = ast.literal_eval(rp2.read())
    p2.wins = ast.literal_eval(rw2.read())
    rp1.close()
    rp2.close()
    rw1.close()
    rw2.close()

    board.display()
    fp1 = open('p1.txt', 'w');
    fp2 = open('p2.txt', 'w');
    fw1 = open('w1.txt', 'w');
    fw2 = open('w2.txt', 'w');

    turn = 0
    while (board.winner(STATE)) == False:
        # Player 1
        action = p1.bestAction(turn, fp1)
        print 'Turn: {}, p1: {}'.format(turn, action)
        # board.play(action, p1.player)
        STATE[action[0]][action[1]] = p1.player
        board.state = np.copy(STATE)
        board.display()
        if board.winner(STATE) != False:
            break
        turn += 1
        p2.update(board.state)
        # Player 2
        action = p2.bestAction(turn, fp2)
        print 'Turn: {}, p2: {}'.format(turn, action)
        # board.play(action, p2.player)
        STATE[action[0]][action[1]] = p2.player
        board.state = np.copy(STATE)
        board.display()
        turn += 1
        p1.update(board.state)

    win = board.winner(STATE)
    if (win == 1):
        print 'Black is win.'
    elif (win == 2):
        print 'White is win.'
    else:
        print 'Tie.'

    fp1.write(str(p1.plays))
    fw1.write(str(p1.wins))
    fp2.write(str(p2.plays))
    fw2.write(str(p2.wins))

    # for item in p1.plays:
    #     f1.write('play: ' + str(p1.plays.values()) + '\n')
    # for item in p1.wins:
    #     f1.write('win: ' + str(item) + '\n')
    # for item in p2.plays:
    #     f2.write('play: ' + str(item) + '\n')
    # for item in p2.wins:
    #     f2.write('win: ' + str(item) + '\n')
    fp1.close()
    fw1.close()
    fp2.close()
    fw2.close()
