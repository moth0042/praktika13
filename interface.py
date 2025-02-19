import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


root = tk.Tk()

root.geometry("800x600")
root.resizable(False, False)

frame1 = ttk.Frame(root)
frame1.pack(fill=tk.X, padx=10, pady=10)

ttk.Label(frame1, text="Выберите таблицу:").pack(side=tk.LEFT, padx=5, pady=5)

selector = ttk.Combobox(frame1, state="readonly")
selector.pack(side=tk.LEFT, padx=5, pady=5)

frame2 = ttk.Frame(root)
frame2.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

scroll = ttk.Scrollbar(frame2, orient=tk.VERTICAL)
scroll.pack(side=tk.RIGHT, fill=tk.Y)
tree = ttk.Treeview(frame2, show="headings", yscroll=scroll.set)
tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

butframe = ttk.Frame(root)
butframe.pack(fill=tk.X, padx=10, pady=10)














root.mainloop()
