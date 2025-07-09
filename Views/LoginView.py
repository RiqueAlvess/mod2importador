import tkinter as tk
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from Services.AutenticateService import AuthService

class LoginView(tk.Tk):
    def __init__(self):
        super().__init__()
        self._setup_window()
        self._setup_ui()
        self._set_initial_focus()

    def _setup_window(self):
        self.title("Mod2Importador")
        self.geometry("420x520")
        self.configure(bg="#0f172a")
        self._center_window()
        self.resizable(False, False)

    def _center_window(self):
        self.update_idletasks()
        screen_w, screen_h = self.winfo_screenwidth(), self.winfo_screenheight()
        x = (screen_w - 420) // 2
        y = (screen_h - 520) // 2
        self.geometry(f"420x520+{x}+{y}")

    def _set_initial_focus(self):
        self.after(100, lambda: self.email_entry.focus_set())

    def _setup_ui(self):
        self._create_main_container()
        self._create_form()

    def _create_main_container(self):
        self.container = tk.Frame(self, bg="white", bd=0, relief="flat")
        self.container.place(relx=0.5, rely=0.5, anchor="center", width=340, height=420)

        tk.Label(
            self.container, text="Bem-vindo de volta",
            font=("Segoe UI", 16, "bold"), bg="white", fg="#0f172a"
        ).pack(pady=(30, 5))

        tk.Label(
            self.container, text="Acesse sua conta para continuar",
            font=("Segoe UI", 10), bg="white", fg="#4b5563"
        ).pack(pady=(0, 25))

    def _create_form(self):
        self.email_entry = self._create_entry("E-mail")
        self.password_entry = self._create_entry("Senha", is_password=True)

        self._create_remember_checkbox()

        login_btn = tk.Button(
            self.container, text="Entrar", bg="#0f172a", fg="white",
            font=("Segoe UI", 11, "bold"), bd=0, height=2,
            relief="flat", command=self._handle_login
        )
        login_btn.pack(pady=(10, 10), fill="x", padx=25)

        self.message_label = tk.Label(
            self.container, text="", font=("Segoe UI", 9), bg="white"
        )
        self.message_label.pack()

        self._load_remembered_user()

    def _create_entry(self, placeholder, is_password=False):
        frame = tk.Frame(self.container, bg="white")
        frame.pack(fill="x", padx=25, pady=(5, 10))

        entry = tk.Entry(
            frame, font=("Segoe UI", 10), bd=1, relief="solid",
            highlightthickness=0, fg="#9ca3af"
        )
        entry.insert(0, placeholder)
        entry.pack(fill="x", ipady=10)

        entry.bind("<FocusIn>", lambda e: self._on_entry_focus_in(entry, placeholder, is_password))
        entry.bind("<FocusOut>", lambda e: self._on_entry_focus_out(entry, placeholder, is_password))
        entry.bind("<Button-1>", lambda e: self._on_entry_click(entry, placeholder, is_password))

        if is_password:
            entry.bind("<Return>", lambda e: self._handle_login())
        else:
            entry.bind("<Return>", lambda e: self.password_entry.focus_set())

        return entry

    def _create_remember_checkbox(self):
        remember_frame = tk.Frame(self.container, bg="white")
        remember_frame.pack(fill="x", pady=(5, 10), padx=25)

        self.remember_var = tk.BooleanVar()
        tk.Checkbutton(
            remember_frame, text="Lembrar-me", variable=self.remember_var,
            bg="white", fg="#374151", font=("Segoe UI", 9),
            activebackground="white", borderwidth=0
        ).pack(side="left")

    def _on_entry_focus_in(self, entry, placeholder, is_password):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="black")
            if is_password:
                entry.config(show="*")

    def _on_entry_focus_out(self, entry, placeholder, is_password):
        if not entry.get().strip():
            entry.insert(0, placeholder)
            entry.config(fg="#9ca3af")
            if is_password:
                entry.config(show="")

    def _on_entry_click(self, entry, placeholder, is_password):
        entry.focus_set()
        if entry.get() == placeholder:
            self._on_entry_focus_in(entry, placeholder, is_password)

    def _get_entry_values(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if email == "E-mail":
            email = ""
        if password == "Senha":
            password = ""
            
        return email.strip(), password.strip()

    def _show_message(self, message, is_error=True):
        color = "#dc2626" if is_error else "#16a34a"
        self.message_label.config(text=message, fg=color)

    def _load_remembered_user(self):
        remembered_email = AuthService._get_remembered_user()
        if remembered_email:
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, remembered_email)
            self.email_entry.config(fg="black")
            self.remember_var.set(True)
            self.password_entry.focus_set()

    def _handle_login(self):
        email, password = self._get_entry_values()

        if not email or not password:
            self._show_message("Preencha todos os campos", is_error=True)
            return

        try:
            result = AuthService.autenticar(email, password, self.remember_var.get())
            
            if result.success:
                self._show_message("Login realizado com sucesso!", is_error=False)
                self.after(1500, lambda: self._on_login_success(result.user))
            else:
                self._show_message(result.message, is_error=True)
                
        except Exception as e:
            self._show_message("Erro interno. Tente novamente.", is_error=True)

    def _on_login_success(self, user):
            self.destroy()
            from Views.MainView import MainView
            main_view = MainView(user)
            main_view.mainloop()

if __name__ == "__main__":
    app = LoginView()
    app.mainloop()