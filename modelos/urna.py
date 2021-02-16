import json, datetime
from modelos.candidato import Candidato
from modelos.eleitor import Eleitor
from modelos.registro import Registros
from modelos.cedula import Cedula
from modelos.utxo import UTXO

class registroComparecimento:
    id_eleitor = ''
    assinatura = ''

#========================================================================================================    
    def __init__(self, eleitor, assinatura):
        self.id_eleitor = eleitor.ID
        self.assinatura = assinatura

#========================================================================================================
    def serializar(self):
        return {
                'id_eleitor': self.id_eleitor,
                'timestamp': str(datetime.datetime.now().timestamp()),
                'assinatura': self.assinatura
            }

#========================================================================================================
class Urna:
    cedulas = []
    eleitores = []
    candidatos = []
    registros = Registros() 
    utxo = UTXO

    def __init__(self):
        try:
            with open("/tmp/registros.json", 'r') as f:
                print(f)
                self.registros.importar(f)
        except IOError:
            print("Arquivo inexistente")

#========================================================================================================
    