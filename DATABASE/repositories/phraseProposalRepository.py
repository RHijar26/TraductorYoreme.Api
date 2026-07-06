from typing import List, Optional, Tuple
from datetime import datetime, date
from sqlalchemy import func, or_, sql, text

import sys
from pathlib import Path

# Agregar la raíz del proyecto al path
root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root))

from DATABASE.enums.phraseStatusEnum import PhraseStatus

from DATABASE.models.phraseProposal import PhraseProposal
from DATABASE import db

class PhraseProposalRepository:

    @staticmethod
    def create(phraseId: int,authorId: int,proposedText: str, reason: str) -> Tuple[Optional[PhraseProposal], Optional[str]]:
        existing_proposal = PhraseProposalRepository.get_by_author_phrase(authorId,phraseId)
        
        if existing_proposal:
            return None, f"No se pueden registar mas de 1 propuesta simultaneamente"
        
        try:
            new_proposal = PhraseProposal(
              PhraseId = phraseId,
              AuthorId = authorId,
              ProposedText = proposedText,
              Reason = reason,
              StatusId = PhraseStatus.PENDING,
              CreateDate=date.today(),              
              
            )

            db.db.session.add(new_proposal)
            db.db.session.commit()

            return new_proposal, None
        except Exception as e:
            db.db.session.rollback()
            return None, f"Error al crear frase: {str(e)}"

    @staticmethod
    def get_by_author_phrase(authorId,phraseId) -> Optional[PhraseProposal]:
        """Obtiene la propuesta en base al autor y la frase
        
        Args:
            phraseId: ID de la frase
            authorId: Id del usuario que creó la propuesta
        
        Returns:
            Phrase o None si no existe
        """
        return PhraseProposal.query.filter_by(AuthorId=authorId,PhraseId=phraseId,StatusId=PhraseStatus.PENDING).first()

    @staticmethod
    def get_phrase_proposals(phraseId: int, page: int = 1, page_size: int = 5) -> List[PhraseProposal]:
        """Obtiene todas las propuestas de una frase
        
        Args:
            phraseId: ID de la frase
            page: Número de página
            page_size: Tamaño de página
        
        Returns:
            Lista de propuestas
        """
        sql = text(f"""
           SELECT 
            PP."Id"
            ,PP."ProposedText"
            ,PP."Reason"
            ,CONCAT(U."Name", ' ', U."LastName", ' ', U."SecondLastName") AS "User"		
            ,CASE 
                -- Si la fecha es hoy o futura
                WHEN PP."CreateDate" >= CURRENT_DATE THEN 'Hoy'
                -- Si pasaron menos de 7 días
                WHEN (CURRENT_DATE - PP."CreateDate") < 7 
                    THEN (CURRENT_DATE - PP."CreateDate")::VARCHAR || 'd ago'    
                -- Si pasaron menos de 30 días
                WHEN (CURRENT_DATE - PP."CreateDate") < 30 
                    THEN (CURRENT_DATE - PP."CreateDate")::VARCHAR || ' días'
                -- Si pasó 1 mes exacto
                WHEN EXTRACT(MONTH FROM AGE(CURRENT_DATE, PP."CreateDate")) = 1 
                    THEN '1m ago'
                -- Si pasaron menos de 12 meses
                WHEN EXTRACT(MONTH FROM AGE(CURRENT_DATE, PP."CreateDate")) < 12 
                    THEN EXTRACT(MONTH FROM AGE(CURRENT_DATE, PP."CreateDate"))::VARCHAR || 'm ago'
                -- Si pasaron más de 12 meses
                ELSE EXTRACT(YEAR FROM AGE(CURRENT_DATE, PP."CreateDate"))::VARCHAR || 'y ago'
            END AS TimeAgo
            FROM public."PhraseProposal" AS PP
            INNER JOIN public."Users" AS U ON U."Id" = PP."AuthorId";

        """)
    
        result = db.db.session.execute(sql, {"page_size": page_size, "offset": (page - 1) * page_size})
        return [row._mapping for row in result]
    

    @staticmethod
    def vote_proposal(proposalId: int, userId: int, vote: bool) -> Tuple[Optional[PhraseProposal], Optional[str]]:
        """Vota una propuesta de frase
        
        Args:
            proposalId: ID de la propuesta
            userId: ID del usuario que vota
            vote: True si es positivo, False si es negativo
        
        Returns:
            Tuple[Optional[PhraseProposal], Optional[str]]: La propuesta actualizada y un mensaje de error si ocurre alguno
        """
        proposal = PhraseProposal.query.get(proposalId)
        
        if not proposal:
            return None, "Propuesta no encontrada"
        
        # Aquí deberías implementar la lógica para registrar el voto del usuario.
        # Esto podría implicar crear una tabla de votos y actualizar el conteo de votos en la propuesta.
        
        try:
            # Ejemplo de actualización de votos (esto es solo un ejemplo, ajusta según tu modelo)
            if vote:
                proposal.PositiveVotes += 1
            else:
                proposal.NegativeVotes += 1
            
            db.db.session.commit()
            return proposal, None
        except Exception as e:
            db.db.session.rollback()
            return None, f"Error al votar la propuesta: {str(e)}"