
from datetime import datetime

import pytest

from estruturas.avl import ArvoreAVL
from models.evento import Evento


def criar_evento(id):
    return Evento(
        id=id,
        nome=f"Evento {id}",
        descricao="Evento de teste",
        categoria="Show",
        local="Brasília",
        data_hora=datetime(2026, 12, 20, 18, 0),
        vagas=100,
    )


def verificar_balanceamento(no):
    if no is None:
        return 0

    altura_esquerda = verificar_balanceamento(no.esquerda)
    altura_direita = verificar_balanceamento(no.direita)

    assert abs(altura_esquerda - altura_direita) <= 1

    assert no.altura == 1 + max(
        altura_esquerda,
        altura_direita
    )

    return no.altura


def test_insercao_e_busca():
    arvore = ArvoreAVL()

    for id in [30, 20, 10, 25, 40, 50]:
        arvore.inserir(criar_evento(id))

    assert arvore.buscar(25).id == 25
    assert arvore.buscar(99) is None

    verificar_balanceamento(arvore.raiz)


def test_rotacoes():
    casos = [
        [30, 20, 10],  # LL
        [10, 20, 30],  # RR
        [30, 10, 20],  # LR
        [10, 30, 20],  # RL
    ]

    for caso in casos:
        arvore = ArvoreAVL()

        for id in caso:
            arvore.inserir(criar_evento(id))

        assert arvore.raiz.evento.id == 20
        verificar_balanceamento(arvore.raiz)


def test_remocao():
    arvore = ArvoreAVL()

    for id in [30, 20, 40, 10, 25, 35, 50]:
        arvore.inserir(criar_evento(id))

    arvore.remover(20)

    assert arvore.buscar(20) is None
    assert arvore.buscar(30).id == 30

    verificar_balanceamento(arvore.raiz)


def test_ordem_crescente():
    arvore = ArvoreAVL()

    for id in [50, 20, 40, 10, 30]:
        arvore.inserir(criar_evento(id))

    ids = [evento.id for evento in arvore.em_ordem()]

    assert ids == [10, 20, 30, 40, 50]


def test_nao_permite_ids_repetidos():
    arvore = ArvoreAVL()

    arvore.inserir(criar_evento(10))

    with pytest.raises(ValueError):
        arvore.inserir(criar_evento(10))
