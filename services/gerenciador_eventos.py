
from estruturas.avl import ArvoreAVL
from estruturas.heap import MinHeap
from estruturas.rubro_negra import ArvoreRubroNegra
from services.persistencia import Persistencia


class GerenciadorEventos:
    """Integra as árvores e a persistência SQLite."""

    def __init__(self, persistencia=None):
        self.arvore_avl = ArvoreAVL()
        self.heap = MinHeap()
        self.arvore_rubro_negra = ArvoreRubroNegra()
        self.persistencia = (
            persistencia if persistencia is not None else Persistencia()
        )

        # Recupera os eventos salvos no banco.
        for evento in self.persistencia.listar():
            self._inserir_estruturas(evento)

    def _inserir_estruturas(self, evento):
        self.arvore_avl.inserir(evento)
        self.heap.inserir(evento)
        self.arvore_rubro_negra.inserir(evento)

    def cadastrar(self, evento):
        if self.arvore_avl.buscar(evento.id) is not None:
            raise ValueError("Já existe um evento com esse ID.")

        self._inserir_estruturas(evento)
        self.persistencia.salvar(evento)
        return evento

    def buscar(self, id_evento):
        return self.arvore_avl.buscar(id_evento)

    def proximo_evento(self):
        return self.heap.consultar_proximo()

    def listar_eventos(self):
        return self.arvore_rubro_negra.em_ordem()

    def consultar_intervalo(self, inicio, fim):
        if inicio > fim:
            raise ValueError(
                "A data inicial não pode ser posterior à final."
            )
        return self.arvore_rubro_negra.consultar_intervalo(inicio, fim)

    def remover(self, id_evento):
        evento = self.arvore_avl.buscar(id_evento)

        if evento is None:
            return None

        self.arvore_avl.remover(id_evento)
        self.arvore_rubro_negra.remover(evento.data_hora, evento.id)

        self.heap = MinHeap()
        for item in self.arvore_avl.em_ordem():
            self.heap.inserir(item)

        self.persistencia.remover(id_evento)
        return evento

    def atualizar(self, id_evento, novo_evento):
        if id_evento != novo_evento.id:
            raise ValueError("O ID do evento não pode ser alterado.")

        antigo = self.arvore_avl.buscar(id_evento)

        if antigo is None:
            return None

        self.remover(id_evento)
        self.cadastrar(novo_evento)
        return novo_evento

    def quantidade(self):
        return len(self.arvore_avl.em_ordem())
