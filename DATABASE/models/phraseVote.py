from datetime import datetime, date
from DATABASE.db import db

class PhraseVote(db.Model):
    """
    Modelo para votos de frases.
    Basado en la tabla PhraseVote de PostgreSQL.
    """
    __tablename__ = 'PhraseVote'

    Id = db.Column('Id', db.BigInteger, primary_key=True, autoincrement=True)
    PhraseId = db.Column('PhraseId', db.BigInteger, nullable=False)
    UserId = db.Column('UserId', db.BigInteger, nullable=False)    
    CreateDate = db.Column('CreateDate', db.Date, nullable=False, default=date.today)

    def __repr__(self):
        return f"<PhraseVote {self.Id} - Phrase {self.PhraseId}>"

    def to_dict(self):
        data = {
            'id': self.Id,
            'phraseId': self.PhraseId,
            'userId': self.UserId,            
            'createDate': self.CreateDate.isoformat() if self.CreateDate else None,
        }
        return data