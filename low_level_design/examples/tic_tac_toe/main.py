class Board:
    def __init__(self, n, m):
        self.board = []
        for i in range(n):
            self.board.append([-1]*m)
        self.is_first_player_turn = True
        self.game_status = -1

    def move(self, row, col):
        if(self.board[row][col] == -1):
            raise Exception('Already occupied')
        if(self.is_first_player_turn == True):
            self.board[row][col] = 1
        else:
            self.board[row][col] = 2
        self.is_first_player_turn = not self.is_first_player_turn
        self.check()

    '''def check(self):
        for i in range(n):
            for j in range(m):
       '''

class Game:
    def __init__(self, player_1, player_2, board):
        self.player_1 = player_1
        self.player_2 = player_2
        self.board = board

    def make_move(self):

    def check_game_status(self):

    def start_game(self):
        while(self.board.game_status == -1):
