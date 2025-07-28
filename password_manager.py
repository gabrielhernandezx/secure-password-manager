#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox, ttk
import random
import string
import sqlite3
from cryptography.fernet import Fernet

# Generar una clave para cifrar/descifrar contraseñas (solo válida mientras la app esté abierta)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Conectar a la base de datos SQLite
conn = sqlite3.connect('passwords.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS passwords
             (id INTEGER PRIMARY KEY, description TEXT, password TEXT)''')
conn.commit()

def generate_password(length=12, use_uppercase=True, use_digits=True, use_punctuation=True):
    characters = string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_punctuation:
        characters += string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def save_password(description, password):
    encrypted_password = cipher_suite.encrypt(password.encode())
    c.execute("INSERT INTO passwords (description, password) VALUES (?, ?)", (description, encrypted_password))
    conn.commit()

def get_passwords():
    c.execute("SELECT description, password FROM passwords")
    passwords = c.fetchall()
    return [(desc, cipher_suite.decrypt(pw).decode()) for desc, pw in passwords]

def on_generate():
    try:
        length = int(entry_length.get())
        if length < 1:
            raise ValueError("La longitud debe ser positiva.")
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return

    password = generate_password(length, var_uppercase.get(), var_digits.get(), var_punctuation.get())
    entry_password.delete(0, tk.END)
    entry_password.insert(0, password)

def on_save():
    description = entry_description.get()
    password = entry_password.get()
    if description and password:
        save_password(description, password)
        messagebox.showinfo("Guardado", "Contraseña guardada exitosamente")
        entry_description.delete(0, tk.END)
        entry_password.delete(0, tk.END)
    else:
        messagebox.showwarning("Advertencia", "Por favor, complete todos los campos")

def on_show():
    passwords = get_passwords()
    passwords_str = "\n".join([f"{desc}: {pw}" for desc, pw in passwords])
    messagebox.showinfo("Contraseñas Guardadas", passwords_str)

# GUI con tkinter
root = tk.Tk()
root.title("Gestor de Contraseñas Seguras")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#f0f0f0", foreground="#000")
style.configure("TLabel", padding=6, background="#f0f0f0", foreground="#000")
style.configure("TCheckbutton", background="#f0f0f0", foreground="#000")
root.configure(bg="#f0f0f0")

var_uppercase = tk.BooleanVar(value=True)
var_digits = tk.BooleanVar(value=True)
var_punctuation = tk.BooleanVar(value=True)

ttk.Label(frame, text="Descripción").grid(row=0, column=0, sticky=tk.W)
entry_description = ttk.Entry(frame, width=30)
entry_description.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Longitud").grid(row=1, column=0, sticky=tk.W)
entry_length = ttk.Entry(frame, width=10)
entry_length.grid(row=1, column=1, sticky=(tk.W, tk.E))
entry_length.insert(0, "12")

ttk.Label(frame, text="Contraseña").grid(row=2, column=0, sticky=tk.W)
entry_password = ttk.Entry(frame, width=30)
entry_password.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E))

ttk.Checkbutton(frame, text="Incluir Mayúsculas", variable=var_uppercase).grid(row=3, column=0, columnspan=2, sticky=tk.W)
ttk.Checkbutton(frame, text="Incluir Dígitos", variable=var_digits).grid(row=4, column=0, columnspan=2, sticky=tk.W)
ttk.Checkbutton(frame, text="Incluir Puntuación", variable=var_punctuation).grid(row=5, column=0, columnspan=2, sticky=tk.W)

ttk.Button(frame, text="Generar", command=on_generate).grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E))
ttk.Button(frame, text="Guardar", command=on_save).grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E))
ttk.Button(frame, text="Mostrar Contraseñas", command=on_show).grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E))

for widget in frame.winfo_children():
    widget.grid_configure(padx=5, pady=5)

root.mainloop()
conn.close()
