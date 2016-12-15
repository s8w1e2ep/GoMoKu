# -*- coding: UTF-8 -*-
from random import choice
from math import log, sqrt
import numpy as np
import time

class Board:
    def __init__(self):
        self.state = np.array([[0] * 15] * 15)
    # 下子
    def play(self, pos, player):
        i, j = pos[0], pos[1]
        self.state[i][j] = player
    # 判斷是否有贏家
    def winner(self, state):
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

class MonteCarlo(object):
    def __init__(self, board, player):
        # C: UCB1常數, MAX_TIME: 模擬時間, MAX_MOVE: 最大移動步數
        # board: 目前盤面 player: 代表玩家
        # states: 狀態表
        # wins, plays: 贏棋的次數, 模擬的次數
        self.board = board
        self.player = player
        self.C = 1
        self.MAX_TIME = 1
        self.MAX_MOVE = 100
        self.MAX_DEPTH = 10
        self.states = []
        self.update(board.state)
        self.wins = {}
        self.plays = {}
    # 更新狀態
    def update(self, state):
        # 添加新狀態
        temp = state
        self.states.append(temp)
    # 回傳合法的走法
    def legalMoves(self, state, turn):
        state = state.reshape(1, 225)[0]
        if(turn != 0):
            return ([(pos / 15, pos % 15) for pos in np.where(state == 0)[0]])
        else:
            return ([(pos / 15, pos % 15) for pos in np.where(state == 0)[0] if (pos / 15 < 2 or pos / 15 > 12) or (pos % 15 < 2 or pos % 15 > 12)])
    # 找出最好的走法
    def bestAction(self, turn):
        # 找出最佳下法
        state = self.states[-1]
        moves = self.legalMoves(state, turn)
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

        moves_states = [(pos, self.updateState(state, pos, self.player)) for pos in moves]
        # 確認模擬次數，時間
        print 'Turn: {0}, Time: {1}(s)'.format(game, time.time() - begin)
        # 選擇最大勝率的走法
        rate_wins, best_move = max(
            (float(self.wins.get(pos, 0)) / self.plays.get(pos, 1), pos)
            for pos, s in moves_states
        )
        # 顯示所有走法勝率
        # for x in sorted(
        #     ((100.0 * self.wins.get(pos, 0) / self.plays.get(pos, 1),
        #       self.wins.get(pos, 0), self.plays.get(pos, 0), pos)
        #       for pos, s in moves_states),
        #     reverse=True
        # ):
        #     print "{3}: {0:.2f}% ({1} / {2})".format(*x)

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
        state = states_copy[-1]

        expand = True
        for t in xrange(1, self.MAX_MOVE + 1):
            player = 1 << ((t + 1) % 2)
            moves = self.legalMoves(state, turn)
            if len(moves) == 0:
                return

            # 取得目前玩家在每個狀態的模擬次數
            play = [plays.get(pos) for pos in moves]
            # 確保每個步驟都有初始值，而不是None
            if all(play):
                # total log(模擬總次數)
                total = log(np.sum(play))
                # 取得最大UCB1值state的action
                value, pos, state = max(
                    ((wins[pos] / plays[pos]) +
                    self.C * sqrt(total / plays[pos]), pos, self.updateState(state, pos, player))
                    for pos in moves
                )
            else:
                pos = choice(moves)
                state = self.updateState(state, pos, player)
            # 設定初始值
            if (expand and pos not in plays):
                expand = False
                plays[pos] = 0
                wins[pos] = 0
                if (t > self.MAX_DEPTH):
                    self.MAX_DEPTH = t
            # 更新拜訪集合
            visited.add(pos)

            winner = self.board.winner(state)
            if winner != False:
                break

        for pos in visited:
            if pos not in plays:
                continue
            plays[pos] += 1
            if self.player == winner:
                wins[pos] += 1
    # 回傳模擬的state
    def updateState(self, state, pos, player):
        temp = np.copy(state)
        i, j = pos[0], pos[1]
        temp[i][j] = player
        return temp

if __name__=="__main__":
    board = Board()
    STATE = np.copy(board.state)
    p1 = MonteCarlo(board, 1)
    p2 = MonteCarlo(board, 2)
    board.display()

    turn = 0
    while (board.winner(STATE)) == False:
        # Player 1
        action = p1.bestAction(turn)
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
        action = p2.bestAction(turn)
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
