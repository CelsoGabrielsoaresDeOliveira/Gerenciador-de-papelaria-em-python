import tkinter as tk
from tkinter import messagebox
import sqlite3

def registrar_funcionario(email, senha):
    try:
        conn = sqlite3.connect("papelaria.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO funcionarios (email, senha) VALUES (?, ?)", (email, senha))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao registrar: {e}")
        return False

def abrir_tela_registro():
    janela = tk.Toplevel()
    janela.title("Registrar Funcionário")
    janela.configure(bg="#FFCE9D")  
    janela.geometry("450x280")

    
    tk.Label(janela, text="Email:", bg="#FFCE9D", fg="#003366", font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_email = tk.Entry(janela, bg="#ffffff", font=("Arial", 11), width=30)
    entry_email.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(janela, text="Senha:", bg="#FFCE9D", fg="#003366", font=("Arial", 11)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
    entry_senha = tk.Entry(janela, show="*", bg="#ffffff", font=("Arial", 11), width=30)
    entry_senha.grid(row=1, column=1, padx=10, pady=10)

    
    def registrar():
        email = entry_email.get()
        senha = entry_senha.get()

        if not email or not senha:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
            return 

        if registrar_funcionario(email, senha):
            messagebox.showinfo("Sucesso", "Funcionário registrado com sucesso!")
            janela.destroy()

        else:
            messagebox.showerror("Erro", "Erro ao registrar funcionário.")


    tk.Button(janela, text="Registrar", command=registrar,
              bg="#0059b3", fg="white", font=("Arial", 11), width=20).grid(
        row=2, column=1, columnspan=2, pady=10
    )