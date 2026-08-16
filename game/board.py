class Board:
    EMPTY = 0
    PLAYER_1 = 1
    PLAYER_2 = 2 # Also CPU

    def __init__(self, rows=15, cols=15):
        self.rows = rows
        self.cols = cols
        # 0 = empty, 1 = p1 (hollow), 2 = p2 (solid)
        self.grid = [[self.EMPTY for _ in range(cols)] for _ in range(rows)]
        self.piece_count = {self.PLAYER_1: 0, self.PLAYER_2: 0}

    def place_piece(self, r, c, player):
        """Returns True if placement was successful, False if invalid."""
        if self.is_valid_move(r, c):
            self.grid[r][c] = player
            self.piece_count[player] += 1
            return True
        return False

    def remove_piece(self, r, c):
        """Removes a piece from the board (for undo)."""
        if 0 <= r < self.rows and 0 <= c < self.cols:
            player = self.grid[r][c]
            if player != self.EMPTY:
                self.grid[r][c] = self.EMPTY
                self.piece_count[player] -= 1
                return True
        return False

    def is_valid_move(self, r, c):
        """Checks if a cell is on board and empty."""
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.grid[r][c] == self.EMPTY
        return False

    def get_cell(self, r, c):
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.grid[r][c]
        return None

    def is_full(self):
        return sum(self.piece_count.values()) == self.rows * self.cols

    def clear(self):
        self.grid = [[self.EMPTY for _ in range(self.cols)] for _ in range(self.rows)]
        self.piece_count = {self.PLAYER_1: 0, self.PLAYER_2: 0}
