import tkinter as tk
from tkinter import messagebox
import sys
from pathlib import Path
from datetime import datetime

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from Models.Usuarios import Usuario
from Services.AutenticateService import AuthService

class MainView(tk.Tk):
    def __init__(self, user: Usuario):
        super().__init__()
        self.user = user
        self._setup_window()
        self._setup_ui()

    def _setup_window(self):
        nome = self.user.nome or self.user.email.split('@')[0]
        self.title(f"Mod2Importador - {nome}")
        self.geometry("800x600")
        self.configure(bg="#0f172a")
        self._center_window()
        self.resizable(False, False)

    def _center_window(self):
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        x = (sw - 800) // 2
        y = (sh - 600) // 2
        self.geometry(f"800x600+{x}+{y}")

    def _setup_ui(self):
        self._create_header()
        self._create_main_container()

    def _create_header(self):
        frame = tk.Frame(self, bg="#1e293b", height=60)
        frame.pack(fill="x", side="top")
        frame.pack_propagate(False)

        container = tk.Frame(frame, bg="#1e293b")
        container.pack(fill="both", expand=True, padx=20)

        nome = self.user.nome or self.user.email.split('@')[0]
        saudacao = self._get_saudacao()
        label = tk.Label(container, text=f"{saudacao}, {nome}!", font=("Segoe UI", 14, "bold"), bg="#1e293b", fg="white")
        label.pack(side="left")

        btn = tk.Button(container, text="Sair", command=self._handle_logout, bg="#dc2626", fg="white",
                        font=("Segoe UI", 10, "bold"), bd=0, padx=15, pady=5, relief="flat", cursor="hand2")
        btn.pack(side="right")
        btn.bind("<Enter>", lambda e: btn.config(bg="#b91c1c"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#dc2626"))

    def _create_main_container(self):
        self.container = tk.Frame(self, bg="white")
        self.container.place(relx=0.5, rely=0.52, anchor="center", width=680, height=460)

        tk.Label(self.container, text="Sistema de Importação", font=("Segoe UI", 20, "bold"), bg="white", fg="#0f172a").pack(pady=(40, 5))
        tk.Label(self.container, text="Selecione uma opção para continuar", font=("Segoe UI", 11), bg="white", fg="#64748b").pack(pady=(0, 30))

        self._create_function_cards()

    def _create_function_cards(self):
        frame = tk.Frame(self.container, bg="white")
        frame.pack(expand=True, fill="both", padx=50, pady=10)

        self._create_card(frame, "📊", "Nova Importação", "Importar dados usando layouts configurados", "#3b82f6", self._handle_nova_importacao)
        self._create_card(frame, "📋", "Visualizar Logs", "Consultar histórico de importações", "#10b981", self._handle_visualizar_logs)
        self._create_card(frame, "⚙️", "Novo Layout", "Criar ou editar layouts de importação", "#8b5cf6", self._handle_novo_layout)

    def _create_card(self, parent, icon, title, desc, color, command):
        card = tk.Frame(parent, bg="white", relief="solid", bd=1, highlightthickness=0)
        card.pack(fill="x", pady=8, padx=30)

        btn = tk.Frame(card, bg="white", cursor="hand2")
        btn.pack(fill="both", expand=True)
        btn.bind("<Button-1>", lambda e: command())

        content = tk.Frame(btn, bg="white")
        content.pack(fill="x", padx=25)

        left = tk.Frame(content, bg="white")
        left.pack(side="left", fill="y")

        icon_frame = tk.Frame(left, bg=color, width=45, height=45)
        icon_frame.pack(side="left", padx=(0, 15))
        icon_frame.pack_propagate(False)
        tk.Label(icon_frame, text=icon, bg=color, fg="white", font=("Segoe UI", 20)).place(relx=0.5, rely=0.5, anchor="center")

        text = tk.Frame(left, bg="white")
        text.pack(side="left", fill="y", pady=6)
        tk.Label(text, text=title, font=("Segoe UI", 13, "bold"), bg="white", fg="#0f172a").pack(anchor="w")
        tk.Label(text, text=desc, font=("Segoe UI", 10), bg="white", fg="#64748b").pack(anchor="w", pady=(1, 0))

        tk.Label(content, text="→", font=("Segoe UI", 14, "bold"), bg="white", fg="#94a3b8").pack(side="right", padx=15)

        self._setup_card_hover(card, btn, content, left, text)

    def _setup_card_hover(self, card, btn, content, left, text):
        def on_enter(_):
            card.config(relief="solid", bd=2, highlightbackground="#cbd5e1")
            for w in [btn, content, left, text]:
                w.config(bg="#f1f5f9")
        def on_leave(_):
            card.config(relief="solid", bd=1)
            for w in [btn, content, left, text]:
                w.config(bg="white")
        for w in [card, btn]:
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)

    def _get_saudacao(self):
        hora = datetime.now().hour
        return "Bom dia" if 6 <= hora < 12 else "Boa tarde" if hora < 18 else "Boa noite"

    def _handle_nova_importacao(self):
        messagebox.showinfo("Nova Importação", "Funcionalidade em desenvolvimento")

    def _handle_visualizar_logs(self):
        messagebox.showinfo("Visualizar Logs", "Funcionalidade em desenvolvimento")

    def _handle_novo_layout(self):
        messagebox.showinfo("Novo Layout", "Funcionalidade em desenvolvimento")

    def _handle_logout(self):
        if messagebox.askyesno("Logout", "Deseja realmente sair?"):
            AuthService.clear_remember_user()
            self.destroy()
            from Views.LoginView import LoginView
            LoginView().mainloop()


