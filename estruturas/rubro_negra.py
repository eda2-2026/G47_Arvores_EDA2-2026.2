
VERMELHO = "V"
PRETO = "P"


class NoRubroNegra:
    def __init__(self, evento, cor=VERMELHO):
        self.evento = evento
        self.cor = cor
        self.esquerda = None
        self.direita = None
        self.pai = None


class ArvoreRubroNegra:
    def __init__(self):
        self.NIL = NoRubroNegra(None, PRETO)
        self.NIL.esquerda = self.NIL
        self.NIL.direita = self.NIL
        self.raiz = self.NIL

    def _chave(self, evento):
        return (evento.data_hora, evento.id)

    def buscar(self, data_hora, id_evento):
        chave = (data_hora, id_evento)
        atual = self.raiz

        while atual != self.NIL:
            chave_atual = self._chave(atual.evento)
            if chave == chave_atual:
                return atual.evento
            if chave < chave_atual:
                atual = atual.esquerda
            else:
                atual = atual.direita

        return None

    def inserir(self, evento):
        novo = NoRubroNegra(evento)
        novo.esquerda = self.NIL
        novo.direita = self.NIL

        pai = self.NIL
        atual = self.raiz
        chave = self._chave(evento)

        while atual != self.NIL:
            pai = atual
            chave_atual = self._chave(atual.evento)

            if chave == chave_atual:
                raise ValueError("Evento já cadastrado nessa posição.")
            if chave < chave_atual:
                atual = atual.esquerda
            else:
                atual = atual.direita

        novo.pai = pai

        if pai == self.NIL:
            self.raiz = novo
        elif chave < self._chave(pai.evento):
            pai.esquerda = novo
        else:
            pai.direita = novo

        self._corrigir_insercao(novo)

    def _rotacao_esquerda(self, x):
        y = x.direita
        x.direita = y.esquerda

        if y.esquerda != self.NIL:
            y.esquerda.pai = x

        y.pai = x.pai

        if x.pai == self.NIL:
            self.raiz = y
        elif x == x.pai.esquerda:
            x.pai.esquerda = y
        else:
            x.pai.direita = y

        y.esquerda = x
        x.pai = y

    def _rotacao_direita(self, y):
        x = y.esquerda
        y.esquerda = x.direita

        if x.direita != self.NIL:
            x.direita.pai = y

        x.pai = y.pai

        if y.pai == self.NIL:
            self.raiz = x
        elif y == y.pai.direita:
            y.pai.direita = x
        else:
            y.pai.esquerda = x

        x.direita = y
        y.pai = x

    def _corrigir_insercao(self, z):
        while z.pai.cor == VERMELHO:
            if z.pai == z.pai.pai.esquerda:
                tio = z.pai.pai.direita

                if tio.cor == VERMELHO:
                    z.pai.cor = PRETO
                    tio.cor = PRETO
                    z.pai.pai.cor = VERMELHO
                    z = z.pai.pai
                else:
                    if z == z.pai.direita:
                        z = z.pai
                        self._rotacao_esquerda(z)

                    z.pai.cor = PRETO
                    z.pai.pai.cor = VERMELHO
                    self._rotacao_direita(z.pai.pai)
            else:
                tio = z.pai.pai.esquerda

                if tio.cor == VERMELHO:
                    z.pai.cor = PRETO
                    tio.cor = PRETO
                    z.pai.pai.cor = VERMELHO
                    z = z.pai.pai
                else:
                    if z == z.pai.esquerda:
                        z = z.pai
                        self._rotacao_direita(z)

                    z.pai.cor = PRETO
                    z.pai.pai.cor = VERMELHO
                    self._rotacao_esquerda(z.pai.pai)

        self.raiz.cor = PRETO

    def _menor_no(self, no):
        while no.esquerda != self.NIL:
            no = no.esquerda
        return no

    def _transplantar(self, u, v):
        if u.pai == self.NIL:
            self.raiz = v
        elif u == u.pai.esquerda:
            u.pai.esquerda = v
        else:
            u.pai.direita = v

        v.pai = u.pai

    def remover(self, data_hora, id_evento):
        chave = (data_hora, id_evento)
        z = self.raiz

        while z != self.NIL and self._chave(z.evento) != chave:
            if chave < self._chave(z.evento):
                z = z.esquerda
            else:
                z = z.direita

        if z == self.NIL:
            return None

        removido = z.evento
        y = z
        cor_original = y.cor

        if z.esquerda == self.NIL:
            x = z.direita
            self._transplantar(z, z.direita)
        elif z.direita == self.NIL:
            x = z.esquerda
            self._transplantar(z, z.esquerda)
        else:
            y = self._menor_no(z.direita)
            cor_original = y.cor
            x = y.direita

            if y.pai == z:
                x.pai = y
            else:
                self._transplantar(y, y.direita)
                y.direita = z.direita
                y.direita.pai = y

            self._transplantar(z, y)
            y.esquerda = z.esquerda
            y.esquerda.pai = y
            y.cor = z.cor

        if cor_original == PRETO:
            self._corrigir_remocao(x)

        return removido

    def _corrigir_remocao(self, x):
        while x != self.raiz and x.cor == PRETO:
            if x == x.pai.esquerda:
                irmao = x.pai.direita

                if irmao.cor == VERMELHO:
                    irmao.cor = PRETO
                    x.pai.cor = VERMELHO
                    self._rotacao_esquerda(x.pai)
                    irmao = x.pai.direita

                if irmao.esquerda.cor == PRETO and irmao.direita.cor == PRETO:
                    irmao.cor = VERMELHO
                    x = x.pai
                else:
                    if irmao.direita.cor == PRETO:
                        irmao.esquerda.cor = PRETO
                        irmao.cor = VERMELHO
                        self._rotacao_direita(irmao)
                        irmao = x.pai.direita

                    irmao.cor = x.pai.cor
                    x.pai.cor = PRETO
                    irmao.direita.cor = PRETO
                    self._rotacao_esquerda(x.pai)
                    x = self.raiz
            else:
                irmao = x.pai.esquerda

                if irmao.cor == VERMELHO:
                    irmao.cor = PRETO
                    x.pai.cor = VERMELHO
                    self._rotacao_direita(x.pai)
                    irmao = x.pai.esquerda

                if irmao.direita.cor == PRETO and irmao.esquerda.cor == PRETO:
                    irmao.cor = VERMELHO
                    x = x.pai
                else:
                    if irmao.esquerda.cor == PRETO:
                        irmao.direita.cor = PRETO
                        irmao.cor = VERMELHO
                        self._rotacao_esquerda(irmao)
                        irmao = x.pai.esquerda

                    irmao.cor = x.pai.cor
                    x.pai.cor = PRETO
                    irmao.esquerda.cor = PRETO
                    self._rotacao_direita(x.pai)
                    x = self.raiz

        x.cor = PRETO

    def em_ordem(self):
        resultado = []

        def percorrer(no):
            if no != self.NIL:
                percorrer(no.esquerda)
                resultado.append(no.evento)
                percorrer(no.direita)

        percorrer(self.raiz)
        return resultado

    def consultar_intervalo(self, inicio, fim):
        return [
            evento for evento in self.em_ordem()
            if inicio <= evento.data_hora <= fim
        ]
