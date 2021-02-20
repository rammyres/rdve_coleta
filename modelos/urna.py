import json, datetime, uuid, binascii
from datetime import datetime
from modelos.cedula import Cedula
from modelos.transacao import Transacao
from modelos.cedulasEmBranco import CedulasEmBranco
from modelos.cedulasPreenchidas import CedulasPreenchidas
from modelos.utxo import UTXO
from ecdsa import SigningKey, VerifyingKey, SECP256k1
from pymerkle import MerkleTree
from Crypto.Hash import SHA256


#========================================================================================================
class Urna:
    urnaID = ''
    endereco = ''
    utxo = None
    cedulasEmBranco = None
    CedulasPreenchidas = CedulasPreenchidas(urnaID)
    chavePrivada = None 
    chavePublica = None 
    regsComparecimento = []

#========================================================================================================
    def __init__(self, qtdEleitores = None, arquivoUrna = None):
        self.urnaID = str(uuid.uuid4())
        self.endereco = 'URNA'
        self.utxo = UTXO(arquivoUTXO='/tmp/utxo.json')
        self.chavePrivada = SigningKey.generate(curve=SECP256k1)
        self.chavePublica = self.chavePrivada.verifying_key

        if qtdEleitores:
            self.cedulasEmBranco = CedulasEmBranco(self.urnaID, qtdEleitores)
    
#========================================================================================================
    def registrarVoto(self, endereco):
        cedula = self.cedulasEmBranco.pop(0)
        assinatura = self.assinar('{}:{}'.format(cedula.ID, endereco))
        cedula.registrarVoto(endereco, assinatura)
        self.CedulasPreenchidas.append(cedula)
        self.utxo.transferirSaldo(
            endereco_origem=self.endereco,
            endereco_destino=endereco,
            assinatura=assinatura,
            saldo_transferido=1
            )

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
    def inserirReqVoto(self, reqvoto):
        sha256 = SHA256.new()
        dados = ':'.join((
                        reqvoto['nome'],
                        reqvoto['endereco'],
                        datetime.now().timestamp.to_string(),
                        reqvoto['assinatura']))

        timestamp = datetime.now().timestamp.to_string()
        if isinstance(reqvoto, dict):
            reg_comparecimento = {
                'eleitor': reqvoto['nome'],
                'endereco': reqvoto['endereco'],
                'timestamp': timestamp,
                'assinatura': reqvoto['assinatura'],
                'hash': sha256.update(dados.encode()).hexdigest()
            }
            self.regsComparecimento.append(reg_comparecimento)

            assinatura = self.assinar(
                ':'.join(
                    (
                        reqvoto['endereco'],
                        self.endereco,
                        '1'
                    )
                )
            )

            self.utxo.transferirSaldo(
                endereco_origem=reqvoto['endereco'],
                endereco_destino=self.endereco,
                saldo_transferido=1,
                assinatura = assinatura
                )
#========================================================================================================
    def serializar(self):
        return {
            'header': 'produtos_de_votacao',
            'urnaID': self.urnaID,
            'chavePrivada': binascii.unhexlify(self.chavePrivada.to_string()).decode(),
            'chavePublica': binascii.unhexlify(self.chavePublica.to_string()).decode(),
            'registros': [registro for registro in self.regsComparecimento],
            'cedulasEmBranco': [cedula.serializar() for cedula in self.cedulasEmBranco],
            'cedulasPreenchidas': [cedula.serializar() for cedula in self.CedulasPreenchidas],

        }
        


#========================================================================================================
    def assinar(self, dados):
        if isinstance(dados, bytes):
            return self.chavePrivada.sign(dados)
        else:
            return self.chavePrivada.sign(binascii.unhexlify(dados))
    
