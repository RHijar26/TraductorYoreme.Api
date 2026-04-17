from typing import List, Optional, Tuple
from datetime import datetime, date
from sqlalchemy import func, or_

import sys
from pathlib import Path

# Agregar la raíz del proyecto al path
root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root))

from DATABASE.models.model import Model
from DATABASE import db

class ModelRepository:



    @staticmethod
    def create(name: str, description: str) -> Tuple[Optional[Model], Optional[str]]:
        """Crea un nuevo modelo en la base de datos.
        
        Args:
            name: Nombre del modelo
            description: Descripción del modelo
        
        Returns:
            Tuple[Optional[Model], Optional[str]]: El modelo creado y un mensaje de error si ocurre            
        """

        is_valid, error_msg = Model.validate_name(name)
        if not is_valid:
            return None, error_msg
        
        is_valid, error_msg = Model.validate_description(description)
        if not is_valid:
             return None, error_msg
        
        existing_model = ModelRepository.get_by_name(name)
        if existing_model:
            return None, f"El nombre '{name}' ya está registrado para otro modelo."

        try:
            model = Model(
                Name=name.strip(),
                Description=description.strip(),
                State=0,  # Estado inicial
                BleuScore=0,  # Puntaje inicial
                ChrScore=0,  # Puntaje inicial
                CreateDate=date.today(),
                Active=True
            )

            db.db.session.add(model)
            db.db.session.commit()

            return model, None
        except Exception as e:
            db.db.session.rollback()
            return None, f"Error al crear modelo: {str(e)}"
    
    def delete(model_id: int) -> Tuple[bool, Optional[str]]:
        """Elimina un modelo de la base de datos (soft delete).
        
        Args:
            model_id: ID del modelo a eliminar
        
        Returns:
            Tuple[bool, Optional[str]]: True si se eliminó correctamente, False y mensaje de error si ocurre
        """
        try:
            model = ModelRepository.get_by_id(model_id)
            if not model:
                return False, f"Modelo no encontrado."
            
            model.Active = False  # Soft delete
            db.db.session.commit()
            return True, None
        except Exception as e:
            db.db.session.rollback()
            return False, f"Error al eliminar modelo: {str(e)}"

    def get_by_id(model_id: int) -> Optional[Model]:
        """Obtiene un modelo por su ID.
        
        Args:
            model_id: ID del modelo
        
        Returns:
            Model o None si no existe
        """
        return Model.query.get(model_id)

    def get_all() -> List[Model]:
        """Obtiene todos los modelos activos."""
        
        return Model.query.filter_by(Active=True).all()

    @staticmethod
    def get_by_name(name: str) -> Optional[Model]:
        """
        Obtiene un modelo por nombre (case-insensitive).
        
        Args:
            name: Nombre del modelo
        
        Returns:
            Model o None si no existe
        """
        return Model.query.filter(
            func.lower(Model.Name) == name.lower()
        ).first()

