from typing import List, Optional, Tuple
from datetime import datetime, date
from sqlalchemy import func, or_, sql, text

import sys
from pathlib import Path

# Agregar la raíz del proyecto al path
root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root))

from DATABASE.models.phraseVote import PhraseVote
from DATABASE.repositories.phraseRepository import PhraseRepository
from DATABASE import db


class PhraseVoteRepository:
    @staticmethod
    def handle(phraseId: int, userId: int) -> Tuple[Optional[PhraseVote], Optional[str]]:

        existing_phrase = PhraseRepository.get_by_id(phraseId)
        if not existing_phrase:
            return None, f"Frase no válida"

        existing_vote = PhraseVoteRepository.get_by_user_phrase(userId, phraseId)

        if existing_vote:
            db.db.session.delete(existing_vote)
            db.db.session.commit()
            return False,None

        try:
            new_vote = PhraseVote(
                PhraseId=phraseId,
                UserId=userId,
                CreateDate=date.today(),
            )

            db.db.session.add(new_vote)
            db.db.session.commit()

            return True, None
        except Exception as e:
            db.db.session.rollback()
            return None, f"Error al crear voto: {str(e)}"        

    @staticmethod
    def get_by_user_phrase(userId, phraseId) -> Optional[PhraseVote]:
        """Obtiene el voto en base al usuario y la frase
        
        Args:
            phraseId: ID de la frase
            userId: Id del usuario que creó el voto
        
        Returns:
            PhraseVote o None si no existe
        """
        return PhraseVote.query.filter_by(UserId=userId, PhraseId=phraseId).first()