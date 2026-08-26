"""Camada de persistência de dados usando SQLite (módulo padrão do Python).

Fornece funções para inicializar o banco e realizar operações básicas
(CRUD) sobre a tabela ``produtos``.

Nesta etapa o banco ainda NÃO está conectado à aplicação (main.py).
"""

import sqlite3
from contextlib import closing

# Caminho do arquivo local do banco de dados.
DB_DEFAULT_PATH = "compras.db"

# Schema desejado da tabela ``produtos``.
# ``quantidade`` e ``preco_unitario`` são opcionais (aceitam NULL):
# o usuário pode montar a lista em casa e preencher quantidade/preço depois.
_DDL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS produtos (
        id             INTEGER PRIMARY KEY AUTOINCREMENT,
        nome           TEXT    NOT NULL,
        quantidade     REAL,
        preco_unitario REAL,
        comprado       INTEGER NOT NULL DEFAULT 0
    )
"""

# Colunas que devem passar a permitir NULL durante a migração.
_COLUNAS_NULABLES = ("quantidade", "preco_unitario")


def _conectar(db_path=DB_DEFAULT_PATH):
    """Abre e retorna uma conexão com o banco SQLite."""
    return sqlite3.connect(db_path)


def _schema_colunas(conn):
    """Retorna um dicionário {nome_coluna: {'notnull': 0 ou 1}} com base em
    ``PRAGMA table_info(produtos)``."""
    colunas = {}
    for linha in conn.execute("PRAGMA table_info(produtos)").fetchall():
        _, nome, _, notnull, _, _ = linha
        colunas[nome] = {"notnull": bool(notnull)}
    return colunas


def _requer_migracao(conn):
    """Indica se a tabela ``produtos`` ainda usa ``NOT NULL`` nas colunas
    ``quantidade`` e/ou ``preco_unitario`` (portanto precisa de migração)."""
    colunas = _schema_colunas(conn)
    if "quantidade" not in colunas or "preco_unitario" not in colunas:
        return False
    return any(colunas[nome]["notnull"] for nome in _COLUNAS_NULABLES)


def _migrar_tabela(conn):
    """Recria a tabela ``produtos`` sem ``NOT NULL`` em quantidade/preco,
    preservando todos os dados e IDs existentes.

    O SQLite não permite remover a restrição ``NOT NULL`` via ALTER TABLE,
    então a tabela é recriada (rename -> create -> copy -> drop).
    """
    conn.execute("ALTER TABLE produtos RENAME TO produtos_antiga")
    # Recria a tabela ``produtos`` com o schema desejado (nome livre novamente).
    conn.execute(_DDL_CRIAR_TABELA)
    conn.execute(
        """
        INSERT INTO produtos (id, nome, quantidade, preco_unitario, comprado)
        SELECT id, nome, quantidade, preco_unitario, comprado
        FROM produtos_antiga
        """
    )
    conn.execute("DROP TABLE produtos_antiga")


def inicializar_banco(db_path=DB_DEFAULT_PATH):
    """Cria a tabela ``produtos`` (já permitindo NULL em quantidade/preço)
    e executa a migração necessária para bancos existentes que ainda usavam
    ``NOT NULL`` nessas duas colunas."""
    with closing(_conectar(db_path)) as conn:
        # Para bancos novos, cria a tabela já com o schema desejado.
        conn.execute(_DDL_CRIAR_TABELA)
        # Para bancos existentes antigos, migra somente quando necessário.
        if _requer_migracao(conn):
            _migrar_tabela(conn)
        conn.commit()


def inserir_produto(nome, quantidade, preco_unitario, comprado=0, db_path=DB_DEFAULT_PATH):
    """Insere um novo produto e retorna o seu ``id`` gerado.

    ``quantidade`` e ``preco_unitario`` são opcionais: passe ``None``
    (ou omita o valor) quando ainda não souber esses dados; eles serão
    salvos como NULL no banco e podem ser preenchidos depois.

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

    ``quantidade`` e ``preco_unitario`` são opcionais: passe ``None`` para
    remover/limpar o valor (salvo como NULL no banco).

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