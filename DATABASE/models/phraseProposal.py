from datetime import datetime, date
from DATABASE.db import db


class PhraseProposal(db.Model):
    """
    Modelo para propuestas de frases.
    Basado en la tabla PhraseProposal de PostgreSQL.
    """
    __tablename__ = 'PhraseProposal'

    Id = db.Column('Id', db.BigInteger, primary_key=True, autoincrement=True)
    PhraseId = db.Column('PhraseId', db.BigInteger, nullable=False)
    AuthorId = db.Column('AuthorId', db.BigInteger, nullable=False)
    ProposedText = db.Column('ProposedText', db.Text, nullable=False)
    StatusId = db.Column('StatusId', db.BigInteger, nullable=False)
    Votes = db.Column('Votes', db.SmallInteger, nullable=False, default=0)
    CreateDate = db.Column('CreateDate', db.Date, nullable=False, default=date.today)
    ResolvedAt = db.Column('ResolvedAt', db.Date, nullable=True)
    ResolutionNote = db.Column('ResolutionNote', db.Text, nullable=True)
    Reason = db.Column('Reason', db.Text, nullable=False)

    def __repr__(self):
        return f"<PhraseProposal {self.Id} - Phrase {self.PhraseId}>"

    def to_dict(self):
        data = {
            'id': self.Id,
            'phraseId': self.PhraseId,
            'authorId': self.AuthorId,
            'proposedText': self.ProposedText,
            'status': self.StatusId,
            'votes': self.Votes,
            'createDate': self.CreateDate.isoformat() if self.CreateDate else None,
            'resolvedAt': self.ResolvedAt.isoformat() if self.ResolvedAt else None,
            'resolutionNote': self.ResolutionNote,
            'reason': self.Reason,
        }
        return data