
from datetime import datetime, timedelta

import pytest

from estruturas.rubro_negra import (
    ArvoreRubroNegra,
    VERMELHO,
    PRETO,
)
from models.evento import Evento


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


def verificar_propriedades(arvore):
    assert arvore.raiz.cor == PRETO

    def verificar(no):
        if no == arvore.NIL:
            return 1

        if no.cor == VERMELHO:
            assert no.esquerda.cor == PRETO
            assert no.direita.cor == PRETO

        altura_esquerda = verificar(no.esquerda)
        altura_direita = verificar(no.direita)

        assert altura_esquerda == altura_direita

        return altura_esquerda + (1 if no.cor == PRETO else 0)

    verificar(arvore.raiz)


def test_insercao_e_busca():
    arvore = ArvoreRubroNegra()

    eventos = [
        criar_evento(1, 5),
        criar_evento(2, 2),
        criar_evento(3, 8),
        criar_evento(4, 1),
    ]

    for evento in eventos:
        arvore.inserir(evento)

    encontrado = arvore.buscar(eventos[1].data_hora, 2)

    assert encontrado.id == 2
    assert arvore.buscar(datetime(2026, 1, 1), 99) is None
    verificar_propriedades(arvore)


def test_ordem_cronologica():
    arvore = ArvoreRubroNegra()

    for evento in [
        criar_evento(1, 5),
        criar_evento(2, 2),
        criar_evento(3, 8),
    ]:
        arvore.inserir(evento)

    ids = [evento.id for evento in arvore.em_ordem()]

    assert ids == [2, 1, 3]


def test_consulta_intervalo():
    arvore = ArvoreRubroNegra()

    for evento in [
    criar_evento(1, 1),
    criar_evento(2, 5),
    criar_evento(3, 9),
]:
        arvore.inserir(evento)

    inicio = datetime(2026, 12, 5)
    fim = datetime(2026, 12, 10)

    resultado = arvore.consultar_intervalo(inicio, fim)

    assert [evento.id for evento in resultado] == [2, 3]


def test_remocao():
    arvore = ArvoreRubroNegra()

    eventos = [
        criar_evento(1, 5),
        criar_evento(2, 2),
        criar_evento(3, 8),
        criar_evento(4, 1),
        criar_evento(5, 6),
        criar_evento(6, 9),
    ]

    for evento in eventos:
        arvore.inserir(evento)

    removido = arvore.remover(eventos[1].data_hora, 2)

    assert removido.id == 2
    assert arvore.buscar(eventos[1].data_hora, 2) is None
    verificar_propriedades(arvore)


def test_remover_arvore_vazia():
    arvore = ArvoreRubroNegra()

    assert arvore.remover(datetime(2026, 12, 1), 1) is None
    assert arvore.em_ordem() == []


def test_nao_permite_chave_repetida():
    arvore = ArvoreRubroNegra()
    evento = criar_evento(1, 5)

    arvore.inserir(evento)

    with pytest.raises(ValueError):
        arvore.inserir(evento)
