
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Evento:
    id: int
    nome: str
    descricao: str
    categoria: str
    local: str
    data_hora: datetime
    vagas: int

    def __post_init__(self):
        if self.id <= 0:
            raise ValueError("O ID deve ser positivo.")

        if not self.nome.strip():
            raise ValueError("O nome do evento é obrigatório.")

        if self.vagas < 0:
            raise ValueError("A quantidade de vagas não pode ser negativa.")

    def __str__(self):
        return (
            f"Evento {self.id}: {self.nome} | "
            f"{self.data_hora.strftime('%d/%m/%Y %H:%M')} | "
            f"{self.local}"
        )
