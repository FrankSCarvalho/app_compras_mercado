# Progress — app_compras_mercado

> Status consolidado em **2026-08-29** a partir do código em `HEAD` (`a2ecb62`).
> Legenda: ✅ feito · 🟠 parcial · ⬜ não existe / ideia futura

## Funcionalidades

| Funcionalidade | Status | Evidência no código |
|----------------|--------|---------------------|
| Persistência SQLite (`produtos` em `compras.db`) | ✅ | `database.py` (CRUD completo + `inicializar_banco`) |
| Adicionar produto (nome, quantidade, preço) | ✅ | `adicionar_produto()` → `database.inserir_produto()` |
| Listar produtos carregados do banco | ✅ | `carregar_produtos()` → `database.buscar_produtos()` |
| Editar produto | ✅ | `salvar_produto()` → `database.atualizar_produto()` + `atualizar_item_visual()` |
| Excluir produto (com confirmação) | ✅ | `abrir_confirmacao_exclusao()` / `excluir_produto()` |
| Marcar/desmarcar "comprado" (persistido) | ✅ | `alternar_comprado()` → `database.atualizar_comprado()` |
| Quantidade e preço opcionais (NULL → "—") | ✅ | colunas nullable + validação opcional em add/save |
| Subtotal por item e total geral | ✅ | cálculo em memória (`subtotal`/`total_compra`) |
| Validações de entrada (nome, qtd > 0, preço >= 0, vírgula decimal) | ✅ | `adicionar_produto()` e `salvar_produto()` |
| Migração de schema (bancos antigos NOT NULL) | ✅ | `_requer_migracao()` / `_migrar_tabela()` |
| Mensagem de lista vazia | ✅ | `mensagem_vazia` (Stack + visibilidade) |
| Interface toda em pt-BR / moeda R$ | ✅ | textos e `formatar_moeda()` |
| Teste manual da camada de banco | ✅ | `test_database.py` (script manual; usa banco temporário e imprime "RESULTADO DO TESTE: PASS") |
| Teste de exibição (Qtd/Preço/Subtotal/"—") com mock Flet | ✅ (descartável) | `tmp_full.py` (extrai funções de `main.py` via AST + mock) |
| **`flet build apk` / distribuição móvel** | 🟠 (documentado, **não validado**) | procedimento presente no README, mas estrutura necessária (`src/`, `assets/`, `pyproject.toml`) **ausente** e sem evidência de execução bem-sucedida |
| **QR Code / câmera / leitura de código de barras** | ⬜ | **não existe** nenhuma implementação no código |
| **Exportar/limpar lista após compra** | ⬜ | não existe |
| **Categorias / pesquisa / favoritos** | ⬜ | não existe |
| **Listas múltiplas / múltiplos usuários / nuvem** | ⬜ | não existe; app é pessoal e local |
| **Histórico de compras** | ⬜ | não existe |
| **Total filtrar itens comprados** | ⬜ | comportamento atual soma tudo (decisão registrada) |

## O que está pronto

- Ciclo completo de uso: criar lista, adicionar produtos com/sem preço, ver total,
  marcar comprado durante a compra, editar e excluir.
- Banco local idempotente (criação + migração automática) e camada `database.py`
  testável isoladamente.
- Instruções de execução desktop e Android (dev) no `README.md`.

## O que falta / está pendente (dívidas técnicas)

1. Corrigir **docstring desatualizada** no topo de `database.py` ("banco ainda NÃO
   está conectado" — já está conectado).
2. Decidir o destino do **`tmp_full.py`** (teste descartável versionado no `main`).
3. Validar/estruturar o **build de APK** (`flet build apk`) — exige `src/`, `assets/
   icon.png` e `pyproject.toml`, hoje ausentes.
4. Avaliar teclado numérico nos campos de quantidade/preço (não exibe vírgula em
   alguns teclados).
5. Não há pipeline de testes automatizados (pytest/unittest) nem CI.

## Ideias futuras (NÃO implementadas — aguardam decisão)

- QR Code / código de barras com câmera (apenas mencionado pelo usuário; zero código).
- Qualquer outro recurso só deve entrar em `progress.md` após existir no código.

## Estado geral do desenvolvimento

Estágio **funcional em ambiente local/desktop** (e Android em modo dev via Flet app).
Sem release, sem build de produção versionado, sem testes automatizados em CI.
Evolução recente foi rápida e concentrada entre 24–26/08/2026.