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
    def __init__(self, id_produto, codigo, nome, marca, preco_unitario, cnpj_vendedor):
        self.id_produto = id_produto
        self.codigo = codigo
        self.nome = nome
        self.marca = marca
        self.preco_unitario = preco_unitario
        self.cnpj_vendedor = cnpj_vendedor


class Fornecedor:
    def __init__(self, id_fornecedor, nome, cnpj, endereco, telefone):
        self.id_fornecedor = id_fornecedor
        self.nome = nome
        self.cnpj = cnpj
        self.endereco = endereco
        self.telefone = telefone


class Notificacao:
    def __init__(self, id_notificacao, mensagem, data):
        self.id_notificacao = id_notificacao
        self.mensagem = mensagem
        self.data = data


class Movimentacao:
    def __init__(self, id_movimentacao, tipo, quantidade, data):
        self.id_movimentacao = id_movimentacao
        self.tipo = tipo
        self.quantidade = quantidade
        self.data = data


class Sistema:
    def __init__(self):
        self.usuarios = []
        self.produtos = []
        self.fornecedores = []
        self.notificacoes = []
        self.movimentacoes = []
        self.carregar_dados()

    def carregar_dados(self):
        arquivos = [
            ("usuarios.pkl", "usuarios"),
            ("produtos.pkl", "produtos"),
            ("fornecedores.pkl", "fornecedores"),
            ("notificacoes.pkl", "notificacoes"),
            ("movimentacoes.pkl", "movimentacoes")
        ]

        for nome_arquivo, lista in arquivos:
            if os.path.exists(nome_arquivo):
                with open(nome_arquivo, "rb") as arquivo:
                    setattr(self, lista, pickle.load(arquivo))

    def salvar_usuarios(self):
        with open("usuarios.pkl", "wb") as arquivo:
            pickle.dump(self.usuarios, arquivo)

    def salvar_produtos(self):
        with open("produtos.pkl", "wb") as arquivo:
            pickle.dump(self.produtos, arquivo)

    def salvar_fornecedores(self):
        with open("fornecedores.pkl", "wb") as arquivo:
            pickle.dump(self.fornecedores, arquivo)

    def salvar_notificacoes(self):
        with open("notificacoes.pkl", "wb") as arquivo:
            pickle.dump(self.notificacoes, arquivo)

    def salvar_movimentacoes(self):
        with open("movimentacoes.pkl", "wb") as arquivo:
            pickle.dump(self.movimentacoes, arquivo)

    def cadastrar_usuario(self):
        print("\n--- CADASTRO DE USUÁRIO ---")

        id_usuario = len(self.usuarios) + 1
        cpf = input("Digite seu CPF: ")
        cnpj = input("Digite o CNPJ da loja: ")
        email = input("Digite seu e-mail: ")
        senha = input("Digite sua senha: ")

        print("\n1 - Vendedor")
        print("2 - Visualizador")
        tipo = input("Escolha o tipo de usuário: ")

        if tipo == "1":
            tipo_usuario = "vendedor"
        elif tipo == "2":
            tipo_usuario = "visualizador"
        else:
            print("Tipo de usuário inválido!")
            return

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
                return usuario

        print("E-mail ou senha incorretos!")
        return None

    def listar_produtos(self, cnpj):
        print("\n--- ESTOQUE DA LOJA ---")

        encontrados = False

        for produto in self.produtos:
            if getattr(produto, "cnpj_vendedor", "") == cnpj:
                print("\nCódigo:", produto.codigo)
                print("Nome:", produto.nome)
                print("Marca:", produto.marca)
                print("Preço unitário: R$", produto.preco_unitario)
                encontrados = True

        if not encontrados:
            print("Nenhum produto encontrado para esse CNPJ.")

    def cadastrar_produto(self, usuario):
        print("\n--- CADASTRO DE PRODUTO ---")

        id_produto = len(self.produtos) + 1
        codigo = input("Digite o código do produto: ")

        for produto in self.produtos:
            if (produto.codigo == codigo and
                    getattr(produto, "cnpj_vendedor", "") == usuario.cnpj):
                print("Código já cadastrado nessa loja!")
                return

        nome = input("Digite o nome do produto: ")
        marca = input("Digite a marca: ")
        preco_unitario = float(input("Digite o preço unitário: R$ "))

        novo_produto = Produto(
            id_produto, codigo, nome, marca,
            preco_unitario, usuario.cnpj
        )

        self.produtos.append(novo_produto)
        self.salvar_produtos()

        print("Produto cadastrado com sucesso!")

    def editar_produto(self, usuario):
        print("\n--- EDITAR PRODUTO ---")

        codigo = input("Digite o código do produto que deseja editar: ")

        for produto in self.produtos:
            if (produto.codigo == codigo and
                    getattr(produto, "cnpj_vendedor", "") == usuario.cnpj):

                print("Produto encontrado!")

                produto.nome = input("Novo nome: ")
                produto.marca = input("Nova marca: ")
                produto.preco_unitario = float(input("Novo preço: R$ "))

                self.salvar_produtos()

                print("Produto atualizado com sucesso!")
                return

        print("Produto não encontrado na sua loja!")

    def excluir_produto(self, usuario):
        print("\n--- EXCLUIR PRODUTO ---")

        codigo = input("Digite o código do produto que deseja excluir: ")

        for produto in self.produtos:
            if (produto.codigo == codigo and
                    getattr(produto, "cnpj_vendedor", "") == usuario.cnpj):

                print("Produto:", produto.nome)

                confirmar = input("Deseja realmente excluir? (s/n): ")

                if confirmar.lower() == "s":
                    self.produtos.remove(produto)
                    self.salvar_produtos()
                    print("Produto excluído com sucesso!")
                else:
                    print("Exclusão cancelada!")

                return

        print("Produto não encontrado na sua loja!")

    def menu_vendedor(self, usuario):
        while True:
            print("\n===== MENU DO VENDEDOR =====")
            print("1 - Listar meus produtos")
            print("2 - Cadastrar produto")
            print("3 - Editar produto")
            print("4 - Excluir produto")
            print("5 - Voltar")

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.listar_produtos(usuario.cnpj)

            elif opcao == "2":
                self.cadastrar_produto(usuario)

            elif opcao == "3":
                self.editar_produto(usuario)

            elif opcao == "4":
                self.excluir_produto(usuario)

            elif opcao == "5":
                break

            else:
                print("Opção inválida!")

    def menu_visualizador(self):
        while True:
            print("\n===== MENU DO VISUALIZADOR =====")
            print("1 - Consultar estoque de uma loja")
            print("2 - Voltar")

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                cnpj = input("Digite o CNPJ do vendedor: ")
                self.listar_produtos(cnpj)

            elif opcao == "2":
                break

            else:
                print("Opção inválida!")


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
        usuario = sistema.fazer_login()

        if usuario:
            if usuario.tipo_usuario == "vendedor":
                sistema.menu_vendedor(usuario)

            elif usuario.tipo_usuario == "visualizador":
                sistema.menu_visualizador()

            else:
                print("Tipo de usuário não reconhecido!")

    elif opcao == "3":
        print("Sistema encerrado!")
        break

    else:
        print("Opção inválida!")
