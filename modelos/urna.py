import json, datetime, uuid, binascii
from modelos.candidato import Candidato
from modelos.eleitor import Eleitor
from modelos.registro import Registros
from modelos.cedula import Cedula
from modelos.cedulasEmBranco import CedulasEmBranco
from modelos.cedulasPreenchidas import CedulasPreenchidas
from modelos.utxo import UTXO
from modelos.transacao import Transacao
from ecdsa import SigningKey, VerifyingKey, SECP256k1
from pymerkle import MerkleTree

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
    urnaID = ''
    endereco = ''
    chavePrivada = None
    chavePublica = None
    cedulasEmBranco = None
    cedulasPreenchidas = None
    candidatos = []
    regsComparecimento = []
    registros = Registros() 
    utxo = None

    def __init__(self):
        self.urnaID = str(uuid.uuid4())
        self.chavePrivada = SigningKey.generate(curve=SECP256k1)
        self.cedulasPreenchidas = CedulasPreenchidas(self.urnaID)
        self.registros.importar("/tmp/registros.json")
        self.utxo = UTXO(arquivoUTXO='/tmp/utxo.json')
        self.cedulasEmBranco = CedulasEmBranco(
                                quantidade = len(self.registros.eleitores),
                                urnaID = self.urnaID
                                )

        if len(self.registros.candidatos)>0:
            for c in self.registros.candidatos:
                self.candidatos.append({
                    'apelido': c.apelido,
                    'numero': c.numero,
                    'endereco': c.endereco
                    }
                )

        self.utxo.novoEndereco(self.transacaoCriacao())
        
        self.imporarReqVoto(arquivo='/tmp/reqvoto.json')
        
#========================================================================================================
# Retorna o dict referente ao candidato
#========================================================================================================

    def transacaoCriacao(self):
        transacao = Transacao(
            tipo='criar_endereco',
            tipo_endereco='urna',
            endereco_destino=self.endereco,
            assinatura=self
        )
        return transacao
#========================================================================================================

    def transferirSaldo(self, endereco_origem, endereco_destino):


#========================================================================================================

    def assinar(self, dados):
        if isinstance(dados, bytes):
            return self.chavePrivada.sign(dados)
        else:
            return self.chavePrivada.sign(binascii.unhexlify(dados))

#========================================================================================================
    def retornarCandidatoPorNumero(self, numero):
        for c in self.candidatos:
            if c.numero == numero:
                return self.candidatos[self.candidatos.index(c)]
        return None

# ========================================================================================================
    def registrarVoto(self, numero):
        cedula = self.cedulasEmBranco.pop(0)
        cedula.registrarVoto(
            self.retornarCandidatoPorNumero(numero=numero)['endereco']
            )

#========================================================================================================
    