from datetime import datetime, date
from DATABASE.db import db
import re

class PhraseStatus(db.Model):
    """
    Modelo para estados de frases del sistema.
    Basado en la tabla PhraseStatus de PostgreSQL.
    """


    __tablename__ = 'PhraseStatus'

    Id = db.Column('Id', db.SmallInteger, primary_key=True, autoincrement=True)    
    Code = db.Column('Code', db.Text, nullable=False)    
    Name = db.Column('Name', db.Text, nullable=False)
    CreateDate = db.Column('CreateDate', db.Date, nullable=False, default=date.today)
    Active = db.Column('Active', db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"<PhraseStatus {self.Name}>"            
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