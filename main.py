import flet as ft


def main(page: ft.Page):
    page.title = "Lista de Compras"
    page.padding = 20
    page.spacing = 20

    # Título no topo
    titulo = ft.Text(
        "Minha Lista de Compras",
        size=24,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    # Área central reservada para os produtos
    area_produtos = ft.Container(
        content=ft.Text(
            "Sua lista está vazia",
            size=16,
            color=ft.Colors.GREY,
            text_align=ft.TextAlign.CENTER,
        ),
        expand=True,
        alignment=ft.Alignment.CENTER,
        border=ft.Border.all(1, ft.Colors.GREY_300),
        border_radius=10,
        padding=20,
    )

    # Área inferior com o total
    total = ft.Row(
        controls=[
            ft.Text("Total:", size=18, weight=ft.FontWeight.BOLD),
            ft.Text("R$ 0,00", size=18, weight=ft.FontWeight.BOLD),
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

    # Diálogo do formulário de produto
    dialogo_produto = ft.AlertDialog(
        modal=True,
        title=ft.Text("Adicionar Produto"),
        content=ft.Column(
            controls=[
                campo_nome,
                campo_quantidade,
                campo_preco,
            ],
            tight=True,
            spacing=12,
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: fechar_dialogo()),
            ft.FilledButton("Adicionar", on_click=lambda e: fechar_dialogo()),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def abrir_dialogo():
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