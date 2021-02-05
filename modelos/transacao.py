import json

class Transacao:
    endereco_origem = ''
    endereco_destino = ''
    saldo = 1
    def __init__(self, endereco_origem, endereco_destino):
        self.endereco_destino = endereco_destino
        self.endereco_origem = endereco_origem
        
    
    def paraJson(self):
        return json.dumps(
            {
                'endereco_origem': self.endereco_destino,
                'endereco_destino': self.endereco_destino,
                'saldo': 1
            }, indent=4
        )