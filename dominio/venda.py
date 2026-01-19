import uuid
from venda_produto import VendaProduto
class Venda():
    def __init__(self, id_cliente, data_venda, id=str(uuid.uuid4())):
        self.id = id
        self.id_cliente = id_cliente
        self.data_venda = data_venda
        self.produtos = list[VendaProduto] = []

    def to_dict(self):
        return {
            "id":self.id,
            "id_cliente":self.id_cliente,
            "data_venda":self.data_venda,
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(uuid.UUID(data['id']), data['id_cliente'], data['data_venda'])