import os
import textwrap
import uuid
import json

class Produto():
    def __init__(self, nome: str, preco: float, quantidade_estoque: int, id:str | None = None):
        self.id = id if id is not None else str(uuid.uuid4())
        self.nome = nome
        self.__preco = preco
        self.__quantidade_estoque = quantidade_estoque
    
    def atualizar_produto(self, novo_preco, nova_quantidade):
        if novo_preco < 0 and nova_quantidade < 0:
            raise ValueError("Preço inválido")
        self.__preco = novo_preco
        self.__quantidade_estoque = nova_quantidade

    def to_dict(self):
        return {
            "id":self.id,
            "nome":self.nome,
            "preco":self.__preco,
            "quantidade_estoque":self.__quantidade_estoque,
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data['id'], data['nome'], data['preco'], data['quantidade_estoque'])

# class Cliente():
#     def __init__(self, nome, cpf, telefone, id=str(uuid.uuid4())):
#         self.id = id
#         self.nome = nome
#         self.cpf = cpf
#         self.numero_telefone = telefone

#     def to_dict(self):
#         return {
#             "id":self.id,
#             "nome":self.nome,
#             "cpf":self.cpf,
#             "numero_telefone":self.numero_telefone,
#         }
    
#     @classmethod
#     def from_dict(cls, data):
#         return cls(uuid.UUID(data['id']), data['nome'], data['cpf'], data['numero_telefone'])

# class Venda():
#     def __init__(self, id_cliente, data_venda, id=str(uuid.uuid4())):
#         self.id = id
#         self.id_cliente = id_cliente
#         self.data_venda = data_venda

#     def to_dict(self):
#         return {
#             "id":self.id,
#             "id_cliente":self.id_cliente,
#             "data_venda":self.data_venda,
#         }
    
#     @classmethod
#     def from_dict(cls, data):
#         return cls(uuid.UUID(data['id']), data['id_cliente'], data['data_venda'])

# class VendaProduto():
#     def __init__(self, id_venda, id_produto, quantidade_produto, id=str(uuid.uuid4())):
#         self.id = id
#         self.id_venda = id_venda
#         self.id_produto = id_produto
#         self.quantidade_produto = quantidade_produto

#     def to_dict(self):
#         return {
#             "id":self.id,
#             "id_venda":self.id_venda,
#             "id_produto":self.id_produto,
#             "quantidade_produto":self.quantidade_produto,
#         }
    
#     @classmethod
#     def from_dict(cls, data):
#         return cls(uuid.UUID(data['id']), data['id_venda'], data['id_produto'], data['quantidade_produto'])
    


def carregar_objetos_arquivo(arquivo: str):
    objetos = []

    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            objetos = json.load(f)
    return objetos



def salvar_produto(produto, arquivo="produtos.json"):
    produtos = carregar_objetos_arquivo(arquivo)

    # Verifica duplicidade
    if any(p['nome'].lower() == produto.nome.lower() for p in produtos) and produto.id not in produtos:
        raise ValueError("Produto já existe")
    
    for i, p in enumerate(produtos):
        if p["id"] == produto.id:
            produtos[i] = produto.to_dict()  # sobrescreve
            break
    else:
        produtos.append(produto.to_dict())

    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(produtos, f, indent=2, ensure_ascii=False)



def procurar_produto(nome_produto: str, arquivo="produtos.json") -> Produto:
    produto = None
    produtos = carregar_objetos_arquivo(arquivo)
    for i, p in enumerate(produtos):
        if p["nome"].lower() == nome_produto.lower():
            produto = Produto.from_dict(p)
    return produto

def adicionar_produto():
    print("Cadastre um produto:")
    nome_produto = input("Forneça o nome do produto:")
    while True:
        try:
            preco_produto = float(input("Preço: R$").replace(",", "."))
            if preco_produto < 0:
                raise ValueError
            break
        except ValueError:
            print("Digite um preço válido.")
    while True:
        quantidade_estoque = input("Forneça a quantidade do produto:")
        if quantidade_estoque.isdigit():
            quantidade_estoque = int(quantidade_estoque)
            break
        print("Digite apenas números.")
    produto = Produto(nome_produto, preco_produto, quantidade_estoque)
    salvar_produto(produto=produto)



def visualizar_estoque():
    print("visualizei")



def atualizar_produto():
    while True:
        nome_produto = input("Digite o nome do produto que deseja atualizar:")
        produto = procurar_produto(nome_produto)
        if produto is None:
            print("Produto não encontrado")
        else:
            salvar_produto(produto)
            break


def excluir_produto():
    print("exclui")



def sair_do_sistema():
    print("sai")



def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')



def selecionar_opcao() -> int:
    menu = """
    Selecione uma opção:
    1. Adicionar produto
    2. Atualizar produto
    3. Excluir produto
    4. Visualizar estoque
    5. Sair do sistema
    """ 
    opcoes_validas = {'1', '2', '3', '4', '5'}
    quantidade_tentativas = 0
    while True:
        print(textwrap.dedent(menu))
        opcao_selecionada = input("Digite uma opção: ")
        limpar_tela()
        if opcao_selecionada in opcoes_validas:
            return int(opcao_selecionada)
        quantidade_tentativas += 1
        print(f'Opção inválida!\n')



def main():
    opcao = 0
    while True and opcao != 5:
        opcoes = {
            1:adicionar_produto,
            2:atualizar_produto,
            3:excluir_produto,
            4:visualizar_estoque,
            5:sair_do_sistema,
        }
        opcao = selecionar_opcao()
        
        func = opcoes.get(opcao)
        if func:
            func()
        limpar_tela()
        print("Operação Finalizada!")

if __name__ == "__main__":
    main()