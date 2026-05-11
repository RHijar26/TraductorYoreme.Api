from typing import List, Optional, Tuple
from datetime import datetime, date
from sqlalchemy import func, or_, text

import sys
from pathlib import Path

# Agregar la raíz del proyecto al path
root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root))

from DATABASE.models.phrase import Phrase
from DATABASE.repositories.lenguageRepository import LenguageRepository
from DATABASE.repositories.modelRepository import ModelRepository
from DATABASE.repositories.regionRepository import RegionRepository
from DATABASE.repositories.phraseStatusRepository import PhraseStatusRepository
from DATABASE import db

class PhraseRepository:


    def create(sourceLanguage: int, targetLanguage: int, regionId : int, modelId: int, phrase: str, traduction: str) -> Tuple[Optional[Phrase], Optional[str]]:
        
        existing_source_lenguage = LenguageRepository.get_by_id(sourceLanguage)
        if not existing_source_lenguage:
            return None, f"Lenguaje de origen no válido"
        
        existing_target_lenguage = LenguageRepository.get_by_id(targetLanguage)
        if not existing_target_lenguage:
            return None, f"Lenguaje de destino no válido"
                
        existing_region = RegionRepository.get_by_id(regionId)
        if not existing_region:
            return None, f"Región no válida"
        
        existing_model = ModelRepository.get_by_id(modelId)
        if not existing_model:
            return None, f"Modelo no válido"
        
        existing_status = PhraseStatusRepository.get_by_code("PEN")
        if not existing_status:
            return None, f"Estado no válido"
        
        try:
            new_phrase = Phrase(
                SourceLanguageId=existing_source_lenguage.Id,
                TargetLanguageId=existing_target_lenguage.Id,
                RegionId=existing_region.Id,
                ModelId=existing_model.Id,
                StatusId=existing_status.Id,
                Phrase=phrase.strip(),
                Traduction=traduction.strip(),
                CreateDate=date.today(),
                Active=True
            )

            db.db.session.add(new_phrase)
            db.db.session.commit()

            return new_phrase, None
        except Exception as e:
            db.db.session.rollback()
            return None, f"Error al crear frase: {str(e)}"

    def update( phraseId:int, regionId:int, modelId:int, traduction:str) -> Tuple[Optional[Phrase], Optional[str]]:
        """
        Actualiza una frase existente en la base de datos.
        Args:
            phraseId: ID de la frase a actualizar
            regionId: Nuevo ID de la región
            modelId: Nuevo ID del modelo
            traduction: Nueva traducción de la frase        
        """

        phrase = PhraseRepository.get_by_id(phraseId)
        if not phrase:
            return None, f"Frase no encontrada"
        
        try:
            existing_region = RegionRepository.get_by_id(regionId)
            if not existing_region:
                return None, f"Región no válida"
            
            existing_model = ModelRepository.get_by_id(modelId)
            if not existing_model:
                return None, f"Modelo no válido"
            
            phrase.RegionId = existing_region.Id
            phrase.ModelId = existing_model.Id
            phrase.Traduction = traduction.strip()
            db.db.session.commit()

            return phrase, None            
        except Exception as e:
            db.db.session.rollback()
            return None, f"Error al actualizar frase: {str(e)}"

    def delete(phrase_id: int) -> Tuple[bool, Optional[str]]:
        """Elimina una frase de la base de datos (soft delete).
        
        Args:
            phrase_id: ID de la frase a eliminar
        
        Returns:
            Tuple[bool, Optional[str]]: True si se eliminó correctamente, False y mensaje de error si ocurre
        """
        try:
            phrase = PhraseRepository.get_by_id(phrase_id)
            if not phrase:
                return False, f"Frase no encontrada."
            
            phrase.Active = False  # Soft delete
            db.db.session.commit()
            return True, None
        except Exception as e:
            db.db.session.rollback()
            return False, f"Error al eliminar frase: {str(e)}"

    def get_by_id(phrase_id: int) -> Optional[Phrase]:
        """Obtiene una frase por su ID.
        
        Args:
            phrase_id: ID de la frase
        
        Returns:
            Phrase o None si no existe
        """
        return Phrase.query.get(phrase_id)

    def get_all() -> List[Phrase]:
        """Obtiene todas las frases registradas en la base de datos.
        
        Returns:
            List[Phrase]: Lista de objetos Phrase
        """
        sql = text('SELECT * FROM "Phrases" WHERE "Active" = true ORDER BY "Id" DESC')
        return Phrase.query.from_statement(sql).all()