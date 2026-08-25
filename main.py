import flet as ft


def main(page: ft.Page):
    page.title = "Lista de Compras"
    page.padding = 20
    page.spacing = 20

    # Lista de produtos em memória
    produtos = []

    # Título no topo
    titulo = ft.Text(
        "Minha Lista de Compras",
        size=24,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    # Mensagem de lista vazia
    mensagem_vazia = ft.Text(
        "Sua lista está vazia",
        size=16,
        color=ft.Colors.GREY,
        text_align=ft.TextAlign.CENTER,
    )

    # Lista de produtos (ListView)
    lista_produtos = ft.ListView(
        expand=True,
        spacing=8,
        padding=0,
    )

    # Área central reservada para os produtos
    area_produtos = ft.Container(
        content=ft.Stack(
            controls=[
                mensagem_vazia,
                lista_produtos,
            ],
            expand=True,
        ),
        expand=True,
        alignment=ft.Alignment.CENTER,
        border=ft.Border.all(1, ft.Colors.GREY_300),
        border_radius=10,
        padding=20,
    )

    # Área inferior com o total
    texto_total = ft.Text("R$ 0,00", size=18, weight=ft.FontWeight.BOLD)
    total = ft.Row(
        controls=[
            ft.Text("Total:", size=18, weight=ft.FontWeight.BOLD),
            texto_total,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # Campos do formulário de produto
    campo_nome = ft.TextField(
        label="Nome do produto",
        autofocus=True,
    )
    campo_quantidade = ft.TextField(
        label="Quantidade",
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    campo_preco = ft.TextField(
        label="Preço unitário",
        keyboard_type=ft.KeyboardType.NUMBER,
        prefix="R$ ",
    )

    # Mensagem de erro
    mensagem_erro = ft.Text(
        "",
        size=14,
        color=ft.Colors.RED,
        visible=False,
    )

    def formatar_moeda(valor):
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def adicionar_produto(e):
        # Validação do nome
        nome = campo_nome.value.strip()
        if not nome:
            mensagem_erro.value = "O nome do produto não pode estar vazio."
            mensagem_erro.visible = True
            page.update()
            return

        # Validação da quantidade
        try:
            quantidade = float(campo_quantidade.value.replace(",", "."))
            if quantidade <= 0:
                raise ValueError
        except (ValueError, AttributeError):
            mensagem_erro.value = "A quantidade deve ser um número maior que zero."
            mensagem_erro.visible = True
            page.update()
            return

        # Validação do preço
        try:
            preco = float(campo_preco.value.replace(",", "."))
            if preco < 0:
                raise ValueError
        except (ValueError, AttributeError):
            mensagem_erro.value = "O preço deve ser um número maior ou igual a zero."
            mensagem_erro.visible = True
            page.update()
            return

        # Calcular subtotal
        subtotal = quantidade * preco

        # Adicionar produto à lista
        produtos.append(
            {
                "nome": nome,
                "quantidade": quantidade,
                "preco": preco,
                "subtotal": subtotal,
            }
        )

        # Criar item visual do produto
        item_produto = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(nome, size=16, weight=ft.FontWeight.BOLD, expand=True),
                            ft.Text(f"Qtd: {quantidade:g}", size=14),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Row(
                        controls=[
                            ft.Text(f"Preço: {formatar_moeda(preco)}", size=14, color=ft.Colors.GREY),
                            ft.Text(f"Subtotal: {formatar_moeda(subtotal)}", size=14, weight=ft.FontWeight.BOLD),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
                spacing=4,
            ),
            padding=12,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            bgcolor=ft.Colors.WHITE,
        )

        # Adicionar item à lista visual
        lista_produtos.controls.append(item_produto)

        # Calcular o total da compra (soma dos subtotais)
        total_compra = sum(p["subtotal"] for p in produtos)

        # Atualizar o campo Total na parte inferior
        texto_total.value = formatar_moeda(total_compra)

        # Ocultar mensagem de lista vazia
        mensagem_vazia.visible = False

        # Limpar campos do formulário
        campo_nome.value = ""
        campo_quantidade.value = ""
        campo_preco.value = ""
        mensagem_erro.value = ""
        mensagem_erro.visible = False

        # Fechar o formulário
        fechar_dialogo()

        # Atualizar a página
        page.update()

    # Diálogo do formulário de produto
    dialogo_produto = ft.AlertDialog(
        modal=True,
        title=ft.Text("Adicionar Produto"),
        content=ft.Column(
            controls=[
                campo_nome,
                campo_quantidade,
                campo_preco,
                mensagem_erro,
            ],
            tight=True,
            spacing=12,
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: fechar_dialogo()),
            ft.FilledButton("Adicionar", on_click=adicionar_produto),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def abrir_dialogo():
        mensagem_erro.value = ""
        mensagem_erro.visible = False
        page.show_dialog(dialogo_produto)

    def fechar_dialogo():
        page.pop_dialog()

    # Botão para adicionar produto
    botao_adicionar = ft.FilledButton(
        "Adicionar Produto",
        icon=ft.Icons.ADD,
        width=float("inf"),
        height=48,
        on_click=lambda e: abrir_dialogo(),
    )

    # Estrutura principal da tela
    page.add(
        ft.Column(
            controls=[
                titulo,
                area_produtos,
                total,
                botao_adicionar,
            ],
            expand=True,
            spacing=20,
        )
    )


ft.run(main)