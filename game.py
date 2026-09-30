from board import Board


DIFFICULTIES = {
    "easy": (6, 6, 6),
    "medium": (9, 9, 15),
    "hard": (12, 12, 30),
}


class Minesweeper:
    def __init__(self):
        self.board = Board()
        self.difficulty = "easy"

    def select_difficulty(self):
        while True:
            choice = input("Difficulty (easy/medium/hard) [easy]: ").strip().lower()
            if not choice:
                choice = "easy"
            if choice in DIFFICULTIES:
                self.difficulty = choice
                self.board = Board(*DIFFICULTIES[choice])
                return
            print("Choose easy, medium, or hard.")

    def display(self, reveal_mines=False):
        b = self.board
        print("\n   " + " ".join(str(c + 1) for c in range(b.cols)))
        for r in range(b.rows):
            cells = []
            for c in range(b.cols):
                pos = (r, c)
                if reveal_mines and pos in b.mines:
                    ch = "*"
                elif pos in b.flags:
                    ch = "F"
                elif pos not in b.revealed:
                    ch = "#"
                elif pos in b.mines:
                    ch = "*"
                else:
                    ch = str(b.adjacent_mines(r, c))
                cells.append(ch)
            print(f"{r + 1:2} " + " ".join(cells))

    def run(self):
        print("Minesweeper")
        self.select_difficulty()
        print(f"Difficulty: {self.difficulty.title()}")
        print("Commands: r row col | f row col | q")
        while True:
            self.display()
            raw = input("> ").strip().lower()
            if raw == "q":
                return
            parts = raw.split()
            if len(parts) != 3 or parts[0] not in {"r", "f"}:
                print("Use r row col or f row col.")
                continue
            try:
                r, c = int(parts[1]) - 1, int(parts[2]) - 1
            except ValueError:
                print("Coordinates must be numbers.")
                continue
            if not self.board.in_bounds(r, c):
                print("Outside the board.")
                continue

            if parts[0] == "f":
                pos = (r, c)
                was_flagged = pos in self.board.flags
                if not self.board.toggle_flag(pos):
                    print("Cannot flag that cell.")
                else:
                    print("Flag removed." if was_flagged else "Flag placed.")
                continue

            pos = (r, c)
            if pos in self.board.flags:
                print("That cell is flagged; unflag it before revealing.")
                continue
            previous_revealed = len(self.board.revealed)
            if self.board.reveal(pos):
                self.display(reveal_mines=True)
                print("BOOM! You hit a mine.")
                return
            revealed_count = len(self.board.revealed) - previous_revealed
            if revealed_count:
                noun = "cell" if revealed_count == 1 else "cells"
                print(f"Revealed {revealed_count} safe {noun}.")
            else:
                print("That cell was already revealed.")
            if self.board.won():
                self.display()
                print("You cleared the board!")
                return
