import uuid, json

class Cedula:
    urnaID = ''
    ID = ''
    assinatura = ''
    endereco_destino = ''

#========================================================================================================
    def __init__(self, urnaID, ID = None, endereco_destino = None, assinatura = None):
        self.urnaID = urnaID
        if not ID and not endereco_destino and not assinatura:
            self.ID = str(uuid.uuid4())
        else:
            self.ID = ID
            self.endereco_destino = endereco_destino
            self.assinatura = assinatura

#========================================================================================================
    def dados(self):
        return ':'.join(
            (self.urnaID, self.ID, self.destino, 1)
        )

#========================================================================================================    
    def registrarVoto(self, destino, assinatura):
        self.destino = destino
        self.assinatura = assinatura

#========================================================================================================
    def serializar(self):
        return {
                'urnaID': self.urnaID,
                'id': self.ID,
                'destino': self.endereco_destino,
                'saldo': 1,
                'assinatura': self.assinatura
            }

