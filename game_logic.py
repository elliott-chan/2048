import random

class Game2048():
    def __init__(self, size=4):
        self.size = size
        self.board = [[None for _ in range(size)] for _ in range(size)]
        self.score = 0

        print(f"[DEBUG] Created empty {size}x{size} board:")
        self.print_board()
        self.add_initial_tiles()
        print("[DEBUG] Board after adding initial tiles:")
        self.print_board()
    
    def print_board(self):
        for row in self.board:
            print(' '.join(str(cell) if cell is not None else '.' for cell in row))
        print()

    def add_initial_tiles(self):
        count = random.randint(2,16) # random number of '2's at random cells
        print(f"[DEBUG] Adding {count} initial tile(s) of value 2.")
        for _ in range(count):
            self.add_random_tile(value=2)

    def move_left(self):
        moved = False
        for r in range(self.size):
            original_row = self.board[r][:]
            new_row = [cell for cell in original_row if cell is not None]
            for i in range(1, len(new_row)):
                if new_row[i] == new_row[i-1]:
                    new_row[i-1] *= 2
                    self.score += new_row[i-1]
                    new_row[i] = None # type: ignore
            new_row = [cell for cell in new_row if cell is not None]
            new_row += [None] * (self.size - len(new_row))
            if new_row != original_row:
                self.board[r] = new_row
                moved = True
        return moved
    
    def move_right(self):
        self.board = [list(reversed(row)) for row in self.board]
        moved = self.move_left()
        self.board = [list(reversed(row)) for row in self.board]
        return moved
    
    def move_up(self):
        self.board = [list(row) for row in zip(*self.board)]
        moved = self.move_left()
        self.board = [list(row) for row in zip(*self.board)]
        return moved
    
    def move_down(self):
        self.board = [list(row) for row in zip(*self.board)]
        moved = self.move_right()
        self.board = [list(row) for row in zip(*self.board)]
        return moved

    def add_random_tile(self, value=None):
        empty_cells = [(r, c) for r in range(self.size) for c in range(self.size) if self.board[r][c] is None]
        if not empty_cells:
            print("[DEBUG] No empty cells available to add a tile.")
            return
        r, c = random.choice(empty_cells)
        tile_value = value if value is not None else random.choice([2, 4])
        self.board[r][c] = tile_value # type: ignore
        print(f"[DEBUG] Added tile {tile_value} at position ({r}, {c})")
    
    def check_status(self):
        for row in self.board:
            if None in row:
                return "ONGOING"
        for r in range(self.size):
            for c in range(self.size - 1):
                if self.board[r][c] == self.board[r][c + 1]:
                    return "ONGOING"
        for c in range(self.size):
            for r in range(self.size - 1):
                if self.board[r][c] == self.board[r + 1][c]:
                    return "ONGOING"
        return "GAME OVER"

def main():
    # test game
    game = Game2048()
    
    controls = {
        'w': 'up',
        'a': 'left',
        's': 'down',
        'd': 'right'
    }

    while True:
        status = game.check_status()
        if status == "GAME OVER":
            print("--- GAME OVER ---")
            print(f"Final Score: {game.score}")
            break

        print(f"Current Score: {game.score}")
        game.print_board()

        user_input = input("Enter move: ").lower()

        if user_input == 'q':
            break

        if user_input in controls:
            direction = controls[user_input]
            move_method = getattr(game, f'move_{direction}')
            moved = move_method()
            if moved:
                game.add_random_tile()
            else:
                print("Move not possible. Try a different direction.")
        else:
            print("Invalid input. Use 'w', 'a', 's', 'd' to move or 'q' to quit.")

if __name__ == "__main__":
    main()
    