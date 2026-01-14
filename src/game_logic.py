import random

class Game2048():
    def __init__(self, size=4):
        self.size = size
        self.board = [[None for _ in range(size)] for _ in range(size)]
        self.score = 0

        self.add_initial_tiles()
    
    def print_board(self):
        for row in self.board:
            print(' '.join(str(cell) if cell is not None else '.' for cell in row))
        print()

    def add_initial_tiles(self):
        count = random.randint(2, 16)  # random number of '2's at random cells
        for _ in range(count):
            self.add_random_tile(value=2)

    def move_left(self, event=None):
        moved = False
        for r in range(self.size):
            original_row = self.board[r][:]
            # Compress: remove None values
            new_row = [cell for cell in original_row if cell is not None]
            
            # Merge: combine adjacent equal tiles (only once per tile)
            merged_row = []
            skip_next = False
            for i in range(len(new_row)):
                if skip_next:
                    skip_next = False
                    continue
                    
                # Check if we can merge with next tile
                if i + 1 < len(new_row) and new_row[i] == new_row[i + 1]:
                    merged_value = new_row[i] * 2
                    merged_row.append(merged_value)
                    self.score += merged_value
                    skip_next = True  # Skip the next tile as it was merged
                else:
                    merged_row.append(new_row[i])
            
            # Pad with None to maintain size
            merged_row += [None] * (self.size - len(merged_row))
            
            if merged_row != original_row:
                self.board[r] = merged_row
                moved = True
                
        return moved
    
    def move_right(self, event=None):
        # Reverse, move left, reverse back
        self.board = [list(reversed(row)) for row in self.board]
        moved = self.move_left()
        self.board = [list(reversed(row)) for row in self.board]
        return moved
    
    def move_up(self, event=None):
        # Transpose, move left, transpose back
        self.board = [list(row) for row in zip(*self.board)]
        moved = self.move_left()
        self.board = [list(row) for row in zip(*self.board)]
        return moved
    
    def move_down(self, event=None):
        # Transpose, move right, transpose back
        self.board = [list(row) for row in zip(*self.board)]
        moved = self.move_right()
        self.board = [list(row) for row in zip(*self.board)]
        return moved

    def add_random_tile(self, value=None):
        empty_cells = [(r, c) for r in range(self.size) for c in range(self.size) if self.board[r][c] is None]
        if not empty_cells:
            return
        r, c = random.choice(empty_cells)
        tile_value = value if value is not None else random.choice([2, 4])
        self.board[r][c] = tile_value
    
    def check_status(self):
        # First, check for a winning tile anywhere on the board
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 2048:
                    return "WIN"

        has_empty = False
        # Check for empty cells and possible merges (right and down)
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] is None:
                    has_empty = True
                # check right neighbor
                if c + 1 < self.size and self.board[r][c] is not None and self.board[r][c] == self.board[r][c + 1]:
                    return "ONGOING"
                # check down neighbor
                if r + 1 < self.size and self.board[r][c] is not None and self.board[r][c] == self.board[r + 1][c]:
                    return "ONGOING"

        if has_empty:
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
        elif status == "WIN":
            print("--- YOU WIN! ---")
            print(f"Score: {game.score}")
            cont = input("Continue playing? (y/n): ").lower()
            if cont != 'y':
                break

        print(f"Current Score: {game.score}")
        game.print_board()

        user_input = input("Enter move (w/a/s/d) or 'q' to quit: ").lower()

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