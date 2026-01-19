
import uuid

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