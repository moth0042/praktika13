import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

connection = sqlite3.connect('fairytale.db')
cur = connection.cursor()

res = cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tablesnames = []
for name in res.fetchall():
    if name[0] != 'sqlite_sequence':
        print(name[0])
        tablesnames.append(name)

def exitt():
    confirm = messagebox.askyesno("Подтверждение выхода", "Вы уверены, что хотите выйти из программы?")
    if confirm:
        connection.commit()
        connection.close()
        root.destroy()

def tables():
    try:
        for row in tree.get_children():
            tree.delete(row)
        tree['columns'] = []
        tree.heading("#0", text="", anchor=tk.W)
        name = selector.get()
        cur.execute(f"SELECT * FROM {name}")
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]        
        tree['columns'] = columns
        for col in columns:
            tree.heading(col, text=col, anchor=tk.W)
            tree.column(col, anchor=tk.W, minwidth=100, width=100)
        for i in rows:
            tree.insert('', tk.END, values=i)
    except:
        messagebox.showerror("Ошибка", "Выберите таблицу")

def add():
    table_name = selector.get()
    columns = [desc[0] for desc in cur.description]
    def saveme():
        values = [entry.get() for entry in entries]
        try:
            cur.execute(
                f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['?'] * len(values))})",
                values
            )
            connection.commit()
            add_window.destroy()
            tables()
        except sqlite3.Error as err:
            messagebox.showerror("Ошибка", f"Не удалось добавить запись:\n{err}")
    add_window = tk.Toplevel(root)
    add_window.resizable(False, False)
    add_window.iconphoto(False, icon)
    style = ttk.Style(add_window)    
    add_window.title("Добавить запись")
    entries = []
    for i, col in enumerate(columns):
        ttk.Label(add_window, text=col).grid(row=i, column=0, padx=5, pady=5)
        entry = ttk.Entry(add_window)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries.append(entry)
    ttk.Button(add_window, text="Сохранить", command=saveme).grid(row=len(columns), column=0, columnspan=2, pady=10)

def delete():
    table_name = selector.get()
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Предупреждение", "Выберите запись для удаления.")
        return
    record = tree.item(selected_item)['values']
    columns = [desc[0] for desc in cur.description]
    clause = " AND ".join([f"{col}=?" for col in columns])
    confirm = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить эту запись?")
    if not confirm:
        return
    try:
        cur.execute(f"DELETE FROM {table_name} WHERE {clause}", record)
        connection.commit()
        tables()
        messagebox.showinfo("Успех", "Запись успешно удалена.")
    except sqlite3.Error as err:
        messagebox.showerror("Ошибка", f"Не удалось удалить запись:\n{err}")

def edit():
    table_name = selector.get()
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Предупреждение", "Выберите запись для редактирования.")
        return
    record = tree.item(selected_item)['values']
    columns = [desc[0] for desc in cur.description]
    def saveme():
        new_values = [entry.get() for entry in entries]
        set_clause = ", ".join([f"{col}=?" for col in columns])
        clause = " AND ".join([f"{col}=?" for col in columns])
        try:
            cur.execute(
                f"UPDATE {table_name} SET {set_clause} WHERE {clause}",
                new_values + record
            )
            connection.commit()
            edit_window.destroy()
            tables()
        except sqlite3.Error as err:
            messagebox.showerror("Ошибка", f"Не удалось обновить запись:\n{err}")
    edit_window = tk.Toplevel(root)
    edit_window.resizable(False, False)
    edit_window.iconphoto(False, icon)   
    edit_window.title("Редактировать запись")
    entries = []
    for i, (col, value) in enumerate(zip(columns, record)):
        ttk.Label(edit_window, text=col).grid(row=i, column=0, padx=5, pady=5)
        entry = ttk.Entry(edit_window)
        entry.insert(0, value)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries.append(entry)
    ttk.Button(edit_window, text="Сохранить", command=saveme).grid(row=len(columns), column=0, columnspan=2, pady=10)

queries = []
file = open('запросы.txt', 'r').read().splitlines()
for i in file:
    if file.index(i) == 0 or file.index(i) % 2 == 0:
        queries.append(i)
def query():
    def selectq():
        try:
            q = selector2.get()
            select = file[file.index(q)+1]
            for row in tree.get_children():
                tree.delete(row)
            tree['columns'] = []
            tree.heading("#0", text="", anchor=tk.W)
            cur.execute(select)
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]        
            tree['columns'] = columns
            for col in columns:
                tree.heading(col, text=col, anchor=tk.W)
                tree.column(col, anchor=tk.W, minwidth=100, width=100)
            for i in rows:
                tree.insert('', tk.END, values=i)
            query_window.destroy()
        except:
            messagebox.showerror("Ошибка", "Выберите запрос")
            return
    query_window = tk.Toplevel(root)
    query_window.resizable(False, False)
    query_window.iconphoto(False, icon)   
    query_window.title("Выбор запроса")
    selector2 = ttk.Combobox(query_window, values=queries, state="readonly", width=100)
    selector2.pack(side=tk.TOP, padx=5, pady=5)
    selector2.current(0)
    ttk.Button(query_window, text="Вывести", command=selectq).pack(side=tk.BOTTOM, padx=5, pady=10)    

root = tk.Tk()

root.geometry("800x600")
root.resizable(False, False)
root.title("База данных")
icon = tk.PhotoImage(file='icon.png')
root.iconphoto(False, icon)

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
scroll2 = ttk.Scrollbar(frame2, orient=tk.HORIZONTAL)
scroll2.pack(side=tk.BOTTOM, fill=tk.X)
tree = ttk.Treeview(frame2, show="headings", yscrollcommand=scroll.set, xscrollcommand=scroll2.set)
tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
scroll.config(command=tree.yview)
scroll2.config(command=tree.xview)

butframe = ttk.Frame(root)
butframe.pack(fill=tk.X, padx=10, pady=10)

ttk.Button(butframe, text="Добавить", command=add).pack(side=tk.LEFT, padx=5)
ttk.Button(butframe, text="Удалить", command=delete).pack(side=tk.LEFT, padx=5)
ttk.Button(butframe, text="Редактировать", command=edit).pack(side=tk.LEFT, padx=5)
ttk.Button(butframe, text="Запросы", command=query).pack(side=tk.LEFT, padx=5)
ttk.Button(frame1, width=3, text="⟲", command=tables).pack(side=tk.LEFT, padx=5, pady=5)
ttk.Button(butframe, text="Выход", command=exitt).pack(side=tk.RIGHT, padx=5)








root.protocol('WM_DELETE_WINDOW', exitt)
root.mainloop()
