
from estruturas.avl import ArvoreAVL
from estruturas.heap import MinHeap
from estruturas.rubro_negra import ArvoreRubroNegra


class GerenciadorEventos:
    """Integra as três estruturas de dados do EventTree."""

    def __init__(self):
        self.arvore_avl = ArvoreAVL()
        self.heap = MinHeap()
        self.arvore_rubro_negra = ArvoreRubroNegra()

    def cadastrar(self, evento):
        """Cadastra um evento nas três estruturas."""
        if self.arvore_avl.buscar(evento.id) is not None:
            raise ValueError("Já existe um evento com esse ID.")

        self.arvore_avl.inserir(evento)
        self.heap.inserir(evento)
        self.arvore_rubro_negra.inserir(evento)

        return evento

    def buscar(self, id_evento):
        """Busca um evento pelo ID usando a AVL."""
        return self.arvore_avl.buscar(id_evento)

    def proximo_evento(self):
        """Retorna o evento mais próximo usando o Min-Heap."""
        return self.heap.consultar_proximo()

    def listar_eventos(self):
        """Lista todos os eventos em ordem cronológica."""
        return self.arvore_rubro_negra.em_ordem()

    def consultar_intervalo(self, inicio, fim):
        """Consulta eventos entre duas datas."""
        if inicio > fim:
            raise ValueError("A data inicial não pode ser posterior à final.")

        return self.arvore_rubro_negra.consultar_intervalo(inicio, fim)

    def remover(self, id_evento):
        """Remove um evento das três estruturas."""
        evento = self.arvore_avl.buscar(id_evento)

        if evento is None:
            return None

        self.arvore_avl.remover(id_evento)
        self.arvore_rubro_negra.remover(evento.data_hora, evento.id)

        # Reconstrói o heap sem o evento removido.
        self.heap = MinHeap()
        for item in self.arvore_avl.em_ordem():
            self.heap.inserir(item)

        return evento

    def atualizar(self, id_evento, novo_evento):
        """Atualiza os dados de um evento mantendo os índices sincronizados."""
        if id_evento != novo_evento.id:
            raise ValueError("O ID do evento não pode ser alterado.")

        antigo = self.arvore_avl.buscar(id_evento)

        if antigo is None:
            return None

        self.remover(id_evento)
        self.cadastrar(novo_evento)

        return novo_evento

    def quantidade(self):
        """Retorna a quantidade de eventos cadastrados."""
        return len(self.arvore_avl.em_ordem())
