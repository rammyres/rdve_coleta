import uuid, json

class Cedula:
    ID = ''
    assinatura = ''
    destino = ''

#========================================================================================================
    def __init__(self):
        self.ID = uuid.uuid4()

#========================================================================================================
    def dados(self):
        return ':'.join(
            (self.ID, self.destino, 1)
        )

#========================================================================================================    
    def registrarVoto(self, destino, assinatura):
        self.destino = destino
        self.assinatura = assinatura

#========================================================================================================
    def serializar(self):
        return {
                'id': self.ID,
                'destino': self.destino,
                'saldo': 1,
                'assinatura': self.assinatura
            }

