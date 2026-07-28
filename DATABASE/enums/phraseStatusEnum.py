from enum import StrEnum

class PhraseStatus(StrEnum):
    PENDING = '1'
    REVIEWED = '2'
    APPROVED = '3'
    DECLINED = '4'