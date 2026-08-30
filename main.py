import flet as ft

import database


def main(page: ft.Page):
    page.title = "Lista de Compras"
    page.theme_mode = ft.ThemeMode.LIGHT
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
        # Seguro para None: exibe "—" em vez de tentar formatar
        if valor is None:
            return "—"
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def excluir_produto(e, produto, item_produto):
        # Fechar a caixa de confirmação
        page.pop_dialog()

        # Excluir o produto do banco de dados (SQLite) primeiro
        database.excluir_produto(produto["id"])

        # Remover o produto da lista em memória
        produtos.remove(produto)

        # Remover o item visual da lista
        lista_produtos.controls.remove(item_produto)

        # Recalcular o total da compra (soma somente produtos com subtotal)
        total_compra = sum(
            p["subtotal"] for p in produtos if p["subtotal"] is not None
        )
        texto_total.value = formatar_moeda(total_compra)

        # Se não houver mais produtos, mostrar a mensagem de lista vazia
        if not produtos:
            mensagem_vazia.visible = True

        # Atualizar a página
        page.update()

    def abrir_confirmacao_exclusao(e, produto, item_produto):
        # Caixa de confirmação nativa do Flet antes de excluir
        dialogo_exclusao = ft.AlertDialog(
            modal=False,
            title=ft.Text("Excluir produto?"),
            content=ft.Text(f"Deseja excluir \"{produto['nome']}\" da lista?"),
            actions=[
                # "Cancelar" fecha a confirmação sem alterar nada
                ft.TextButton("Cancelar", on_click=lambda e: page.pop_dialog()),
                # "Excluir" chama a função que exclui do banco e da memória
                ft.FilledButton(
                    "Excluir",
                    on_click=lambda e: excluir_produto(e, produto, item_produto),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.show_dialog(dialogo_exclusao)

    def alternar_comprado(e, produto, texto_nome, texto_qtd, texto_preco, texto_subtotal):
        # Persistir o estado "comprado" no banco de dados usando o id do produto
        database.atualizar_comprado(produto["id"], e.control.value)

        # Atualizar o estado do produto na lista em memória
        produto["comprado"] = e.control.value

        if e.control.value:
            # Produto comprado: riscar o nome e atenuar os dados
            texto_nome.style = ft.TextStyle(
                decoration=ft.TextDecoration.LINE_THROUGH,
                color=ft.Colors.GREY,
            )
            texto_qtd.color = ft.Colors.GREY
            texto_preco.color = ft.Colors.GREY
            texto_subtotal.color = ft.Colors.GREY
        else:
            # Produto desmarcado: voltar ao estado normal
            texto_nome.style = ft.TextStyle(
                decoration=ft.TextDecoration.NONE,
                color=ft.Colors.BLACK,
            )
            texto_qtd.color = ft.Colors.BLACK
            texto_preco.color = ft.Colors.GREY
            texto_subtotal.color = ft.Colors.BLACK

        page.update()

    def criar_item_produto(produto):
        # Extrai os dados do produto (que possui a chave "preco")
        nome = produto["nome"]
        quantidade = produto["quantidade"]
        preco = produto["preco"]
        subtotal = produto["subtotal"]
        comprado = bool(produto["comprado"])

        # Textos do produto (para controle visual ao marcar como comprado)
        texto_nome = ft.Text(nome, size=16, weight=ft.FontWeight.BOLD, expand=True)
        texto_qtd = ft.Text(
            ("Qtd: —" if quantidade is None else f"Qtd: {quantidade:g}"),
            size=14,
        )
        texto_preco = ft.Text(
            f"Preço: {formatar_moeda(preco)}",
            size=14,
            color=ft.Colors.GREY,
        )
        texto_subtotal = ft.Text(
            f"Subtotal: {formatar_moeda(subtotal)}",
            size=14,
            weight=ft.FontWeight.BOLD,
        )

        # Checkbox para marcar o produto como comprado
        checkbox = ft.Checkbox(
            value=comprado,
            on_change=lambda e: alternar_comprado(
                e, produto, texto_nome, texto_qtd, texto_preco, texto_subtotal
            ),
        )

        # Aplica o estilo de "comprado" quando o produto já chega marcado
        if comprado:
            texto_nome.style = ft.TextStyle(
                decoration=ft.TextDecoration.LINE_THROUGH,
                color=ft.Colors.GREY,
            )
            texto_qtd.color = ft.Colors.GREY
            texto_preco.color = ft.Colors.GREY
            texto_subtotal.color = ft.Colors.GREY

        # Botão para editar o produto
        botao_editar = ft.IconButton(
            icon=ft.Icons.EDIT_OUTLINED,
            icon_color=ft.Colors.BLUE,
            tooltip="Editar produto",
            on_click=lambda e: abrir_edicao_produto(produto),
        )

        # Botão para excluir o produto
        botao_excluir = ft.IconButton(
            icon=ft.Icons.DELETE_OUTLINE,
            icon_color=ft.Colors.RED,
            tooltip="Excluir produto",
            on_click=lambda e: abrir_confirmacao_exclusao(e, produto, item_produto),
        )

        # Criar item visual do produto
        item_produto = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            checkbox,
                            texto_nome,
                            texto_qtd,
                            botao_editar,
                            botao_excluir,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Row(
                        controls=[
                            texto_preco,
                            texto_subtotal,
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

        # Guardar referência ao item visual (usada na edição para recriar o card)
        produto["_item"] = item_produto

        # Adicionar item à lista visual
        lista_produtos.controls.append(item_produto)

    def carregar_produtos():
        # Busca os produtos já salvos no banco de dados
        for item in database.buscar_produtos():
            # Subtotal: calculado somente quando quantidade E preco existirem
            if item["quantidade"] is not None and item["preco_unitario"] is not None:
                subtotal = item["quantidade"] * item["preco_unitario"]
            else:
                subtotal = None
            produto = {
                "id": item["id"],
                "nome": item["nome"],
                "quantidade": item["quantidade"],
                "preco": item["preco_unitario"],
                "subtotal": subtotal,
                "comprado": bool(item["comprado"]),
            }
            produtos.append(produto)
            criar_item_produto(produto)

        # Ocultar a mensagem de lista vazia se houver produtos
        mensagem_vazia.visible = not produtos

        # Recalcular o total da compra (soma somente produtos com subtotal)
        total_compra = sum(
            p["subtotal"] for p in produtos if p["subtotal"] is not None
        )
        texto_total.value = formatar_moeda(total_compra)

    def adicionar_produto(e):
        # Validação do nome (continua obrigatório)
        nome = campo_nome.value.strip()
        if not nome:
            mensagem_erro.value = "O nome do produto não pode estar vazio."
            mensagem_erro.visible = True
            page.update()
            return

        # Quantidade é opcional: campo vazio => None
        valor_quantidade = (campo_quantidade.value or "").strip()
        if valor_quantidade == "":
            quantidade = None
        else:
            try:
                quantidade = float(valor_quantidade.replace(",", "."))
                if quantidade <= 0:
                    raise ValueError
            except (ValueError, AttributeError):
                mensagem_erro.value = "A quantidade deve ser um número maior que zero."
                mensagem_erro.visible = True
                page.update()
                return

        # Preço unitário é opcional: campo vazio => None
        valor_preco = (campo_preco.value or "").strip()
        if valor_preco == "":
            preco = None
        else:
            try:
                preco = float(valor_preco.replace(",", "."))
                if preco < 0:
                    raise ValueError
            except (ValueError, AttributeError):
                mensagem_erro.value = "O preço deve ser um número maior ou igual a zero."
                mensagem_erro.visible = True
                page.update()
                return

        # Subtotal: calculado somente quando quantidade E preço estiverem presentes
        if quantidade is not None and preco is not None:
            subtotal = quantidade * preco
        else:
            subtotal = None

        # Salvar o produto no banco de dados e obter o id gerado
        try:
            produto_id = database.inserir_produto(nome, quantidade, preco)
        except Exception as erro:
            mensagem_erro.value = f"Não foi possível salvar o produto: {erro}"
            mensagem_erro.visible = True
            page.update()
            return

        # Adicionar produto à lista (mesmo quando quantidade ou preço forem None)
        produto = {
            "id": produto_id,
            "nome": nome,
            "quantidade": quantidade,
            "preco": preco,
            "subtotal": subtotal,
            "comprado": False,
        }
        produtos.append(produto)

        # Criar e adicionar o item visual do produto
        criar_item_produto(produto)

        # Total geral: soma somente os produtos cujo subtotal não é None
        total_compra = sum(
            p["subtotal"] for p in produtos if p["subtotal"] is not None
        )

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

    # Estado do produto em edição (None = novo produto / adição)
    produto_em_edicao = None

    # Título e botão de ação dinâmicos do formulário de produto
    titulo_dialogo = ft.Text("Adicionar Produto")
    botao_acao_dialogo = ft.FilledButton("Adicionar", on_click=adicionar_produto)

    # Diálogo do formulário de produto (reutilizado para adicionar e editar)
    dialogo_produto = ft.AlertDialog(
        modal=True,
        title=titulo_dialogo,
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
            botao_acao_dialogo,
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def abrir_dialogo():
        # Ajusta o formulário para o modo "adicionar"
        nonlocal produto_em_edicao
        produto_em_edicao = None
        titulo_dialogo.value = "Adicionar Produto"
        botao_acao_dialogo.text = "Adicionar"
        botao_acao_dialogo.on_click = adicionar_produto
        mensagem_erro.value = ""
        mensagem_erro.visible = False
        page.show_dialog(dialogo_produto)

    def abrir_edicao_produto(produto):
        # Preenche o formulário com os dados atuais do produto
        nonlocal produto_em_edicao
        produto_em_edicao = produto
        campo_nome.value = produto["nome"]
        # Quantidade/preço ausentes (None) iniciam o campo vazio
        campo_quantidade.value = (
            "" if produto["quantidade"] is None
            else "{:g}".format(produto["quantidade"])
        )
        campo_preco.value = (
            "" if produto["preco"] is None
            else "{:g}".format(produto["preco"])
        )
        mensagem_erro.value = ""
        mensagem_erro.visible = False
        # Ajusta título e botão de ação para o modo edição
        titulo_dialogo.value = "Editar Produto"
        botao_acao_dialogo.text = "Salvar"
        botao_acao_dialogo.on_click = salvar_produto
        page.show_dialog(dialogo_produto)

    def atualizar_item_visual(produto):
        # Recria o item visual do produto na mesma posição que estava
        item_antigo = produto.get("_item")
        if item_antigo in lista_produtos.controls:
            indice = lista_produtos.controls.index(item_antigo)
            lista_produtos.controls.pop(indice)
            criar_item_produto(produto)
            novo_item = produto["_item"]
            lista_produtos.controls.remove(novo_item)
            lista_produtos.controls.insert(indice, novo_item)

    def salvar_produto(e):
        nonlocal produto_em_edicao
        produto = produto_em_edicao

        # Validação do nome (mesmas regras do cadastro)
        nome = campo_nome.value.strip()
        if not nome:
            mensagem_erro.value = "O nome do produto não pode estar vazio."
            mensagem_erro.visible = True
            page.update()
            return

        # Validação da quantidade (opcional: campo vazio => None)
        valor_quantidade = (campo_quantidade.value or "").strip()
        if valor_quantidade == "":
            quantidade = None
        else:
            try:
                quantidade = float(valor_quantidade.replace(",", "."))
                if quantidade <= 0:
                    raise ValueError
            except (ValueError, AttributeError):
                mensagem_erro.value = "A quantidade deve ser um número maior que zero."
                mensagem_erro.visible = True
                page.update()
                return

        # Validação do preço (opcional: campo vazio => None)
        valor_preco = (campo_preco.value or "").strip()
        if valor_preco == "":
            preco = None
        else:
            try:
                preco = float(valor_preco.replace(",", "."))
                if preco < 0:
                    raise ValueError
            except (ValueError, AttributeError):
                mensagem_erro.value = "O preço deve ser um número maior ou igual a zero."
                mensagem_erro.visible = True
                page.update()
                return

        # Subtotal: calculado somente quando quantidade E preço estiverem presentes
        if quantidade is not None and preco is not None:
            subtotal = quantidade * preco
        else:
            subtotal = None

        # Atualizar o produto no banco de dados (SQLite)
        try:
            database.atualizar_produto(produto["id"], nome, quantidade, preco)
        except Exception as erro:
            mensagem_erro.value = f"Não foi possível salvar o produto: {erro}"
            mensagem_erro.visible = True
            page.update()
            return

        # Atualizar os dados do produto em memória (preserva "id" e "comprado")
        produto["nome"] = nome
        produto["quantidade"] = quantidade
        produto["preco"] = preco
        produto["subtotal"] = subtotal

        # Atualizar o item visual correspondente
        atualizar_item_visual(produto)

        # Recalcular o total da compra (soma somente produtos com subtotal)
        total_compra = sum(
            p["subtotal"] for p in produtos if p["subtotal"] is not None
        )
        texto_total.value = formatar_moeda(total_compra)

        # Reset do estado de edição
        produto_em_edicao = None

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

    # Inicializar o banco de dados e carregar os produtos existentes
    database.inicializar_banco()
    carregar_produtos()
    page.update()


ft.run(main)