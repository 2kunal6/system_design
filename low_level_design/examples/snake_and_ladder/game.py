from random import randint

class Board:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.player_turn = 1
        self.player_1_pos = 0
        self.player_2_pos = 0
        self.ladders = []
        self.snakes = []
        self.status = 0

    def add_ladder(self, start, end):
        self.ladders.append([start, end])

    def add_snake(self, start, end):
        self.snakes.append([start, end])

    def process_asset(self, asset):
        for val in asset:
            if(self.player_1_pos == val[0]):
                self.player_1_pos = val[1]
            if (self.player_2_pos == val[0]):
                self.player_2_pos = val[1]

    def process_ladder_or_snake(self):
        self.process_asset(self.ladders)
        self.process_asset(self.snakes)
        if(self.player_1_pos == self.row * self.col):
            self.status = 1
        if (self.player_2_pos == self.row * self.col):
            self.status = 2

    def make_move(self):
        dice_val = randint(1, 6)
        if(self.player_turn == 1):
            self.player_1_pos+=dice_val
            self.player_turn = 2
        else:
            self.player_2_pos += dice_val
            self.player_turn = 1
        self.process_ladder_or_snake()
        print(self.player_1_pos, self.player_2_pos)

class Game:
    def __init__(self, board):
        self.board = board

    def start_game(self):
        while(self.board.status == 0):
            self.board.make_move()
        print(self.board.status)

board = Board(10, 10)
game = Game(board)
game.start_game()