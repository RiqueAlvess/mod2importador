import hashlib
import base64
import json
import os
from typing import Optional, Union
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from Models.Usuarios import Usuario
from Services.DatabaseService import SessionLocal

load_dotenv()
PASSWORD_SECRET = os.getenv("PASSWORD_SECRET", "")
AUTH_FILE = Path("usuario_autenticado.json")

class AuthResult:
    """Classe para resultado da autenticação"""
    def __init__(self, success: bool, user: Optional[Usuario] = None, message: str = ""):
        self.success = success
        self.user = user
        self.message = message

class AuthService:
    @staticmethod
    def _hash_password(password: str) -> str:
        """Gera hash da senha com salt"""
        senha_com_salt = password + PASSWORD_SECRET
        hash_sha256 = hashlib.sha256(senha_com_salt.encode("utf-8")).digest()
        return base64.b64encode(hash_sha256).decode("utf-8")
    
    @staticmethod
    def _save_remember_user(email: str) -> None:
        """Salva dados do usuário para lembrar"""
        try:
            AUTH_FILE.write_text(
                json.dumps({"email": email}, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )
        except Exception as e:
            print(f"Erro ao salvar dados de lembrança: {e}")
    
    @staticmethod
    def _get_remembered_user() -> Optional[str]:
        """Recupera email do usuário lembrado"""
        try:
            if AUTH_FILE.exists():
                data = json.loads(AUTH_FILE.read_text(encoding="utf-8"))
                return data.get("email")
        except Exception:
            pass
        return None
    
    @staticmethod
    def clear_remember_user() -> None:
        """Remove dados de lembrança"""
        try:
            if AUTH_FILE.exists():
                AUTH_FILE.unlink()
        except Exception:
            pass
    
    @staticmethod
    def autenticar(email: str, password: str, lembrar: bool = False) -> AuthResult:
        """
        Autentica usuário de forma otimizada
        
        Args:
            email: Email do usuário
            password: Senha do usuário
            lembrar: Se deve lembrar do usuário
            
        Returns:
            AuthResult com resultado da autenticação
        """
        # Validação básica
        if not email or not password:
            return AuthResult(False, message="Email e senha são obrigatórios")
        
        # Hash da senha
        senha_final = AuthService._hash_password(password)
        
        # Busca no banco com context manager
        try:
            with SessionLocal() as db:
                usuario = db.query(Usuario).filter(
                    Usuario.email == email,
                    Usuario.senha_hash == senha_final
                ).first()
                
                if not usuario:
                    return AuthResult(False, message="Credenciais inválidas")
                
                # Detach do objeto da sessão para uso fora do contexto
                db.expunge(usuario)
                
                # Salvar dados de lembrança se solicitado
                if lembrar:
                    AuthService._save_remember_user(email)
                else:
                    AuthService.clear_remember_user()
                
                return AuthResult(True, usuario, "Login realizado com sucesso")
                
        except SQLAlchemyError as e:
            return AuthResult(False, message="Erro de conexão com banco de dados")
        except Exception as e:
            return AuthResult(False, message="Erro interno do servidor")


def autenticar(email: str, password: str, lembrar: bool = False) -> Union[Usuario, str]:
    """Função de compatibilidade - retorna Usuario ou string de erro"""
    result = AuthService.autenticar(email, password, lembrar)
    return result.user if result.success else result.message