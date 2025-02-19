import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

connection = sqlite3.connect('my_database.db')
cur = connection.cursor()

res = cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tablesnames = []
for name in res.fetchall():
    print(name[0])
    tablesnames.append(name)

def tables():
    name = selector.get()
    cur.execute(f"SELECT * FROM {name}")
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]        
    tree['columns'] = columns
    for col in columns:
        tree.heading(col, text=col, anchor=tk.W)
        tree.column(col, anchor=tk.W, width=100)
    for i in rows:
        tree.insert('', tk.END, values=i)

root = tk.Tk()

root.geometry("800x600")
root.resizable(False, False)

frame1 = ttk.Frame(root)
frame1.pack(fill=tk.X, padx=10, pady=10)

ttk.Label(frame1, text="Выберите таблицу:").pack(side=tk.LEFT, padx=5, pady=5)

selector = ttk.Combobox(frame1, values=tablesnames, state="readonly")
selector.pack(side=tk.LEFT, padx=5, pady=5)
selector.bind("<<ComboboxSelected>>", lambda e: tables())

frame2 = ttk.Frame(root)
frame2.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

scroll = ttk.Scrollbar(frame2, orient=tk.VERTICAL)
scroll.pack(side=tk.RIGHT, fill=tk.Y)
tree = ttk.Treeview(frame2, show="headings", yscroll=scroll.set)
tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

butframe = ttk.Frame(root)
butframe.pack(fill=tk.X, padx=10, pady=10)













connection.commit()
#connection.close()
root.mainloop()
