from modelos.cedula import Cedula
import json

class CedulasEmBranco(list):
    
    def __init__(self, urnaID, quantidade):
        for _ in range(quantidade):
            self.append(Cedula(urnaID = urnaID))

#========================================================================================================
    def serializar(self):
        return {
            'header':'cedulasEmBranco',
            'cedulas': [c.serializar() for c in self]
        }
    
#========================================================================================================
    def exportar(self, arquivo):
        with open(arquivo, 'w') as f:
            json.dump(self.serializar(), f)
            f.close()