from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from Services.DatabaseService import Base
from datetime import datetime
from uuid import uuid4
import uuid

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    nome = Column(String, nullable=True)
    empresa = Column(String, nullable=True)
    hash_maquina = Column(String, nullable=True)
    data_ativacao = Column(DateTime, nullable=True)
    ativo = Column(Boolean, default=True, nullable=False)
    criado_em = Column(DateTime, default=func.now(), nullable=False)
    atualizado_em = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<Usuario(id={self.id}, email='{self.email}')>"

    def to_dict(self):
        return {
            'id': str(self.id),
            'email': self.email,
            'nome': self.nome,
            'empresa': self.empresa,
            'ativo': self.ativo,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None,
            'atualizado_em': self.atualizado_em.isoformat() if self.atualizado_em else None
        }