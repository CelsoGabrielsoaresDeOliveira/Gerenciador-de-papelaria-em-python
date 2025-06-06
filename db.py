import sqlite3
from tkinter import messagebox

def conectar():
    return sqlite3.connect("papelaria.db")

def criar_tabela_funcionarios():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS funcionarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao criar tabela: {e}")

def criar_tabela_mercadoria():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Mercadoria (
                ID INTEGER PRIMARY KEY,
                Nome TEXT NOT NULL,
                Tipo TEXT NOT NULL,
                Preco REAL NOT NULL,
                Qtde_Estoque INTEGER NOT NULL
            )
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao criar tabela Mercadoria: {e}")
