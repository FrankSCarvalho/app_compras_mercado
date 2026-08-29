# Banco de Dados — app_compras_mercado

## Visão geral

- **Motor**: SQLite, acessado pelo módulo padrão `sqlite3` do Python.
- **Arquivo**: `compras.db`, na raiz do projeto (criado na primeira execução).
  **Não versionado** (`.gitignore` ignora `*.db`). O conteúdo do arquivo (registros)
  varia conforme o uso da aplicação e **não deve ser documentado no Memory Bank**.
- **Localização do código**: `database.py` (módulo autônomo; nenhuma dependência
  externa).
- **Conexão**: cada função do módulo abre e fecha a própria conexão
  (`with closing(sqlite3.connect(db_path)) as conn`), com `commit` no fim.
- **Default**: `DB_DEFAULT_PATH = "compras.db"`. Todas as funções aceitam
  `db_path` opcional — o que permite testes com bancos temporários.

## Tabela única: `produtos`

| Coluna           | Tipo      | Restrições                    | Observação |
|------------------|-----------|-------------------------------|------------|
| `id`             | `INTEGER` | `PRIMARY KEY AUTOINCREMENT`   | gerado pelo SQLite |
| `nome`           | `TEXT`    | `NOT NULL`                    | obrigatório na UI |
| `quantidade`     | `REAL`    | — (aceita NULL)               | opcional; `None` → NULL |
| `preco_unitario` | `REAL`    | — (aceita NULL)               | opcional; `None` → NULL |
| `comprado`       | `INTEGER` | `NOT NULL DEFAULT 0`          | 0 = não comprado, 1 = comprado |

DDL real (constante `_DDL_CRIAR_TABELA` em `database.py`):

```sql
CREATE TABLE IF NOT EXISTS produtos (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    nome           TEXT    NOT NULL,
    quantidade     REAL,
    preco_unitario REAL,
    comprado       INTEGER NOT NULL DEFAULT 0
)
```

## Relacionamentos

- **Nenhum**: existe uma única tabela (`produtos`) e a auxiliar `sqlite_sequence`
  (gerada automaticamente pelo `AUTOINCREMENT`). Não há FKs, joins nem outras
  entidades (sem categorias, listas múltiplas, usuários etc.).

## Migração de schema

- **Objetivo**: permitir `NULL` em `quantidade` e `preco_unitario` (bancos antigos
  tinham `NOT NULL`).
- **Detecção** — `_requer_migracao(conn)`: lê `PRAGMA table_info(produtos)` via
  `_schema_colunas(conn)` e verifica se alguma coluna de `_COLUNAS_NULABLES`
  (`quantidade`, `preco_unitario`) ainda tem `notnull`.
- **Execução** — `_migrar_tabela(conn)`, no padrão *rename → create → copy → drop*:
  1. `ALTER TABLE produtos RENAME TO produtos_antiga`
  2. recria `produtos` com o DDL desejado
  3. `INSERT INTO produtos (id, nome, quantidade, preco_unitario, comprado)
     SELECT ... FROM produtos_antiga` (preserva IDs e dados)
  4. `DROP TABLE produtos_antiga`
- **Trigger**: sempre em `inicializar_banco()` (cria a tabela se não existe e migra
  somente quando necessário). Idempotente.

## API do módulo `database`

| Função | Assinatura | Comportamento |
|--------|-----------|---------------|
| `inicializar_banco` | `(db_path=DB_DEFAULT_PATH)` | cria tabela + migração idempotente; faz `commit` |
| `inserir_produto` | `(nome, quantidade, preco_unitario, comprado=0, db_path=...)` | `INSERT`; retorna `cursor.lastrowid` (`id`) |
| `buscar_produtos` | `(db_path=...)` | `SELECT ... ORDER BY id`; retorna lista de dicts |
| `atualizar_produto` | `(id, nome, quantidade, preco_unitario, db_path=...)` | atualiza nome/qtd/preço; **preserva `comprado`** |
| `atualizar_comprado` | `(id, comprado, db_path=...)` | seta `comprado` para 0/1 |
| `excluir_produto` | `(id, db_path=...)` | `DELETE FROM produtos WHERE id = ?` |

Detalhes:
- `buscar_produtos` define `conn.row_factory = sqlite3.Row` e converte para dicts.
- `inserir_produto` normaliza `comprado` com `1 if comprado else 0`.
- Todos os SQLs são **parametrizados** (`?`).
- Não há função explícita para "limpar lista" ou "estatísticas".

## Regras de mapeamento UI ↔ banco

- Memória/UI usa `preco`; banco usa `preco_unitario` (traduzido em
  `carregar_produtos()` e no dict `produto`).
- `comprado` é `INTEGER` no banco e `bool` na UI (`bool(item["comprado"])`).
- `quantidade`/`preco_unitario` nulos no banco → `None` na memória → exibição "—".