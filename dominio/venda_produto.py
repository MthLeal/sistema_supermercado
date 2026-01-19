import   uuid

class VendaProduto():
    def __init__(self, id_produto, quantidade_produto, id=str(uuid.uuid4())):
        self.id = id
        self.id_produto = id_produto
        self.quantidade_produto = quantidade_produto

    def to_dict(self):
        return {
            "id":self.id,
            "id_produto":self.id_produto,
            "quantidade_produto":self.quantidade_produto,
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(uuid.UUID(data['id']), data['id_venda'], data['id_produto'], data['quantidade_produto'])