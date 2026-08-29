# Active Context — app_compras_mercado

> Atualizado em: **2026-08-29** (data desta análise; último commit do projeto: `a2ecb62`, 2026-08-26).

## Estado atual (commit `a2ecb62` — branch `main`, sincronizado com `origin/main`)

O aplicativo está funcional para o fluxo completo de lista de compras:

- CRUD de produtos com persistência SQLite (`compras.db`).
- Quantidade e preço unitário opcionais (NULL no banco; "—" na tela).
- Subtotal por item e total geral (moeda pt-BR).
- Checkbox "comprado" com persistência e estilo visual.
- Edição e exclusão com diálogos; validações de entrada.
- Migração automática de bancos antigos (colunas `quantidade`/`preco_unitario` com
  `NOT NULL` → permitindo `NULL`).

Árvore de trabalho limpa (sem alterações em arquivos rastreados no momento desta
análise).

## Mudanças recentes (por ordem do histórico)

- `b19e43f` (2026-08-26) e `a2ecb62` (2026-08-26): implementação completa do CRUD —
  adição/edição/exclusão de produtos, marcação "comprado", totais, migração do banco e
  novo teste integrado `tmp_full.py`.
- `a5872df` (2026-08-24): criação do `.gitignore` e refatoração de `main.py`.
- `f87e16d` (2026-08-24): criação de `database.py` e `test_database.py`.
- Commits iniciais em `main.py`: evolução incremental da interface e dos handlers.

## Pontos de atenção antes de modificar o projeto

1. **Duas chaves para o mesmo dado**: banco `preco_unitario` vs memória/UI `preco` —
   qualquer alteração precisa traduzir nos dois lugares (`buscar_produtos` →
   `carregar_produtos`, edição, `salvar_produto`).
2. **Estado fechado em `main()`**: toda a lógica e controles vivem como closures/variáveis
   locais de `main` — testes unitários exigem mocks (o `tmp_full.py` usa AST) ou
   refatoração planejada.
3. **Subtotal/total derivados**: sempre `None` quando falta quantidade ou preço; a soma
   do total **ignora** subtotais `None` e **não** filtra produtos comprados.
4. **`database.py` é reutilizável** (aceita `db_path`): é a camada ideal para testes
   com bancos temporários (como faz `test_database.py`).
5. **`compras.db` não é versionado**: mudanças de schema devem ser feitas por migração
   idempotente em `inicializar_banco()`; bancos locais antigos precisarão da migração.
6. Não há estrutura `src/`, `assets/` ou `pyproject.toml` — o comando
   `flet build apk` do README ainda **não** foi aplicado/validado no projeto.

## Inconsistências conhecidas

1. Docstring desatualizada em `database.py` (linhas iniciais): afirma que o banco
   "ainda NÃO está conectado à aplicação (main.py)", mas `main.py` chama
   `database.inicializar_banco()`, `database.buscar_produtos()`,
   `database.inserir_produto()`, `database.atualizar_produto()`,
   `database.atualizar_comprado()` e `database.excluir_produto()`. **Código é a verdade**;
   a docstring deve ser corrigida em uma futura sessão.
2. `tmp_full.py` é um **teste integrado descartável** (ver comentários internos) que foi
   versionado no `main` — não afeta o app, mas é candidato a remoção/movimentação.
3. README diz "Python 3.10 ou superior": o `.venv` local usa Python **3.14.5** —
   ok, mas nenhum CI/teste confirma compatibilidade mínima.
4. `campo_quantidade` e `campo_preco` usam teclado numérico (`KeyboardType.NUMBER`),
   porém a entrada aceita vírgula decimal — experiência em teclados mobile pode ser
   desconfortável.

## Próximos passos lógicos (não definidos oficialmente no repositório)

- Nada de roadmap explícito existe no código/README. Ideias mencionadas em conversas
  anteriores (fono: **QR Code / escaneamento de código de barras / câmera**) **não
  existem no código** e **não foram implementadas**. Registrar como ideias futuras
  até decisão do usuário.
- Correções candidatas (somente quando autorizadas): docstring de `database.py`,
  remover/mover `tmp_full.py`, revisar teclado numérico dos campos decimais.