import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from relatorio import registrar_acao, exibir_relatorio  

def conectar():
    return sqlite3.connect("papelaria.db")

def adicionar_item():
    codigo = entry_codigo.get()
    nome = entry_nome.get()
    preco = entry_preco.get()
    quantidade = entry_quantidade.get()
    categoria = entry_categoria.get()

    try:
        codigo = int(codigo)
        preco = float(preco)
        quantidade = int(quantidade)

        if not (nome and categoria):
            raise ValueError

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Mercadoria WHERE ID = ?", (codigo,))
        if cursor.fetchone():
            messagebox.showerror("Erro", "Código já existe. Use o botão Atualizar para alterar o item.")
        else:
            cursor.execute("""
                INSERT INTO Mercadoria (ID, Nome, Tipo, Preco, Qtde_Estoque)
                VALUES (?, ?, ?, ?, ?)
            """, (codigo, nome, categoria, preco, quantidade))
            conn.commit()
            registrar_acao("Adicionar", f"Código: {codigo}, Nome: {nome}, Qtde: {quantidade}, Categoria: {categoria}")
            atualizar_lista()
            limpar_campos()
            desabilitar_botoes()
        conn.close()

    except ValueError:
        messagebox.showerror("Erro", "Preencha todos os campos corretamente com valores válidos.")

def remover_item():
    codigo = entry_codigo.get()
    if not codigo:
        messagebox.showwarning("Aviso", "Selecione um produto para remover.")
        return

    resposta = messagebox.askyesno("Confirmar exclusão", "Deseja excluir esse produto?")
    if resposta:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Mercadoria WHERE ID = ?", (codigo,))
        if cursor.rowcount == 0:
            messagebox.showerror("Erro", "Código do produto não encontrado.")
        else:
            conn.commit()
            registrar_acao("Remover", f"Código: {codigo}")
            atualizar_lista()
            limpar_campos()
            desabilitar_botoes()
        conn.close()

def atualizar_item():
    codigo = entry_codigo.get()
    nome = entry_nome.get()
    preco = entry_preco.get()
    quantidade = entry_quantidade.get()
    categoria = entry_categoria.get()

    try:
        preco = float(preco)
        quantidade = int(quantidade)

        if not codigo or not nome or not categoria:
            messagebox.showerror("Erro", "Preencha todos os campos corretamente.")
            return

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Mercadoria WHERE ID = ?", (codigo,))
        if cursor.fetchone():
            cursor.execute("""
                UPDATE Mercadoria
                SET Nome = ?, Tipo = ?, Preco = ?, Qtde_Estoque = ?
                WHERE ID = ?
            """, (nome, categoria, preco, quantidade, codigo))
            conn.commit()
            registrar_acao("Atualizar", f"Código: {codigo}, Nome: {nome}, Qtde: {quantidade}, Categoria: {categoria}")
            atualizar_lista()
            limpar_campos()
            desabilitar_botoes()
        else:
            messagebox.showerror("Erro", "Código do produto não encontrado para atualização.")
        conn.close()
    except ValueError:
        messagebox.showerror("Erro", "Preencha todos os campos corretamente com valores válidos.")

def limpar_campos():
    entry_codigo.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    entry_preco.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)
    entry_categoria.delete(0, tk.END)

def desabilitar_botoes():
    btn_remover.config(state=tk.DISABLED)
    btn_atualizar.config(state=tk.DISABLED)

def habilitar_botoes():
    btn_remover.config(state=tk.NORMAL)
    btn_atualizar.config(state=tk.NORMAL)

def on_selecionar_item(event):
    selecionado = lista.focus()
    if not selecionado:
        return
    valores = lista.item(selecionado, 'values')
    if valores:
        entry_codigo.delete(0, tk.END)
        entry_codigo.insert(0, valores[0])
        entry_nome.delete(0, tk.END)
        entry_nome.insert(0, valores[1])
        preco_str = valores[2].replace("R$ ", "").replace(",", ".")
        entry_preco.delete(0, tk.END)
        entry_preco.insert(0, preco_str)
        entry_quantidade.delete(0, tk.END)
        entry_quantidade.insert(0, valores[3])
        entry_categoria.delete(0, tk.END)
        entry_categoria.insert(0, valores[4])
        habilitar_botoes()

def atualizar_lista():
    for item in lista.get_children():
        lista.delete(item)

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT ID, Nome, Tipo, Preco, Qtde_Estoque FROM Mercadoria")
    for row in cursor.fetchall():
        preco_formatado = f"R$ {row[3]:.2f}".replace(".", ",")
        lista.insert("", tk.END, values=(row[0], row[1], preco_formatado, row[4], row[2]))
    conn.close()

def abrir_tela_gerenciamento():
    global entry_codigo, entry_nome, entry_preco, entry_quantidade, entry_categoria, lista, btn_remover, btn_atualizar

    janela = tk.Tk()
    janela.title("Gerenciamento de Produtos")
    janela.configure(bg="#FFCE9D")
    janela.geometry("750x600")

    fonte_label = ("Arial", 12)

    tk.Label(janela, text="Código:", bg="#FFCE9D", fg="#003366", font=fonte_label).pack(pady=3)
    entry_codigo = tk.Entry(janela, font=("Arial", 12), bg="#ffffff", width=30)
    entry_codigo.pack()

    tk.Label(janela, text="Nome:", bg="#FFCE9D", fg="#003366", font=fonte_label).pack(pady=3)
    entry_nome = tk.Entry(janela, font=("Arial", 12), bg="#ffffff", width=30)
    entry_nome.pack()

    tk.Label(janela, text="Preço:", bg="#FFCE9D", fg="#003366", font=fonte_label).pack(pady=3)
    entry_preco = tk.Entry(janela, font=("Arial", 12), bg="#ffffff", width=30)
    entry_preco.pack()

    tk.Label(janela, text="Quantidade:", bg="#FFCE9D", fg="#003366", font=fonte_label).pack(pady=3)
    entry_quantidade = tk.Entry(janela, font=("Arial", 12), bg="#ffffff", width=30)
    entry_quantidade.pack()

    tk.Label(janela, text="Categoria:", bg="#FFCE9D", fg="#003366", font=fonte_label).pack(pady=3)
    entry_categoria = tk.Entry(janela, font=("Arial", 12), bg="#ffffff", width=30)
    entry_categoria.pack()

    btn_adicionar = tk.Button(janela, text="Adicionar", command=adicionar_item, bg="#0059b3", fg="white", font=("Arial", 11), width=20)
    btn_adicionar.pack(pady=5)

    btn_remover = tk.Button(janela, text="Remover", command=remover_item, bg="#b30000", fg="white", font=("Arial", 11), width=20, state=tk.DISABLED)
    btn_remover.pack(pady=5)

    btn_atualizar = tk.Button(janela, text="Atualizar", command=atualizar_item, bg="#ffaa00", fg="white", font=("Arial", 11), width=20, state=tk.DISABLED)
    btn_atualizar.pack(pady=5)

    btn_relatorio = tk.Button(janela, text="Relatório", command=exibir_relatorio, bg="#28a745", fg="white", font=("Arial", 11), width=20)
    btn_relatorio.pack(pady=5)

    colunas = ("codigo", "nome", "preco", "quantidade", "categoria")
    lista = ttk.Treeview(janela, columns=colunas, show="headings", height=10)
    lista.pack(pady=10)

    for col in colunas:
        lista.heading(col, text=col.capitalize())
        lista.column(col, width=130, anchor="center")

    lista.bind("<<TreeviewSelect>>", on_selecionar_item)

    atualizar_lista()

    janela.mainloop()


if __name__ == "__main__":
    abrir_tela_gerenciamento()
