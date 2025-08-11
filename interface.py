import customtkinter as ctk

#configurando o tema escuro
ctk.set_appearance_mode("dark")

def validar_login():
    usuario = campo_usuario.get()
    senha = campo_pass.get()

    if usuario == 'iron_man' and senha == 'pitbull_raivoso':
        result_login.configure(text='Login efetuado com sucesso', text_color='green')
    else:
        result_login.configure(text='Login ou senha incorretos', text_color='red')

#tamanho da janela
app = ctk.CTk()
app.title("JARVIS")
app.geometry("350x450")

#criação dos campos
#label
label_usuario = ctk.CTkLabel(app, text='Usuario')
label_usuario.pack(pady=10)

#entry
campo_usuario = ctk.CTkEntry(app,placeholder_text='Digite seu usuario')
campo_usuario.pack(pady=10)

label_pass = ctk.CTkLabel(app, text='Senha')
label_pass.pack(pady=10)

#entry
campo_pass = ctk.CTkEntry(app,placeholder_text='Digite sua senha')
campo_pass.pack(pady=10)

#botao
botao_login = ctk.CTkButton(app, text='Entrar', command=validar_login)
botao_login.pack(pady=10)

#feedback
result_login = ctk.CTkLabel(app, text='')
result_login.pack(pady=10)

#criando as caixas de texto
app.mainloop()