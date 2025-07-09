import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from platform import system

# Tenta importar as dependências do projeto. Falha silenciosamente se não encontrar,
# pois o bloco de teste no final do arquivo fornecerá simulações.
try:
    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    from Utils.ApiStructure import ApiStructure
    from Utils.TransformationRules import TransformationRules, TransformationRule
    from Utils.FieldConfig import FieldType, FieldConfig, CategoryConfig
    from Services.FileService import FileService
    from Services.LayoutService import LayoutService
    from Services.ValidationService import ValidationService
except ImportError:
    print("Aviso: Módulos do projeto não encontrados. O código funcionará, mas apenas o bloco de teste é executável de forma independente.")


# -----------------------------------------------------------------------------
# 1. CLASSE AUXILIAR PARA ROLAGEM
# -----------------------------------------------------------------------------

class ScrollableFrame(tk.Frame):
    """
    Um frame rolável reutilizável que encapsula a lógica do Canvas e Scrollbar.
    A rolagem com o mouse wheel é ativada por padrão para uma melhor experiência.
    """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self, bg=kwargs.get('bg', 'white'), highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.inner_frame = tk.Frame(self.canvas, bg=kwargs.get('bg', 'white'))
        self.canvas_window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.inner_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.bind_all("<MouseWheel>", self._on_mousewheel, add="+")
        self.bind_all("<Button-4>", self._on_mousewheel, add="+")
        self.bind_all("<Button-5>", self._on_mousewheel, add="+")

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        # Garante que a rolagem do mouse funcione em diferentes sistemas operacionais
        if self.canvas.winfo_exists() and self.scrollbar.winfo_exists():
            if system() == 'Linux':
                if event.num == 4: self.canvas.yview_scroll(-1, "units")
                elif event.num == 5: self.canvas.yview_scroll(1, "units")
            else:
                 self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

# -----------------------------------------------------------------------------
# 2. CLASSE PRINCIPAL DA INTERFACE
# -----------------------------------------------------------------------------

class LayoutCreatorView(tk.Toplevel):
    """Interface aprimorada para criação e edição de layouts"""
    
    def __init__(self, parent, user):
        super().__init__(parent)
        self.parent = parent
        self.user = user
        
        self.file_service = FileService()
        self.layout_service = LayoutService()
        self.validation_service = ValidationService()
        
        self.api_structure = ApiStructure.get_structure()
        
        self.current_file_path = None
        self.file_columns = []
        self.field_mappings = {}
        self.transformation_selections = {}
        
        self._setup_window()
        self._setup_ui()
    
    def _setup_window(self):
        self.title("Configurar Layout de Importação")
        self.geometry("1400x900")
        self.configure(bg="#f8fafc")
        self.minsize(1100, 700)
        self._center_window()
        self.transient(self.parent)
        self.grab_set()
    
    def _center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def _setup_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._create_header()
        self._create_main_content()
    
    def _create_header(self):
        header_frame = tk.Frame(self, bg="#1e293b", height=80)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.pack_propagate(False)
        
        container = tk.Frame(header_frame, bg="#1e293b")
        container.pack(fill="both", expand=True, padx=30, pady=20)
        
        tk.Label(container, text="Configurar Layout de Importação", font=("Segoe UI", 18, "bold"), bg="#1e293b", fg="white").pack(side="left")
        self._create_header_buttons(container)
    
    def _create_header_buttons(self, parent):
        btn_frame = tk.Frame(parent, bg="#1e293b")
        btn_frame.pack(side="right")
        btn_style = {"font": ("Segoe UI", 10, "bold"), "fg": "white", "bd": 0, "padx": 20, "pady": 8, "relief": "flat", "cursor": "hand2"}
        
        tk.Button(btn_frame, text="💾 Salvar Layout", command=self._on_save_layout, bg="#16a34a", **btn_style).pack(side="right", padx=(10, 0))
        tk.Button(btn_frame, text="📁 Carregar Layout", command=self._on_load_layout, bg="#3b82f6", **btn_style).pack(side="right", padx=(10, 0))
        tk.Button(btn_frame, text="✕ Fechar", command=self.destroy, bg="#dc2626", **btn_style).pack(side="right")
    
    def _create_main_content(self):
        main_frame = tk.Frame(self, bg="#f8fafc")
        main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1, minsize=400)
        main_frame.grid_columnconfigure(1, weight=3)
        
        left_panel = tk.Frame(main_frame, bg="white", relief="solid", bd=1)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        right_panel = tk.Frame(main_frame, bg="white", relief="solid", bd=1)
        right_panel.grid(row=0, column=1, sticky="nsew")
        
        self._create_config_panel(left_panel)
        self._create_mapping_panel(right_panel)
    
    def _create_config_panel(self, parent):
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        title_frame = tk.Frame(parent, bg="#f1f5f9", height=50)
        title_frame.grid(row=0, column=0, sticky="ew")
        title_frame.pack_propagate(False)
        tk.Label(title_frame, text="⚙️ Configurações", font=("Segoe UI", 14, "bold"), bg="#f1f5f9", fg="#0f172a").pack(pady=10, padx=20, side="left")
        
        scrollable_content = ScrollableFrame(parent, bg="white")
        scrollable_content.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self._create_config_form(scrollable_content.inner_frame)
    
    def _create_config_form(self, parent):
        self._create_text_field(parent, "Nome do Layout:", "layout_name_entry")
        self._create_text_field(parent, "Descrição:", "description_entry")
        self._create_separator(parent)
        self._create_file_section(parent)
        self._create_separator(parent)
        self._create_api_section(parent)
        self._create_separator(parent)
        self._create_columns_preview(parent)
    
    def _create_text_field(self, parent, label_text: str, entry_name: str):
        tk.Label(parent, text=label_text, font=("Segoe UI", 10, "bold"), bg="white", fg="#374151").pack(anchor="w", pady=(10, 5))
        entry = tk.Entry(parent, font=("Segoe UI", 10), bd=1, relief="solid", highlightthickness=1, highlightcolor="#3b82f6", highlightbackground="#cbd5e1")
        entry.pack(fill="x", ipady=8)
        setattr(self, entry_name, entry)

    def _create_separator(self, parent):
        tk.Frame(parent, bg="#e5e7eb", height=1).pack(fill="x", pady=20)
        
    def _create_file_section(self, parent):
        tk.Label(parent, text="Arquivo de Exemplo:", font=("Segoe UI", 10, "bold"), bg="white", fg="#374151").pack(anchor="w", pady=(10, 5))
        
        file_frame = tk.Frame(parent, bg="white")
        file_frame.pack(fill="x", pady=(0, 10))
        
        self.file_path_var = tk.StringVar()
        file_entry = tk.Entry(file_frame, textvariable=self.file_path_var, font=("Segoe UI", 10), bd=1, relief="solid", state="readonly")
        file_entry.pack(side="left", fill="x", expand=True, ipady=8)
        
        browse_btn = tk.Button(file_frame, text="📁 Procurar", command=self._on_browse_file, bg="#6b7280", fg="white", font=("Segoe UI", 10), bd=0, padx=15, pady=8, relief="flat", cursor="hand2")
        browse_btn.pack(side="right", padx=(10, 0))
        
        tk.Label(parent, text="Linha do Cabeçalho:", font=("Segoe UI", 10, "bold"), bg="white", fg="#374151").pack(anchor="w", pady=(10, 5))
        self.header_row_var = tk.StringVar(value="1")
        header_entry = tk.Entry(parent, textvariable=self.header_row_var, font=("Segoe UI", 10), bd=1, relief="solid", width=10)
        header_entry.pack(anchor="w", ipady=8)
        header_entry.bind('<KeyRelease>', self._on_header_row_change)

    def _create_api_section(self, parent):
        tk.Label(parent, text="Configurações da API:", font=("Segoe UI", 10, "bold"), bg="white", fg="#374151").pack(anchor="w", pady=(10, 5))
        api_frame = tk.Frame(parent, bg="#f8fafc", relief="solid", bd=1)
        api_frame.pack(fill="x", pady=(0, 10))
        api_frame.columnconfigure(0, weight=1)

        def create_api_field(row, label, var_name, is_password=False):
            tk.Label(api_frame, text=label, font=("Segoe UI", 9), bg="#f8fafc", fg="#374151").grid(row=row, column=0, sticky="w", padx=15, pady=(10, 2))
            entry = tk.Entry(api_frame, font=("Segoe UI", 10), bd=1, relief="solid", show="*" if is_password else "")
            entry.grid(row=row+1, column=0, sticky="ew", padx=15, pady=(0, 10), ipady=5)
            setattr(self, var_name, entry)
        
        create_api_field(0, "Código da Empresa:", "company_code_entry")
        create_api_field(2, "Usuário da API:", "api_user_entry")
        create_api_field(4, "Senha da API:", "api_password_entry", is_password=True)

    def _create_columns_preview(self, parent):
        tk.Label(parent, text="Colunas Detectadas:", font=("Segoe UI", 10, "bold"), bg="white", fg="#374151").pack(anchor="w", pady=(10, 5))
        
        preview_frame = tk.Frame(parent, bd=1, relief="solid")
        preview_frame.pack(fill="x", expand=True)
        self.columns_text = tk.Text(preview_frame, height=8, font=("Courier New", 9), bg="#f8fafc", state="disabled", bd=0, relief="flat", wrap="none")
        
        v_scroll = ttk.Scrollbar(preview_frame, orient="vertical", command=self.columns_text.yview)
        h_scroll = ttk.Scrollbar(preview_frame, orient="horizontal", command=self.columns_text.xview)
        self.columns_text.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")
        self.columns_text.pack(side="left", fill="both", expand=True)
        self._update_columns_display()
        
    def _create_mapping_panel(self, parent):
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        title_frame = tk.Frame(parent, bg="#f1f5f9", height=50)
        title_frame.grid(row=0, column=0, sticky="ew")
        title_frame.pack_propagate(False)
        tk.Label(title_frame, text="🔗 Mapeamento de Campos", font=("Segoe UI", 14, "bold"), bg="#f1f5f9", fg="#0f172a").pack(pady=10, padx=20, side="left")
        
        self._create_search_bar(title_frame)
        
        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[10, 5])
        self.notebook = ttk.Notebook(parent, style="TNotebook")
        self.notebook.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self._create_category_tabs()

    def _create_search_bar(self, parent):
        search_frame = tk.Frame(parent, bg="#f1f5f9")
        search_frame.pack(side="right", padx=20)
        tk.Label(search_frame, text="🔍", font=("Segoe UI", 12), bg="#f1f5f9", fg="#6b7280").pack(side="left", padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._on_search_change)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=("Segoe UI", 10), bd=1, relief="solid", width=30)
        search_entry.pack(side="left", ipady=5)

    def _create_category_tabs(self):
        sorted_categories = sorted(self.api_structure.items(), key=lambda x: x[1].order)
        
        for category_key, category_config in sorted_categories:
            tab_content_frame = ScrollableFrame(self.notebook, bg="white")
            self.notebook.add(tab_content_frame, text=f"{category_config.icon} {category_config.title}")
            self._create_category_fields(category_key, category_config, tab_content_frame.inner_frame)
    
    def _create_category_fields(self, category_key: str, category_config, parent):
        if category_config.description:
            tk.Label(parent, text=category_config.description, font=("Segoe UI", 10), bg="white", fg="#6b7280", wraplength=700, justify="left").pack(anchor="w", padx=15, pady=(10, 20))
        
        sorted_fields = sorted(category_config.fields.items(), key=lambda x: (not x[1].required, x[1].display_name))
        for field_key, field_config in sorted_fields:
            self._create_field_mapping_widget(parent, category_key, field_key, field_config)
    
    def _create_field_mapping_widget(self, parent, category_key: str, field_key: str, field_config):
        field_path = f"{category_key}.{field_key}"
        field_frame = tk.Frame(parent, bg="white", relief="solid", bd=1)
        field_frame.pack(fill="x", pady=5, padx=10)
        
        header_frame = tk.Frame(field_frame, bg="#f8fafc")
        header_frame.pack(fill="x", ipady=5)
        header_frame.grid_columnconfigure(0, weight=1)

        name_frame = tk.Frame(header_frame, bg="#f8fafc")
        name_frame.grid(row=0, column=0, sticky="w", padx=15)
        
        tk.Label(name_frame, text=field_config.display_name, font=("Segoe UI", 10, "bold"), bg="#f8fafc", fg="#0f172a").pack(side="left")
        if field_config.required:
            tk.Label(name_frame, text="*", font=("Segoe UI", 12, "bold"), bg="#f8fafc", fg="#dc2626").pack(side="left", padx=(2, 0))

        details_frame = tk.Frame(header_frame, bg="#f8fafc")
        details_frame.grid(row=0, column=1, sticky="e", padx=15)
        
        tk.Label(details_frame, text=f"({field_config.field_type})", font=("Segoe UI", 9), bg="#f8fafc", fg="#6b7280").pack(anchor="e")
        if field_config.example:
            tk.Label(details_frame, text=f"Ex: {field_config.example}", font=("Segoe UI", 8), bg="#f8fafc", fg="#9ca3af").pack(anchor="e")

        content_frame = tk.Frame(field_frame, bg="white")
        content_frame.pack(fill="x", padx=15, pady=15)
        
        self._create_column_mapping(content_frame, field_path, field_config)
        
        if field_config.field_type in [FieldType.STRING, FieldType.TEXT]:
            self._create_transformations_section(content_frame, field_path, field_config)
            
        self.field_mappings.setdefault(field_path, {})['widget'] = field_frame

    def _create_column_mapping(self, parent, field_path: str, field_config):
        tk.Label(parent, text="Coluna do arquivo:", font=("Segoe UI", 9, "bold"), bg="white", fg="#374151").pack(anchor="w", pady=(0, 5))
        
        column_var = tk.StringVar(value="Não mapear")
        column_combo = ttk.Combobox(parent, textvariable=column_var, values=["Não mapear"] + self.file_columns, state="readonly", font=("Segoe UI", 10))
        column_combo.pack(anchor="w", fill="x", pady=(0, 10))
        
        if field_config.description:
            tk.Label(parent, text=field_config.description, font=("Segoe UI", 8), bg="white", fg="#6b7280", wraplength=600, justify="left").pack(anchor="w", pady=(0, 5))
            
        self.field_mappings.setdefault(field_path, {}).update({
            'column_var': column_var, 'combo': column_combo, 'field_config': field_config
        })

    def _create_transformations_section(self, parent, field_path: str, field_config):
        applicable_rules = TransformationRules.get_applicable_rules(field_config.field_type)
        if not applicable_rules: return

        tk.Label(parent, text="Transformações:", font=("Segoe UI", 9, "bold"), bg="white", fg="#374151").pack(anchor="w", pady=(10, 5))
        trans_frame = tk.Frame(parent, bg="white")
        trans_frame.pack(fill="x", pady=(0, 5))

        transform_vars = {}
        for rule in applicable_rules:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(trans_frame, text=rule.name, variable=var, bg="white", fg="#374151", font=("Segoe UI", 9), activebackground="white", borderwidth=0)
            cb.pack(anchor="w", padx=(10, 0))
            transform_vars[rule.key] = var
        self.transformation_selections[field_path] = transform_vars

    # --- Event Handlers e Métodos Auxiliares ---
    
    def _on_browse_file(self):
        filetypes = [("Arquivos Excel", "*.xlsx *.xls"), ("Arquivos CSV", "*.csv"), ("Todos", "*.*")]
        file_path = filedialog.askopenfilename(title="Selecionar arquivo de exemplo", filetypes=filetypes)
        if file_path:
            self.current_file_path = Path(file_path)
            self.file_path_var.set(self.current_file_path.name)
            self._load_file_columns()
    
    def _on_header_row_change(self, event=None):
        if self.current_file_path: self._load_file_columns()
    
    def _on_search_change(self, *args):
        search_term = self.search_var.get().lower()
        try:
            current_tab_widget = self.notebook.nametowidget(self.notebook.select())
            parent_frame = current_tab_widget.inner_frame
        except (tk.TclError, KeyError): return

        for field_path, data in self.field_mappings.items():
            field_widget = data.get('widget')
            if field_widget and field_widget.master == parent_frame:
                display_name = data['field_config'].display_name.lower()
                if search_term in display_name:
                    field_widget.pack(fill="x", pady=5, padx=10)
                else:
                    field_widget.pack_forget()

    def _on_save_layout(self):
        layout_data = self._collect_layout_data()
        if not layout_data: return
        is_valid, errors = self.validation_service.validate_layout_config(layout_data)
        if not is_valid:
            messagebox.showerror("Erros de Validação", "Erros encontrados:\n\n" + "\n".join(errors))
            return
        if self.layout_service.create_layout(layout_data):
            messagebox.showinfo("Sucesso", f"Layout '{layout_data['name']}' salvo com sucesso!")
            self.destroy()
        else:
            messagebox.showerror("Erro", "Não foi possível salvar o layout.")
    
    def _on_load_layout(self):
        layouts = self.layout_service.list_layouts()
        if not layouts:
            messagebox.showinfo("Informação", "Nenhum layout salvo foi encontrado.")
            return
        self._show_layout_selection_dialog(layouts)

    def _load_file_columns(self):
        try:
            header_row = int(self.header_row_var.get())
            self.file_columns = self.file_service.get_file_columns(str(self.current_file_path), header_row -1)
            self._update_columns_display()
            self._update_column_combos()
        except ValueError:
            messagebox.showerror("Erro", "A linha do cabeçalho deve ser um número inteiro positivo.")
        except Exception as e:
            messagebox.showerror("Erro ao Ler Arquivo", f"Não foi possível carregar as colunas:\n{e}")
    
    def _update_columns_display(self):
        self.columns_text.config(state="normal")
        self.columns_text.delete(1.0, tk.END)
        if not self.file_columns:
            self.columns_text.insert(tk.END, "Nenhuma coluna detectada ou arquivo não selecionado.")
        else:
            text_content = "\n".join([f"{i+1: >3}. {col}" for i, col in enumerate(self.file_columns)])
            self.columns_text.insert(tk.END, text_content)
        self.columns_text.config(state="disabled")

    def _update_column_combos(self):
        new_values = ["Não mapear"] + self.file_columns
        for data in self.field_mappings.values():
            if (combo := data.get('combo')):
                if (current_value := data['column_var'].get()) not in new_values:
                    data['column_var'].set("Não mapear")
                combo['values'] = new_values
    
    def _collect_layout_data(self) -> Optional[Dict[str, Any]]:
        layout_name = self.layout_name_entry.get().strip()
        if not layout_name:
            messagebox.showerror("Entrada Inválida", "O nome do layout é obrigatório.")
            return None
        
        if self.layout_service.layout_exists(layout_name):
            if not messagebox.askyesno("Confirmar Sobrescrita", f"O layout '{layout_name}' já existe. Deseja sobrescrevê-lo?"):
                return None
        
        field_mappings_data = {fp: data['column_var'].get() for fp, data in self.field_mappings.items() if data['column_var'].get() != "Não mapear"}
        transformations_data = {fp: [key for key, var in trans_vars.items() if var.get()] for fp, trans_vars in self.transformation_selections.items()}
        
        return {
            'name': layout_name,
            'description': self.description_entry.get().strip(),
            'file_config': {'header_row': self.header_row_var.get(), 'file_columns': self.file_columns},
            'api_config': {'company_code': self.company_code_entry.get().strip(), 'api_user': self.api_user_entry.get().strip(), 'api_password': self.api_password_entry.get().strip()},
            'field_mappings': field_mappings_data,
            'transformations': {k: v for k, v in transformations_data.items() if v}
        }
    
    def _show_layout_selection_dialog(self, layouts: List[Dict[str, Any]]):
        dialog = tk.Toplevel(self)
        dialog.title("Carregar Layout")
        dialog.geometry("500x400")
        dialog.transient(self)
        dialog.grab_set()

        tk.Label(dialog, text="Selecione um layout para carregar:", font=("Segoe UI", 12, "bold")).pack(pady=20)
        listbox = tk.Listbox(dialog, font=("Segoe UI", 10), selectbackground="#3b82f6")
        listbox.pack(fill="both", expand=True, padx=20, pady=10)
        
        for i, layout in enumerate(layouts):
            listbox.insert(tk.END, f"{layout.get('name', f'Layout {i+1}')}")
        
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=20)

        def load_selected():
            if (selection := listbox.curselection()):
                self._load_layout_data(layouts[selection[0]])
                dialog.destroy()
        
        tk.Button(btn_frame, text="Carregar", command=load_selected, bg="#3b82f6", fg="white", font=("Segoe UI", 10, "bold"), padx=20, pady=5).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Cancelar", command=dialog.destroy, bg="#6b7280", fg="white", font=("Segoe UI", 10, "bold"), padx=20, pady=5).pack(side="left")

    def _load_layout_data(self, layout_data: Dict[str, Any]):
        # Limpar interface
        for entry in [self.layout_name_entry, self.description_entry, self.company_code_entry, self.api_user_entry, self.api_password_entry]: entry.delete(0, tk.END)
        for data in self.field_mappings.values(): data.get('column_var', tk.StringVar()).set("Não mapear")
        for trans in self.transformation_selections.values():
            for var in trans.values(): var.set(False)

        # Preencher dados
        self.layout_name_entry.insert(0, layout_data.get('name', ''))
        self.description_entry.insert(0, layout_data.get('description', ''))
        api_config = layout_data.get('api_config', {})
        self.company_code_entry.insert(0, api_config.get('company_code', ''))
        self.api_user_entry.insert(0, api_config.get('api_user', ''))
        self.api_password_entry.insert(0, api_config.get('api_password', ''))
        
        file_config = layout_data.get('file_config', {})
        self.header_row_var.set(file_config.get('header_row', '1'))
        self.file_columns = file_config.get('file_columns', [])
        self._update_columns_display()
        self._update_column_combos()
        
        for fp, col in layout_data.get('field_mappings', {}).items():
            if fp in self.field_mappings: self.field_mappings[fp]['column_var'].set(col)
        
        for fp, keys in layout_data.get('transformations', {}).items():
            if fp in self.transformation_selections:
                for key, var in self.transformation_selections[fp].items(): var.set(key in keys)
        
        messagebox.showinfo("Sucesso", f"Layout '{layout_data['name']}' carregado.")
