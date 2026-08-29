# Product Context — app_compras_mercado

## Por que o projeto existe

Ir ao supermercado com uma lista desorganizada (papel, aplicativos genéricos de notas)
gera esquecimentos e gastos acima do planejado. O projeto nasce para oferecer uma
ferramenta simples e direta de **lista de compras**, com foco em pouca fricção:
adicionar o produto, estimar o custo e marcar o que já foi pego na loja.

## Problema que resolve

- **Esquecimento de itens**: centralizar a lista em um único lugar, persistida entre
  execuções (SQLite local), em vez de um app que perde dados ao fechar.
- **Controle de custo**: preço unitário opcional por produto, com subtotal por item e
  total geral estimado, todos formatados em moeda brasileira (R$).
- **Rastreio durante a compra**: checkbox "comprado" para saber o que já foi pego
  (visual riscado/atenuado).
- **Criação gradual da lista**: em casa se anota apenas o nome; quantidade e preço
  podem ser preenchidos depois (campos opcionais que aceitam NULL no banco).

## Usuário esperado

- Pessoa individual que faz compras de mercado e quer planejar e acompanhar sua lista
  no celular (via app do Flet) e/ou no computador (desktop).
- Não há multi-usuário, contas ou autenticação: é uma ferramenta pessoal e local.
- A interface é inteiramente em **português (pt-BR)**, com formatação de moeda
  brasileira e letras "—" quando quantidade/preço não informados.

## Como a aplicação funciona (fluxo principal)

1. **Início**: `database.inicializar_banco()` cria/migra a tabela `produtos` e
   `carregar_produtos()` popula a tela com o que já está salvo. Se vazia, mostra
   "Sua lista está vazia".
2. **Adicionar**: botão "Adicionar Produto" abre um diálogo com *Nome do produto*
   (obrigatório), *Quantidade* (opcional) e *Preço unitário* (opcional). O subtotal é
   calculado apenas quando quantidade e preço estão presentes.
3. **Editar**: botão de lápis em cada item reabre o mesmo diálogo com os dados
   preenchidos (modo "Salvar").
4. **Excluir**: botão de lixeira abre confirmação e remove do banco e da tela.
5. **Marcar comprado**: checkbox por item persiste o estado e aplica o estilo
   riscado/cinza.
6. **Total**: somatório dos subtotais não nulos, atualizado a cada operação.

## Experiência do usuário

- Tela única (sem navegação entre páginas), voltada para uso rápido.
- Diálogos modais para formulário e confirmação.
- Feedback imediato de erro em `mensagem_erro` (vermelho) para validações.
- Execução multi-plataforma via Flet: desktop nativo e celular Android/iOS durante o
  desenvolvimento (`flet run --android main.py`).

## Premissas e limites registrados

- Os dados ficam somente no dispositivo (arquivo `compras.db`); não há backup ou
  exportação.
- O total geral **não filtra** produtos marcados como comprados (somam-se todos os
  subtotais não nulos).
- Não há categorias, pesquisa, favoritos, listas múltiplas ou ordenação manual:
  a ordem é a ordem de inserção (`ORDER BY id`).