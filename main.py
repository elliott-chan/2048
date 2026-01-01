from tkinter import Tk
from gui import DCMApp

def main():
    root = Tk()
    root.title("2048")
    root.geometry("900x640")
    root.minsize(800, 560)
    app = DCMApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()