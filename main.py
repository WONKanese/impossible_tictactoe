import random

times = 0

class GameState:

    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.turn = "X"

    def render(self):
        for j, row in enumerate(self.board):
            for i, tile in enumerate(row):
                if i != 2:
                    print(tile, end="|")
                else:
                    print(tile)
            if j != 2:
                print("-----")

    def place(self, x, y, side="na"):
        if side == "na":
            side = self.turn
        self.board[y][x] = side
        self.turn = "O" if self.turn == "X" else "X"

    def copy_and_place(self, move, side):
        new_state = GameState()
        new_state.board = [row[:] for row in self.board]
        new_state.turn = self.turn
        new_state.place(move[0], move[1], side)
        return new_state

    def get_available_moves(self):
        return [(i, j) for j, row in enumerate(self.board) for i, tile in enumerate(row) if tile == " "]

    def check_state(self):
        # Check horizontal and vertical
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != " ":
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != " ":
                return self.board[0][i]

        # Check diagonal
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            return self.board[0][2]

        # Check for ongoing or tie
        if any(" " in row for row in self.board):
            return "ongoing"
        return "tie"

class AI:

    def __init__(self, side):
        print("AI created for", side)
        self.side = side

    def score(self, board):
        state = board.check_state()
        if state == "tie":
            return 0
        if state == self.side:
            return 1
        return -1

    def minimax(self, board, depth, maximizing):
        result = board.check_state()
        if result != "ongoing":
            return self.score(board)

        if maximizing:
            best_score = -float("inf")
            for move in board.get_available_moves():
                new_board = board.copy_and_place(move, self.side)
                score = self.minimax(new_board, depth + 1, False)
                best_score = max(best_score, score)
            return best_score
        else:
            opponent_side = "O" if self.side == "X" else "X"
            best_score = float("inf")
            for move in board.get_available_moves():
                new_board = board.copy_and_place(move, opponent_side)
                score = self.minimax(new_board, depth + 1, True)
                best_score = min(best_score, score)
            return best_score

    def best_move(self, board):
        best_score = -float("inf")
        best_move = None
        for move in board.get_available_moves():
            new_board = board.copy_and_place(move, self.side)
            score = self.minimax(new_board, 0, False)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

# Example usage:
main = GameState()
ai_player = AI("X")

while main.check_state() == "ongoing":
    ai_move = ai_player.best_move(main)
    main.place(ai_move[0], ai_move[1], "X")
    if main.check_state() != "ongoing":
        break
    main.render()
    while (True):
        print("~~~~~~~~~~~~~~~~")
        x = int(input("x: ")) - 1
        y = int(input("y: ")) - 1
        print("~~~~~~~~~~~~~~~~")
        if (x, y) in main.get_available_moves():
            break
        else:
            print("Invalid Move")
    main.place(x, y, "O")
    main.render()
print(main.check_state(), "Wins!")
main.render()
