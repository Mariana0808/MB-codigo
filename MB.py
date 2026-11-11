import pickle
import os


class Usuario:
    def __init__(self, id_usuario, cpf, cnpj, email, senha, tipo_usuario):
        self.id_usuario = id_usuario
        self.cpf = cpf
        self.cnpj = cnpj
        self.email = email
        self.senha = senha
        self.tipo_usuario = tipo_usuario


class Produto:
    def __init__(self, id_produto, codigo, nome, marca, preco_unitario):
        self.id_produto = id_produto
        self.codigo = codigo
        self.nome = nome
        self.marca = marca
        self.preco_unitario = preco_unitario


class Sistema:
    def __init__(self):
        self.usuarios = []
        self.produtos = []
        self.carregar_dados()

    def carregar_dados(self):
        if os.path.exists("usuarios.pkl"):
            with open("usuarios.pkl", "rb") as arquivo:
                self.usuarios = pickle.load(arquivo)

        if os.path.exists("produtos.pkl"):
            with open("produtos.pkl", "rb") as arquivo:
                self.produtos = pickle.load(arquivo)

    def salvar_usuarios(self):
        with open("usuarios.pkl", "wb") as arquivo:
            pickle.dump(self.usuarios, arquivo)

    def salvar_produtos(self):
        with open("produtos.pkl", "wb") as arquivo:
            pickle.dump(self.produtos, arquivo)

    def cadastrar_usuario(self):
        print("\n--- CADASTRO DE USUÁRIO ---")

        id_usuario = len(self.usuarios) + 1
        cpf = input("Digite seu CPF: ")
        cnpj = input("Digite seu CNPJ: ")
        email = input("Digite seu e-mail: ")
        senha = input("Digite sua senha: ")
        tipo_usuario = input("Digite o tipo de usuário: ")

        for usuario in self.usuarios:
            if usuario.email == email:
                print("E-mail já cadastrado!")
                return

        novo_usuario = Usuario(
            id_usuario, cpf, cnpj, email, senha, tipo_usuario
        )

        self.usuarios.append(novo_usuario)
        self.salvar_usuarios()

        print("Usuário cadastrado com sucesso!")

    def fazer_login(self):
        print("\n--- LOGIN ---")

        email = input("Digite seu e-mail: ")
        senha = input("Digite sua senha: ")

        for usuario in self.usuarios:
            if usuario.email == email and usuario.senha == senha:
                print("\nLogin realizado com sucesso!")
                return True

        print("E-mail ou senha incorretos!")
        return False

    def listar_produtos(self):
        print("\n--- LISTA DE PRODUTOS ---")

        if not self.produtos:
            print("Nenhum produto cadastrado.")
            return

        for produto in self.produtos:
            print("\nCódigo:", produto.codigo)
            print("Nome:", produto.nome)
            print("Marca:", produto.marca)
            print("Preço unitário: R$", produto.preco_unitario)

    def cadastrar_produto(self):
        print("\n--- CADASTRO DE PRODUTO ---")

        id_produto = len(self.produtos) + 1
        codigo = input("Digite o código do produto: ")

        for produto in self.produtos:
            if produto.codigo == codigo:
                print("Código já cadastrado!")
                return

        nome = input("Digite o nome do produto: ")
        marca = input("Digite a marca: ")
        preco_unitario = float(input("Digite o preço unitário: R$ "))

        novo_produto = Produto(
            id_produto, codigo, nome, marca, preco_unitario
        )

        self.produtos.append(novo_produto)
        self.salvar_produtos()

        print("Produto cadastrado com sucesso!")

    def editar_produto(self):
        print("\n--- EDITAR PRODUTO ---")

        codigo = input("Digite o código do produto que deseja editar: ")

        for produto in self.produtos:
            if produto.codigo == codigo:
                print("Produto encontrado!")

                produto.nome = input("Novo nome: ")
                produto.marca = input("Nova marca: ")
                produto.preco_unitario = float(
                    input("Novo preço: R$ ")
                )

                self.salvar_produtos()

                print("Produto atualizado com sucesso!")
                return

        print("Produto não encontrado!")

    def excluir_produto(self):
        print("\n--- EXCLUIR PRODUTO ---")

        codigo = input("Digite o código do produto que deseja excluir: ")

        for produto in self.produtos:
            if produto.codigo == codigo:
                print("Produto:", produto.nome)

                confirmar = input("Deseja realmente excluir? (s/n): ")

                if confirmar.lower() == "s":
                    self.produtos.remove(produto)
                    self.salvar_produtos()
                    print("Produto excluído com sucesso!")
                else:
                    print("Exclusão cancelada!")

                return

        print("Produto não encontrado!")


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
        if sistema.fazer_login():
            print("Acesso ao sistema autorizado!")

            while True:
                print("\n===== MENU DO SISTEMA =====")
                print("1 - Listar produtos")
                print("2 - Cadastrar produto")
                print("3 - Editar produto")
                print("4 - Excluir produto")
                print("5 - Voltar")

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
                    break

                else:
                    print("Opção inválida!")

    elif opcao == "3":
        print("Sistema encerrado!")
        break

    else:
        print("Opção inválida!")
