from typing import List, Optional, Tuple
from datetime import datetime, date
from sqlalchemy import func, or_

import sys
from pathlib import Path

# Agregar la raíz del proyecto al path
root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root))

from DATABASE.models.phraseStatus import PhraseStatus
from DATABASE import db

class PhraseStatusRepository:

    def get_by_code(status_code: str) -> Optional[PhraseStatus]:
        """Obtiene un estado de frase por su código.
        
        Args:
            status_code: Código del estado de frase
        
        Returns:
            PhraseStatus o None si no existe
        """
        return PhraseStatus.query.filter_by(Code=status_code).first()

    def get_all() -> List[PhraseStatus]:
        """Obtiene todos los estados de frase registrados en la base de datos.
        
        Returns:
            List[PhraseStatus]: Lista de objetos PhraseStatus
        """
        return PhraseStatus.query.filter_by(Active=True).all()