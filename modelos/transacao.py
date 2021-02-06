import json, uuid
from hashlib import sha256

class Transacao:
    ID = ''

    endereco_origem = ''
    endereco_destino = ''
    saldo_transferido = 0
    assinatura = ''
    Hash = ''

    def __init__(self, endereco_origem, endereco_destino, saldo_transferido, assinatura):
        self.ID = uuid.uuid4()
        self.endereco_destino = endereco_destino
        self.endereco_origem = endereco_origem
        self.saldo_transferido = saldo_transferido
        self.assinatura = assinatura


    def dados(self): 
        return ':'.join(
            (
                self.ID,
                self.endereco_origem,
                self.endereco_destino,
                self.saldo_transferido,
                self.assinatura
            )
        )
        
    def gerarHash(self):
        h = sha256()
        h.update(self.dados().encode())

        return h.hexdigest()

    
    def paraJson(self):
        return json.dumps(
            {
                'id': self.ID,
                'endereco_origem': self.endereco_destino,
                'endereco_destino': self.endereco_destino,
                'saldo_transferido': self.saldo_transferido,
                'assinatura': self.assinatura,
                'hash': self.Hash
            }, indent=4
        )