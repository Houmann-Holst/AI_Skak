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

        # Grøn / hvid (lichess style)
        light_color = "#eeeed2"
        dark_color = "#769656"

        for row in range(8):
            for col in range(8):
                color = light_color if (row + col) % 2 == 0 else dark_color
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline=color
                )

        # Ingen brik-tekst rendering (fjernet med vilje)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    gui = ChessGUI()
    gui.run()

