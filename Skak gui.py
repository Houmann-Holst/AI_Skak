import tkinter as tk
import chess

class ChessGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chess GUI")

        self.board = chess.Board()

        self.canvas = tk.Canvas(self.root, width=480, height=480)
        self.canvas.pack()

        self.square_size = 60
        self.draw_board()

    def update_board(self, fen):
        self.board = chess.Board(fen)
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        colors = ["#f0d9b5", "#b58863"]

        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                row = 7 - chess.square_rank(square)
                col = chess.square_file(square)
                x = col * self.square_size + 30
                y = row * self.square_size + 30
                self.canvas.create_text(x, y, text=piece.symbol(), font=("Arial", 24))

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    gui = ChessGUI()
    gui.run()
