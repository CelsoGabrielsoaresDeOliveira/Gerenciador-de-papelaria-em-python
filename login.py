import sqlite3

from tkinter import messagebox

def realizar_login(email, senha):
    try:
        
        conn = sqlite3.connect("papelaria.db")
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM funcionarios WHERE email = ? AND senha = ?", (email, senha))
        resultado = cursor.fetchone()
        conn.close()

        return resultado is not None
    except Exception as e:
        messagebox.showerror("Erro", f"Erro de conexão: {e}")
        return False

