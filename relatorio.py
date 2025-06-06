
import sqlite3
import tkinter as tk
from tkinter import ttk

def conectar():
    return sqlite3.connect("papelaria.db")

def criar_tabela_relatorio():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Relatorio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            acao TEXT NOT NULL,
            detalhes TEXT,
            data_hora TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def registrar_acao(acao, detalhes):
    from datetime import datetime
    criar_tabela_relatorio()
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Relatorio (acao, detalhes, data_hora)
        VALUES (?, ?, ?)
    """, (acao, detalhes, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def exibir_relatorio():
    criar_tabela_relatorio()

    janela = janela = tk.Tk()

    janela.title("Relatório de Ações")
    janela.geometry("800x400")
    janela.configure(bg="#f0f0f0")

    colunas = ("id", "acao", "detalhes", "data_hora")
    lista = ttk.Treeview(janela, columns=colunas, show="headings")
    lista.pack(expand=True, fill="both", padx=10, pady=10)

    for col in colunas:
        lista.heading(col, text=col.capitalize())
        lista.column(col, anchor="center")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Relatorio ORDER BY id DESC")
    for row in cursor.fetchall():
        lista.insert("", tk.END, values=row)
    conn.close()
