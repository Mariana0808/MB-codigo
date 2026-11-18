import pickle
import os
from datetime import datetime, date, timedelta


# ==============================
# CLASSES
# ==============================

class Usuario:
    def __init__(self, cpf, cnpj, email, senha, tipo_usuario):
        self.cpf = cpf
        self.cnpj = cnpj
        self.email = email
        self.senha = senha
        self.tipo_usuario = tipo_usuario


class Produto:
    def __init__(self, codigo, nome, marca, preco_unitario, quantidade, validade):
        self.codigo = codigo
        self.nome = nome
        self.marca = marca
        self.preco_unitario = preco_unitario
        self.quantidade = quantidade
        self.validade = validade


# ==============================
# SISTEMA
# ==============================

class Sistema:

    def __init__(self):
        self.usuarios = self.carregar_dados("usuarios.pkl")
        self.produtos = self.carregar_dados("produtos.pkl")
        self.movimentacoes = self.carregar_dados("movimentacoes.pkl")

    def carregar_dados(self, arquivo):
        if os.path.exists(arquivo):
            try:
                with open(arquivo, "rb") as f:
                    return pickle.load(f)
            except:
                return []
        return []

    def salvar_dados(self):
        with open("usuarios.pkl", "wb") as f:
            pickle.dump(self.usuarios, f)

        with open("produtos.pkl", "wb") as f:
            pickle.dump(self.produtos, f)

        with open("movimentacoes.pkl", "wb") as f:
            pickle.dump(self.movimentacoes, f)

    # ==============================
    # CADASTRO DE USUÁRIO
    # ==============================

    def cadastrar_usuario(self):

        print("\n--- CADASTRO DE USUÁRIO ---")

        cpf = input("Digite seu CPF: ")
        cnpj = input("Digite seu CNPJ: ")
        email = input("Digite seu e-mail: ")
        senha = input("Digite sua senha: ")

        print("\nEscolha o tipo de usuário:")
        print("1 - Vendedor")
        print("2 - Visualizador")

        tipo = input("Escolha: ")

        if tipo == "1":
            tipo_usuario = "Vendedor"
        elif tipo == "2":
            tipo_usuario = "Visualizador"
        else:
            print("Opção inválida!")
            return

        # Verificar dados duplicados
        for usuario in self.usuarios:

            if getattr(usuario, "cpf", None) == cpf:
                print("Erro: este CPF já está cadastrado!")
                return

            if getattr(usuario, "cnpj", None) == cnpj:
                print("Erro: este CNPJ já está cadastrado!")
                return

            if getattr(usuario, "email", None) == email:
                print("Erro: este e-mail já está cadastrado!")
                return

            if getattr(usuario, "senha", None) == senha:
                print("Erro: esta senha já está sendo utilizada!")
                return

        novo_usuario = Usuario(cpf, cnpj, email, senha, tipo_usuario)

        self.usuarios.append(novo_usuario)
        self.salvar_dados()

        print("Usuário cadastrado com sucesso!")

    # ==============================
    # LOGIN
    # ==============================

    def fazer_login(self):

        print("\n--- LOGIN ---")

        email = input("Digite seu e-mail: ")
        senha = input("Digite sua senha: ")

        for usuario in self.usuarios:
            if usuario.email == email and usuario.senha == senha:
                print("\nLogin realizado com sucesso!")
                return usuario

        print("E-mail ou senha incorretos!")
        return None

    # ==============================
    # LISTAR PRODUTOS
    # ==============================

    def listar_produtos(self):

        print("\n--- PRODUTOS CADASTRADOS ---")

        if not self.produtos:
            print("Nenhum produto cadastrado!")
            return

        for produto in self.produtos:
            print("-------------------------")
            print("Código:", produto.codigo)
            print("Nome:", produto.nome)
            print("Marca:", produto.marca)
            print("Preço unitário: R$", produto.preco_unitario)
            print("Quantidade:", getattr(produto, "quantidade", 0))
            print("Validade:", getattr(produto, "validade", "Não informada"))

    # ==============================
    # CADASTRAR PRODUTO
    # ==============================

    def cadastrar_produto(self):

        print("\n--- CADASTRAR PRODUTO ---")

        codigo = input("Código: ")

        for produto in self.produtos:
            if produto.codigo == codigo:
                print("Já existe um produto com esse código!")
                return

        nome = input("Nome: ")
        marca = input("Marca: ")

        try:
            preco = float(input("Preço unitário: R$ "))
            quantidade = int(input("Quantidade: "))
        except ValueError:
            print("Digite valores numéricos válidos!")
            return

        validade = input("Validade (DD/MM/AAAA): ")

        try:
            datetime.strptime(validade, "%d/%m/%Y")
        except ValueError:
            print("Data inválida!")
            return

        if preco < 0 or quantidade < 0:
            print("Preço e quantidade não podem ser negativos!")
            return

        produto = Produto(codigo, nome, marca, preco, quantidade, validade)

        self.produtos.append(produto)
        self.salvar_dados()

        print("Produto cadastrado com sucesso!")

    # ==============================
    # EDITAR PRODUTO
    # ==============================

    def editar_produto(self):

        print("\n--- EDITAR PRODUTO ---")

        codigo = input("Digite o código do produto: ")

        for produto in self.produtos:

            if produto.codigo == codigo:

                produto.nome = input("Novo nome: ")
                produto.marca = input("Nova marca: ")

                try:
                    produto.preco_unitario = float(input("Novo preço: R$ "))
                    produto.quantidade = int(input("Nova quantidade: "))
                except ValueError:
                    print("Valores inválidos!")
                    return

                validade = input("Nova validade (DD/MM/AAAA): ")

                try:
                    datetime.strptime(validade, "%d/%m/%Y")
                except ValueError:
                    print("Data inválida!")
                    return

                produto.validade = validade

                self.salvar_dados()
                print("Produto atualizado com sucesso!")
                return

        print("Produto não encontrado!")

    # ==============================
    # EXCLUIR PRODUTO
    # ==============================

    def excluir_produto(self):

        print("\n--- EXCLUIR PRODUTO ---")

        codigo = input("Digite o código do produto: ")

        for produto in self.produtos:

            if produto.codigo == codigo:

                self.produtos.remove(produto)
                self.salvar_dados()

                print("Produto excluído com sucesso!")
                return

        print("Produto não encontrado!")

    # ==============================
    # PESQUISAR PRODUTO
    # ==============================

    def pesquisar_produto(self):

        print("\n--- PESQUISAR PRODUTO ---")

        busca = input("Digite o nome ou código do produto: ").lower()

        encontrado = False

        for produto in self.produtos:

            if busca in produto.nome.lower() or busca == produto.codigo.lower():

                print("-------------------------")
                print("Código:", produto.codigo)
                print("Nome:", produto.nome)
                print("Marca:", produto.marca)
                print("Preço: R$", produto.preco_unitario)
                print("Quantidade:", getattr(produto, "quantidade", 0))
                print("Validade:", getattr(produto, "validade", "Não informada"))

                encontrado = True

        if not encontrado:
            print("Produto não encontrado!")

    # ==============================
    # ENTRADA DE ESTOQUE
    # ==============================

    def entrada_estoque(self):

        print("\n--- ENTRADA DE ESTOQUE ---")

        codigo = input("Código do produto: ")

        for produto in self.produtos:

            if produto.codigo == codigo:

                try:
                    quantidade = int(input("Quantidade de entrada: "))
                except ValueError:
                    print("Digite uma quantidade válida!")
                    return

                if quantidade <= 0:
                    print("A quantidade deve ser maior que zero!")
                    return

                produto.quantidade = getattr(produto, "quantidade", 0) + quantidade

                self.movimentacoes.append(
                    f"Entrada de {quantidade} unidades do produto {produto.nome} - {datetime.now()}"
                )

                self.salvar_dados()

                print("Entrada registrada com sucesso!")
                return

        print("Produto não encontrado!")

    # ==============================
    # SAÍDA DE ESTOQUE
    # ==============================

    def saida_estoque(self):

        print("\n--- SAÍDA DE ESTOQUE ---")

        codigo = input("Código do produto: ")

        for produto in self.produtos:

            if produto.codigo == codigo:

                try:
                    quantidade = int(input("Quantidade de saída: "))
                except ValueError:
                    print("Digite uma quantidade válida!")
                    return

                if quantidade <= 0:
                    print("A quantidade deve ser maior que zero!")
                    return

                if quantidade > getattr(produto, "quantidade", 0):
                    print("Estoque insuficiente!")
                    return

                produto.quantidade -= quantidade

                self.movimentacoes.append(
                    f"Saída de {quantidade} unidades do produto {produto.nome} - {datetime.now()}"
                )

                self.salvar_dados()

                print("Saída registrada com sucesso!")
                return

        print("Produto não encontrado!")

    # ==============================
    # PRODUTOS COM ESTOQUE BAIXO
    # ==============================

    def estoque_baixo(self):

        print("\n--- PRODUTOS COM ESTOQUE BAIXO ---")

        encontrado = False

        for produto in self.produtos:

            if getattr(produto, "quantidade", 0) <= 5:

                print(produto.nome, "- Quantidade:", produto.quantidade)
                encontrado = True

        if not encontrado:
            print("Nenhum produto com estoque baixo!")

    # ==============================
    # PRODUTOS PRÓXIMOS DO VENCIMENTO
    # ==============================

    def produtos_vencimento(self):

        print("\n--- PRODUTOS PRÓXIMOS DO VENCIMENTO ---")

        hoje = date.today()
        limite = hoje + timedelta(days=30)

        encontrado = False

        for produto in self.produtos:

            validade = getattr(produto, "validade", None)

            if not validade:
                continue

            try:
                data_validade = datetime.strptime(validade, "%d/%m/%Y").date()
            except ValueError:
                continue

            if hoje <= data_validade <= limite:

                print(produto.nome, "- Validade:", validade)
                encontrado = True

        if not encontrado:
            print("Nenhum produto próximo do vencimento!")

    # ==============================
    # VALOR TOTAL DO ESTOQUE
    # ==============================

    def valor_total_estoque(self):

        total = 0

        for produto in self.produtos:

            quantidade = getattr(produto, "quantidade", 0)
            total += produto.preco_unitario * quantidade

        print("\nValor total do estoque: R$", round(total, 2))

    # ==============================
    # HISTÓRICO DE MOVIMENTAÇÕES
    # ==============================

    def historico_movimentacoes(self):

        print("\n--- HISTÓRICO DE MOVIMENTAÇÕES ---")

        if not self.movimentacoes:
            print("Nenhuma movimentação registrada!")
            return

        for movimentacao in self.movimentacoes:
            print(movimentacao)


# ==============================
# MENU DO VENDEDOR
# ==============================

def menu_vendedor(sistema):

    while True:

        print("\n===== MENU DO VENDEDOR =====")
        print("1 - Listar produtos")
        print("2 - Cadastrar produto")
        print("3 - Editar produto")
        print("4 - Excluir produto")
        print("5 - Pesquisar produto")
        print("6 - Entrada de estoque")
        print("7 - Saída de estoque")
        print("8 - Produtos com estoque baixo")
        print("9 - Produtos próximos do vencimento")
        print("10 - Valor total do estoque")
        print("11 - Histórico de movimentações")
        print("12 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            sistema.listar_produtos()

        elif opcao == "2":
            sistema.cadastrar_produto()

        elif opcao == "3":
            sistema.editar_produto()

        elif opcao == "4":
            sistema.excluir_produto()

        elif opcao == "5":
            sistema.pesquisar_produto()

        elif opcao == "6":
            sistema.entrada_estoque()

        elif opcao == "7":
            sistema.saida_estoque()

        elif opcao == "8":
            sistema.estoque_baixo()

        elif opcao == "9":
            sistema.produtos_vencimento()

        elif opcao == "10":
            sistema.valor_total_estoque()

        elif opcao == "11":
            sistema.historico_movimentacoes()

        elif opcao == "12":
            print("Saindo do menu do vendedor...")
            break

        else:
            print("Opção inválida!")


# ==============================
# MENU DO VISUALIZADOR
# ==============================

def menu_visualizador(sistema):

    while True:

        print("\n===== MENU DO VISUALIZADOR =====")
        print("1 - Listar produtos")
        print("2 - Pesquisar produto")
        print("3 - Produtos próximos do vencimento")
        print("4 - Produtos com estoque baixo")
        print("5 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            sistema.listar_produtos()

        elif opcao == "2":
            sistema.pesquisar_produto()

        elif opcao == "3":
            sistema.produtos_vencimento()

        elif opcao == "4":
            sistema.estoque_baixo()

        elif opcao == "5":
            print("Saindo do menu do visualizador...")
            break

        else:
            print("Opção inválida!")


# ==============================
# INÍCIO DO SISTEMA
# ==============================

sistema = Sistema()

while True:

    print("\n===== SISTEMA DE ESTOQUE =====")
    print("1 - Cadastrar usuário")
    print("2 - Fazer login")
    print("3 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":

        sistema.cadastrar_usuario()

    elif opcao == "2":

        usuario_logado = sistema.fazer_login()

        if usuario_logado is not None:

            if usuario_logado.tipo_usuario.lower() == "vendedor":
                menu_vendedor(sistema)

            elif usuario_logado.tipo_usuario.lower() == "visualizador":
                menu_visualizador(sistema)

            else:
                print("Tipo de usuário não reconhecido!")

    elif opcao == "3":

        print("Sistema encerrado!")
        break

    else:
        print("Opção inválida!")