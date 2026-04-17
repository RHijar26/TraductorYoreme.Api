# database/models.py
from datetime import datetime, date
from DATABASE.db import db
import re

class Region(db.Model):
    """
    Modelo para regiones del sistema.
    Basado en la tabla Regions de PostgreSQL.
    """
    __tablename__ = 'Regions'
    
    # Columnas (nombres con PascalCase como en tu BD)
    Id = db.Column('Id', db.BigInteger, primary_key=True, autoincrement=True)    
    Name = db.Column('Name', db.Text, nullable=False)
    Description = db.Column('Description', db.Text, nullable=False)        
    CreateDate = db.Column('CreateDate', db.Date, nullable=False, default=date.today)
    Active = db.Column('Active', db.Boolean, nullable=False, default=True)
    
    def __repr__(self):
        return f"<Region {self.Name}>"
    

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
    
    @staticmethod
    def validate_description(description: str) -> tuple[bool, str]:
        """
        Valida que una descripción sea válida.
        
        Args:
            description: Descripción a validar
        
        Returns:
            (is_valid, error_message)
        """
        if not description:
            return False, "Descripción es requerida"
        
        description = description.strip()
        
        if len(description) < 10:
            return False, "Descripción debe tener al menos 10 caracteres"
        
        if len(description) > 1000:
            return False, "Descripción no puede tener más de 1000 caracteres"

        return True, ""
    
    
    def to_dict(self):
        """
        Convierte el modelo a diccionario para JSON.                
        """    
        data = {
            'id': self.Id,
            'name': self.Name,
            'description': self.Description,                        
            'createDate': self.CreateDate.isoformat() if self.CreateDate else None,            
        }
        
        return data