"""Camada de persistência de dados usando SQLite (módulo padrão do Python).

Fornece funções para inicializar o banco e realizar operações básicas
(CRUD) sobre a tabela ``produtos``.

Nesta etapa o banco ainda NÃO está conectado à aplicação (main.py).
"""

import sqlite3
from contextlib import closing

# Caminho do arquivo local do banco de dados.
DB_DEFAULT_PATH = "compras.db"


def _conectar(db_path=DB_DEFAULT_PATH):
    """Abre e retorna uma conexão com o banco SQLite."""
    return sqlite3.connect(db_path)


def inicializar_banco(db_path=DB_DEFAULT_PATH):
    """Cria a tabela ``produtos`` caso ela ainda não exista."""
    with closing(_conectar(db_path)) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS produtos (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                nome           TEXT    NOT NULL,
                quantidade     REAL    NOT NULL,
                preco_unitario REAL    NOT NULL,
                comprado       INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        conn.commit()


def inserir_produto(nome, quantidade, preco_unitario, comprado=0, db_path=DB_DEFAULT_PATH):
    """Insere um novo produto e retorna o seu ``id`` gerado.

    ``comprado`` deve ser 0 (não comprado) ou 1 (comprado).
    """
    with closing(_conectar(db_path)) as conn:
        cursor = conn.execute(
            """
            INSERT INTO produtos (nome, quantidade, preco_unitario, comprado)
            VALUES (?, ?, ?, ?)
            """,
            (nome, quantidade, preco_unitario, 1 if comprado else 0),
        )
        conn.commit()
        return cursor.lastrowid


def buscar_produtos(db_path=DB_DEFAULT_PATH):
    """Retorna todos os produtos como uma lista de dicionários."""
    with closing(_conectar(db_path)) as conn:
        conn.row_factory = sqlite3.Row
        linhas = conn.execute(
            """
            SELECT id, nome, quantidade, preco_unitario, comprado
            FROM produtos
            ORDER BY id
            """
        ).fetchall()
        return [dict(linha) for linha in linhas]


def atualizar_produto(id, nome, quantidade, preco_unitario, db_path=DB_DEFAULT_PATH):
    """Atualiza nome, quantidade e preço unitário de um produto pelo seu ``id``.

    Preserva o valor atual da coluna ``comprado``.
    """
    with closing(_conectar(db_path)) as conn:
        conn.execute(
            """
            UPDATE produtos
            SET nome = ?, quantidade = ?, preco_unitario = ?
            WHERE id = ?
            """,
            (nome, quantidade, preco_unitario, id),
        )
        conn.commit()


def atualizar_comprado(id, comprado, db_path=DB_DEFAULT_PATH):
    """Atualiza o estado ``comprado`` de um produto pelo seu ``id``."""
    with closing(_conectar(db_path)) as conn:
        conn.execute(
            "UPDATE produtos SET comprado = ? WHERE id = ?",
            (1 if comprado else 0, id),
        )
        conn.commit()


def excluir_produto(id, db_path=DB_DEFAULT_PATH):
    """Exclui um produto pelo seu ``id``."""
    with closing(_conectar(db_path)) as conn:
        conn.execute("DELETE FROM produtos WHERE id = ?", (id,))
        conn.commit()