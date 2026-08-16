class MoveHistory:
    def __init__(self):
        self.moves = [] # Stack of (row, col, player)

    def push(self, r, c, player):
        self.moves.append((r, c, player))

    def pop(self):
        if self.moves:
            return self.moves.pop()
        return None

    def get_last_move(self):
        if self.moves:
            return self.moves[-1]
        return None

    def clear(self):
        self.moves = []

    def count(self):
        return len(self.moves)
