import tkinter as tk
from tkinter import ttk, messagebox
from game_logic import Game2048

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

def center_window(root: tk.Tk, w=900, h=640):
    root.geometry(f"{w}x{h}")
    root.minsize(820, 560)
    root.update_idletasks()
    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    x = int((sw - w) / 2)
    y = int((sh - h) / 2.5)
    root.geometry(f"+{x}+{y}")

class GameFrame(ttk.Frame):
    def __init__(self, root: tk.Tk):
        super().__init__(root)
        # Center the board in the parent window
        self.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
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
        return True
    
    def game_over(self, status):
        self.overlay = tk.Frame(self, bg="#686262", width=400, height=400)
        self.overlay.place(relx=0.5, rely=0.5, anchor='center', width=420, height=420)
        msg_text = "WINNER!" if status == "WIN" else "GAME OVER!"
        msg_color = COLORS["success"] if status == "WIN" else COLORS["danger"]
        msg = tk.Label(self.overlay, text=msg_text, font=("Arial", 32, "bold"), bg="#686262", fg=msg_color)
        msg.pack(expand=True)
        btn = tk.Button(self.overlay, text="Restart", font=("Arial", 16, "bold"), bg=COLORS["accent"], fg=COLORS["accent_fg"], command=self.reset_game)
        btn.pack(pady=20)

    def update_visuals(self):
        status = self.game_logic.check_status()
        if status in ["GAME OVER", "WIN"]:
            self.game_over(status)
        elif status == "WIN":
            self.game_over("WIN")
        
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
# App
class App:
    def __init__(self, master):
        self.master = master
        apply_style(master)
        center_window(master)
        master.title("2048")

        self.game_frame = GameFrame(master)

        self.master.bind("<Key>", self.on_key)
    def on_key(self, event):
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

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()