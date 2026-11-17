
class MinHeap:
    """Heap que mantém o evento mais próximo na raiz."""

    def __init__(self):
        self.elementos = []

    def __len__(self):
        return len(self.elementos)

    def esta_vazia(self):
        return len(self.elementos) == 0

    def _chave(self, evento):
        return (evento.data_hora, evento.id)

    def inserir(self, evento):
        self.elementos.append(evento)
        self._subir(len(self.elementos) - 1)

    def _subir(self, indice):
        while indice > 0:
            pai = (indice - 1) // 2

            if self._chave(self.elementos[indice]) < self._chave(
                self.elementos[pai]
            ):
                self.elementos[indice], self.elementos[pai] = (
                    self.elementos[pai],
                    self.elementos[indice],
                )
                indice = pai
            else:
                break

    def consultar_proximo(self):
        if self.esta_vazia():
            return None

        return self.elementos[0]

    def remover_proximo(self):
        if self.esta_vazia():
            return None

        if len(self.elementos) == 1:
            return self.elementos.pop()

        proximo = self.elementos[0]
        self.elementos[0] = self.elementos.pop()
        self._descer(0)

        return proximo

    def _descer(self, indice):
        tamanho = len(self.elementos)

        while True:
            menor = indice
            esquerda = 2 * indice + 1
            direita = 2 * indice + 2

            if (
                esquerda < tamanho
                and self._chave(self.elementos[esquerda])
                < self._chave(self.elementos[menor])
            ):
                menor = esquerda

            if (
                direita < tamanho
                and self._chave(self.elementos[direita])
                < self._chave(self.elementos[menor])
            ):
                menor = direita

            if menor == indice:
                break

            self.elementos[indice], self.elementos[menor] = (
                self.elementos[menor],
                self.elementos[indice],
            )

            indice = menor

    def visualizar(self):
        return list(self.elementos)
