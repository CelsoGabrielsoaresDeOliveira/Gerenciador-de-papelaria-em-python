import tkinter as tk
from tkinter import messagebox
from login import realizar_login
from register import abrir_tela_registro
from reset_password import abrir_tela_redefinir
from gerenciamento import abrir_tela_gerenciamento
from db import criar_tabela_funcionarios, criar_tabela_mercadoria  # Importa a função de criação da tabela


# Chame as funções para criar as tabelas ao iniciar o aplicativo
criar_tabela_funcionarios()
criar_tabela_mercadoria()

def fazer_login():
    email = entry_email.get()
    senha = entry_senha.get()
    if realizar_login(email, senha):
        messagebox.showinfo("Login", "Login realizado com sucesso!")
        abrir_tela_gerenciamento()
        root.destroy()
    else:
        messagebox.showerror("Erro", "Email ou senha incorretos.")

root = tk.Tk()
root.title("Papelaria Papel & Arte")
root.configure(bg="#FFCE9D")
root.geometry("550x280")

tk.Label(root, text="Email:", bg="#FFCE9D", fg="#003366", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
entry_email = tk.Entry(root, font=("Arial", 12), bg="#ffffff", width=30)
entry_email.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Senha:", bg="#FFCE9D", fg="#003366", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
entry_senha = tk.Entry(root, show="*", font=("Arial", 12), bg="#ffffff", width=30)
entry_senha.grid(row=1, column=1, padx=10, pady=5)

btn_login = tk.Button(root, text="Login", command=fazer_login, bg="#0059b3", fg="white", font=("Arial", 11), width=20)
btn_login.grid(row=2, column=1, columnspan=2, pady=10)

btn_registro = tk.Button(root, text="Registrar-se", command=abrir_tela_registro, bg="#ffffff", fg="#0059b3", font=("Arial", 10))
btn_registro.grid(row=4, column=1, pady=5)

btn_esqueceu = tk.Button(root, text="Esqueceu a senha?", command=abrir_tela_redefinir, bg="#ffffff", fg="#0059b3", font=("Arial", 10))
btn_esqueceu.grid(row=3, column=1, pady=5)

root.mainloop()
