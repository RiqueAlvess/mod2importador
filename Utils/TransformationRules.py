from typing import Dict, List
from dataclasses import dataclass

@dataclass
class TransformationRule:
    """Regra de transformação de dados"""
    key: str
    name: str
    description: str
    applicable_types: List[str]
    category: str

class TransformationRules:
    """Catálogo de regras de transformação disponíveis"""
    
    @staticmethod
    def get_all_rules() -> Dict[str, TransformationRule]:
        """Retorna todas as regras de transformação disponíveis"""
        return {
            # Formatação de texto
            "remove_spaces": TransformationRule(
                key="remove_spaces",
                name="Remover Espaços",
                description="Remove todos os espaços em branco",
                applicable_types=["string", "text"],
                category="Formatação"
            ),
            "remove_dots": TransformationRule(
                key="remove_dots",
                name="Remover Pontos",
                description="Remove todos os pontos (.)",
                applicable_types=["string", "text"],
                category="Formatação"
            ),
            "remove_special_chars": TransformationRule(
                key="remove_special_chars",
                name="Remover Caracteres Especiais",
                description="Remove caracteres especiais, mantendo apenas letras, números e espaços",
                applicable_types=["string", "text"],
                category="Formatação"
            ),
            "lowercase": TransformationRule(
                key="lowercase",
                name="Converter para Minúsculo",
                description="Converte todo o texto para minúsculo",
                applicable_types=["string", "text"],
                category="Formatação"
            ),
            "uppercase": TransformationRule(
                key="uppercase",
                name="Converter para Maiúsculo",
                description="Converte todo o texto para maiúsculo",
                applicable_types=["string", "text"],
                category="Formatação"
            ),
            "trim": TransformationRule(
                key="trim",
                name="Remover Espaços Laterais",
                description="Remove espaços no início e fim do texto",
                applicable_types=["string", "text"],
                category="Formatação"
            ),
            
            # Formatação específica
            "format_cpf": TransformationRule(
                key="format_cpf",
                name="Formatar CPF",
                description="Formata como CPF (###.###.###-##)",
                applicable_types=["string"],
                category="Documentos"
            ),
            "format_cnpj": TransformationRule(
                key="format_cnpj",
                name="Formatar CNPJ",
                description="Formata como CNPJ (##.###.###/####-##)",
                applicable_types=["string"],
                category="Documentos"
            ),
            "format_phone": TransformationRule(
                key="format_phone",
                name="Formatar Telefone",
                description="Formata como telefone brasileiro",
                applicable_types=["string"],
                category="Contato"
            ),
            "format_cep": TransformationRule(
                key="format_cep",
                name="Formatar CEP",
                description="Formata como CEP (#####-###)",
                applicable_types=["string"],
                category="Endereço"
            ),
            
            # Formatação de datas
            "format_date_ddmmyyyy": TransformationRule(
                key="format_date_ddmmyyyy",
                name="Data DD/MM/YYYY",
                description="Converte para formato DD/MM/YYYY",
                applicable_types=["string", "date"],
                category="Data"
            ),
            "format_date_mmddyyyy": TransformationRule(
                key="format_date_mmddyyyy",
                name="Data MM/DD/YYYY",
                description="Converte para formato MM/DD/YYYY",
                applicable_types=["string", "date"],
                category="Data"
            ),
            "format_date_yyyymmdd": TransformationRule(
                key="format_date_yyyymmdd",
                name="Data YYYY-MM-DD",
                description="Converte para formato YYYY-MM-DD",
                applicable_types=["string", "date"],
                category="Data"
            ),
            
            # Validação e limpeza
            "validate_email": TransformationRule(
                key="validate_email",
                name="Validar Email",
                description="Valida formato de email",
                applicable_types=["string"],
                category="Validação"
            ),
            "validate_cpf": TransformationRule(
                key="validate_cpf",
                name="Validar CPF",
                description="Valida dígitos verificadores do CPF",
                applicable_types=["string"],
                category="Validação"
            ),
            "validate_cnpj": TransformationRule(
                key="validate_cnpj",
                name="Validar CNPJ",
                description="Valida dígitos verificadores do CNPJ",
                applicable_types=["string"],
                category="Validação"
            ),
            
            # Conversão de tipos
            "convert_to_integer": TransformationRule(
                key="convert_to_integer",
                name="Converter para Inteiro",
                description="Converte valor para número inteiro",
                applicable_types=["string", "float"],
                category="Conversão"
            ),
            "convert_to_float": TransformationRule(
                key="convert_to_float",
                name="Converter para Decimal",
                description="Converte valor para número decimal",
                applicable_types=["string", "integer"],
                category="Conversão"
            ),
            "convert_to_boolean": TransformationRule(
                key="convert_to_boolean",
                name="Converter para Booleano",
                description="Converte para verdadeiro/falso",
                applicable_types=["string", "integer"],
                category="Conversão"
            )
        }
    
    @staticmethod
    def get_rules_by_category() -> Dict[str, List[TransformationRule]]:
        """Retorna regras agrupadas por categoria"""
        rules = TransformationRules.get_all_rules()
        categories = {}
        
        for rule in rules.values():
            if rule.category not in categories:
                categories[rule.category] = []
            categories[rule.category].append(rule)
        
        return categories
    
    @staticmethod
    def get_applicable_rules(field_type: str) -> List[TransformationRule]:
        """Retorna regras aplicáveis a um tipo de campo específico"""
        rules = TransformationRules.get_all_rules()
        applicable = []
        
        for rule in rules.values():
            if field_type in rule.applicable_types:
                applicable.append(rule)
        
        return applicable

