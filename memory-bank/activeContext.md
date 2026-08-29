# Active Context — app_compras_mercado

> Último commit conhecido do projeto: `a2ecb62` (branch `main`, 2026-08-26).
> Este documento descreve o estado **durável** do projeto; detalhes efêmeros da
> execução local (registros do `compras.db`, estado do working tree) não são mantidos
> aqui.

## Estado atual

O aplicativo está funcional para o fluxo completo de lista de compras:

- CRUD de produtos com persistência SQLite (`compras.db`).
- Quantidade e preço unitário opcionais (NULL no banco; "—" na tela).
- Subtotal por item e total geral (moeda pt-BR).
- Checkbox "comprado" com persistência e estilo visual.
- Edição e exclusão com diálogos; validações de entrada.
- Migração automática de bancos antigos (colunas `quantidade`/`preco_unitario` com
  `NOT NULL` → permitindo `NULL`).

## Mudanças relevantes (histórico)

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
6. **APK não validado**: não há estrutura `src/`, `assets/` ou `pyproject.toml` — o
   comando `flet build apk` do README é apenas procedimento **documentado**, sem
   evidência de execução bem-sucedida (ver `techContext.md`).

## Inconsistências conhecidas (documentação × código)

1. Docstring desatualizada em `database.py` (linhas iniciais): afirma que o banco
   "ainda NÃO está conectado à aplicação (main.py)", mas `main.py` chama
   `database.inicializar_banco()`, `database.buscar_produtos()`,
   `database.inserir_produto()`, `database.atualizar_produto()`,
   `database.atualizar_comprado()` e `database.excluir_produto()`. **Código é a verdade**;
   a docstring deve ser corrigida em uma futura sessão.
2. `tmp_full.py` é um **teste integrado descartável** (segundo cabeçalho e comentários
   internos) que foi versionado no `main` — não afeta o app, mas é candidato a
   remoção/movimentação.
3. Nenhum CI/teste confirma a compatibilidade mínima (**Python 3.10+**) declarada no
   README; só se observou execução local em Python mais novo (ver `techContext.md`).

## Registro importante

- **QR Code / câmera / leitura de código de barras NÃO são funcionalidades existentes.**
  Não há nenhuma implementação dessas features no código. Qualquer menção futura deve
  ser tratada exclusivamente como **ideia futura/não implementada** (detalhes em
  `progress.md`).

## Para onde vão os demais temas

- Dívidas técnicas e correções candidatas → `progress.md`.
- Versões, requisitos e ambiente observado → `techContext.md`.
- Tabela/colunas/migrações/API do banco → `banco_de_dados.md`.