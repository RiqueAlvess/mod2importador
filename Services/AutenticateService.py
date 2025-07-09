import hashlib
import base64
import json
import os
import platform
import getpass
from typing import Optional, Union
from pathlib import Path
from datetime import datetime
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
    def _get_machine_hash() -> str:
        """Gera hash único da máquina"""
        try:
            machine_info = []
            machine_info.append(platform.node())
            machine_info.append(getpass.getuser())
            machine_info.append(platform.system())
            machine_info.append(platform.release())
            machine_info.append(platform.machine())
            
            combined_info = "_".join(machine_info)
            hash_sha256 = hashlib.sha256(combined_info.encode("utf-8")).digest()
            return base64.b64encode(hash_sha256).decode("utf-8")
            
        except Exception as e:
            print(f"Erro ao gerar hash da máquina: {e}")
            fallback = f"{platform.node()}_{getpass.getuser()}"
            hash_sha256 = hashlib.sha256(fallback.encode("utf-8")).digest()
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
    def _is_machine_authorized(usuario: Usuario, current_machine_hash: str) -> bool:
        """Verifica se a máquina atual está autorizada para o usuário"""
        if not usuario.hash_maquina:
            return True
        return usuario.hash_maquina == current_machine_hash
    
    @staticmethod
    def _update_machine_hash(usuario: Usuario, machine_hash: str) -> None:
        """Atualiza o hash da máquina no banco de dados"""
        try:
            with SessionLocal() as db:
                db_usuario = db.query(Usuario).filter(Usuario.id == usuario.id).first()
                if db_usuario:
                    db_usuario.hash_maquina = machine_hash
                    if not db_usuario.data_ativacao:
                        db_usuario.data_ativacao = datetime.now()
                    db_usuario.atualizado_em = datetime.now()
                    db.commit()
        except Exception as e:
            print(f"Erro ao atualizar hash da máquina: {e}")
    
    @staticmethod
    def autenticar(email: str, password: str, lembrar: bool = False) -> AuthResult:
        """
        Autentica usuário com verificação de hash da máquina
        """
        if not email or not password:
            return AuthResult(False, message="Email e senha são obrigatórios")
        
        senha_final = AuthService._hash_password(password)
        current_machine_hash = AuthService._get_machine_hash()
        
        try:
            with SessionLocal() as db:
                usuario = db.query(Usuario).filter(
                    Usuario.email == email,
                    Usuario.senha_hash == senha_final,
                    Usuario.ativo == True
                ).first()
                
                if not usuario:
                    return AuthResult(False, message="Credenciais inválidas")
                
                if not AuthService._is_machine_authorized(usuario, current_machine_hash):
                    return AuthResult(
                        False, 
                        message="Acesso negado. Esta máquina não está autorizada para este usuário."
                    )
                
                db.expunge(usuario)
                
                if not usuario.hash_maquina:
                    AuthService._update_machine_hash(usuario, current_machine_hash)
                    usuario.hash_maquina = current_machine_hash
                
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
    """Função de compatibilidade"""
    result = AuthService.autenticar(email, password, lembrar)
    return result.user if result.success else result.message