import tkinter as tk
from tkinter import ttk, messagebox
import random

# Themes
"""
STYLES TO BE CHANGED
"""
COLORS = {
    "bg": "#0b1220",
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

# Order that the device returns values in its echo payload
ECHO_PARAM_ORDER = [
    "LRL",
    "URL",
    "Ventricular Amp",
    "Atrial Amp",
    "Ventricular PW",
    "Atrial PW",
    "Ventricular Sens",
    "Atrial Sens",
    "ARP",
    "VRP",
    "MSR",
    "Activity Threshold",
    "Response Factor",
    "Reaction Time",
    "Recovery Time",
]

EGRAM_CLAMP = 0.7
EGRAM_SCROLL_STEP = 3  # how many sample positions to advance per echo for faster scrolling


def apply_style(root: tk.Tk) -> None:
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    COLORS.update(
        {
            "bg": "#0c1220",
            "card": "#161e31",
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

    # Entries
    style.configure(
        "TEntry",
        fieldbackground="#1c2438",
        foreground=COLORS["text"],
        bordercolor="#2a3454",
        relief="flat",
        padding=8,
    )

    # Buttons
    style.configure(
        "Accent.TButton",
        background=COLORS["accent1"],
        foreground="#ffffff",
        borderwidth=0,
        padding=(16, 8),
        font=FONT_MD,
        relief="flat",
    )
    style.map(
        "Accent.TButton",
        background=[("active", COLORS["accent2"]), ("pressed", "#5b21b6")],
    )

    style.configure(
        "TButton",
        background="#1f2937",
        foreground=COLORS["text"],
        borderwidth=0,
        padding=(14, 6),
        font=FONT_MD,
        relief="flat",
    )
    style.map(
        "TButton",
        background=[("active", "#374151"), ("pressed", "#111827")],
    )


def center_window(root: tk.Tk, w=900, h=640):
    root.geometry(f"{w}x{h}")
    root.minsize(820, 560)
    root.update_idletasks()
    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    x = int((sw - w) / 2)
    y = int((sh - h) / 2.5)
    root.geometry(f"+{x}+{y}")

# App
class DCMApp:
    def __init__(self, master):
        self.master = master
        apply_style(master)
        center_window(master)
        master.title("2048")

class Game(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid()
