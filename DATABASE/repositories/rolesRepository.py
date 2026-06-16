import sys
from pathlib import Path
from typing import Optional

# Agregar la raíz del proyecto al path
root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root))

from DATABASE.models.roles import Roles
from DATABASE import db


class RolesRepository:

    
    @staticmethod
    def get_by_id(role_id: int) -> Optional[Roles]:
        return Roles.query.get(role_id)
