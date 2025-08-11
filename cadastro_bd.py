import customtkinter as ctk
import sqlite3
from tkinter import messagebox
import os
import hashlib

# === CONFIGURAÇÕES DA JANELA ===
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# === BANCO DE DADOS ===
def init_db():
    os.makedirs("./data_base", exist_ok=True)
    conn = sqlite3.connect("./data_base/usuarios.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

# === FUNÇÕES DE SEGURANÇA ===
def hash_password(password):
    """Criptografa a senha usando SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_password(password):
    """Valida se a senha atende aos critérios mínimos"""
    if len(password) < 6:
        return False, "A senha deve ter pelo menos 6 caracteres"
    if not any(c.isdigit() for c in password):
        return False, "A senha deve conter pelo menos um número"
    return True, "Senha válida"

def validate_username(username):
    """Valida se o username atende aos critérios"""
    if len(username) < 3:
        return False, "O username deve ter pelo menos 3 caracteres"
    if not username.isalnum():
        return False, "O username deve conter apenas letras e números"
    return True, "Username válido"

# === FUNÇÕES PRINCIPAIS ===
def cadastrar():
    nome = entry_nome.get().strip()
    username = entry_username_cad.get().strip()
    senha = entry_senha_cad.get().strip()
    confirmar_senha = entry_confirmar_senha.get().strip()

    # Validações
    if not nome or not username or not senha or not confirmar_senha:
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return

    if len(nome) < 2:
        messagebox.showerror("Erro", "O nome deve ter pelo menos 2 caracteres!")
        return

    # Validar username
    valid_user, msg_user = validate_username(username)
    if not valid_user:
        messagebox.showerror("Erro", msg_user)
        return

    # Validar senha
    valid_pass, msg_pass = validate_password(senha)
    if not valid_pass:
        messagebox.showerror("Erro", msg_pass)
        return

    if senha != confirmar_senha:
        messagebox.showerror("Erro", "As senhas não coincidem!")
        return

    # Criptografar senha
    senha_hash = hash_password(senha)

    conn = sqlite3.connect("./data_base/usuarios.db")
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (nome, username, senha) VALUES (?, ?, ?)", 
                   (nome, username.lower(), senha_hash))
        conn.commit()
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        limpar_campos_cadastro()
        frame_cadastro.pack_forget()
        frame_login.pack(pady=20)
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "Username já existe! Escolha outro.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao cadastrar: {str(e)}")
    finally:
        conn.close()

def login():
    username = entry_username_log.get().strip()
    senha = entry_senha_log.get().strip()

    if not username or not senha:
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return

    senha_hash = hash_password(senha)

    conn = sqlite3.connect("./data_base/usuarios.db")
    cur = conn.cursor()
    try:
        cur.execute("SELECT nome FROM users WHERE username = ? AND senha = ?", 
                   (username.lower(), senha_hash))
        user = cur.fetchone()
        
        if user:
            messagebox.showinfo("Bem-vindo", f"Login realizado com sucesso!\nOlá, {user[0]}!")
            limpar_campos_login()
            abrir_dashboard(user[0])
        else:
            messagebox.showerror("Erro", "Username ou senha incorretos!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao fazer login: {str(e)}")
    finally:
        conn.close()

def abrir_dashboard(nome_usuario):
    """Abre uma tela de dashboard após login bem-sucedido"""
    frame_login.pack_forget()
    frame_dashboard.pack(pady=20, fill="both", expand=True)
    
    # Atualizar label com nome do usuário
    label_usuario_dashboard.configure(text=f"Bem-vindo, {nome_usuario}!")

def logout():
    """Faz logout e volta para a tela de login"""
    frame_dashboard.pack_forget()
    frame_login.pack(pady=20)
    limpar_campos_login()

# === FUNÇÕES DE NAVEGAÇÃO ===
def abrir_cadastro():
    frame_login.pack_forget()
    frame_cadastro.pack(pady=20)

def abrir_login():
    frame_cadastro.pack_forget()
    frame_dashboard.pack_forget()
    frame_login.pack(pady=20)

def limpar_campos_login():
    entry_username_log.delete(0, 'end')
    entry_senha_log.delete(0, 'end')

def limpar_campos_cadastro():
    entry_nome.delete(0, 'end')
    entry_username_cad.delete(0, 'end')
    entry_senha_cad.delete(0, 'end')
    entry_confirmar_senha.delete(0, 'end')

# === JANELA PRINCIPAL ===
root = ctk.CTk()
root.title("Sistema de Login Seguro")
root.geometry("500x600")
root.resizable(True, True)

# Inicializar banco de dados
init_db()

# === FRAME LOGIN ===
frame_login = ctk.CTkFrame(root)
frame_login.pack(pady=20)

ctk.CTkLabel(frame_login, text="🔐 LOGIN", font=("Arial", 24, "bold")).pack(pady=(20, 10))
ctk.CTkLabel(frame_login, text="Faça login em sua conta", font=("Arial", 12)).pack(pady=(0, 20))

entry_username_log = ctk.CTkEntry(frame_login, placeholder_text="Username", width=300, height=35)
entry_username_log.pack(pady=8)

entry_senha_log = ctk.CTkEntry(frame_login, placeholder_text="Senha", show="*", width=300, height=35)
entry_senha_log.pack(pady=8)

btn_login = ctk.CTkButton(frame_login, text="Entrar", command=login, width=300, height=35)
btn_login.pack(pady=(15, 8))

ctk.CTkLabel(frame_login, text="Não tem uma conta?", font=("Arial", 11)).pack(pady=(10, 5))
btn_abrir_cadastro = ctk.CTkButton(frame_login, text="Criar Conta", command=abrir_cadastro, 
                                  fg_color="transparent", hover_color=("gray70", "gray30"))
btn_abrir_cadastro.pack(pady=(0, 20))

# === FRAME CADASTRO ===
frame_cadastro = ctk.CTkFrame(root)

ctk.CTkLabel(frame_cadastro, text="📝 CADASTRO", font=("Arial", 24, "bold")).pack(pady=(20, 10))
ctk.CTkLabel(frame_cadastro, text="Crie sua conta", font=("Arial", 12)).pack(pady=(0, 20))

entry_nome = ctk.CTkEntry(frame_cadastro, placeholder_text="Nome completo", width=300, height=35)
entry_nome.pack(pady=8)

entry_username_cad = ctk.CTkEntry(frame_cadastro, placeholder_text="Username (mín. 3 caracteres)", width=300, height=35)
entry_username_cad.pack(pady=8)

entry_senha_cad = ctk.CTkEntry(frame_cadastro, placeholder_text="Senha (mín. 6 caracteres + número)", 
                              show="*", width=300, height=35)
entry_senha_cad.pack(pady=8)

entry_confirmar_senha = ctk.CTkEntry(frame_cadastro, placeholder_text="Confirmar senha", 
                                    show="*", width=300, height=35)
entry_confirmar_senha.pack(pady=8)

btn_cadastrar = ctk.CTkButton(frame_cadastro, text="Registrar", command=cadastrar, width=300, height=35)
btn_cadastrar.pack(pady=(15, 8))

btn_abrir_login = ctk.CTkButton(frame_cadastro, text="Já tenho uma conta", command=abrir_login,
                               fg_color="transparent", hover_color=("gray70", "gray30"))
btn_abrir_login.pack(pady=(10, 20))

# === FRAME DASHBOARD ===
frame_dashboard = ctk.CTkFrame(root)

ctk.CTkLabel(frame_dashboard, text="🎯 DASHBOARD", font=("Arial", 24, "bold")).pack(pady=(20, 10))

label_usuario_dashboard = ctk.CTkLabel(frame_dashboard, text="", font=("Arial", 16))
label_usuario_dashboard.pack(pady=10)

ctk.CTkLabel(frame_dashboard, text="Login realizado com sucesso!", 
            font=("Arial", 12), text_color="green").pack(pady=10)

# Botões do dashboard
frame_botoes_dash = ctk.CTkFrame(frame_dashboard, fg_color="transparent")
frame_botoes_dash.pack(pady=20)

btn_perfil = ctk.CTkButton(frame_botoes_dash, text="👤 Meu Perfil", width=200)
btn_perfil.pack(pady=5)

btn_configuracoes = ctk.CTkButton(frame_botoes_dash, text="⚙️ Configurações", width=200)
btn_configuracoes.pack(pady=5)

btn_logout = ctk.CTkButton(frame_botoes_dash, text="🚪 Sair", command=logout, 
                          fg_color="red", hover_color="darkred", width=200)
btn_logout.pack(pady=15)

# === BIND ENTER KEY ===
def on_enter_login(event):
    login()

def on_enter_cadastro(event):
    cadastrar()

root.bind('<Return>', on_enter_login)
entry_senha_log.bind('<Return>', on_enter_login)
entry_confirmar_senha.bind('<Return>', on_enter_cadastro)

# === INICIAR APLICAÇÃO ===
if __name__ == "__main__":
    root.mainloop()