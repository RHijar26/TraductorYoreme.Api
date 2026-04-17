# database/models.py
from datetime import datetime, date
from DATABASE.db import db
import re


class Model(db.Model):
    """
    Modelo para modelos del sistema.
    Basado en la tabla Models de PostgreSQL.
    """


    __tablename__ = 'Models'

    Id = db.Column('Id', db.BigInteger, primary_key=True, autoincrement=True)    
    Name = db.Column('Name', db.Text, nullable=False)
    Description = db.Column('Description', db.Text, nullable=False)    
    State = db.Column('State', db.SmallInteger, nullable=False)    
    BleuScore = db.Column('BleuScore', db.SmallInteger, nullable=False)    
    ChrScore = db.Column('ChrScore', db.SmallInteger, nullable=False)    
    CreateDate = db.Column('CreateDate', db.Date, nullable=False, default=date.today)
    Active = db.Column('Active', db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"<Model {self.Name}>"
    
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
        state_map = {            
            0: "Testing",
            1: "Produccion",
            2: "Archivado",
        }    

        state_class_map = {            
            0: "px-2 py-1 rounded-full bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400 text-xs font-bold",
            1: "px-2 py-1 rounded-full bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400 text-xs font-bold",
            2: "px-2 py-1 rounded-full bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-400 text-xs font-bold",
        }

        data = {
            'id': self.Id,
            'name': self.Name,
            'description': self.Description,
            'state': state_map.get(self.State, "Desconocido"),
            'class': state_class_map.get(self.State, "badge-dark"),
            'bleuScore': self.BleuScore,
            'chrScore': self.ChrScore,
            'createDate': self.CreateDate.isoformat() if self.CreateDate else None,            
        }
        
        return data