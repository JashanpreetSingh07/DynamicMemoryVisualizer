# File: app.py

from tkinter import Tk
from frontend.main_ui import DynamicMemoryVisualizerApp

def main():
    root = Tk()
    app = DynamicMemoryVisualizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
