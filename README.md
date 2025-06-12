# 👓 Sistema Ótica da Família

Bem-vindo ao **Sistema Ótica da Família**!  
Este é um sistema desktop para gerenciamento de clientes, orçamentos e vendas em óticas, feito em Python com PySide6 (Qt).  
Ideal para controle de pedidos de óculos de grau, óculos de sol e lentes de contato, com interface moderna, intuitiva e fácil de usar.

---

## ✨ Funcionalidades Principais

- **Cadastro rápido** de clientes e orçamentos
- **Busca** por nome ou número da OS (ID)
- **Registro e edição** de datas de compra e entrega (com máscara e validação)
- **Alteração** de laboratório, forma de pagamento, loja e médico
- **Edição rápida** de qualquer campo via duplo clique na tabela
- **Exclusão** de clientes
- **Interface escura** e responsiva
- **Banco de dados local** (SQLite) automático

---

## 🖼️ Captura de Tela


![Captura de tela 2025-06-12 150445](https://github.com/user-attachments/assets/840a5d3b-8621-475e-a141-420d719e3034)


![Captura de tela 2025-06-12 150307](https://github.com/user-attachments/assets/1ef81cd4-c91e-4af8-8ea1-db9cf660eb89)

---

## 🚀 Como rodar o sistema

1. **Clone o repositório:**
   ```sh
   git clone https://github.com/LUNDWw/otica_sistme_py.git
   cd otica_sistme_py
   ```

2. **(Opcional) Crie um ambiente virtual:**
   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Instale as dependências:**
   ```sh
   pip install -r requirements.txt
   ```
   > Se não houver `requirements.txt`, instale manualmente:
   ```sh
   pip install PySide6
   ```

4. **Execute o sistema:**
   ```sh
   python sistma_otica.pyw
   ```

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **PySide6 (Qt for Python)**
- **SQLite** (banco de dados local, gerado automaticamente)

---

## 📁 Estrutura do Projeto

```
otica_sistme_py/
├── sistma_otica.pyw
├── clientes_otica.db  # (gerado automaticamente)
├── README.md
└── requirements.txt
```

---

## 💡 Como funciona?

- **Cadastro:**  
  Clique em um dos botões ("Óculos de grau", "Óculos de sol", "Lentes de contato") para cadastrar um novo cliente e orçamento.
- **Busca:**  
  Use "Buscar por nome" ou "Buscar por OS" para localizar rapidamente clientes.
- **Edição:**  
  Dê duplo clique em qualquer célula da tabela para editar o campo correspondente.
- **Entrega:**  
  Registre a data de entrega de um pedido facilmente.
- **Alteração de laboratório:**  
  Atualize o laboratório responsável por um pedido.
- **Exclusão:**  
  Selecione um cliente e clique em "Deletar cliente" para removê-lo do sistema.

---

## 📋 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👤 Autor

Desenvolvido por [Lucas Lundw](https://github.com/LUNDWw).
Nome: Lucas Porto
LinkedIn: https://www.linkedin.com/in/lucas-eduardo-a69a132b9/
---

> ⭐ Se gostou do projeto, deixe uma estrela no repositório!
