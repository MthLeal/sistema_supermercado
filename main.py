import os
import textwrap
import uuid
import json
import pandas as pd
import time

class Produto():
    def __init__(self, nome: str, preco: float, quantidade_estoque: int, id:str | None = None):
        self.id = id if id is not None else str(uuid.uuid4())
        self.nome = nome
        self.__preco = preco
        self.__quantidade_estoque = quantidade_estoque

    def atualizar_produto(self,novo_nome, novo_preco, nova_quantidade):
        if novo_preco < 0 and nova_quantidade < 0:
            raise ValueError("Preço inválido")
        self.nome = novo_nome
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
        return cls(data['nome'], data['preco'], data['quantidade_estoque'], data['id'])


class Cliente():
    def __init__(self, nome, cpf, telefone, id=str(uuid.uuid4())):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.numero_telefone = telefone

    def to_dict(self):
        return {
            "id":self.id,
            "nome":self.nome,
            "cpf":self.cpf,
            "numero_telefone":self.numero_telefone,
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(uuid.UUID(data['id']), data['nome'], data['cpf'], data['numero_telefone'])

class Venda():
    def __init__(self, id_cliente, data_venda, id=str(uuid.uuid4())):
        self.id = id
        self.id_cliente = id_cliente
        self.data_venda = data_venda

    def to_dict(self):
        return {
            "id":self.id,
            "id_cliente":self.id_cliente,
            "data_venda":self.data_venda,
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(uuid.UUID(data['id']), data['id_cliente'], data['data_venda'])

class VendaProduto():
    def __init__(self, id_venda, id_produto, quantidade_produto, id=str(uuid.uuid4())):
        self.id = id
        self.id_venda = id_venda
        self.id_produto = id_produto
        self.quantidade_produto = quantidade_produto

    def to_dict(self):
        return {
            "id":self.id,
            "id_venda":self.id_venda,
            "id_produto":self.id_produto,
            "quantidade_produto":self.quantidade_produto,
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(uuid.UUID(data['id']), data['id_venda'], data['id_produto'], data['quantidade_produto'])

def carregar_objetos_arquivo(arquivo: str) -> list[dict]:
    objetos = []

    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            objetos = json.load(f)
    return objetos



def salvar_produto(produto, arquivo="produtos.json", excluir=False):
    produtos = carregar_objetos_arquivo(arquivo)

    # Verifica duplicidade
    if not excluir and any(p['nome'].lower() == produto.nome.lower() and p['id'] != produto.id for p in produtos):
        raise ValueError("Produto já existe")
    
    for i, p in enumerate(produtos):
        if p["id"] == produto.id:
            if not excluir:
                produtos[i] = produto.to_dict()  # sobrescreve
            else:
                produtos.remove(produto.to_dict())
            break
    else:
        # Adiciona novo produto
        produtos.append(produto.to_dict())

    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(produtos, f, indent=2, ensure_ascii=False)


def procurar_produto(nome_produto: str, arquivo="produtos.json") -> Produto:
    #Função que procura um produto dentro do arquivo json de produtos
    produto = None
    produtos = carregar_objetos_arquivo(arquivo)
    for p in produtos:
        if p["nome"].lower() == nome_produto.lower():
            produto = Produto.from_dict(p)
            break
    return produto



def adicionar_produto(id_produto=None):
    if id_produto is None:
        print("Cadastre um produto:")
    else:
        print("Forneça as novas informações do produto:")
    while True:
        nome_produto = input("Forneça o nome do produto:")
        produto = procurar_produto(nome_produto)
        if produto is not None and id_produto is None:
            print("Produto já cadastrado, insira outro nome.")
        else:
            break
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
    if not produto:
        produto = Produto(nome_produto, preco_produto, quantidade_estoque, id_produto)
    else:
        produto.atualizar_produto(nome_produto, preco_produto, quantidade_estoque)
    salvar_produto(produto=produto)
    limpar_tela()



def visualizar_estoque():
    while True:
        if not existe_produtos_estoque():
            print("Estoque vazio, cadastre um produto para visualizar o estoque.\n" \
            "Voltando para tela Inicial")
            time.sleep(8)
            break
        tabela_produtos = pd.read_json("produtos.json")
        colunas_renomeadas = {"nome":"Nome do Produto", "preco":"Preço", "quantidade_estoque":"Quantidade em Estoque"}
        tabela_produtos = tabela_produtos.rename(columns=colunas_renomeadas)
        tabela_formatada = tabela_produtos.to_string(columns=["Nome do Produto", "Preço", "Quantidade em Estoque"], index=False)
        print(tabela_formatada)
        input("\n\nDigite qualquer texto para sair da tela de visualização:")
        break
    limpar_tela()

def existe_produtos_estoque():
    produtos_estoque = carregar_objetos_arquivo("produtos.json")
    return len(produtos_estoque) != 0

def atualizar_produto():
    while True:
        if not existe_produtos_estoque():
            print("Não há produtos no estoque, adicione produtos para poder realizar a ação de atualizar produto.\n"
            "Voltando para a tela inicial")
            time.sleep(8)
            break

        nome_produto = input("Digite o nome do produto que deseja atualizar:")
        produto = procurar_produto(nome_produto)
        if produto is None:
            print("Produto não encontrado")
        else:
            # Adiciona o produto, porém com o mesmo id, sobreescrevendo o objeto no json, reaproveitando lógica
            adicionar_produto(produto.id)
            break
    limpar_tela()



def excluir_produto():
    while True:
            if not existe_produtos_estoque():
                print("Não há produtos no estoque, adicione produtos para poder realizar a ação de excluir produto.\n"
                "Voltando para a tela inicial")
                time.sleep(8)
                break
            nome_produto = input("Digite o nome do produto que deseja excluir:")
            produto = procurar_produto(nome_produto=nome_produto)
            if produto is None:
                print("Produto não encontrado, certifique que o nome está correto")
            else:
                salvar_produto(produto=produto, excluir=True)
                break
    limpar_tela()



def sair_do_sistema():
    print("Saindo do Sistema.")



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
        print("Operação finalizada com sucesso!")

if __name__ == "__main__":
    main()