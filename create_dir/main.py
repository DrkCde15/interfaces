import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, filedialog

def criar_pastas_com_datas():
    base_dir = entry_dir.get().strip()
    data_inicial = entry_inicio.get().strip()
    data_final = entry_fim.get().strip()

    if not base_dir:
        messagebox.showerror("Erro", "Selecione o diretório base.")
        return

    if not os.path.exists(base_dir):
        messagebox.showerror("Erro", "Diretório não encontrado.")
        return

    try:
        inicio = datetime.strptime(data_inicial, "%Y%m")
        fim = datetime.strptime(data_final, "%Y%m")
    except ValueError:
        messagebox.showerror("Erro", "Formato inválido. Use o formato YYYYMM (ex: 202210).")
        return

    if inicio > fim:
        messagebox.showerror("Erro", "A data inicial não pode ser maior que a final.")
        return

    data_atual = inicio
    criadas = 0
    while data_atual <= fim:
        nome_pasta = data_atual.strftime("%Y%m")
        caminho_pasta = os.path.join(base_dir, nome_pasta)
        os.makedirs(caminho_pasta, exist_ok=True)
        criadas += 1

        # avança 1 mês
        if data_atual.month == 12:
            data_atual = datetime(data_atual.year + 1, 1, 1)
        else:
            data_atual = datetime(data_atual.year, data_atual.month + 1, 1)

    messagebox.showinfo("Concluído", f"{criadas} pastas criadas com sucesso!")

def selecionar_diretorio():
    caminho = filedialog.askdirectory()
    if caminho:
        entry_dir.delete(0, tk.END)
        entry_dir.insert(0, caminho)

# ----- INTERFACE -----
root = tk.Tk()
root.title("Criador de Pastas por Data")
root.geometry("400x250")
root.resizable(False, False)

# Diretório base
tk.Label(root, text="Diretório base:").pack(anchor="w", padx=10, pady=(10,0))
frame_dir = tk.Frame(root)
frame_dir.pack(fill="x", padx=10)
entry_dir = tk.Entry(frame_dir)
entry_dir.pack(side="left", fill="x", expand=True)
tk.Button(frame_dir, text="Selecionar", command=selecionar_diretorio).pack(side="left", padx=5)

# Data inicial
tk.Label(root, text="Data inicial (YYYYMM):").pack(anchor="w", padx=10, pady=(10,0))
entry_inicio = tk.Entry(root)
entry_inicio.pack(fill="x", padx=10)

# Data final
tk.Label(root, text="Data final (YYYYMM):").pack(anchor="w", padx=10, pady=(10,0))
entry_fim = tk.Entry(root)
entry_fim.pack(fill="x", padx=10)

# Botão principal
tk.Button(root, text="Criar Pastas", command=criar_pastas_com_datas, bg="#4CAF50", fg="white").pack(pady=20)

root.mainloop()
