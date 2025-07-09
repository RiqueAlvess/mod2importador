from typing import Dict, Any, List, Tuple
from Utils.ApiStructure import ApiStructure

class ValidationService:
    def __init__(self):
        self.structure = ApiStructure.get_structure()

    def validate_layout_config(self, layout: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors: List[str] = []

        if not layout.get('name', '').strip():
            errors.append('Nome do layout ausente')

        api_conf = layout.get('api_config') or {}
        identificacao = self.structure.get('identificacao')
        if identificacao:
            for key, field in identificacao.fields.items():
                if field.required and not api_conf.get(key):
                    errors.append(f"Campo obrigatório da API {field.display_name} ausente")

        mappings = layout.get('field_mappings') or {}
        for category in self.structure.values():
            if not getattr(category, 'required', False):
                continue
            for field_key, field in category.fields.items():
                full_key = f"{category.key}.{field_key}"
                if field.required and full_key not in mappings:
                    errors.append(f"Mapeamento obrigatório ausente para {field.display_name}")

        file_conf = layout.get('file_config') or {}
        header = file_conf.get('header_row', 0)
        try:
            if int(header) < 0:
                errors.append('Linha do cabeçalho inválida')
        except Exception:
            errors.append('Linha do cabeçalho inválida')

        return (len(errors) == 0, errors)
