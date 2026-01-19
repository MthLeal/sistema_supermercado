import os
import textwrap
import json
import pandas as pd
import time
from dominio.produto import Produto


def carregar_objetos_arquivo(arquivo: str) -> list[dict]:
    objetos = []

    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            objetos = json.load(f)
    return objetos


def salvar_produto(produto, arquivo="data/produtos.json", excluir=False):
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


def procurar_produto(nome_produto: str, arquivo="data/produtos.json") -> Produto:
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
        tabela_produtos = pd.read_json("data/produtos.json")
        colunas_renomeadas = {"nome":"Nome do Produto", "preco":"Preço", "quantidade_estoque":"Quantidade em Estoque"}
        tabela_produtos = tabela_produtos.rename(columns=colunas_renomeadas)
        tabela_formatada = tabela_produtos.to_string(columns=["Nome do Produto", "Preço", "Quantidade em Estoque"], index=False)
        print(tabela_formatada)
        input("\n\nDigite qualquer texto para sair da tela de visualização:")
        break
    limpar_tela()


def existe_produtos_estoque():
    produtos_estoque = carregar_objetos_arquivo("data/produtos.json")
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