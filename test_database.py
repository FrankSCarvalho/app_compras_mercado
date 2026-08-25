"""Teste simples da camada de banco de dados (database.py).

Usa um arquivo temporário para não interferir no banco real (compras.db).
O arquivo temporário é removido ao final.
"""

import os
import sqlite3
import tempfile
from contextlib import closing

import database


def mostrar_estrutura(db_path):
    """Exibe a estrutura (colunas) da tabela produtos."""
    with closing(sqlite3.connect(db_path)) as conn:
        colunas = conn.execute("PRAGMA table_info(produtos)").fetchall()
    print("Estrutura da tabela 'produtos':")
    print(f"{'cid':<4} {'name':<15} {'type':<10} {'notnull':<8} {'dflt_value':<12} {'pk':<3}")
    for cid, name, tipo, notnull, dflt, pk in colunas:
        print(f"{cid:<4} {name:<15} {tipo:<10} {'S' if notnull else 'N':<8} {str(dflt):<12} {pk}")


def main():
    # Cria um arquivo temporário para o banco do teste.
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    try:
        print("== Inicializando banco ==")
        database.inicializar_banco(db_path)

        print("== Inserindo produto de teste ==")
        prod_id = database.inserir_produto(
            "Produto de teste", quantidade=3, preco_unitario=2.50, comprado=0, db_path=db_path
        )
        assert prod_id is not None and prod_id > 0, "Falha ao inserir produto"
        print(f"  Produto inserido com id = {prod_id}")

        print("== Buscando o produto ==")
        produtos = database.buscar_produtos(db_path)
        assert len(produtos) == 1, f"Esperado 1 produto, obtido {len(produtos)}"
        produto = produtos[0]
        assert produto["id"] == prod_id
        assert produto["nome"] == "Produto de teste"
        assert produto["quantidade"] == 3
        assert produto["preco_unitario"] == 2.50
        assert produto["comprado"] == 0
        print(f"  Produto encontrado: {produto}")

        print("== Atualizando estado de comprado ==")
        database.atualizar_comprado(prod_id, True, db_path)
        produtos = database.buscar_produtos(db_path)
        assert produtos[0]["comprado"] == 1, "Estado 'comprado' não foi atualizado para 1"
        print(f"  Estado comprado atualizado: {produtos[0]['comprado']}")

        print("== Excluindo o produto ==")
        database.excluir_produto(prod_id, db_path)
        produtos = database.buscar_produtos(db_path)
        assert len(produtos) == 0, f"Produto não foi removido: {produtos}"
        print("  Produto removido com sucesso")

        print()
        print("RESULTADO DO TESTE: PASS")
        print()
        mostrar_estrutura(db_path)

    finally:
        # Remove o arquivo temporário criado para o teste.
        if os.path.exists(db_path):
            os.remove(db_path)
            print()
            print(f"Arquivo temporário removido: {db_path}")


if __name__ == "__main__":
    main()