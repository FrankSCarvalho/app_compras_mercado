# Tech Context — app_compras_mercado

## Stack e versões

| Item | Versão/Valor | Onde consta |
|------|--------------|-------------|
| Python | **3.10+** (requisito) | `README.md` |
| Python no `.venv` local (Windows) | **3.14.5** | verificado via `python --version` no ambiente |
| Flet | **0.86.5** | `requirements.txt` (`flet==0.86.5`) e verificado no `.venv` |
| SQLite | stdlib do Python (**3.50.4** drivers) | `sqlite3.sqlite_version` |
| Banco gerado | `compras.db` (arquivo local, não versionado) | criado pelo app na raiz |
| Módulos externos | **apenas `flet`** | `requirements.txt` |
| Sistema | Windows (dev; Flet é cross-platform) | ambiente atual |

> Nota: `requirements.txt` contém somente `flet==0.86.5`. `database.py` usa apenas
> módulos da biblioteca padrão (`sqlite3`, `contextlib`).

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
- celular e PC na mesma rede Wi-Fi; um **QR code** (recurso do Flet, **não** é uma
  funcionalidade do app) é exibido para conectar.

### Gerar APK (distribuição)

```bash
.venv\Scripts\flet.exe build apk
```

- Requer JDK 17 e Android SDK (instalados automaticamente na primeira execução);
- exige estrutura recomendada (`src/main.py`, `assets/icon.png`, `pyproject.toml` ou
  `requirements.txt`) — **não aprovado ainda** no projeto atual (não há `src/` nem
  `assets/`).

## Estrutura de arquivos do repositório (HEAD)

```
app_compras_mercado/
├── .gitignore          # template Git + extras (dbs e tempCodeRunnerFile.py)
├── README.md           # instruções de instalação/execução/mobile
├── database.py         # camada de persistência SQLite (funções CRUD + migração)
├── main.py             # aplicação Flet (UI, validações, eventos)
├── requirements.txt    # única dependência: flet==0.86.5
├── test_database.py    # script de teste manual da camada database (banco temporário)
└── tmp_full.py         # teste integrado descartável (mocka Flet via AST, valida UI)
```

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