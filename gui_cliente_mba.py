# gui_cliente_mba.py
import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_BASE = "http://127.0.0.1:5000"  # ajuste se necessário


def normaliza_cpf(cpf: str) -> str:
    return "".join(ch for ch in cpf if ch.isdigit())


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MBA SENAC - Inscrições (Cliente API)")
        self.geometry("720x520")
        self.minsize(720, 520)

        self.container = ttk.Frame(self, padding=16)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        for F in (TelaPrincipal, TelaCadastrar, TelaConsultarMenu,
                  TelaConsultarUsuario, TelaResultadoLista):
            frame = F(parent=self.container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.show("TelaPrincipal")

    def show(self, name):
        self.frames[name].tkraise()

    # --- chamadas de API ---
    def api_register(self, payload: dict):
        try:
            r = requests.post(f"{API_BASE}/users/register", json=payload, timeout=10)
            data = r.json() if "application/json" in r.headers.get("content-type", "") else r.text
            return r.status_code, data
        except requests.RequestException as e:
            return 0, {"error": f"Falha de conexão: {e}"}

    def api_find(self, cpf: str, dn: str):
        try:
            params = {"cpf": cpf, "datadeNascimento": dn}
            r = requests.get(f"{API_BASE}/users/find", params=params, timeout=10)
            data = r.json() if "application/json" in r.headers.get("content-type", "") else r.text
            return r.status_code, data
        except requests.RequestException as e:
            return 0, {"error": f"Falha de conexão: {e}"}

    def api_all(self):
        try:
            r = requests.get(f"{API_BASE}/users/all", timeout=10)
            data = r.json() if "application/json" in r.headers.get("content-type", "") else r.text
            return r.status_code, data
        except requests.RequestException as e:
            return 0, {"error": f"Falha de conexão: {e}"}


# --------------------- Base de telas ---------------------
class BaseTela(ttk.Frame):
    def titulo(self, text):
        lbl = ttk.Label(self, text=text, font=("Segoe UI", 16, "bold"))
        lbl.pack(anchor="w", pady=(0, 12))
        return lbl

    def linha(self):
        sep = ttk.Separator(self, orient="horizontal")
        sep.pack(fill="x", pady=8)
        return sep

    def botoes_confirmar_voltar(self, on_confirm, on_back,
                                text_confirm="Confirmar", text_back="Voltar"):
        btns = ttk.Frame(self)
        btns.pack(anchor="e", pady=(12, 0))
        b1 = ttk.Button(btns, text=text_confirm, command=on_confirm)
        b0 = ttk.Button(btns, text=text_back, command=on_back)
        b1.grid(row=0, column=0, padx=(0, 8))
        b0.grid(row=0, column=1)
        return b1, b0


# --------------------- Telas ---------------------
class TelaPrincipal(BaseTela):
    def __init__(self, parent, controller: App):
        super().__init__(parent)
        self.controller = controller

        self.titulo("Digite a opção desejada:")
        self.linha()

        body = ttk.Frame(self)
        body.pack(fill="both", expand=True)

        ttk.Button(body, text="Cadastrar Usuário",
                   command=lambda: controller.show("TelaCadastrar"), width=40).pack(pady=8)

        ttk.Button(body, text="Consultar",
                   command=lambda: controller.show("TelaConsultarMenu"), width=40).pack(pady=8)


class TelaCadastrar(BaseTela):
    def __init__(self, parent, controller: App):
        super().__init__(parent)
        self.controller = controller

        self.titulo("Cadastrar Usuário")
        self.linha()

        form = ttk.Frame(self)
        form.pack(fill="x")

        self.var_nome = tk.StringVar()
        self.var_cpf = tk.StringVar()
        self.var_dn = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_tel = tk.StringVar()
        self.var_sexo = tk.StringVar()

        self._entrada(form, "Nome Completo", self.var_nome, 0)
        self._entrada(form, "CPF", self.var_cpf, 1)
        self._entrada(form, "Data de Nascimento (YYYY-MM-DD)", self.var_dn, 2)
        self._entrada(form, "Email", self.var_email, 3)
        self._entrada(form, "Telefone", self.var_tel, 4)
        self._entrada(form, "Sexo", self.var_sexo, 5)

        self.botoes_confirmar_voltar(self.on_confirm,
                                     lambda: controller.show("TelaPrincipal"))

    def _entrada(self, parent, label, var, row):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=4)
        e = ttk.Entry(parent, textvariable=var, width=50)
        e.grid(row=row, column=1, sticky="ew", padx=8, pady=4)
        parent.grid_columnconfigure(1, weight=1)
        return e

    def on_confirm(self):
        nome = self.var_nome.get().strip()
        cpf = normaliza_cpf(self.var_cpf.get().strip())
        dn = self.var_dn.get().strip()
        email = self.var_email.get().strip()
        tel = self.var_tel.get().strip()
        sexo = self.var_sexo.get().strip()

        obrig = {"Nome Completo": nome, "CPF": cpf, "Data de Nascimento": dn,
                 "Email": email, "Telefone": tel, "Sexo": sexo}
        faltando = [k for k, v in obrig.items() if not v]
        if faltando:
            messagebox.showwarning("Campos obrigatórios", f"Preencha: {', '.join(faltando)}")
            return

        payload = {
            "nomeCompleto": nome,
            "cpf": cpf,
            "datadeNascimento": dn,
            "email": email,
            "telefone": tel,
            "sexo": sexo
        }
        status, data = self.controller.api_register(payload)
        if status == 201:
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            # limpa
            self.var_nome.set(""); self.var_cpf.set(""); self.var_dn.set("")
            self.var_email.set(""); self.var_tel.set(""); self.var_sexo.set("")
        elif status == 409:
            msg = data.get("error") if isinstance(data, dict) else str(data)
            messagebox.showerror("Duplicidade", msg)
        elif status == 400:
            msg = data.get("error") if isinstance(data, dict) else str(data)
            messagebox.showerror("Dados inválidos", msg)
        elif status == 0:
            messagebox.showerror("Conexão", data.get("error"))
        else:
            messagebox.showerror("Erro", f"HTTP {status}: {data}")


class TelaConsultarMenu(BaseTela):
    def __init__(self, parent, controller: App):
        super().__init__(parent)
        self.controller = controller

        self.titulo("Consultar")
        self.linha()

        body = ttk.Frame(self)
        body.pack(fill="both", expand=True)

        ttk.Button(body, text="Consultar Usuário", width=40,
                   command=lambda: controller.show("TelaConsultarUsuario")).pack(pady=8)

        # Chama diretamente a API e abre a lista — sem tela de confirmação
        ttk.Button(body, text="Consultar Todos os Usuários", width=40,
                   command=self.consultar_todos).pack(pady=8)

        ttk.Button(body, text="Voltar", width=40,
                   command=lambda: controller.show("TelaPrincipal")).pack(pady=8)

    def consultar_todos(self):
        status, data = self.controller.api_all()
        if status == 200:
            usuarios = None
            if isinstance(data, dict) and "usuarios" in data and isinstance(data["usuarios"], list):
                usuarios = data["usuarios"]
            elif isinstance(data, dict):
                valores = list(data.values())
                if valores and isinstance(valores[0], dict) and "cpf" in valores[0]:
                    usuarios = valores

            if usuarios is None:
                msg = data.get("message") if isinstance(data, dict) else str(data)
                messagebox.showinfo("Resultado", msg or "Nenhum usuário encontrado.")
                return

            lista = self.controller.frames["TelaResultadoLista"]
            lista.preencher(usuarios)
            self.controller.show("TelaResultadoLista")
        elif status == 0:
            messagebox.showerror("Conexão", data.get("error"))
        else:
            messagebox.showerror("Erro", f"HTTP {status}: {data}")


class TelaConsultarUsuario(BaseTela):
    def __init__(self, parent, controller: App):
        super().__init__(parent)
        self.controller = controller

        self.titulo("Consultar Usuário")
        self.linha()

        form = ttk.Frame(self)
        form.pack(fill="x")

        self.var_cpf = tk.StringVar()
        self.var_dn = tk.StringVar()

        self._entrada(form, "CPF", self.var_cpf, 0)
        self._entrada(form, "Data de Nascimento (YYYY-MM-DD)", self.var_dn, 1)

        self.botoes_confirmar_voltar(self.on_confirm,
                                     lambda: controller.show("TelaConsultarMenu"))

    def _entrada(self, parent, label, var, row):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=4)
        e = ttk.Entry(parent, textvariable=var, width=40)
        e.grid(row=row, column=1, sticky="ew", padx=8, pady=4)
        parent.grid_columnconfigure(1, weight=1)
        return e

    def on_confirm(self):
        # Consulta e exibe na Tabela (sem popup)
        cpf = normaliza_cpf(self.var_cpf.get().strip())
        dn = self.var_dn.get().strip()
        if not cpf or not dn:
            messagebox.showwarning("Campos obrigatórios", "Informe CPF e Data de Nascimento.")
            return

        status, data = self.controller.api_find(cpf, dn)
        if status == 200 and isinstance(data, dict):
            u = data.get("usuario", {})
            # abre a mesma tela de resultados com 1 registro
            lista = self.controller.frames["TelaResultadoLista"]
            lista.preencher([u])
            self.controller.show("TelaResultadoLista")
        elif status == 404:
            messagebox.showinfo("Resultado", "Usuário não encontrado.")
        elif status == 400:
            msg = data.get("error") if isinstance(data, dict) else str(data)
            messagebox.showerror("Requisição inválida", msg)
        elif status == 0:
            messagebox.showerror("Conexão", data.get("error"))
        else:
            messagebox.showerror("Erro", f"HTTP {status}: {data}")


class TelaResultadoLista(BaseTela):
    def __init__(self, parent, controller: App):
        super().__init__(parent)
        self.controller = controller

        self.titulo("Resultado da Consulta")
        self.linha()

        frame_tbl = ttk.Frame(self)
        frame_tbl.pack(fill="both", expand=True)

        # mantém TODAS as colunas necessárias
        cols = ("id", "nome", "cpf", "dn", "email", "tel", "sexo")
        self.tree = ttk.Treeview(frame_tbl, columns=cols, show="headings")

        headers = {
            "id": "ID",
            "nome": "Nome Completo",
            "cpf": "CPF",
            "dn": "Nascimento",
            "email": "Email",
            "tel": "Telefone",
            "sexo": "Sexo",
        }
        widths = {"id": 70, "nome": 220, "cpf": 120, "dn": 120, "email": 240, "tel": 140, "sexo": 80}

        for c in cols:
            self.tree.heading(c, text=headers[c])
            self.tree.column(c, width=widths[c], stretch=True)

        vsb = ttk.Scrollbar(frame_tbl, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)

        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Botão Voltar
        btns = ttk.Frame(self)
        btns.pack(anchor="e", pady=(12, 0))
        b0 = ttk.Button(btns, text="Voltar", command=lambda: self.controller.show("TelaConsultarMenu"))
        b0.grid(row=0, column=0)

    def preencher(self, usuarios: list):
        # Limpa a tabela
        for i in self.tree.get_children():
            self.tree.delete(i)
        # Adiciona linhas
        for u in usuarios:
            self.tree.insert("", "end", values=(
                u.get("idDoUsuario"),
                u.get("nomeCompleto"),
                u.get("cpf"),
                u.get("datadeNascimento"),
                u.get("email"),
                u.get("telefone"),
                u.get("sexo"),
            ))


if __name__ == "__main__":
    app = App()
    app.mainloop()
