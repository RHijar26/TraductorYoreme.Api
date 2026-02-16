# database/models.py
from datetime import datetime, date
from db import db
import bcrypt
import re
from email_validator import validate_email, EmailNotValidError

class User(db.Model):
    """
    Modelo para usuarios del sistema.
    Basado en la tabla Users de PostgreSQL.
    """
    __tablename__ = 'Users'
    
    # Columnas (nombres con PascalCase como en tu BD)
    Id = db.Column('Id', db.BigInteger, primary_key=True, autoincrement=True)
    Email = db.Column('Email', db.Text, unique=True, nullable=False, index=True)
    Password = db.Column('Password', db.Text, nullable=False)  # Hash de la contraseña
    Name = db.Column('Name', db.Text, nullable=False)
    LastName = db.Column('LastName', db.Text, nullable=False)
    SecondLastName = db.Column('SecondLastName', db.Text, nullable=False)
    CreateDate = db.Column('CreateDate', db.Date, nullable=False, default=date.today)
    Active = db.Column('Active', db.Boolean, nullable=False, default=True)
    
    # Índices adicionales
    __table_args__ = (
        db.Index('idx_users_email_active', 'Email', 'Active'),
    )
    
    def __repr__(self):
        return f"<User {self.Email}>"
    
    # ==========================================
    # Métodos de Contraseña
    # ==========================================
    
    def set_password(self, password: str):
        """
        Hashea y establece la contraseña del usuario.
        
        Args:
            password: Contraseña en texto plano
        """
        # Generar salt y hashear
        salt = bcrypt.gensalt()
        password_bytes = password.encode('utf-8')
        self.Password = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    
    def check_password(self, password: str) -> bool:
        """
        Verifica si la contraseña es correcta.
        
        Args:
            password: Contraseña en texto plano
        
        Returns:
            True si la contraseña es correcta, False si no
        """
        if not self.Password:
            return False
        
        try:
            password_bytes = password.encode('utf-8')
            hash_bytes = self.Password.encode('utf-8')
            return bcrypt.checkpw(password_bytes, hash_bytes)
        except Exception:
            return False
    
    # ==========================================
    # Validaciones Estáticas
    # ==========================================
    
    @staticmethod
    def validate_email(email: str) -> tuple[bool, str]:
        """
        Valida que el email sea válido.
        
        Returns:
            (is_valid, error_message)
        """
        if not email:
            return False, "El email es requerido"
        
        try:
            # Validar y normalizar email
            validated = validate_email(email, check_deliverability=False)
            return True, ""
        except EmailNotValidError as e:
            return False, f"Email inválido: {str(e)}"
    
    @staticmethod
    def validate_password(password: str) -> tuple[bool, str]:
        """
        Valida que la contraseña cumpla los requisitos de seguridad.
        
        Requisitos:
        - Mínimo 8 caracteres
        - Al menos una letra mayúscula
        - Al menos una letra minúscula
        - Al menos un número
        - Al menos un carácter especial
        
        Returns:
            (is_valid, error_message)
        """
        if not password:
            return False, "La contraseña es requerida"
        
        if len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres"
        
        if len(password) > 128:
            return False, "La contraseña no puede tener más de 128 caracteres"
        
        if not re.search(r'[A-Z]', password):
            return False, "La contraseña debe contener al menos una letra mayúscula"
        
        if not re.search(r'[a-z]', password):
            return False, "La contraseña debe contener al menos una letra minúscula"
        
        if not re.search(r'[0-9]', password):
            return False, "La contraseña debe contener al menos un número"
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "La contraseña debe contener al menos un carácter especial (!@#$%^&*(),.?\":{}|<>)"
        
        return True, ""
    
    @staticmethod
    def validate_name(name: str, field_name: str = "Nombre") -> tuple[bool, str]:
        """
        Valida que un nombre sea válido.
        
        Args:
            name: Nombre a validar
            field_name: Nombre del campo para mensajes de error
        
        Returns:
            (is_valid, error_message)
        """
        if not name:
            return False, f"{field_name} es requerido"
        
        name = name.strip()
        
        if len(name) < 2:
            return False, f"{field_name} debe tener al menos 2 caracteres"
        
        if len(name) > 100:
            return False, f"{field_name} no puede tener más de 100 caracteres"
        
        # Solo letras, espacios, acentos y algunos caracteres especiales
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s\'-]+$', name):
            return False, f"{field_name} solo puede contener letras, espacios, acentos y guiones"
        
        return True, ""
    
    # ==========================================
    # Serialización
    # ==========================================
    
    def to_dict(self, include_password=False):
        """
        Convierte el modelo a diccionario para JSON.
        
        Args:
            include_password: Si True, incluye el hash de la contraseña (NO RECOMENDADO)
        """
        data = {
            'id': self.Id,
            'email': self.Email,
            'name': self.Name,
            'last_name': self.LastName,
            'second_last_name': self.SecondLastName,
            'full_name': f"{self.Name} {self.LastName} {self.SecondLastName}".strip(),
            'create_date': self.CreateDate.isoformat() if self.CreateDate else None,
            'active': self.Active
        }
        
        if include_password:
            data['password_hash'] = self.Password
        
        return data
    
    def to_public_dict(self):
        """Datos públicos del usuario (sin información sensible)."""
        return {
            'id': self.Id,
            'name': self.Name,
            'last_name': self.LastName,
            'full_name': f"{self.Name} {self.LastName} {self.SecondLastName}".strip()
        }