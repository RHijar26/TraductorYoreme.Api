from typing import List, Optional, Tuple
from datetime import datetime, date
from sqlalchemy import func, or_

import sys
from pathlib import Path

# Agregar la raíz del proyecto al path
root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root))

from DATABASE.models.lenguage import Lenguage
from DATABASE import db

class LenguageRepository:

    def get_by_id(lenguage_id: int) -> Optional[Lenguage]:
        """Obtiene un lenguaje por su ID.
        
        Args:
            lenguage_id: ID del lenguaje
        
        Returns:
            Lenguage o None si no existe
        """
        return Lenguage.query.get(lenguage_id)

    def get_all() -> List[Lenguage]:
        """Obtiene todos los lenguajes registrados en la base de datos.
        
        Returns:
            List[Lenguage]: Lista de objetos Lenguage
        """
        return Lenguage.query.filter_by(Active=True).all()