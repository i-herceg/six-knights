import time
from copy import deepcopy
import numpy as np
from pprint import pprint
from collections import deque, namedtuple, Counter
from itertools import combinations

Start_Game = namedtuple("Start_Game", ["start_board_str", "end_board_str"])

def visualize(graph):
    row = 0
    print(end="\t_________")
    for node in graph:
        if node[0] != row:
            if row == 0:
                print(end="\n\t| ")
            else:
                print(end="| \n\t| ")
            row +=1
        print(graph[node], end=" ")
    print(end="|\n\t|_______|\n\n")

def initialize(board_str):
    idx2coord = {}
    coord2idx = {}
    counter = 0
    jumps = {}

    i, j = 0, 0
    for line in board_str.strip().split("\n"):
        for item in line:
            idx2coord[counter] = (i, j)
            coord2idx[i, j] = counter
            j += 1
            counter += 1
        i += 1
        j = 0

    for idx1, (i, j) in idx2coord.items():
        for di, dj in [(-2, -1), (-2, + 1), (+2, -1), (+2, +1), 
                       (-1, -2), (+1, -2), (-1, +2), (+1, +2)]:
            ni = i + di
            nj = j + dj
            if (ni, nj) in coord2idx:
                idx2 = coord2idx[ni, nj]
                if idx1 not in jumps:
                    jumps[idx1] = []
                jumps[idx1].append(idx2)
    return jumps
    
def transform(board_str):
    result = ""
    for line in board_str.strip().split("\n"):
        for item in line:
            if item == "B":
                result = result + "1"
            elif item == "W":
                result = result + "0"
            elif item == ".":
                result = result + "2"
    return result

def transform2(board_str,i):
    rows, col = dimension(board_str)
    board = []
    for j in range(rows):
        row = ""
        for k in range(col):
            if i[k] == "1":
                row = row + "B"
            elif i[k] == "0":
                row = row + "W"
            else:
                row = row + "."
        i = i[col:]
        board.append(row)
    return board

def get_graph(input_):
    graph = {(x, y) : '' for x in range(1, len(input_)) for y in range(1, len(input_[0])+1)}

    for i in range(len(input_)):
        row=input_[i]
        for j in range(len(input_[i])):
            graph[(i+1,j+1)]=row[j]
    return graph
              
def dimension(board_str):
    row = 0
    col = 0
    for line in board_str.strip().split("\n"):
        row += 1
        col = len(line)
    return row,col

              
class Board():
    def __init__(self, board: str):
        self.current_board = board
        self.history: list[str] = list()

    def __eq__(self, other):
        return self.current_board == other.current_board and len(self.history) == len(other.history)

    def __le__(self, other):
        return self.current_board == other.current_board and len(self.history) <= len(other.history)

    def make_move(self, home: int, landing: int):
        self.history.append(self.current_board)
        board = list(self.current_board)
        board[home], board[landing] = board[landing], board[home]
        self.current_board = "".join(board)

    def is_empty(self, landing: int) -> bool:
        if self.current_board[landing] == "2":
            return True

class Game():

    def __init__(self, initial_board: Board, goal: str, edges: dict[int, list]):
        self.boards: deque[Board] = deque([initial_board])
        self.goal = goal
        self.edges = edges
        self.history: deque[Board] = deque()

    @staticmethod
    def make_move(board: Board, home: int, landing: int) -> Board:
        board = deepcopy(board)
        board.make_move(home, landing)
        return board

    def check_goal(self, board: Board) -> bool:
        if board.current_board == self.goal:
            return True

    def is_valid_move(self, new_board: Board):
        return not (
            any(
                new_board == board
                for board in self.history
            )
            or any(
                new_board <= board
                for board in self.boards
            )
        )

    def bfs(self):
        start_time = time.perf_counter()
        while self.boards:
            board = self.boards.popleft()
            if self.check_goal(board):
                print(f"Pronađeno rješenje u {len(board.history)} poteza")
                end_time = time.perf_counter()
                execution_time = end_time - start_time
                print(f"Vrijeme izvršavanja je: {execution_time}")
                return board.history
            self.history.append(board)
            #print(len(board.history))
            for home in [i for i, piece in enumerate(board.current_board)
                         if (int(piece) == 0 or int(piece) == 1)]:
                for landing in self.edges[home]:
                    if board.is_empty(landing):
                        new_board = Game.make_move(board, home, landing)
                        if self.is_valid_move(new_board):
                            self.boards.append(new_board)
                            

if __name__ == "__main__":

    game2 = Start_Game("B.B\n...\nW.W", "W.W\n...\nB.B")
    game1 = Start_Game("BBB\n...\n...\nWWW", "WWW\n...\n...\nBBB")
    
    game_2 = Game(
        Board(transform(game2.start_board_str)),
        transform(game2.end_board_str),
        initialize(game2.start_board_str)
        )
    game_1 = Game(
        Board(transform(game1.start_board_str)),
        transform(game1.end_board_str),
        initialize(game1.start_board_str)
        )
    
    history = game_1.bfs()
    move = 0
    for board in history:
        t = transform2(game1.start_board_str,board)
        graph = get_graph(t)
        print("POTEZ: ",move)
        visualize(graph)
        move += 1
    target = transform2(game1.end_board_str,transform(game1.end_board_str))
    print("POTEZ: ",move)
    visualize(get_graph(target))
    print("KRAJ!")







