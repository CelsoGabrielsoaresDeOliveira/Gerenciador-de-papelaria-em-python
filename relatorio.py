import sqlite3
import tkinter as tk
from tkinter import ttk
from datetime import datetime

def conectar():
    """Estabelece a conexão com o banco de dados."""
    return sqlite3.connect("papelaria.db")

def atualizar_ou_criar_tabela_relatorio():
    """
    Cria a tabela Relatorio se ela não existir e garante que a coluna 'email' exista.
    """
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

   
    cursor.execute("PRAGMA table_info(Relatorio)")
    colunas_existentes = [coluna[1] for coluna in cursor.fetchall()]

    if 'email' not in colunas_existentes:
        cursor.execute("ALTER TABLE Relatorio ADD COLUMN email TEXT")

    conn.commit()
    conn.close()


def registrar_acao(acao, detalhes, email=None):
    """
    Registra uma nova ação no banco de dados, incluindo o e-mail do usuário.
    """
    atualizar_ou_criar_tabela_relatorio()
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Relatorio (acao, detalhes, email, data_hora)
        VALUES (?, ?, ?, ?)
    """, (acao, detalhes, email, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()


def exibir_relatorio():
    """Cria e exibe a janela com o relatório de ações, incluindo o email."""
    atualizar_ou_criar_tabela_relatorio()

    janela = tk.Toplevel()
    janela.title("Relatório de Ações")
    janela.geometry("900x500")
    janela.configure(bg="#f0f0f0")

    # Adiciona a coluna 'email'
    colunas = ("id", "acao", "detalhes", "email", "data_hora")
    lista = ttk.Treeview(janela, columns=colunas, show="headings")
    lista.pack(expand=True, fill="both", padx=10, pady=10)

   
    lista.heading("id", text="ID", anchor="center")
    lista.heading("acao", text="Ação", anchor="center")
    lista.heading("detalhes", text="Detalhes", anchor="center")
    lista.heading("email", text="Usuário (Email)", anchor="center")
    lista.heading("data_hora", text="Data e Hora", anchor="center")


    lista.column("id", width=50, anchor="center")
    lista.column("acao", width=120, anchor="w")
    lista.column("detalhes", width=280, anchor="w")
    lista.column("email", width=180, anchor="w")
    lista.column("data_hora", width=150, anchor="center")

    conn = conectar()
    cursor = conn.cursor()
  
    cursor.execute("SELECT id, acao, detalhes, email, data_hora FROM Relatorio ORDER BY id DESC")
    for row in cursor.fetchall():
   
        valores_tratados = ["" if v is None else v for v in row]
        lista.insert("", tk.END, values=valores_tratados)
    conn.close()

    janela.grab_set() 
