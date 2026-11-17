
class NoAVL:
    def __init__(self, evento):
        self.evento = evento
        self.esquerda = None
        self.direita = None
        self.altura = 1


class ArvoreAVL:
    def __init__(self):
        self.raiz = None

    def _altura(self, no):
        return no.altura if no else 0

    def _atualizar_altura(self, no):
        no.altura = 1 + max(
            self._altura(no.esquerda),
            self._altura(no.direita)
        )

    def _fator_balanceamento(self, no):
        if no is None:
            return 0

        return (
            self._altura(no.esquerda)
            - self._altura(no.direita)
        )

    def _rotacao_direita(self, y):
        x = y.esquerda
        subarvore = x.direita

        x.direita = y
        y.esquerda = subarvore

        self._atualizar_altura(y)
        self._atualizar_altura(x)

        return x

    def _rotacao_esquerda(self, x):
        y = x.direita
        subarvore = y.esquerda

        y.esquerda = x
        x.direita = subarvore

        self._atualizar_altura(x)
        self._atualizar_altura(y)

        return y

    def inserir(self, evento):
        self.raiz = self._inserir(self.raiz, evento)

    def _inserir(self, no, evento):
        if no is None:
            return NoAVL(evento)

        if evento.id < no.evento.id:
            no.esquerda = self._inserir(no.esquerda, evento)
        elif evento.id > no.evento.id:
            no.direita = self._inserir(no.direita, evento)
        else:
            raise ValueError("Já existe um evento com esse ID.")

        self._atualizar_altura(no)

        balanceamento = self._fator_balanceamento(no)

        # Caso LL
        if balanceamento > 1 and evento.id < no.esquerda.evento.id:
            return self._rotacao_direita(no)

        # Caso RR
        if balanceamento < -1 and evento.id > no.direita.evento.id:
            return self._rotacao_esquerda(no)

        # Caso LR
        if balanceamento > 1 and evento.id > no.esquerda.evento.id:
            no.esquerda = self._rotacao_esquerda(no.esquerda)
            return self._rotacao_direita(no)

        # Caso RL
        if balanceamento < -1 and evento.id < no.direita.evento.id:
            no.direita = self._rotacao_direita(no.direita)
            return self._rotacao_esquerda(no)

        return no

    def buscar(self, id_evento):
        atual = self.raiz

        while atual is not None:
            if id_evento == atual.evento.id:
                return atual.evento

            if id_evento < atual.evento.id:
                atual = atual.esquerda
            else:
                atual = atual.direita

        return None

    def remover(self, id_evento):
        self.raiz = self._remover(self.raiz, id_evento)

    def _menor_no(self, no):
        atual = no

        while atual.esquerda is not None:
            atual = atual.esquerda

        return atual

    def _remover(self, no, id_evento):
        if no is None:
            return None

        if id_evento < no.evento.id:
            no.esquerda = self._remover(no.esquerda, id_evento)

        elif id_evento > no.evento.id:
            no.direita = self._remover(no.direita, id_evento)

        else:
            if no.esquerda is None:
                return no.direita

            if no.direita is None:
                return no.esquerda

            sucessor = self._menor_no(no.direita)
            no.evento = sucessor.evento
            no.direita = self._remover(
                no.direita,
                sucessor.evento.id
            )

        self._atualizar_altura(no)

        balanceamento = self._fator_balanceamento(no)

        # Caso LL
        if balanceamento > 1 and self._fator_balanceamento(no.esquerda) >= 0:
            return self._rotacao_direita(no)

        # Caso LR
        if balanceamento > 1 and self._fator_balanceamento(no.esquerda) < 0:
            no.esquerda = self._rotacao_esquerda(no.esquerda)
            return self._rotacao_direita(no)

        # Caso RR
        if balanceamento < -1 and self._fator_balanceamento(no.direita) <= 0:
            return self._rotacao_esquerda(no)

        # Caso RL
        if balanceamento < -1 and self._fator_balanceamento(no.direita) > 0:
            no.direita = self._rotacao_direita(no.direita)
            return self._rotacao_esquerda(no)

        return no

    def em_ordem(self):
        resultado = []

        def percorrer(no):
            if no is not None:
                percorrer(no.esquerda)
                resultado.append(no.evento)
                percorrer(no.direita)

        percorrer(self.raiz)
        return resultado
