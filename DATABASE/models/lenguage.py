from datetime import datetime, date
from DATABASE.db import db
import re

class Lenguage(db.Model):
    """
    Modelo para lenguajes del sistema.
    Basado en la tabla Lenguages de PostgreSQL.
    """
    __tablename__ = 'Lenguages'

    Id = db.Column('Id', db.BigInteger, primary_key=True, autoincrement=True)    
    Name = db.Column('Name', db.Text, nullable=False)    
    CreateDate = db.Column('CreateDate', db.Date, nullable=False, default=date.today)
    Active = db.Column('Active', db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"<Lenguage {self.Name}>"
    
    def to_dict(self):
        """
        Convierte el lenguaje a diccionario para JSON.                
        """    
        data = {
            'id': self.Id,
            'name': self.Name,
            'createDate': self.CreateDate.isoformat() if self.CreateDate else None,            
        }
        
        return data