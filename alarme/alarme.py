import customtkinter as ctk
import datetime
import time
import threading
from plyer import notification
from playsound import playsound

# Configurações de aparência
ctk.set_appearance_mode("System") 
ctk.set_default_color_theme("blue")

class DespertadorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Python Alarm Pro")
        self.geometry("400x400") # Aumentei um pouco a altura para caber o novo campo
        self.hora_definida = ""
        self.mensagem_personalizada = ""

        # UI Elements
        self.label_titulo = ctk.CTkLabel(self, text="Despertador", font=("Roboto", 24, "bold"))
        self.label_titulo.pack(pady=15)

        # Campo para a Hora
        self.label_hora = ctk.CTkLabel(self, text="Horário (HH:MM):")
        self.label_hora.pack()
        self.entry_hora = ctk.CTkEntry(self, placeholder_text="07:30", width=120)
        self.entry_hora.pack(pady=5)

        # Campo para a Mensagem
        self.label_msg = ctk.CTkLabel(self, text="Mensagem do Alarme:")
        self.label_msg.pack()
        self.entry_mensagem = ctk.CTkEntry(self, placeholder_text="Ex: Reunião importante", width=250)
        self.entry_mensagem.pack(pady=5)

        self.btn_definir = ctk.CTkButton(self, text="Definir Alarme", command=self.iniciar_thread)
        self.btn_definir.pack(pady=15)

        self.label_status = ctk.CTkLabel(self, text="Status: Aguardando...", text_color="gray")
        self.label_status.pack(pady=5)

        self.btn_soneca = ctk.CTkButton(self, text="Soneca (5 min)", fg_color="orange", hover_color="#D18700", 
                                        command=self.ativar_soneca, state="disabled")
        self.btn_soneca.pack(pady=10)

    def iniciar_thread(self):
        self.hora_definida = self.entry_hora.get()
        self.mensagem_personalizada = self.entry_mensagem.get() or "Hora de acordar!" # Mensagem padrão se estiver vazio
        
        self.label_status.configure(text=f"Alarme para: {self.hora_definida}", text_color="cyan")
        
        # Inicia a verificação em background
        t = threading.Thread(target=self.verificar_alarme, daemon=True)
        t.start()

    def verificar_alarme(self):
        while True:
            agora = datetime.datetime.now().strftime("%H:%M")
            if agora == self.hora_definida:
                # Usa a função after do CTk para interagir com a UI a partir de outra thread com segurança
                self.after(0, self.disparar_alarme)
                break
            time.sleep(10)

    def disparar_alarme(self):
        # Atualiza a interface
        self.label_status.configure(text=f"🔔 {self.mensagem_personalizada}", text_color="red")
        self.btn_soneca.configure(state="normal")
        
        # Notificação do Sistema com a mensagem personalizada
        notification.notify(
            title="Alarme Python",
            message=self.mensagem_personalizada,
            app_name="Despertador",
            timeout=15
        )
        
        # Toca o áudio
        threading.Thread(target=self.tocar_som, daemon=True).start()

    def tocar_som(self):
        try:
            playsound("alarme.mp3")
        except:
            print("Erro ao reproduzir 'alarme.mp3'")

    def ativar_soneca(self):
        nova_hora = (datetime.datetime.now() + datetime.timedelta(minutes=5)).strftime("%H:%M")
        self.hora_definida = nova_hora
        self.entry_hora.delete(0, 'end')
        self.entry_hora.insert(0, nova_hora)
        self.label_status.configure(text=f"Soneca para: {nova_hora}", text_color="orange")
        self.btn_soneca.configure(state="disabled")
        
        t = threading.Thread(target=self.verificar_alarme, daemon=True)
        t.start()

if __name__ == "__main__":
    app = DespertadorApp()
    app.mainloop()