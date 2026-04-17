from typing import List, Optional, Tuple
from datetime import datetime, date
from unicodedata import name
from sqlalchemy import func, or_

import sys
from pathlib import Path

# Agregar la raíz del proyecto al path
root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root))

from DATABASE.models.region import Region
from DATABASE import db

class RegionRepository:

    @staticmethod
    def create(name: str, description: str) -> Tuple[Optional[Region], Optional[str]]:
        """Crea una nueva Region en la base de datos.
        
        Args:
            name: Nombre de la Region   
            description: Descripción de la Region
        
        Returns:
            Tuple[Optional[Region], Optional[str]]: La Region creada y un mensaje de error si ocurre            
        """

        is_valid, error_msg = Region.validate_name(name)
        if not is_valid:
            return None, error_msg
        
        is_valid, error_msg = Region.validate_description(description)
        if not is_valid:
             return None, error_msg
        
        existing_region = RegionRepository.get_by_name(name)
        if existing_region:
            return None, f"El nombre '{name}' ya está registrado para otra región."

        try:
            new_region = Region(
                Name=name, 
                Description=description
            )
            db.db.session.add(new_region)
            db.db.session.commit()
            return new_region, None
        except Exception as e:
            db.db.session.rollback()
            return None, str(e)

    @staticmethod
    def get_by_name(name: str) -> Optional[Region]:
        """
        Obtiene una región por nombre (case-insensitive).
        
        Args:
            name: Nombre de la región
        
        Returns:
            Region o None si no existe
        """
        return Region.query.filter(
            func.lower(Region.Name) == name.lower()
        ).first()


    def delete(region_id: int) -> Tuple[bool, Optional[str]]:
        """
        Elimina una región permanentemente (soft delete).
        
        Args:
            region_id: ID de la región
        
        Returns:
            Tuple[bool, Optional[str]]: True si se eliminó correctamente, False y mensaje de error si no
        """
        region = RegionRepository.get_by_id(region_id)
        if not region:
             return False, "Región no encontrada"
        
        try:
            region.Active = False  # Soft delete
            db.db.session.commit()
            return True, None
        except Exception as e:
            db.db.session.rollback()
            return False, str(e)

    @staticmethod
    def get_by_id(region_id: int) -> Optional[Region]:
        """
        Obtiene una región por ID.
        
        Args:
            region_id: ID de la región
        
        Returns:
            Region o None si no existe
        """
        return Region.query.get(region_id)

    @staticmethod    
    def get_all() -> List[Region]:
        """Obtiene todos los modelos activos."""
        
        return Region.query.filter_by(Active=True).all()

