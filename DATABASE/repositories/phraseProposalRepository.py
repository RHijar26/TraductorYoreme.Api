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
from DATABASE.models.phrase import Phrase

from DATABASE.repositories.userRepository import UserRepository

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
    def approve(proposalId: int,userId : int) -> Tuple[Optional[PhraseProposal], Optional[str]]:
        existing_proposal = PhraseProposal.query.filter_by(Id=proposalId, StatusId=PhraseStatus.PENDING).first()
        
        if not existing_proposal:
            return None, f"Propuesta no válida"
        

        user = UserRepository.get_by_id(userId)
        if not user:
            return None, f"Usuario no válido"

        try:

            # Cancelar todas las PENDING de la misma frase (excepto esta)
            PhraseProposal.query.filter(
                PhraseProposal.PhraseId == existing_proposal.PhraseId,
                PhraseProposal.StatusId == PhraseStatus.PENDING,
                PhraseProposal.Id != proposalId
            ).update(
                {PhraseProposal.StatusId: PhraseStatus.DECLINED,PhraseProposal.ResolutionNote: "Se aceptó otra propuesta para esta frase"},
                synchronize_session=False
            )
            
            existing_proposal.StatusId = PhraseStatus.APPROVED
            existing_proposal.ResolvedAt = date.today()
            existing_proposal.ResolutionNote = f"Tu propuesta fue aceptada por {user.Name} {user.LastName} {user.SecondLastName}"

            Phrase.query.filter_by(Id=existing_proposal.PhraseId
            ).update(
                {Phrase.Traduction: existing_proposal.ProposedText},
                synchronize_session=False
            )

            db.db.session.commit()

            return existing_proposal, None
        except Exception as e:
            db.db.session.rollback()
            return None, f"Error al aprobar propuesta: {str(e)}"

    @staticmethod
    def decline(proposalId: int) -> Tuple[Optional[PhraseProposal], Optional[str]]:
        existing_proposal = PhraseProposal.query.filter_by(Id=proposalId, StatusId=PhraseStatus.PENDING).first()
        
        if not existing_proposal:
            return None, f"Propuesta no válida"
        
        try:
            existing_proposal.StatusId = PhraseStatus.DECLINED
            existing_proposal.ResolvedAt = date.today()
            existing_proposal.ResolutionNote = "Tu propuesta fue declinada"
            db.db.session.commit()

            return existing_proposal, None
        except Exception as e:
            db.db.session.rollback()
            return None, f"Error al declinar propuesta: {str(e)}"

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
            ,PS."Name"	AS Status
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
            INNER JOIN public."Users" AS U ON U."Id" = PP."AuthorId"
            INNER JOIN public."PhraseStatus" AS PS ON PS."Id" = PP."StatusId"
            WHERE PP."PhraseId" = :phraseId
            LIMIT :page_size OFFSET :offset;
        """)
    
        result = db.db.session.execute(sql, {"page_size": page_size, "offset": (page - 1) * page_size,"phraseId": phraseId})
        return [row._mapping for row in result]       