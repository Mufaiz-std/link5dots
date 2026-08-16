from game.board import Board
import random

class GameState:
    MODE_CPU = 'cpu'
    MODE_PVP = 'pvp'
    
    DIFF_EASY = 'easy'
    DIFF_HARD = 'hard'
    
    FIRST_P1 = 'p1' # You / Player 1
    FIRST_P2 = 'p2' # CPU / Player 2
    FIRST_RANDOM = 'random'

    def __init__(self):
        self.mode = self.MODE_CPU
        self.difficulty = self.DIFF_EASY
        self.who_goes_first_setting = self.FIRST_P1
        
        self.board_rows = 15
        self.board_cols = 15
        
        # State
        self.current_player = Board.PLAYER_1
        self.winner = None
        self.win_line = None
        self.is_draw = False
        self.cpu_thinking = False
        
        # We need to remember who actually went first if setting was RANDOM, 
        # so we can re-roll on "Restart" only if setting was RANDOM.
        self._actual_first_player = Board.PLAYER_1
        
    def setup_new_game(self, reroll_random=True):
        self.winner = None
        self.win_line = None
        self.is_draw = False
        self.cpu_thinking = False
        
        if self.who_goes_first_setting == self.FIRST_P1:
            self._actual_first_player = Board.PLAYER_1
        elif self.who_goes_first_setting == self.FIRST_P2:
            self._actual_first_player = Board.PLAYER_2
        else:
            if reroll_random:
                self._actual_first_player = random.choice([Board.PLAYER_1, Board.PLAYER_2])
            # if not rerolling, keep self._actual_first_player as is
            
        self.current_player = self._actual_first_player

    def switch_turn(self):
        if self.current_player == Board.PLAYER_1:
            self.current_player = Board.PLAYER_2
        else:
            self.current_player = Board.PLAYER_1

    def is_game_over(self):
        return self.winner is not None or self.is_draw
