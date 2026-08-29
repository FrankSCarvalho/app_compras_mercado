# Tech Context — app_compras_mercado

## Stack e versões

| Item | Versão/Valor | Classificação | Onde consta |
|------|--------------|---------------|-------------|
| Python | **3.10+ (ou superior)** | ✅ Requisito oficial do projeto | `README.md` ("Python 3.10 ou superior") |
| Python no `.venv` | **3.14.5** | 🖥️ Apenas **ambiente de desenvolvimento observado** (Windows) — **não é requisito** | verificado via `python --version` |
| Flet | **0.86.5** | ✅ Versão fixada do projeto | `requirements.txt` (`flet==0.86.5`) |
| SQLite | stdlib do Python | ✅ dependência de biblioteca padrão, sem versão fixada pelo projeto | driver local observado: `sqlite3.sqlite_version` 3.50.4 (informação do ambiente, não requisito) |
| Banco gerado | `compras.db` (arquivo local, não versionado) | — | criado pelo app na raiz |
| Módulos externos | **apenas `flet`** | ✅ | `requirements.txt` |
| Sistema de desenvolvimento | Windows (Flet é cross-platform) | 🖥️ ambiente observado | ambiente atual |

> **Leitura obrigatória**:
> - **Python 3.10+** e **Flet 0.86.5** são os requisitos oficiais declarados pelo projeto.
> - **Python 3.14.5** é apenas a versão presente no ambiente local analisado; **não deve
>   ser tratada como requisito oficial** nem como a versão mínima do projeto.
> - **SQLite 3.50.4** é a versão dos drivers no ambiente local observado; o projeto usa
>   o `sqlite3` da stdlib, sem fixar versão do SQLite.
> - `requirements.txt` contém somente `flet==0.86.5`. `database.py` usa apenas módulos
>   da biblioteca padrão (`sqlite3`, `contextlib`).

## Ambiente de desenvolvimento (Windows)

- Ambiente virtual já existente em `.venv\` (ignorado pelo `.gitignore`).
- O shell do VS Code/terminal ativa o `.venv` automaticamente
  (`.venv\Scripts\activate.bat`).

## Instalação de dependências

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Executar a aplicação localmente

### Desktop (janela nativa)

```bash
.venv\Scripts\python.exe main.py
```

### Celular Android (durante o desenvolvimento)

```bash
.venv\Scripts\flet.exe run --android main.py
```

- Requer app **Flet** instalado no celular (Google Play, id `com.appveyor.flet`);
- celular e PC na mesma rede Wi-Fi; um **QR code** é exibido para conectar — este QR
  code é um **recurso do próprio Flet** descrito no README, **não** é uma funcionalidade
  do aplicativo `app_compras_mercado` (não há código de QR/câmera no projeto).

### Gerar APK (distribuição)

```bash
.venv\Scripts\flet.exe build apk
```

> ⚠️ **Status: procedimento DOCUMENTADO, NÃO validado.** O `README.md` registra o
> comando `flet build apk`, mas:
> - **não há evidência de que o processo tenha sido executado com sucesso neste projeto**;
> - a estrutura necessária indicada pelo próprio README (`src/main.py`, `assets/icon.png`,
>   `pyproject.toml` ou `requirements.txt`) **não existe** no repositório atual
>   (não há pastas `src/` nem `assets/`);
> - portanto, **a geração de APK não é uma funcionalidade de distribuição já validada** —
>   apenas um procedimento documentado para tentativa futura.
>
> Requer JDK 17 e Android SDK (instalados automaticamente na primeira execução, segundo
> o README).

## Estrutura de arquivos do repositório (HEAD)

```
app_compras_mercado/
├── .clinerules         # regras do Cline para leitura/manutenção do Memory Bank
├── .gitignore          # template Git + extras (dbs e tempCodeRunnerFile.py)
├── README.md           # instruções de instalação/execução/mobile
├── database.py         # camada de persistência SQLite (funções CRUD + migração)
├── main.py             # aplicação Flet (UI, validações, eventos)
├── memory-bank/        # documentação de contexto (Memory Bank)
│   ├── activeContext.md
│   ├── banco_de_dados.md
│   ├── productContext.md
│   ├── progress.md
│   ├── projectbrief.md
│   ├── systemPatterns.md
│   └── techContext.md
├── requirements.txt    # única dependência: flet==0.86.5
├── test_database.py    # script de teste manual da camada database (banco temporário)
└── tmp_full.py         # teste integrado descartável (mocka Flet via AST, valida UI)
```

Todos os arquivos acima estão **versionados** no branch `main`/`HEAD` (incluindo
`.clinerules` e `memory-bank/`, confirmado via `git ls-tree HEAD`).

NÃO versionados (existem localmente):
- `.venv\` — ambiente virtual.
- `compras.db` — banco de dados local gerado em execução (ignorado por `*.db`).
- `__pycache__\` — cache do Python.

## Convenções do código

- **Idioma**: nomes de funções, variáveis, textos da UI, docstrings e mensagens em
  português (pt-BR). `main.py` usa identificadores em pt; `database.py` usa nomes
  técnicos em SQL/pt misto.
- **Formatação de moeda**: helper `formatar_moeda(valor)` → `"R$ 1.234,56"`;
  `None` → `"—"`. Sem `locale`.
- **Quantidade exibida** como `"{:g}"` (formato compacto) quando preenchida; senão "Qtd: —".
- **Boas práticas de conexão**: `with closing(sqlite3.connect(...))` usado por **todas as
  funções** de `database.py` (com `commit` ao final); `conn.row_factory = sqlite3.Row`
  apenas em `buscar_produtos()`.
- **SQL de schema** definido como constante `_DDL_CRIAR_TABELA`; parâmetros sempre
  com `?` (SQL parametrizado, sem interpolação de strings).

## Limitações técnicas conhecidas

- `campo_quantidade` e `campo_preco` usam `ft.KeyboardType.NUMBER`, mas a validação
  aceita vírgula decimal (`replace(",", ".")`) — alguns teclados numéricos mobile não
  expõem vírgula/ponto facilmente.
- Não há testes automatizados via pytest/unittest; os testes são scripts executados
  manualmente.
- App inteiro em um único `main.py` (dificulta testes isolados; `tmp_full.py` contorna
  via AST).
- Sem controle de versão do schema além da migração simples (rename/copy/drop).