
from datetime import datetime

from models.evento import Evento
from services.persistencia import Persistencia


def criar_evento(id):
    return Evento(
        id=id,
        nome=f"Evento {id}",
        descricao="Teste de persistência",
        categoria="Workshop",
        local="Brasília",
        data_hora=datetime(2026, 12, 20, 18, 0),
        vagas=50,
    )


def test_salvar_e_listar(tmp_path):
    banco = Persistencia(str(tmp_path / "teste.db"))

    banco.salvar(criar_evento(1))
    banco.salvar(criar_evento(2))

    eventos = banco.listar()

    assert len(eventos) == 2
    assert eventos[0].id == 1
    assert eventos[1].id == 2


def test_remover_evento(tmp_path):
    banco = Persistencia(str(tmp_path / "teste.db"))

    banco.salvar(criar_evento(1))

    assert banco.remover(1) is True
    assert banco.listar() == []
    assert banco.remover(1) is False


def test_atualizar_evento_existente(tmp_path):
    banco = Persistencia(str(tmp_path / "teste.db"))

    banco.salvar(criar_evento(1))

    evento = criar_evento(1)
    evento.nome = "Evento atualizado"

    banco.salvar(evento)

    assert banco.listar()[0].nome == "Evento atualizado"
    assert len(banco.listar()) == 1
