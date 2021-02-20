import json, datetime, uuid, binascii
from datetime import datetime
from modelos.cedula import Cedula
from modelos.transacao import Transacao
from modelos.cedulasEmBranco import CedulasEmBranco
from modelos.cedulasPreenchidas import CedulasPreenchidas
from modelos.utilitarios import Utilitarios
from modelos.registro import Registros
from modelos.utxo import UTXO
from ecdsa import SigningKey, VerifyingKey, SECP256k1
from pymerkle import MerkleTree
from Crypto.Hash import SHA256


#========================================================================================================
class Urna:
    util = Utilitarios()
    urnaID = ''
    endereco = ''
    utxo = None
    cedulasEmBranco = None
    CedulasPreenchidas = CedulasPreenchidas(urnaID)
    chavePrivada = None 
    chavePublica = None 
    regsComparecimento = []
    reigstros = Registros()
    arvore = None

#========================================================================================================
    def __init__(self, qtdEleitores = None, arquivoUrna = None):
        self.reigstros.importar('/tmp/registros.json')

        if qtdEleitores:
            self.cedulasEmBranco = CedulasEmBranco(self.urnaID, qtdEleitores)
            self.utxo = UTXO(arquivoUTXO='/tmp/utxo.json')

        if not arquivoUrna: 
            self.urnaID = str(uuid.uuid4())
            self.endereco = 'URNA'
            self.chavePrivada = SigningKey.generate(curve=SECP256k1)
            self.chavePublica = self.chavePrivada.verifying_key
            self.arvore = MerkleTree()

        if arquivoUrna:
            with open(arquivoUrna, 'r') as f:
                tmp = json.load(arquivoUrna)
                self.urnaID = tmp['urnaID']
                self.endereco = tmp['endereco']
                self.chavePrivada = SigningKey.from_string(
                    string=binascii.unhexlify(tmp['chavePrivada']), 
                    curve=SECP256k1
                    )
                self.chavePublica = VerifyingKey.from_string(
                    string = binascii.unhexlify(tmp['chavePublica']), 
                    curve=SECP256k1
                    )
                self.regsComparecimento = [reg for reg in tmp['registros']]
                self.CedulasPreenchidas.importarCedulas([cedula for cedula in tmp['cedulasPreenchidas']])
                self.cedulasEmBranco = qtdEleitores - len(self.CedulasPreenchidas)
                
                with open('/tmp/arv_urna_tmp.json', 'w') as arv_tmp:
                    json.dump(tmp['arvore'], arv_tmp)
                    self.arvore = MerkleTree.loadFromFile(arv_tmp)
                    arv_tmp.close()            
                    self.util.remover_seguramente('/tmp/arv_urna_tmp.json', 4)
                f.close()
    
#========================================================================================================
    def registrarVoto(self, endereco):
        sha256 = SHA256.new()
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
        dados = ':'.join((self.endereco, endereco, assinatura))
        self.arvore.update(sha256.update(dados.encode()).hexdigest())
        

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
        print(reqvoto)
        sha256 = SHA256.new()
        timestamp = str(datetime.now().timestamp())
        dados = ':'.join((
                        reqvoto['id_eleitor'],
                        reqvoto['reqID'],
                        timestamp,
                        reqvoto['assinatura']))
        print(dados)

        if isinstance(reqvoto, dict):
            sha256.update(dados.encode())
            reg_comparecimento = {
                'id_eleitor': reqvoto['id_eleitor'],
                'reqID': reqvoto['reqID'],
                'timestamp': timestamp,
                'assinatura': reqvoto['assinatura'],
                'hash': sha256.digest()
            }
            self.regsComparecimento.append(reg_comparecimento)

            assinatura = self.assinar(':'.join(reg_comparecimento))
            self.arvore.update(reg_comparecimento['hash'])

            endereco_eleitor = self.reigstros.retornaEnderecoPeloID(reqvoto['id_eleitor'])

            self.utxo.transferirSaldo(
                endereco_origem=endereco_eleitor,
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
            'arvore': self.arvore.serialize()

        }

#========================================================================================================
    def produtos_de_votacao(self):
        with open('/tmp/produtos_votacao.json', 'w') as f:
            json.dump(self.serializar(), f, indent=4)


#========================================================================================================
    def assinar(self, dados):
        
        assinatura = ''
        if isinstance(dados, bytes):
            assinatura = self.chavePrivada.sign(dados).to_string()
        else:
            assinatura = binascii.hexlify(self.chavePrivada.sign(bytes(dados, encoding='utf8'))).hex()
        
        return assinatura
    
