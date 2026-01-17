import uuid

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