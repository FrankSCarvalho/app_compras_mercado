# System Patterns — app_compras_mercado

## Arquitetura geral

Duas camadas em dois módulos Python, sem framework web e sem ORM:

```
main.py       → Camada de interface (Flet) + regras de negócio/validação
  │  importa e chama
  ▼
database.py   → Camada de persistência (SQLite via sqlite3, módulo padrão)
  │
  ▼
compras.db    → Arquivo SQLite local (raiz do projeto, não versionado)
```

- **`main.py`**: contém `main(page: ft.Page)` que monta toda a UI e **todo o estado de
  execução vive como variáveis locais dessa função** (lista `produtos`, controles de
  texto, diálogos etc.). As funções de manipulação (`adicionar_produto`,
  `salvar_produto`, `excluir_produto`, `alternar_comprado`, etc.) são *closures*
  definidas dentro de `main` e capturam `page` e os controles.
- **`database.py`**: módulo autônomo e reutilizável. Cada função abre a própria
  conexão (`sqlite3.connect`) dentro de `with closing(...)` e faz `commit`.
  Recebe `db_path` como parâmetro com default `DB_DEFAULT_PATH = "compras.db"`.

## Padrões técnicos críticos

1. **Estado em memória sincronizado com o banco**:
   - `produtos` (lista de dicts) é a fonte de verdade da camada visual.
   - Chaves do dict por produto: `id`, `nome`, `quantidade`, `preco`, `subtotal`,
     `comprado` (bool) e `_item` (referência ao `ft.Container` visual criado).
   - **Atenção**: o banco usa `preco_unitario`, a memória usa `preco` — a tradução
     ocorre em `carregar_produtos()` e `criar_item_produto()`.
   - A chave `_item` é guardada no dict do produto e usada por
     `atualizar_item_visual()` para recriar o card na mesma posição da `ListView`.
2. **Subtotal e total calculados em memória** (nunca persistidos):
   - `subtotal = quantidade * preco` **apenas quando ambos não forem `None`**;
     senão `subtotal = None` e a UI exibe "—".
   - `total_compra = sum(p["subtotal"] for p in produtos if p["subtotal"] is not None)`.
3. **Valores opcionais com NULL**: quantidade e preço podem ser `None`
   (campo em branco). `formatar_moeda(None)` retorna "—".
4. **Migração idempotente de schema**: `inicializar_banco()` cria a tabela com
   `CREATE TABLE IF NOT EXISTS` e, via `_requer_migracao()` (PRAGMA `table_info`),
   detecta bancos antigos com `NOT NULL` em `quantidade`/`preco_unitario` e recria a
   tabela preservando dados/IDs (rename → create → copy → drop).
5. **Diálogo único reutilizado** para adicionar e editar: `dialogo_produto`, com
   `titulo_dialogo`/`botao_acao_dialogo` ajustados dinamicamente por
   `abrir_dialogo()` (modo adicionar) e `abrir_edicao_produto()` (modo salvar);
   `produto_em_edicao` guarda o produto em edição ou `None`.
6. **Validação de entrada** (em `adicionar_produto` e `salvar_produto`):
   - nome: obrigatório, `.strip()` não vazio;
   - quantidade: opcional; se preenchida → `float(valor.replace(",", "."))`, deve ser `> 0`;
   - preço: opcional; se preenchido → idem, deve ser `>= 0`;
   - erros mostrados em `mensagem_erro` (texto vermelho no diálogo).
7. **Erros de banco tratados na UI**: chamadas a `database.*` em `adicionar_produto`
   e `salvar_produto` ficam em `try/except` exibindo mensagem no diálogo.

## Eventos e operações principais

| Operação | Handler (closure em `main`) | Persistência |
|----------|------------------------------|--------------|
| Carregar ao iniciar | `carregar_produtos()` | `database.buscar_produtos()` |
| Adicionar | `adicionar_produto(e)` → `criar_item_produto()` | `database.inserir_produto(nome, quantidade, preco)` retorna `id` |
| Editar | `abrir_edicao_produto()` → `salvar_produto(e)` → `atualizar_item_visual()` | `database.atualizar_produto(id, nome, quantidade, preco)` |
| Excluir | `abrir_confirmacao_exclusao()` → `excluir_produto()` | `database.excluir_produto(id)` |
| Marcar comprado | `alternar_comprado()` | `database.atualizar_comprado(id, bool)` |
| Abrir formulário (novo) | `abrir_dialogo()` | — |
| Fechar diálogo | `fechar_dialogo()` | `page.pop_dialog()` |

## Árvore de componentes Flet (tela principal)

```
page
└─ ft.Column (expand, spacing=20)
   ├─ titulo  : ft.Text "Minha Lista de Compras" (24, BOLD, CENTER)
   ├─ area_produtos : ft.Container (expand, border GREY_300, radius 10, CENTER)
   │   └─ ft.Stack (expand)
   │       ├─ mensagem_vazia : ft.Text "Sua lista está vazia" (cinza)
   │       └─ lista_produtos : ft.ListView (expand, spacing=8)
   │           └─ item_produto (por produto): ft.Container (WHITE, border, radius 8, padding 12)
   │               └─ ft.Column (spacing=4)
   │                   ├─ ft.Row (SPACE_BETWEEN, nome com expand)
   │                   │   ├─ checkbox   : ft.Checkbox (comprado)
   │                   │   ├─ texto_nome : ft.Text (16, BOLD)
   │                   │   ├─ texto_qtd  : ft.Text "Qtd: N"
   │                   │   ├─ botao_editar : ft.IconButton (EDIT_OUTLINED, azul)
   │                   │   └─ botao_excluir: ft.IconButton (DELETE_OUTLINE, vermelho)
   │                   └─ ft.Row (SPACE_BETWEEN)
   │                       ├─ texto_preco   : ft.Text "Preço: R$ ..."
   │                       └─ texto_subtotal: ft.Text "Subtotal: R$ ..." (BOLD)
   ├─ total : ft.Row (SPACE_BETWEEN) → "Total:" + texto_total
   └─ botao_adicionar : ft.FilledButton "Adicionar Produto" (width=inf, height=48)
```

Diálogos:
- `dialogo_produto` (modal): `campo_nome`, `campo_quantidade`, `campo_preco`,
  `mensagem_erro` + ações "Cancelar" / "Adicionar" | "Salvar".
- `dialogo_exclusao` (não modal, criado sob demanda): "Cancelar" / "Excluir".

## Decisões arquiteturais já tomadas

- **Sem ORM**: `sqlite3` puro (módulo padrão); SQL explícito como constante.
- **Sem persistência de subtotal/total**: derivados em memória; evita dados redundantes.
- **`comprado` como `INTEGER NOT NULL DEFAULT 0`** (0/1 em SQLite), convertido para
  bool na camada de UI.
- **Quantidade e preço unitário opcionais (NULL)**: decisão central do produto —
  "montar a lista em casa e preencher depois".
- **Ordem por `id`** (`ORDER BY id`), equivalente à ordem de inserção.
- **Formatação monetária pt-BR** definida localmente em `formatar_moeda()` (troca de
  separadores), sem biblioteca `locale`.
- **App em arquivo único** (`main.py`); sem separação em views/controllers.
- **Execução via `ft.run(main)`** (API atual do Flet).