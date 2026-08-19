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

    # Botão para adicionar produto
    botao_adicionar = ft.FilledButton(
        "Adicionar Produto",
        icon=ft.Icons.ADD,
        width=float("inf"),
        height=48,
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