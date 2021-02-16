from ecdsa import SigningKey, VerifyingKey, SECP256k1
from Crypto.Hash import RIPEMD160, SHA256
from modelos.transacao import Transacao
from datetime import datetime
import binascii, hashlib, base58, json, uuid

class Eleitor:
    ID = ''
    nome = ''
    endereco = ''
    chavePrivada = None
    chavePublica = None
    assinatura = ''

    def __init__(self, nome = None, ID = None, chavePrivada=None, endereco=None, dicionario = None):

        if dicionario:
            self.importar(dicionario)

        else:  
            self.nome = nome
            if chavePrivada and endereco and ID:
                self.ID = ID
                self.chavePrivada = SigningKey.from_string(chavePrivada)
                self.chavePublica = self.chavePrivada.get_verifying_key()
                self.endereco = endereco

            else: 
                self.ID = str(uuid.uuid4())
                self.chavePrivada = SigningKey.generate(curve=SECP256k1)
                self.chavePublica = self.chavePrivada.get_verifying_key()
                self.endereco = self.gerarEndereco()

        self.assinatura = self.assinar(self.dados())

#========================================================================================================
    def gerarEndereco(self):
        
        chavePublica = '04' + binascii.hexlify(self.chavePublica.to_string()).decode()
        hash256 = hashlib.sha256(binascii.unhexlify(chavePublica))
        ripemd160 = RIPEMD160.new()
        ripemd160.update(hash256.hexdigest().encode())
        hash160 = ripemd160.hexdigest()
        enderecoPublico_a = b"\x00" + hash160.encode()
        checksum = hashlib.sha256(hashlib.sha256(enderecoPublico_a).digest()).digest()[:4]
        enderecoPublico_b = base58.b58encode(enderecoPublico_a + checksum)
        
        return enderecoPublico_b.decode()

#========================================================================================================
    def dados(self):
        dados = ':'.join((
            str(self.ID),
            self.nome,
            binascii.hexlify(self.chavePublica.to_string()).hex(),
            self.endereco
            )
        )

        return dados

#========================================================================================================
    def retornaHash(self):      

        Hash = SHA256.new()
        Hash.update(self.dados().encode())
        
        return Hash.hexdigest()

#========================================================================================================
    def assinar(self, dados):
        
        assinatura = ''
        if isinstance(dados, bytes):
            assinatura = self.chavePrivada.sign(dados).to_string()
        else:
            assinatura = binascii.hexlify(self.chavePrivada.sign(bytes(dados, encoding='utf8'))).hex()
        print(assinatura)
        return assinatura

#========================================================================================================
    def importar(self, dicionario):
        self = Eleitor(
            nome = dicionario['nome'],
            ID = dicionario['id'],
            chavePrivada=dicionario['chavePrivada'],
            endereco=dicionario['endereco']
        )
        return self

#========================================================================================================
    def paraJson(self):
        return json.dumps(
            {
            'tipo':'regEleitor',
            'id': self.ID,
            'nome':self.nome,
            'chavePrivada': binascii.hexlify(self.chavePrivada.to_string()).hex(),
            'chavePublica': binascii.hexlify(self.chavePublica.to_string()).hex(),
            'endereco':self.endereco,
            'hash': self.retornaHash().encode().decode()
            }
        )

#========================================================================================================
    def transacaoCriacao(self):
        transacao = Transacao(tipo='criar_endereco',
                              tipo_endereco='eleitor',
                              endereco=self.endereco,
                              assinatura="")
        transacao.assinatura = self.assinar(transacao.dados())
        transacao.gerarHash() 
        return transacao

#========================================================================================================
    def requererVoto(self):
        reqID = str(uuid.uuid4())
        timestamp = str(datetime.now().timestamp())
        dados = ':'.join((self.ID, reqID, timestamp))

        with open('/tmp/reqvoto.json') as f:
            json.dump(
                {
                    'id_eleitor': self.ID,
                    'reqID': reqID,
                    'timestamp': timestamp,
                    'assinatura': self.assinar(binascii.hexlify(dados))
                },
                f
        )


