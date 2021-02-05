import uuid, json

class Cedula:
    ID = ''
    assinatura = ''
    _destino = ''

    @property
    def destino(self):
        return self._destino

    @destino.setter
    def destino(self, endereco_destino):
        self._destino = endereco_destino

    def __init__(self):
        self.ID = uuid.uuid4()

    def dados(self):
        return ':'.join(
            (self.ID, self.destino, 1)
        )
    
    def registrarVoto(self, destino, assinatura):
        self.destino = destino
        self.assinatura = assinatura


    def paraJson(self):
        return json.dumps(
            {
                'id': self.ID,
                'destino': self.destino,
                'saldo': 1,
                'assinatura': self.assinatura
            }
        )

