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
    candidatos = []
    regsComparecimento = []
    registros = Registros() 
    utxo = None

    def __init__(self):

        self.registros.importar("/tmp/registros.json")
        self.utxo = UTXO(arquivoUTXO='/tmp/utxo.json')

        if len(self.registros.candidatos)>0:
            for c in self.registros.eleitores:
                self.candidatos.append({
                    'apelido': c.apelido,
                    'numero': c.numero,
                    'endereco': c.endereco
                    }
                )
        
#========================================================================================================
# Retorna o dict referente ao candidato
#========================================================================================================
    def retornarCandidatoPorNumero(self, numero):
        for c in self.candidatos:
            if c.numero == numero:
                return self.candidatos[self.candidatos.index(c)]

        return None

# ========================================================================================================
    # def s

#========================================================================================================
    