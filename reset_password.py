import tkinter as tk
from tkinter import messagebox
import sqlite3

def redefinir_senha(email, nova_senha):
    try:
        conn = sqlite3.connect("papelaria.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE funcionarios SET senha = ? WHERE email = ?", (nova_senha, email))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao redefinir: {e}")
        return False

def abrir_tela_redefinir():
    janela = tk.Toplevel()
    janela.title("Redefinir Senha")
    janela.configure(bg="#FFCE9D")  
    janela.geometry("450x280")

    
    tk.Label(janela, text="Email:", bg="#FFCE9D", fg="#003366", font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_email = tk.Entry(janela, bg="#ffffff", font=("Arial", 11), width=30)
    entry_email.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(janela, text="Nova Senha:", bg="#FFCE9D", fg="#003366", font=("Arial", 11)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
    entry_nova_senha = tk.Entry(janela, show="*", bg="#ffffff", font=("Arial", 11), width=30)
    entry_nova_senha.grid(row=1, column=1, padx=10, pady=10)

    
    def redefinir():
        email = entry_email.get()
        nova_senha = entry_nova_senha.get()
        if redefinir_senha(email, nova_senha):
            messagebox.showinfo("Sucesso", "Senha redefinida com sucesso!")
            janela.destroy()

    
    tk.Button(janela, text="Redefinir", command=redefinir, 
              bg="#0059b3", fg="white", font=("Arial", 11), width=20).grid(
        row=2, column=1, columnspan=2, pady=10
    )