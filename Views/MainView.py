import tkinter as tk
from tkinter import messagebox
import sys
from pathlib import Path
from datetime import datetime

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from Models.Usuarios import Usuario
from Services.AutenticateService import AuthService
from Views.LayoutCreatorView import LayoutCreatorView


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
        tk.Label(
            container,
            text=f"{saudacao}, {nome}!",
            font=("Segoe UI", 14, "bold"),
            bg="#1e293b",
            fg="white"
        ).pack(side="left")

        sair_btn = tk.Button(
            container,
            text="Sair",
            command=self._handle_logout,
            bg="#dc2626",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            padx=15,
            pady=5,
            relief="flat",
            cursor="hand2"
        )
        sair_btn.pack(side="right")
        sair_btn.bind("<Enter>", lambda e: sair_btn.config(bg="#b91c1c"))
        sair_btn.bind("<Leave>", lambda e: sair_btn.config(bg="#dc2626"))

    def _create_main_container(self):
        self.container = tk.Frame(self, bg="white")
        self.container.place(relx=0.5, rely=0.52, anchor="center", width=680, height=460)

        tk.Label(
            self.container,
            text="Sistema de Importação",
            font=("Segoe UI", 20, "bold"),
            bg="white",
            fg="#0f172a"
        ).pack(pady=(20, 5))

        tk.Label(
            self.container,
            text="Selecione uma opção para continuar",
            font=("Segoe UI", 11),
            bg="white",
            fg="#64748b"
        ).pack(pady=(0, 15))

        self._create_function_buttons()

    def _create_function_buttons(self):
        frame = tk.Frame(self.container, bg="white")
        frame.pack(expand=True, fill="both", padx=50, pady=10)
        frame.grid_columnconfigure((0,1,2), weight=1)

        btn_specs = [
            ("Nova Importação", "Importar dados usando layouts", "#3b82f6", self._handle_nova_importacao),
            ("Visualizar Logs", "Consultar histórico de importações", "#10b981", self._handle_visualizar_logs),
            ("Novo Layout", "Criar/editar layouts de importação", "#8b5cf6", self._handle_novo_layout),
        ]

        for idx, (title, desc, color, cmd) in enumerate(btn_specs):
            btn = tk.Button(
                frame,
                text=title,
                command=cmd,
                bg=color,
                fg="white",
                font=("Segoe UI", 12, "bold"),
                bd=0,
                relief="raised",
                cursor="hand2",
                width=18,
                height=2
            )
            btn.grid(row=0, column=idx, padx=10, pady=(0,5))

            lbl = tk.Label(
                frame,
                text=desc,
                font=("Segoe UI", 9),
                bg="white",
                fg="#64748b",
                wraplength=140,
                justify="center"
            )
            lbl.grid(row=1, column=idx, padx=10)

    def _get_saudacao(self):
        hora = datetime.now().hour
        if 6 <= hora < 12:
            return "Bom dia"
        if hora < 18:
            return "Boa tarde"
        return "Boa noite"

    def _handle_nova_importacao(self):
        messagebox.showinfo("Nova Importação", "Funcionalidade em desenvolvimento")

    def _handle_visualizar_logs(self):
        messagebox.showinfo("Visualizar Logs", "Funcionalidade em desenvolvimento")

    def _handle_novo_layout(self):
        layout_window = LayoutCreatorView(self, self.user)
        layout_window.grab_set()

    def _handle_logout(self):
        if messagebox.askyesno("Logout", "Deseja realmente sair?"):
            AuthService.clear_remember_user()
            self.destroy()
            from Views.LoginView import LoginView
            LoginView().mainloop()
