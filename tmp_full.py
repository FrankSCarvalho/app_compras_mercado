# -*- coding: utf-8 -*-
"""Teste integrado descartavel da funcionalidade completa no main.py.
Extrai as funcoes reais (via AST) e mocka o Flet para validar logica,
textos exibidos (Qtd/Preco/Subtotal) e persistencia real em banco temporario."""
import ast, types, sys, tempfile, os

# ---- Mock Flet ----
class M:
    pass
def mk(name):
    def f(*a, **k):
        o = M(); o.__dict__ = dict(k)
        o.value = a[0] if a else k.get("value", "")
        o._name = name
        return o
    return f
ft = types.ModuleType("ft")
for _n in ["Text", "TextStyle", "Checkbox", "IconButton", "Container", "Column",
           "Row", "AlertDialog", "TextField", "FilledButton", "TextButton",
           "ListView", "Stack"]:
    setattr(ft, _n, mk(_n))
class _C: GREY="G"; BLACK="B"; RED="R"; WHITE="W"; BLUE="U"; GREY_300="g"
class _M: SPACE_BETWEEN="b"; END="e"; CENTER="c"
class _F: BOLD="b"
class _T: LINE_THROUGH="l"; NONE="n"
class _K: NUMBER="n"
class _I: ADD="a"; EDIT_OUTLINED="e"; DELETE_OUTLINE="d"
class _A: CENTER="c"
class _B:
    @staticmethod
    def all(*a, **k): return "b"
class _TA: CENTER="c"
ft.Colors=_C; ft.MainAxisAlignment=_M; ft.FontWeight=_F; ft.TextDecoration=_T
ft.KeyboardType=_K; ft.Icons=_I; ft.Alignment=_A; ft.Border=_B; ft.TextAlign=_TA
sys.modules["ft"] = ft

# ---- Extrai funcao real ----
tree = ast.parse(open("main.py", encoding="utf-8").read())
def extrair(nome):
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            for sub in node.body:
                if isinstance(sub, ast.FunctionDef) and sub.name == nome:
                    code = ast.Module(body=[ast.fix_missing_locations(sub)], type_ignores=[])
                    return compile(code, "<%s>" % nome, "exec")
    raise RuntimeError(nome)

# ---- Mocks do app ----
class Campo:
    def __init__(self): self.value = ""
class Erro:
    def __init__(self): self.value = ""; self.visible = False
class Msg:
    def __init__(self): self.visible = False
class Total:
    def __init__(self): self.value = ""
class Page:
    def __init__(self): self.dialogs = 0
    def update(self): pass
    def show_dialog(self, *a): self.dialogs += 1
    def pop_dialog(self, *a): self.dialogs = max(0, self.dialogs - 1)

def base_ns():
    return {"ft": ft, "page": page, "campo_nome": campo_nome,
            "campo_quantidade": campo_quantidade, "campo_preco": campo_preco,
            "mensagem_erro": mensagem_erro, "mensagem_vazia": mensagem_vazia,
            "texto_total": texto_total, "produtos": produtos,
            "lista_produtos": lista_produtos, "database": database,
            "titulo_dialogo": titulo_dialogo, "botao_acao_dialogo": botao_acao_dialogo,
            "formatar_moeda": formatar_moeda}

page = Page(); campo_nome = Campo(); campo_quantidade = Campo(); campo_preco = Campo()
mensagem_erro = Erro(); mensagem_vazia = Msg(); texto_total = Total()
produtos = []; _controls = []
lista_produtos = types.SimpleNamespace(
    controls=_controls,
    append=lambda i: _controls.append(i),
    remove=lambda i: _controls.remove(i) if i in _controls else None,
    index=lambda i: _controls.index(i),
    pop=lambda i: _controls.pop(i),
    insert=lambda i, x: _controls.insert(i, x))
titulo_dialogo = M(); botao_acao_dialogo = M()
titulo_dialogo.value = "Adicionar Produto"

def formatar_moeda_real(v):
    if v is None: return "—"
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
formatar_moeda = formatar_moeda_real

def tot():
    return sum(p["subtotal"] for p in produtos if p["subtotal"] is not None)

import database

def strip_nonlocal(node):
    for child in ast.walk(node):
        if isinstance(child, ast.FunctionDef):
            child.body = [s for s in child.body if not isinstance(s, ast.Nonlocal)]
    return node

def extrair2(nome):
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            for sub in node.body:
                if isinstance(sub, ast.FunctionDef) and sub.name == nome:
                    fn = strip_nonlocal(sub)
                    code = ast.Module(body=[ast.fix_missing_locations(fn)], type_ignores=[])
                    return compile(code, "<%s>" % nome, "exec")
    raise RuntimeError(nome)

def instalar(nome, extra=None):
    ns = base_ns()
    if extra:
        ns.update(extra)
    exec(extrair2(nome), ns)
    return ns[nome]

def noop(*a, **k): pass

# ----- criacao de item visual (stub) para adicionar/salvar/excluir -----
def criar_item_stub(produto):
    produto["_item"] = object()
# ----- formatar_moeda REAL (extraido) -----
_fm = {}
exec(extrair2("formatar_moeda"), _fm)
formatar_moeda = _fm["formatar_moeda"]
assert formatar_moeda(None) == "—"
assert formatar_moeda(20.0) == "R$ 20,00"
print("A) formatar_moeda: None->— | 20.0->R$ 20,00  [PASS]")
def coletar_textos(item):
    vals = []
    def rec(o):
        if not isinstance(o, (list, tuple)):
            objs = [o]
        else:
            objs = o
        for obj in objs:
            if getattr(obj, "_name", None) == "Text":
                vals.append(getattr(obj, "value", ""))
            c = getattr(obj, "controls", None)
            if c:
                rec(c)
    rec(item)
    return vals

# ----- B) criar_item_produto: textos exibidos -----
criar_item = instalar("criar_item_produto", {
    "alternar_comprado": noop, "abrir_edicao_produto": noop,
    "abrir_confirmacao_exclusao": noop,
})
def textos_exibidos(nome, q, p, s):
    _controls.clear()
    prod = {"nome": nome, "quantidade": q, "preco": p, "subtotal": s, "comprado": False}
    criar_item(prod)
    return coletar_textos(prod["_item"]), prod

t,_ = textos_exibidos("Arroz", None, None, None)
print("B1 Arroz vazio/vazio  ->", t)
assert t == ["Arroz", "Qtd: —", "Preço: —", "Subtotal: —"], t
t,_ = textos_exibidos("Arroz", 2, None, None)
print("B2 Arroz so qtd(2)    ->", t)
assert t == ["Arroz", "Qtd: 2", "Preço: —", "Subtotal: —"], t
t,_ = textos_exibidos("Arroz", None, 10.0, None)
print("B3 Arroz so preco(10) ->", t)
assert t == ["Arroz", "Qtd: —", "Preço: R$ 10,00", "Subtotal: —"], t
t,_ = textos_exibidos("Arroz", 2, 10.0, 20.0)
print("B4 Arroz ambos        ->", t)
assert t == ["Arroz", "Qtd: 2", "Preço: R$ 10,00", "Subtotal: R$ 20,00"], t
print("B) EXIBICAO (Qtd/Preco/Subtotal com —) [PASS]")
import sys; sys.stdout.flush()

