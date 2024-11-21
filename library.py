import sqlite3
import tkinter as tk
from tkinter import messagebox

# Connect to SQLite database
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Create a Books table without Genre and Price columns
cursor.execute('''
CREATE TABLE IF NOT EXISTS Books (
    BookID INTEGER PRIMARY KEY AUTOINCREMENT,
    Title TEXT NOT NULL,
    Author TEXT NOT NULL,
    PublishedYear INTEGER,
    Status TEXT DEFAULT 'Available'
)
''')

# Check if the Status column exists, and add it if it doesn't
cursor.execute("PRAGMA table_info(Books)")
columns = [column[1] for column in cursor.fetchall()]
if 'Status' not in columns:
    cursor.execute("ALTER TABLE Books ADD COLUMN Status TEXT DEFAULT 'Available'")

# Commit the changes and close the connection
conn.commit()
conn.close()

# Create the main window
root = tk.Tk()
root.title("Library Management System")
root.configure(bg='#8B4513')  # Darker shade of brown background
root.geometry("800x600")  # Make the application window larger

# Configure grid to expand with window size
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=3)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(6, weight=1)

# Add widgets for input fields and buttons
tk.Label(root, text="Title", bg='#8B4513', fg='white').grid(row=0, column=0, sticky='w', padx=10, pady=5)
title_entry = tk.Entry(root, bg='#D2B48C')
title_entry.grid(row=0, column=1, padx=10, pady=5, sticky='ew')

tk.Label(root, text="Author", bg='#8B4513', fg='white').grid(row=1, column=0, sticky='w', padx=10, pady=5)
author_entry = tk.Entry(root, bg='#D2B48C')
author_entry.grid(row=1, column=1, padx=10, pady=5, sticky='ew')

tk.Label(root, text="Year", bg='#8B4513', fg='white').grid(row=2, column=0, sticky='w', padx=10, pady=5)
year_entry = tk.Entry(root, bg='#D2B48C')
year_entry.grid(row=2, column=1, padx=10, pady=5, sticky='ew')

# Add search field and button below the Year input field
tk.Label(root, text="Search", bg='#8B4513', fg='white').grid(row=3, column=0, sticky='w', padx=10, pady=5)
search_entry = tk.Entry(root, bg='#D2B48C')
search_entry.grid(row=3, column=1, padx=10, pady=0, sticky='ew')

def search_book():
    query = search_entry.get()
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Books WHERE Title LIKE ? OR Author LIKE ? OR PublishedYear LIKE ?", ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
        results = cursor.fetchall()
    listbox.delete(0, tk.END)
    for row in results:
        listbox.insert(tk.END, row)

tk.Button(root, text="Search", command=search_book, bg='#8B4513', fg='white').grid(row=3, column=2, padx=10, pady=10, sticky='w')

# Listbox to display books
listbox = tk.Listbox(root, bg='#D2B48C')
listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky='ew')

def display_books():
    listbox.delete(0, tk.END)
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Books")
        books = cursor.fetchall()
        for book in books:
            listbox.insert(tk.END, book)

def add_book():
    title = title_entry.get()
    author = author_entry.get()
    year = year_entry.get()
    if not (title and author and year.isdigit()):
        messagebox.showerror("Error", "All fields must be filled out")
        return
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Books (Title, Author, PublishedYear) VALUES (?, ?, ?)",
                       (title, author, int(year)))
        conn.commit()
        messagebox.showinfo("Success", "Book added successfully!")
        title_entry.delete(0, tk.END)
        author_entry.delete(0, tk.END)
        year_entry.delete(0, tk.END)
        display_books()

tk.Button(root, text="Add Book", command=add_book, bg='#8B4513', fg='white').grid(row=5, column=0, padx=10, pady=5, sticky='ew')

def check_out():
    selected_book = listbox.get(tk.ACTIVE)
    if selected_book:
        book_id = selected_book[0]
        with sqlite3.connect("library.db") as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE Books SET Status = 'Borrowed' WHERE BookID = ?", (book_id,))
            conn.commit()
        display_books()

def check_in():
    selected_book = listbox.get(tk.ACTIVE)
    if selected_book:
        book_id = selected_book[0]
        with sqlite3.connect("library.db") as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE Books SET Status = 'Available' WHERE BookID = ?", (book_id,))
            conn.commit()
        display_books()

def update_book():
    selected_book = listbox.get(tk.ACTIVE)
    if selected_book:
        book_id = selected_book[0]
        title = title_entry.get()
        author = author_entry.get()
        year = year_entry.get()
        if not (title and author and year.isdigit()):
            messagebox.showerror("Error", "All fields must be filled out")
            return
        with sqlite3.connect("library.db") as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE Books SET Title = ?, Author = ?, PublishedYear = ? WHERE BookID = ?",
                           (title, author, int(year), book_id))
            conn.commit()
        display_books()

def remove_book():
    selected_book = listbox.get(tk.ACTIVE)
    if selected_book:
        book_id = selected_book[0]
        with sqlite3.connect("library.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Books WHERE BookID = ?", (book_id,))
            conn.commit()
        display_books()

# Align buttons in the same row
button_frame = tk.Frame(root, bg='#8B4513')
button_frame.grid(row=5, column=1, padx=10, pady=5, sticky='ew')
tk.Button(button_frame, text="Update Book", command=update_book, bg='#8B4513', fg='white').grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Remove Book", command=remove_book, bg='#8B4513', fg='white').grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Check Out", command=check_out, bg='#8B4513', fg='white').grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="Check In", command=check_in, bg='#8B4513', fg='white').grid(row=0, column=3, padx=5)

# Display books initially
display_books()

# Run the main event loop
root.mainloop()