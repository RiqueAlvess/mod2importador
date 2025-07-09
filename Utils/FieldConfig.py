from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from enum import Enum

class FieldType(Enum):
    STRING = "string"
    TEXT = "text"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATE = "date"
    DATETIME = "datetime"
    ENUM = "enum"

@dataclass
class FieldConfig:
    """Configuração de um campo da API"""
    name: str
    display_name: str
    field_type: FieldType
    required: bool = False
    max_length: Optional[int] = None
    format_pattern: Optional[str] = None
    enum_values: Optional[List[str]] = None
    validation_rules: List[str] = field(default_factory=list)
    description: Optional[str] = None
    example: Optional[str] = None
    
    def __post_init__(self):
        if self.field_type == FieldType.ENUM and not self.enum_values:
            raise ValueError(f"Campo enum '{self.name}' deve ter valores definidos")

@dataclass
class CategoryConfig:
    """Configuração de uma categoria de campos"""
    key: str
    title: str
    description: str
    required: bool = False
    fields: Dict[str, FieldConfig] = field(default_factory=dict)
    icon: str = "📄"
    order: int = 0

