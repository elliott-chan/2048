from tkinter import Tk
from gui import App

def main():
    root = Tk()
    root.title("2048")
    root.geometry("900x640")
    root.minsize(800, 560)
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()