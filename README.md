# app_compras_mercado

Aplicativo de lista de compras desenvolvido com [Flet](https://flet.dev) (Python).

## Requisitos

- Python 3.10 ou superior
- Flet 0.86.5

## Instalação

```bash
# Criar e ativar o ambiente virtual
python -m venv .venv
.venv\Scripts\activate

# Instalar as dependências
pip install -r requirements.txt
```

## Executar a aplicação

```bash
.venv\Scripts\python.exe main.py
```

## Testar em um celular Android

### Pré-requisitos

1. **No celular:** Instale o aplicativo **Flet** na Google Play Store:
   - Nome: Flet
   - ID: `com.appveyor.flet`
   - Link: https://play.google.com/store/apps/details?id=com.appveyor.flet

2. **Rede:** O celular e o computador devem estar conectados à **mesma rede Wi-Fi** (ou rede local).

3. **No Windows:** Nenhuma ferramenta adicional é necessária. O Flet CLI já está disponível no ambiente virtual.

### Passos

1. Execute o comando abaixo no terminal (na raiz do projeto):

   ```bash
   .venv\Scripts\flet.exe run --android main.py
   ```

2. Um **QR code** será exibido no terminal.

3. No celular:
   - Abra o aplicativo **Flet**.
   - Aponte a câmera para o QR code (ou use o botão "+" no app e digite a URL exibida).
   - A aplicação abrirá no celular.

### Recursos

- **Hot reload:** Alterações no `main.py` são refletidas instantaneamente no celular.
- **Voltar à tela inicial do Flet App:** Pressione e segure com 3 dedos em qualquer lugar da tela, ou agite o celular.

### Gerar APK (para distribuição)

Para gerar um APK instalável, use o comando:

```bash
.venv\Scripts\flet.exe build apk
```

**Observações:**
- Requer JDK 17 e Android SDK (instalados automaticamente na primeira execução).
- O projeto precisa ter a estrutura recomendada (`src/main.py`, `assets/icon.png`, `pyproject.toml` ou `requirements.txt`).
- O APK gerado é uma versão de **release** (otimizada para produção, sem suporte a debug).