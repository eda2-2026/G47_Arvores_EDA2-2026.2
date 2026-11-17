
import sqlite3
from datetime import datetime

from models.evento import Evento


class Persistencia:
    def __init__(self, caminho="database/eventos.db"):
        self.caminho = caminho
        self._criar_tabela()

    def _conectar(self):
        return sqlite3.connect(self.caminho)

    def _criar_tabela(self):
        with self._conectar() as conexao:
            conexao.execute("""
                CREATE TABLE IF NOT EXISTS eventos (
                    id INTEGER PRIMARY KEY,
                    nome TEXT NOT NULL,
                    descricao TEXT,
                    categoria TEXT NOT NULL,
                    local TEXT NOT NULL,
                    data_hora TEXT NOT NULL,
                    vagas INTEGER NOT NULL
                )
            """)

    def salvar(self, evento):
        with self._conectar() as conexao:
            conexao.execute("""
                INSERT OR REPLACE INTO eventos
                (id, nome, descricao, categoria, local, data_hora, vagas)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                evento.id,
                evento.nome,
                evento.descricao,
                evento.categoria,
                evento.local,
                evento.data_hora.isoformat(),
                evento.vagas,
            ))

    def listar(self):
        with self._conectar() as conexao:
            linhas = conexao.execute("""
                SELECT id, nome, descricao, categoria, local, data_hora, vagas
                FROM eventos
                ORDER BY data_hora, id
            """).fetchall()

        return [
            Evento(
                id=linha[0],
                nome=linha[1],
                descricao=linha[2],
                categoria=linha[3],
                local=linha[4],
                data_hora=datetime.fromisoformat(linha[5]),
                vagas=linha[6],
            )
            for linha in linhas
        ]

    def remover(self, id_evento):
        with self._conectar() as conexao:
            cursor = conexao.execute(
                "DELETE FROM eventos WHERE id = ?",
                (id_evento,),
            )
            return cursor.rowcount > 0
