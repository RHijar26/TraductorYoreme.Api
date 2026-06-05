# database/models.py
from datetime import datetime, date
from DATABASE.db import db
from email_validator import validate_email, EmailNotValidError


class UserRegister(db.Model):
    """
    Modelo para el registro de usuarios.
    Basado en la tabla UserRegister de PostgreSQL.
    """
    __tablename__ = 'UserRegister'
    
    # Columnas (nombres con PascalCase como en tu BD)
    Id = db.Column('Id', db.BigInteger, primary_key=True, autoincrement=True)
    Email = db.Column('Email', db.Text, unique=True, nullable=False, index=True)    
    Name = db.Column('Name', db.Text, nullable=False)
    LastName = db.Column('LastName', db.Text, nullable=False)
    SecondLastName = db.Column('SecondLastName', db.Text, nullable=False)
    AboutMe = db.Column('AboutMe', db.Text, nullable=True)
    CreateDate = db.Column('CreateDate', db.Date, nullable=False, default=date.today)
    ApprovalDate = db.Column('ApprovalDate', db.Date, nullable=True)
    Active = db.Column('Active', db.Boolean, nullable=False, default=False)
    
    def __repr__(self):
        return f"<UserRegister {self.Email}>"
         
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
    