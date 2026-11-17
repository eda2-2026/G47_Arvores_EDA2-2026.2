
from datetime import datetime, timedelta

from estruturas.heap import MinHeap
from models.evento import Evento


def criar_evento(id, dias):
    return Evento(
        id=id,
        nome=f"Evento {id}",
        descricao="Evento de teste",
        categoria="Workshop",
        local="Brasília",
        data_hora=datetime.now() + timedelta(days=dias),
        vagas=50,
    )


def test_heap_insere_e_consulta_proximo():
    heap = MinHeap()

    heap.inserir(criar_evento(1, 5))
    heap.inserir(criar_evento(2, 2))
    heap.inserir(criar_evento(3, 8))

    assert heap.consultar_proximo().id == 2


def test_heap_remove_proximo():
    heap = MinHeap()

    heap.inserir(criar_evento(1, 5))
    heap.inserir(criar_evento(2, 2))

    removido = heap.remover_proximo()

    assert removido.id == 2
    assert heap.consultar_proximo().id == 1


def test_heap_vazia():
    heap = MinHeap()

    assert heap.esta_vazia()
    assert heap.consultar_proximo() is None
    assert heap.remover_proximo() is None
