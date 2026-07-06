from enum import StrEnum

class PhraseStatus(StrEnum):
    PENDING = '1'
    APPROVED = '2'
    DECLINED = '3'