# Project Brief — app_compras_mercado

## Visão geral

`app_compras_mercado` é um aplicativo de **lista de compras de mercado** construído com
[Flet](https://flet.dev) (Python). O usuário cria e gerencia uma lista de produtos com
quantidade e preço unitário opcionais, marca itens como comprados e acompanha o total
estimado da compra. Os dados são persistidos localmente em um banco **SQLite**
(`compras.db`) usando apenas a biblioteca padrão do Python (`sqlite3`).

## Objetivo

Permitir que uma pessoa monte sua lista de compras no computador ou no celular, com a
capacidade de:

- adicionar produtos à lista (nome obrigatório; quantidade e preço opcionais);
- editar produtos já cadastrados;
- excluir produtos (com confirmação);
- marcar/desmarcar produtos como "comprado";
- visualizar quantidade, preço unitário, subtotal e total estimado da compra.

## Escopo atual (confirmado no código)

- Interface gráfica única em `main.py` com Flet.
- Persistência local em SQLite via `database.py`.
- CRUD completo da entidade *produto*.
- Nenhuma autenticação, sincronização na nuvem, histórico de compras, categorias ou
  compartilhamento existem no código atual.

## Stack resumida

| Camada          | Tecnologia                                      |
|-----------------|-------------------------------------------------|
| UI              | Flet 0.86.5 (`flet==0.86.5` no `requirements.txt`) |
| Linguagem       | Python (README exige 3.10+; `.venv` local usa 3.14.5) |
| Persistência    | SQLite via módulo padrão `sqlite3`              |
| Testes          | Scripts manuais (`test_database.py` e `tmp_full.py`) |

## Status

Em desenvolvimento ativo. As funcionalidades de gerenciamento da lista estão
**implementadas e funcionando** no estado atual do `main` (último commit `a2ecb62`).
Não há release, pacote PyPI ou build de APK versionado no repositório.

## Fonte da verdade

- Este documento reflete o estado do código em `HEAD` (commit `a2ecb62`).
- O **código-fonte** (`main.py`, `database.py`) é a fonte primária de verdade.
- O `README.md` é complementar e contém instruções de execução/instalação.