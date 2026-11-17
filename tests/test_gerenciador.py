
from datetime import datetime, timedelta

from models.evento import Evento
from services.gerenciador_eventos import GerenciadorEventos


def criar_evento(id, dias):
    return Evento(
        id=id,
        nome=f"Evento {id}",
        descricao="Evento de teste",
        categoria="Workshop",
        local="Brasília",
        data_hora=datetime(2026, 12, 1) + timedelta(days=dias),
        vagas=50,
    )


def test_cadastrar_e_buscar():
    gerenciador = GerenciadorEventos()
    evento = criar_evento(1, 5)

    gerenciador.cadastrar(evento)

    assert gerenciador.buscar(1).nome == "Evento 1"
    assert gerenciador.quantidade() == 1


def test_proximo_evento():
    gerenciador = GerenciadorEventos()

    gerenciador.cadastrar(criar_evento(1, 5))
    gerenciador.cadastrar(criar_evento(2, 2))

    assert gerenciador.proximo_evento().id == 2


def test_listar_em_ordem_cronologica():
    gerenciador = GerenciadorEventos()

    gerenciador.cadastrar(criar_evento(1, 5))
    gerenciador.cadastrar(criar_evento(2, 2))
    gerenciador.cadastrar(criar_evento(3, 8))

    ids = [evento.id for evento in gerenciador.listar_eventos()]

    assert ids == [2, 1, 3]


def test_remover_evento():
    gerenciador = GerenciadorEventos()

    gerenciador.cadastrar(criar_evento(1, 5))
    gerenciador.cadastrar(criar_evento(2, 2))

    removido = gerenciador.remover(2)

    assert removido.id == 2
    assert gerenciador.buscar(2) is None
    assert gerenciador.proximo_evento().id == 1
    assert gerenciador.quantidade() == 1


def test_atualizar_evento():
    gerenciador = GerenciadorEventos()

    gerenciador.cadastrar(criar_evento(1, 5))

    novo = criar_evento(1, 2)
    gerenciador.atualizar(1, novo)

    assert gerenciador.buscar(1).data_hora == novo.data_hora
    assert gerenciador.proximo_evento().data_hora == novo.data_hora


def test_impedir_id_duplicado():
    gerenciador = GerenciadorEventos()

    gerenciador.cadastrar(criar_evento(1, 5))

    try:
        gerenciador.cadastrar(criar_evento(1, 8))
        assert False, "Deveria impedir IDs duplicados."
    except ValueError:
        assert gerenciador.quantidade() == 1
