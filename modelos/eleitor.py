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
    Hash = ''

    def __init__(self, 
            nome, 
            ID = None, 
            chavePrivada=None, 
            chavePublica = None,
            endereco=None, 
            ):

        if nome and ID and chavePrivada and chavePublica and endereco:  
            self.nome = nome
            self.ID = ID
            self.chavePrivada = SigningKey.from_string(string=binascii.unhexlify(chavePrivada), curve=SECP256k1)
            self.chavePublica = VerifyingKey.from_string(
                string = binascii.unhexlify(chavePublica), 
                curve=SECP256k1
                )
            self.endereco = endereco

        elif nome and not ID and not chavePrivada and not chavePublica and not endereco: 
            self.nome = nome
            self.ID = str(uuid.uuid4())
            self.chavePrivada = SigningKey.generate(curve=SECP256k1)
            self.chavePublica = self.chavePrivada.verifying_key
            self.endereco = self.gerarEndereco()

        else:
            raise TypeError("Eleitor invalido, pulando")

        self.gerarHash()
        
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
            self.ID,
            self.nome,
            binascii.hexlify(self.chavePublica.to_string()).hex(),
            self.endereco
            )
        )

        return dados

#========================================================================================================
    def gerarHash(self):      

        Hash = SHA256.new()
        Hash.update(self.dados().encode())
        
        self.Hash = Hash.hexdigest()

#========================================================================================================
    def assinar(self, dados):
        
        assinatura = ''
        if isinstance(dados, bytes):
            assinatura = self.chavePrivada.sign(dados).to_string()
        else:
            assinatura = binascii.hexlify(self.chavePrivada.sign(bytes(dados, encoding='utf8'))).hex()
        
        return assinatura

#========================================================================================================
    def serializar(self):
        
        return {
            'tipo':'regEleitor',
            'id': self.ID,
            'nome':self.nome,
            'chavePrivada': binascii.hexlify(self.chavePrivada.to_string()).decode(),
            'chavePublica': binascii.hexlify(self.chavePublica.to_string()).decode(),
            'endereco':self.endereco,
            'hash': self.Hash
            }
        
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
        # timestamp = str(datetime.now().timestamp())
        dados = ':'.join((self.ID, reqID))
        print(len(dados))
        print(dados)

        with open('/tmp/reqvoto.json', 'w') as f:
            json.dump(
                {
                    'id_eleitor': self.ID,
                    'reqID': reqID,
                    # 'timestamp': timestamp,
                    'assinatura': self.assinar(dados)
                }, f
        )


