import tkinter as tk
from tkinter import ttk, messagebox
from game_logic import Game2048
from game_AI import GameAI

# Themes
COLORS = {
    "bg": "#94a3b8",
    "card": "#ffffff",
    "muted": "#94a3b8",
    "text": "#e2e8f0",
    "accent": "#3b82f6",
    "accent_fg": "#0b1220",
    "danger": "#ef4444",
    "success": "#10b981",
}

FONT_FAMILY = ("Poppins", "Segoe UI", "Arial", "Helvetica", "sans-serif")
FONT_LG = (FONT_FAMILY[0], 20, "bold")
FONT_MD = (FONT_FAMILY[0], 12)
FONT_SM = (FONT_FAMILY[0], 10)

TILE_COLORS = {
    2: "#f3f4f6",
    4: "#ede9fe",
    8: "#ddd6fe",
    16: "#c4b5fd",
    32: "#a78bfa",
    64: "#8b5cf6",
    128: "#7c3aed",
    256: "#6d28d9",
    512: "#5b21b6",
    1024: "#4c1d95",
    2048: "#3b82f6",
}

def apply_style(root: tk.Tk) -> None:
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    COLORS.update(
        {
            "bg": "#94a3b8",
            "card": "#ffffff",
            "muted": "#a3b3cc",
            "text": "#e9eef9",
            "accent1": "#00b8d9",
            "accent2": "#7c3aed",
            "success": "#10b981",
            "danger": "#ef4444",
        }
    )

    root.configure(bg=COLORS["bg"])
    style.configure("TFrame", background=COLORS["bg"])
    style.configure("Card.TFrame", background=COLORS["card"])

    # Labels
    style.configure(
        "TLabel", background=COLORS["card"], foreground=COLORS["text"], font=FONT_MD
    )
    style.configure(
        "Muted.TLabel", background=COLORS["card"], foreground=COLORS["muted"], font=FONT_SM
    )
    style.configure(
        "Heading.TLabel",
        background=COLORS["card"],
        foreground=COLORS["accent1"],
        font=FONT_LG,
    )

def center_window(root: tk.Tk, w=580, h=530):
    root.geometry(f"{w}x{h}")
    root.minsize(550, 480)
    root.update_idletasks()
    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    x = int((sw - w) / 2)
    y = int((sh - h) / 2.5)
    root.geometry(f"+{x}+{y}")

class GameFrame(ttk.Frame):
    def __init__(self, root: tk.Tk):
        super().__init__(root)
        self.grid(row=0, column=0, sticky="nw", padx=8, pady=12)
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        self.game_logic = Game2048(size=4)

        self.cell_containers = []
        self.labels = []
        TILE_SIZE = 100
        for r in range(4):
            row_containers = []
            row_labels = []
            for c in range(4):
                cell_container = tk.Frame(self, bg='#bbada0', width=TILE_SIZE, height=TILE_SIZE)
                cell_container.grid(row=r+1, column=c, padx=5, pady=5)
                cell_container.grid_propagate(False)
                cell_container.config(width=TILE_SIZE, height=TILE_SIZE)
                row_containers.append(cell_container)
                label = tk.Label(cell_container, font=("Arial", 20, "bold"), bg='#bbada0', fg='#776e65')
                row_labels.append(label)
            self.cell_containers.append(row_containers)
            self.labels.append(row_labels)

        self.score_label = tk.Label(self, text=f"Score: {self.game_logic.score}", font=("Arial", 24, "bold"), bg=COLORS["bg"], fg=COLORS["text"])
        self.score_label.grid(row=0, column=0, columnspan=4, pady=(0, 10))

        # Prevent grid stretching so tiles remain square
        for i in range(4):
            self.grid_rowconfigure(i, weight=0)
            self.grid_columnconfigure(i, weight=0)

        self.update_visuals()

    def reset_game(self):
        if hasattr(self, 'overlay') and self.overlay:
            self.overlay.destroy()
            self.overlay = None
        self.game_logic = Game2048(size=4)
        self.update_visuals()
        # Notify other UI parts (like the sidebar) that the game has been reset
        try:
            self.event_generate("<<GameReset>>")
        except Exception:
            pass
        return True
    
    def game_over(self, status):
        # Even smaller centered overlay so minimal obstruction to the board
        self.overlay = tk.Frame(self, bg="#686262", width=220, height=110)
        self.overlay.place(relx=0.5, rely=0.5, anchor='center', width=240, height=130)
        msg_text = "WINNER!" if status == "WIN" else "GAME OVER!"
        msg_color = COLORS["success"] if status == "WIN" else COLORS["danger"]
        # Smaller font to match reduced overlay size
        msg = tk.Label(self.overlay, text=msg_text, font=("Arial", 16, "bold"), bg="#686262", fg=msg_color)
        msg.pack(expand=True, padx=6, pady=4)
        btn = tk.Button(self.overlay, text="Restart", font=("Arial", 12, "bold"), bg=COLORS["accent"], fg=COLORS["accent_fg"], command=self.reset_game)
        btn.pack(pady=6)

    def update_visuals(self):
        status = self.game_logic.check_status()
        if status in ["GAME OVER", "WIN"]:
            self.game_over(status)
        
        for r in range(4):
            for c in range(4):
                value = self.game_logic.board[r][c]
                cell_container = self.cell_containers[r][c]
                label = self.labels[r][c]
                cell_container.config(bg='#bbada0')
                
                if value is None:
                    # Hide tile by setting empty text
                    label.config(text='', bg='#bbada0', fg='#bbada0')
                    if label.winfo_ismapped() == 0:
                        label.place(relx=0.5, rely=0.5, anchor='center', width=75, height=75)
                else:
                    # Show a larger number tile centered in the background tile
                    bg_color = TILE_COLORS.get(value, '#3c3a32')
                    fg_color = "#f9f6f2" if value > 4 else "#776e65"
                    label.config(text=str(value), bg=bg_color, fg=fg_color, font=("Arial", 20, "bold"))
                    if label.winfo_ismapped() == 0:
                        label.place(relx=0.5, rely=0.5, anchor='center', width=75, height=75)
        self.update_score()

    def update_score(self):
        self.score_label.config(text=f"Score: {self.game_logic.score}")

class Sidebar(ttk.Frame):
    def __init__(self, parent: tk.Widget, game_frame: GameFrame):
        super().__init__(parent)
        self.game_frame = game_frame
        self.grid(row=0, column=1, sticky="n", padx=(6, 12), pady=(230, 12))

        # Hint button
        hint_btn = tk.Button(self, text="Suggestion", font=(FONT_FAMILY[0], 12, "bold"), bg=COLORS["accent"], fg=COLORS["accent_fg"], command=self.on_hint)
        hint_btn.pack(fill='x', pady=(0, 3))

        # Result label (shows direction)
        self.result_label = tk.Label(self, text="--", font=(FONT_FAMILY[0], 18, "bold"), bg=COLORS["card"], fg=COLORS["accent"])
        self.result_label.pack(anchor='center', pady=8)

    def on_hint(self):
        try:
            board = self.game_frame.game_logic.board
            # Call GameAI to get suggested board and validity
            suggested_board, valid = GameAI(board, 10, 5)

            if not valid:
                self.result_label.config(text="No moves", fg=COLORS["danger"])
                return

            # Determine which direction was moved by comparing original board to suggested board
            direction = self._detect_direction(board, suggested_board)
            self.result_label.config(text=direction.upper(), fg=COLORS["success"])
        except Exception as e:
            messagebox.showerror('Hint Error', f'Failed to get hint: {e}')

    def _detect_direction(self, original, suggested):
        """Detect which direction (up/down/left/right) was applied to the board."""
        # Check if the board changed horizontally (left/right) or vertically (up/down)
        # by comparing positions of tiles
        import copy
        temp = Game2048(size=4)
        temp.board = copy.deepcopy(original)
        
        # Try each direction and see which one matches the suggested board
        directions = [('up', temp.move_up), ('down', temp.move_down), 
                      ('left', temp.move_left), ('right', temp.move_right)]
        
        for direction_name, move_func in directions:
            temp_board = copy.deepcopy(original)
            temp.board = temp_board
            move_func()
            if temp.board == suggested:
                return direction_name
        
        return "?"
# App
class App:
    def __init__(self, master):
        self.master = master
        apply_style(master)
        center_window(master)
        master.title("2048")

        # Main container to hold game board (left) and sidebar (right)
        main_frame = ttk.Frame(master)
        main_frame.grid(row=0, column=0, sticky="nsew")
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        self.game_frame = GameFrame(main_frame)
        self.sidebar = Sidebar(main_frame, self.game_frame)

        # Keep columns compact so sidebar stays close to the board
        main_frame.grid_columnconfigure(0, weight=0)
        main_frame.grid_columnconfigure(1, weight=0)

        # Listen for game reset events so we can clear the hint
        main_frame.bind("<<GameReset>>", lambda e: self._clear_hint())

        self.master.bind("<Key>", self.on_key)

        # helper to clear hint label (used by reset event)
        def _clear_hint(e=None):
            if hasattr(self, 'sidebar') and self.sidebar:
                self.sidebar.result_label.config(text="--", fg=COLORS["accent"])
        self._clear_hint = _clear_hint

    def on_key(self, event):
        # If a game-over/win overlay is present, ignore move keys (allow reset 'r' and quit 'q')
        if hasattr(self.game_frame, 'overlay') and self.game_frame.overlay:
            if event.keysym not in ('r', 'q'):
                return

        key_map = {
            'w': self.game_frame.game_logic.move_up,
            'a': self.game_frame.game_logic.move_left,
            's': self.game_frame.game_logic.move_down,
            'd': self.game_frame.game_logic.move_right,
            'Up': self.game_frame.game_logic.move_up,
            'Left': self.game_frame.game_logic.move_left,
            'Down': self.game_frame.game_logic.move_down,
            'Right': self.game_frame.game_logic.move_right,
            'q': self.master.quit,
            'r': self.game_frame.reset_game
        }

        action = key_map.get(event.keysym)
        if action:
            moved = action()
            if moved:
                self.game_frame.game_logic.add_random_tile()
                self.game_frame.update_visuals()
                # Clear previous hint to avoid confusion after the player moves
                if hasattr(self, 'sidebar') and self.sidebar:
                    self.sidebar.result_label.config(text="--", fg=COLORS["accent"])

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()