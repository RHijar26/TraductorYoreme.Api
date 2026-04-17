from datetime import datetime, date
from DATABASE.db import db
import re


class Phrase(db.Model):
    """
    Modelo para frases del sistema.
    Basado en la tabla Phrases de PostgreSQL.
    """


    __tablename__ = 'Phrases'

    Id = db.Column('Id', db.BigInteger, primary_key=True, autoincrement=True)    
    SourceLanguageId = db.Column('SourceLanguageId', db.Text, nullable=False)
    TargetLanguageId = db.Column('TargetLanguageId', db.Text, nullable=False)
    RegionId = db.Column('RegionId', db.BigInteger, nullable=False)
    ModelId = db.Column('ModelId', db.BigInteger, nullable=False)
    StatusId= db.Column('StatusId', db.SmallInteger, nullable=False)
    Phrase = db.Column('Phrase', db.Text, nullable=False)  
    Traduction = db.Column('Traduction', db.Text, nullable=False)  
    CreateDate = db.Column('CreateDate', db.Date, nullable=False, default=date.today)
    Active = db.Column('Active', db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"<Phrase {self.Phrase}>"



    def to_dict(self):
        """
        Convierte la frase a diccionario para JSON.                
        """    
        data = {
            'id': self.Id,
            'sourceLanguageId': self.SourceLanguageId,
            'targetLanguageId': self.TargetLanguageId,
            'regionId': self.RegionId,
            'modelId': self.ModelId,
            'statusId': self.StatusId,
            'phrase': self.Phrase,
            'traduction': self.Traduction,
            'createDate': self.CreateDate.isoformat() if self.CreateDate else None,            
        }
        
        return data