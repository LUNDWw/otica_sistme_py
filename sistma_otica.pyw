from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QInputDialog, QLabel, QHeaderView, QFrame, QSizePolicy, QComboBox, QLineEdit, QDialog, QDialogButtonBox
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import sys
import sqlite3
from datetime import datetime
import re

DB_PATH = "clientes_otica.db"

def criar_tabela():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                orcamento REAL,
                tipo TEXT,
                data_compra TEXT,
                data_entrega TEXT,
                laboratorio TEXT,
                forma_pagamento TEXT,
                loja TEXT,
                medico TEXT
            )
        """)
        conn.commit()
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")
    finally:
        conn.close()

def carregar_clientes():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, nome, orcamento, tipo, data_compra, data_entrega, laboratorio, forma_pagamento, loja, medico FROM clientes")
        clientes = []
        for row in c.fetchall():
            clientes.append({
                "id": row[0],
                "nome": row[1],
                "orcamento": row[2],
                "tipo": row[3],
                "data_compra": row[4],
                "data_entrega": row[5] or "",
                "laboratorio": row[6] or "",
                "forma_pagamento": row[7] or "",
                "loja": row[8] or "",
                "medico": row[9] or ""
            })
        return clientes
    except Exception as e:
        print(f"Erro ao carregar clientes: {e}")
        return []
    finally:
        conn.close()

def salvar_cliente(cliente):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            INSERT INTO clientes (nome, orcamento, tipo, data_compra, data_entrega, laboratorio, forma_pagamento, loja, medico)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            cliente["nome"], cliente["orcamento"], cliente["tipo"], cliente["data_compra"], cliente["data_entrega"],
            cliente["laboratorio"], cliente["forma_pagamento"], cliente["loja"], cliente["medico"]
        ))
        conn.commit()
        cliente_id = c.lastrowid
        return cliente_id
    except Exception as e:
        print(f"Erro ao salvar cliente: {e}")
        return None
    finally:
        conn.close()

def atualizar_cliente(cliente):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            UPDATE clientes SET
                nome=?,
                orcamento=?,
                tipo=?,
                data_compra=?,
                data_entrega=?,
                laboratorio=?,
                forma_pagamento=?,
                loja=?,
                medico=?
            WHERE id=?
        """, (
            cliente["nome"], cliente["orcamento"], cliente["tipo"], cliente["data_compra"], cliente["data_entrega"],
            cliente["laboratorio"], cliente["forma_pagamento"], cliente["loja"], cliente["medico"], cliente["id"]
        ))
        conn.commit()
    except Exception as e:
        print(f"Erro ao atualizar cliente: {e}")
    finally:
        conn.close()

def input_data_mascarada(parent, titulo, label, valor_inicial=""):
    dlg = QDialog(parent)
    dlg.setWindowTitle(titulo)
    layout = QVBoxLayout(dlg)
    lbl = QLabel(label)
    layout.addWidget(lbl)
    line_edit = QLineEdit()
    line_edit.setInputMask("00/00/0000")
    line_edit.setText(valor_inicial)
    layout.addWidget(line_edit)
    buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    layout.addWidget(buttons)
    buttons.accepted.connect(dlg.accept)
    buttons.rejected.connect(dlg.reject)
    if dlg.exec() == QDialog.Accepted:
        return line_edit.text(), True
    return "", False

class OticaApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ótica da Família")
        self.setGeometry(100, 100, 1200, 540)
        self.setStyleSheet("""
            QWidget { background-color: #181a1b; }
            QLabel#Titulo { color: #fff; font-size: 28px; font-weight: bold; }
            QLabel#Sub { color: #b0bec5; font-size: 14px; }
            QFrame#Barra { background-color: #00bcd4; min-height: 4px; max-height: 4px; border-radius: 2px; }
        """)
        criar_tabela()
        self.clientes = carregar_clientes()

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        titulo = QLabel("Ótica da Família", self)
        titulo.setObjectName("Titulo")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        subtitulo = QLabel("Sistema Ótica da Família", self)
        subtitulo.setObjectName("Sub")
        subtitulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitulo)

        barra = QFrame(self)
        barra.setObjectName("Barra")
        layout.addWidget(barra)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)

        self.btn_grau = self.criar_botao("Óculos de grau", "#1976d2", "#fff", "#1565c0")
        self.btn_grau.clicked.connect(lambda: self.adicionar_cliente("Óculos de grau"))
        btn_layout.addWidget(self.btn_grau)

        self.btn_sol = self.criar_botao("Óculos de sol", "#388e3c", "#fff", "#2e7d32")
        self.btn_sol.clicked.connect(lambda: self.adicionar_cliente("Óculos de sol"))
        btn_layout.addWidget(self.btn_sol)

        self.btn_lente = self.criar_botao("Lentes de contato", "#fbc02d", "#181a1b", "#f9a825")
        self.btn_lente.clicked.connect(lambda: self.adicionar_cliente("Lentes de contato"))
        btn_layout.addWidget(self.btn_lente)

        layout.addLayout(btn_layout)

        btn2_layout = QHBoxLayout()
        btn2_layout.setSpacing(20)

        self.btn_buscar_nome = self.criar_botao("Buscar por nome", "#0288d1", "#fff", "#0277bd")
        self.btn_buscar_nome.clicked.connect(self.buscar_cliente_nome)
        btn2_layout.addWidget(self.btn_buscar_nome)

        self.btn_buscar_os = self.criar_botao("Buscar por OS", "#7b1fa2", "#fff", "#6a1b9a")
        self.btn_buscar_os.clicked.connect(self.buscar_cliente_os)
        btn2_layout.addWidget(self.btn_buscar_os)

        self.btn_entrega = self.criar_botao("Registrar entrega", "#f57c00", "#fff", "#ef6c00")
        self.btn_entrega.clicked.connect(self.registrar_entrega)
        btn2_layout.addWidget(self.btn_entrega)

        self.btn_alterar_lab = self.criar_botao("Alterar laboratório", "#009688", "#fff", "#00897b")
        self.btn_alterar_lab.clicked.connect(self.alterar_laboratorio)
        btn2_layout.addWidget(self.btn_alterar_lab)

        self.btn_deletar = self.criar_botao("Deletar cliente", "#d32f2f", "#fff", "#b71c1c")
        self.btn_deletar.clicked.connect(self.deletar_cliente)
        btn2_layout.addWidget(self.btn_deletar)

        self.btn_finalizar = self.criar_botao("Finalizar", "#455a64", "#fff", "#263238")
        self.btn_finalizar.clicked.connect(self.close)
        btn2_layout.addWidget(self.btn_finalizar)

        self.btn_editar = self.criar_botao("Editar cliente", "#1976d2", "#fff", "#1565c0")
        self.btn_editar.clicked.connect(self.editar_cliente)
        btn2_layout.addWidget(self.btn_editar)

        layout.addLayout(btn2_layout)

        label_lista = QLabel("Clientes cadastrados:", self)
        label_lista.setFont(QFont("Segoe UI", 13, QFont.Bold))
        label_lista.setStyleSheet("color: #00bcd4; margin-top: 10px;")
        layout.addWidget(label_lista)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(10)
        self.tabela.setHorizontalHeaderLabels([
            "OS", "Nome", "Orçamento", "Produto", "Data Compra", "Data Entrega", "Laboratório", "Pagamento", "Loja", "Médico"
        ])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabela.setAlternatingRowColors(True)
        self.tabela.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela.setSelectionMode(QTableWidget.SingleSelection)
        self.tabela.verticalHeader().setVisible(False)
        self.tabela.setStyleSheet("""
            QTableWidget {
                background-color: #2c2c2c;
                color: #eee;
                font-size: 15px;
                border: 1px solid #444;
                selection-background-color: #26c6da; /* Azul claro para seleção */
                selection-color: #fff;
                gridline-color: #444;
            }
            QHeaderView::section {
                background-color: #00bcd4;
                color: #fff;
                font-weight: bold;
                border: none;
                font-size: 16px;
                padding: 8px 0;
            }
            QTableWidget::item {
                padding: 8px;
                border: none;
            }
            QTableWidget::item:selected,
            QTableWidget::item:hover:selected {
                background-color: #26c6da; /* Azul claro para seleção e hover */
                color: #fff;
            }
            QTableWidget::item:hover {
                background-color: #26c6da; /* Azul claro ao passar o mouse */
                color: #fff;
            }
            QTableWidget::item:alternate {
                background-color: #232323;
            }
            QScrollBar:vertical {
                background: #2c2c2c;
                width: 12px;
                margin: 2px 0 2px 0;
            }
            QScrollBar::handle:vertical {
                background: #00bcd4;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
            }
        """)
        layout.addWidget(self.tabela)

        self.atualizar_lista()

        # Permitir edição de célula específica ao dar duplo clique
        self.tabela.cellDoubleClicked.connect(self.editar_celula)

    def criar_botao(self, texto, cor_bg, cor_fg, cor_hover):
        btn = QPushButton(texto)
        btn.setMinimumHeight(44)
        btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {cor_bg};
                color: {cor_fg};
                font-weight: bold;
                border: none;
                border-radius: 18px;
                padding: 12px 22px;
                font-size: 16px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.18);
            }}
            QPushButton:hover {{
                background-color: {cor_hover};
                box-shadow: 0 4px 16px rgba(0,0,0,0.28);
            }}
        """)
        return btn

    def atualizar_lista(self):
        self.clientes = carregar_clientes()
        self.tabela.setRowCount(0)
        for cliente in self.clientes:
            self.tabela.insertRow(self.tabela.rowCount())
            self.tabela.setItem(self.tabela.rowCount()-1, 0, QTableWidgetItem(str(cliente["id"])))
            self.tabela.setItem(self.tabela.rowCount()-1, 1, QTableWidgetItem(cliente["nome"]))
            self.tabela.setItem(self.tabela.rowCount()-1, 2, QTableWidgetItem(f"R$ {cliente['orcamento']:.2f}"))
            self.tabela.setItem(self.tabela.rowCount()-1, 3, QTableWidgetItem(cliente["tipo"]))
            self.tabela.setItem(self.tabela.rowCount()-1, 4, QTableWidgetItem(cliente.get("data_compra", "")))
            self.tabela.setItem(self.tabela.rowCount()-1, 5, QTableWidgetItem(cliente.get("data_entrega", "")))
            self.tabela.setItem(self.tabela.rowCount()-1, 6, QTableWidgetItem(cliente.get("laboratorio", "")))
            self.tabela.setItem(self.tabela.rowCount()-1, 7, QTableWidgetItem(cliente.get("forma_pagamento", "")))
            self.tabela.setItem(self.tabela.rowCount()-1, 8, QTableWidgetItem(cliente.get("loja", "")))
            self.tabela.setItem(self.tabela.rowCount()-1, 9, QTableWidgetItem(cliente.get("medico", "")))

    def adicionar_cliente(self, tipo):
        orcamento, ok1 = QInputDialog.getDouble(self, "Orçamento", f"Qual o valor do orçamento para {tipo}?", decimals=2)
        if not ok1:
            return
        nome, ok2 = QInputDialog.getText(self, "Nome", "Nome do cliente:")
        if not ok2 or not nome.strip():
            QMessageBox.warning(self, "Erro", "Nome inválido.")
            return
        laboratorio, ok3 = QInputDialog.getText(self, "Laboratório", "Para qual laboratório foi enviado o produto?")
        if not ok3 or not laboratorio.strip():
            QMessageBox.warning(self, "Erro", "Laboratório inválido.")
            return
        formas = ["Pix", "À vista", "Cartão de crédito", "Boleto"]
        forma_pagamento, ok4 = QInputDialog.getItem(self, "Forma de Pagamento", "Selecione a forma de pagamento:", formas, 0, False)
        if not ok4 or not forma_pagamento:
            QMessageBox.warning(self, "Erro", "Forma de pagamento inválida.")
            return
        loja, ok5 = QInputDialog.getText(self, "Loja", "Digite o nome da loja:")
        if not ok5 or not loja.strip():
            QMessageBox.warning(self, "Erro", "Loja inválida.")
            return
        medico, ok6 = QInputDialog.getText(self, "Médico", "Digite o nome do médico:")
        if not ok6 or not medico.strip():
            QMessageBox.warning(self, "Erro", "Médico inválido.")
            return
        data_compra = datetime.now().strftime("%d/%m/%Y")
        cliente = {
            "nome": nome.strip(),
            "orcamento": orcamento,
            "tipo": tipo,
            "data_compra": data_compra,
            "data_entrega": "",
            "laboratorio": laboratorio.strip(),
            "forma_pagamento": forma_pagamento,
            "loja": loja.strip(),
            "medico": medico.strip()
        }
        cliente_id = salvar_cliente(cliente)
        if cliente_id is None:
            QMessageBox.warning(self, "Erro", "Erro ao salvar cliente no banco de dados.")
            return
        cliente["id"] = cliente_id
        self.clientes = carregar_clientes()
        QMessageBox.information(self, "Sucesso", f"Obrigado, {nome}! Seu orçamento de R$ {orcamento:.2f} foi registrado.")
        self.atualizar_lista()

    def deletar_cliente(self):
        if not self.clientes:
            QMessageBox.information(self, "Aviso", "Nenhum cliente cadastrado ainda.")
            return
        row = self.tabela.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Selecione", "Selecione um cliente na tabela para deletar.")
            return
        cliente = self.clientes[row]
        confirm = QMessageBox.question(self, "Confirmar", f"Tem certeza que deseja deletar o cliente {cliente['nome']}?")
        if confirm == QMessageBox.Yes:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("DELETE FROM clientes WHERE id=?", (cliente["id"],))
            conn.commit()
            conn.close()
            self.clientes = carregar_clientes()
            self.atualizar_lista()
            QMessageBox.information(self, "Deletado", "Cliente deletado com sucesso.")

    def registrar_entrega(self):
        if not self.clientes:
            QMessageBox.information(self, "Aviso", "Nenhum cliente cadastrado ainda.")
            return
        os_id, ok = QInputDialog.getInt(
            self,
            "Registrar Entrega",
            f"Digite o número da OS (ID do cliente):",
            1
        )
        if not ok:
            return
        cliente = next((c for c in self.clientes if c["id"] == os_id), None)
        if cliente:
            data_compra = cliente.get("data_compra", "")
            while True:
                data_entrega, ok2 = input_data_mascarada(self, "Data de Entrega", "Digite a data de entrega:", "")
                if not ok2:
                    return
                if not re.match(r"^\d{2}/\d{2}/\d{4}$", data_entrega.strip()):
                    QMessageBox.warning(self, "Erro", "Formato de data inválido. Use dd/mm/aaaa.")
                    continue
                try:
                    dt_compra = datetime.strptime(data_compra, "%d/%m/%Y")
                    dt_entrega = datetime.strptime(data_entrega.strip(), "%d/%m/%Y")
                except ValueError:
                    QMessageBox.warning(self, "Erro", "Data inválida.")
                    continue
                if dt_entrega < dt_compra:
                    QMessageBox.warning(self, "Erro", "A data de entrega não pode ser anterior à data de compra.")
                    continue
                break
            cliente["data_entrega"] = data_entrega.strip()
            atualizar_cliente(cliente)
            self.clientes = carregar_clientes()
            QMessageBox.information(self, "Sucesso", f"Data de entrega registrada para OS {os_id}.")
            self.atualizar_lista()
        else:
            QMessageBox.warning(self, "Não encontrado", "OS não encontrada.")

    def buscar_cliente_nome(self):
        if not self.clientes:
            QMessageBox.information(self, "Aviso", "Nenhum cliente cadastrado ainda.")
            return
        nome_busca, ok = QInputDialog.getText(self, "Buscar Cliente", "Digite o nome do cliente:")
        if ok and nome_busca:
            nome_busca = nome_busca.strip().lower()
            encontrados = []
            for cliente in self.clientes:
                if nome_busca in cliente["nome"].strip().lower():
                    encontrados.append(cliente)
            if encontrados:
                msg = ""
                for cliente in encontrados:
                    msg += (
                        f"OS: {cliente['id']}\nCliente: {cliente['nome']}\nOrçamento: R$ {cliente['orcamento']:.2f}\nProduto: {cliente['tipo']}\n"
                        f"Data Compra: {cliente.get('data_compra','')}\nData Entrega: {cliente.get('data_entrega','')}\nLaboratório: {cliente.get('laboratorio','')}\n"
                        f"Pagamento: {cliente.get('forma_pagamento','')}\nLoja: {cliente.get('loja','')}\nMédico: {cliente.get('medico','')}\n\n"
                    )
                QMessageBox.information(self, "Cliente(s) encontrado(s)", msg)
                return
            QMessageBox.warning(self, "Não encontrado", "Cliente não encontrado.")

    def buscar_cliente_os(self):
        if not self.clientes:
            QMessageBox.information(self, "Aviso", "Nenhum cliente cadastrado ainda.")
            return
        os_id, ok = QInputDialog.getInt(
            self,
            "Buscar por OS",
            f"Digite o número da OS (ID do cliente):",
            1
        )
        if not ok:
            return
        cliente = next((c for c in self.clientes if c["id"] == os_id), None)
        if cliente:
            QMessageBox.information(
                self, "Cliente encontrado",
                f"OS: {cliente['id']}\nCliente: {cliente['nome']}\nOrçamento: R$ {cliente['orcamento']:.2f}\nProduto: {cliente['tipo']}\n"
                f"Data Compra: {cliente.get('data_compra','')}\nData Entrega: {cliente.get('data_entrega','')}\nLaboratório: {cliente.get('laboratorio','')}\n"
                f"Pagamento: {cliente.get('forma_pagamento','')}\nLoja: {cliente.get('loja','')}\nMédico: {cliente.get('medico','')}"
            )
        else:
            QMessageBox.warning(self, "Não encontrado", "OS não encontrada.")

    def alterar_laboratorio(self):
        if not self.clientes:
            QMessageBox.information(self, "Aviso", "Nenhum cliente cadastrado ainda.")
            return
        os_id, ok = QInputDialog.getInt(
            self,
            "Alterar Laboratório",
            f"Digite o número da OS (ID do cliente):",
            1
        )
        if not ok:
            return
        cliente = next((c for c in self.clientes if c["id"] == os_id), None)
        if cliente:
            lab_atual = cliente.get("laboratorio", "")
            novo_lab, ok2 = QInputDialog.getText(
                self,
                "Novo Laboratório",
                f"Laboratório atual: {lab_atual}\nDigite o novo nome do laboratório:"
            )
            if ok2 and novo_lab.strip():
                cliente["laboratorio"] = novo_lab.strip()
                atualizar_cliente(cliente)
                self.clientes = carregar_clientes()
                QMessageBox.information(self, "Sucesso", f"Laboratório alterado para OS {os_id}.")
                self.atualizar_lista()
            else:
                QMessageBox.warning(self, "Erro", "Nome de laboratório inválido.")
        else:
            QMessageBox.warning(self, "Não encontrado", "OS não encontrada.")

    def editar_cliente(self):
        if not self.clientes:
            QMessageBox.information(self, "Aviso", "Nenhum cliente cadastrado ainda.")
            return
        row = self.tabela.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Selecione", "Selecione um cliente na tabela para editar.")
            return
        cliente = self.clientes[row]
        nome, ok = QInputDialog.getText(self, "Editar Nome", "Nome:", text=cliente["nome"])
        if not ok or not nome.strip():
            QMessageBox.warning(self, "Erro", "Nome inválido.")
            return
        orcamento, ok = QInputDialog.getDouble(self, "Editar Orçamento", "Orçamento:", value=cliente["orcamento"], decimals=2)
        if not ok:
            QMessageBox.warning(self, "Erro", "Orçamento inválido.")
            return
        tipos = ["Óculos de grau", "Óculos de sol", "Lentes de contato"]
        tipo, ok = QInputDialog.getItem(self, "Editar Produto", "Tipo:", tipos, tipos.index(cliente["tipo"]) if cliente["tipo"] in tipos else 0, False)
        if not ok:
            QMessageBox.warning(self, "Erro", "Tipo inválido.")
            return
        laboratorio, ok = QInputDialog.getText(self, "Editar Laboratório", "Laboratório:", text=cliente["laboratorio"])
        if not ok or not laboratorio.strip():
            QMessageBox.warning(self, "Erro", "Laboratório inválido.")
            return

        # Editar data de compra com máscara e validação
        while True:
            data_compra, ok = input_data_mascarada(self, "Editar Data de Compra", "Data de compra (dd/mm/aaaa):", cliente["data_compra"])
            if not ok or not data_compra.strip():
                QMessageBox.warning(self, "Erro", "Data de compra inválida.")
                return
            if not re.match(r"^\d{2}/\d{2}/\d{4}$", data_compra.strip()):
                QMessageBox.warning(self, "Erro", "Formato de data inválido. Use dd/mm/aaaa.")
                continue
            try:
                dt_compra = datetime.strptime(data_compra.strip(), "%d/%m/%Y")
            except ValueError:
                QMessageBox.warning(self, "Erro", "Data inválida.")
                continue
            break

        # Editar data de entrega com máscara e validação
        while True:
            data_entrega, ok = input_data_mascarada(self, "Editar Data de Entrega", "Data de entrega (dd/mm/aaaa):", cliente["data_entrega"])
            if not ok:
                QMessageBox.warning(self, "Erro", "Data de entrega inválida.")
                return
            if not data_entrega.strip():
                break  # Permite campo vazio
            if not re.match(r"^\d{2}/\d{2}/\d{4}$", data_entrega.strip()):
                QMessageBox.warning(self, "Erro", "Formato de data inválido. Use dd/mm/aaaa.")
                continue
            try:
                dt_entrega = datetime.strptime(data_entrega.strip(), "%d/%m/%Y")
                if dt_entrega < dt_compra:
                    QMessageBox.warning(self, "Erro", "A data de entrega não pode ser anterior à data de compra.")
                    continue
            except ValueError:
                QMessageBox.warning(self, "Erro", "Data inválida.")
                continue
            break

        formas = ["Pix", "À vista", "Cartão de crédito", "Boleto"]
        forma_pagamento, ok = QInputDialog.getItem(self, "Editar Forma de Pagamento", "Forma de pagamento:", formas, formas.index(cliente["forma_pagamento"]) if cliente["forma_pagamento"] in formas else 0, False)
        if not ok:
            QMessageBox.warning(self, "Erro", "Forma de pagamento inválida.")
            return
        loja, ok = QInputDialog.getText(self, "Editar Loja", "Loja:", text=cliente.get("loja", ""))
        if not ok or not loja.strip():
            QMessageBox.warning(self, "Erro", "Loja inválida.")
            return
        medico, ok = QInputDialog.getText(self, "Editar Médico", "Médico:", text=cliente.get("medico", ""))
        if not ok or not medico.strip():
            QMessageBox.warning(self, "Erro", "Médico inválido.")
            return
        cliente["nome"] = nome.strip()
        cliente["orcamento"] = orcamento
        cliente["tipo"] = tipo
        cliente["laboratorio"] = laboratorio.strip()
        cliente["data_compra"] = data_compra.strip()
        cliente["data_entrega"] = data_entrega.strip()
        cliente["forma_pagamento"] = forma_pagamento
        cliente["loja"] = loja.strip()
        cliente["medico"] = medico.strip()
        atualizar_cliente(cliente)
        self.clientes = carregar_clientes()
        self.atualizar_lista()
        QMessageBox.information(self, "Sucesso", "Informações do cliente atualizadas com sucesso.")

    def editar_celula(self, row, column):
        if not self.clientes:
            return
        cliente = self.clientes[row]
        campos = [
            ("OS", None),
            ("Nome", "nome"),
            ("Orçamento", "orcamento"),
            ("Produto", "tipo"),
            ("Data Compra", "data_compra"),
            ("Data Entrega", "data_entrega"),
            ("Laboratório", "laboratorio"),
            ("Pagamento", "forma_pagamento"),
            ("Loja", "loja"),
            ("Médico", "medico"),
        ]
        campo_nome, campo_chave = campos[column]

        if campo_chave is None:
            QMessageBox.information(self, "Aviso", "Não é possível editar o número da OS.")
            return

        valor_atual = cliente[campo_chave]

        # Edição conforme o campo
        if campo_chave == "orcamento":
            novo_valor, ok = QInputDialog.getDouble(self, "Editar Orçamento", "Novo orçamento:", value=cliente["orcamento"], decimals=2)
            if ok:
                cliente["orcamento"] = novo_valor
            else:
                return
        elif campo_chave == "tipo":
            tipos = ["Óculos de grau", "Óculos de sol", "Lentes de contato"]
            novo_valor, ok = QInputDialog.getItem(self, "Editar Produto", "Tipo:", tipos, tipos.index(cliente["tipo"]) if cliente["tipo"] in tipos else 0, False)
            if ok:
                cliente["tipo"] = novo_valor
            else:
                return
        elif campo_chave == "forma_pagamento":
            formas = ["Pix", "À vista", "Cartão de crédito", "Boleto"]
            novo_valor, ok = QInputDialog.getItem(self, "Editar Forma de Pagamento", "Forma de pagamento:", formas, formas.index(cliente["forma_pagamento"]) if cliente["forma_pagamento"] in formas else 0, False)
            if ok:
                cliente["forma_pagamento"] = novo_valor
            else:
                return
        elif campo_chave in ["data_compra", "data_entrega"]:
            while True:
                novo_valor, ok = input_data_mascarada(self, f"Editar {campo_nome}", f"Nova {campo_nome.lower()} (dd/mm/aaaa):", valor_atual)
                if not ok:
                    return
                if not re.match(r"^\d{2}/\d{2}/\d{4}$", novo_valor.strip()):
                    QMessageBox.warning(self, "Erro", "Formato de data inválido. Use dd/mm/aaaa.")
                    continue
                try:
                    dt_novo = datetime.strptime(novo_valor.strip(), "%d/%m/%Y")
                    if campo_chave == "data_entrega":
                        dt_compra = datetime.strptime(cliente["data_compra"], "%d/%m/%Y")
                        if dt_novo < dt_compra:
                            QMessageBox.warning(self, "Erro", "A data de entrega não pode ser anterior à data de compra.")
                            continue
                except ValueError:
                    QMessageBox.warning(self, "Erro", "Data inválida.")
                    continue
                cliente[campo_chave] = novo_valor.strip()
                break
        else:
            novo_valor, ok = QInputDialog.getText(self, f"Editar {campo_nome}", f"Novo {campo_nome.lower()}:", text=valor_atual)
            if ok and novo_valor.strip():
                cliente[campo_chave] = novo_valor.strip()
            elif ok:
                QMessageBox.warning(self, "Erro", f"{campo_nome} não pode ser vazio.")
                return
            else:
                return

        atualizar_cliente(cliente)
        self.clientes = carregar_clientes()
        self.atualizar_lista()
        QMessageBox.information(self, "Sucesso", f"{campo_nome} atualizado com sucesso.")

if __name__ == "__main__":
    criar_tabela()
    app = QApplication(sys.argv)
    janela = OticaApp()
    janela.show()
    sys.exit(app.exec())