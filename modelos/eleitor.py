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
            processo,
            nome = None, 
            ID = None, 
            chavePrivada=None, 
            endereco=None, 
            dicionario = None):

        
        if processo == 'importar' and dicionario:
            self.importar(dicionario)

        elif processo == 'importacao_interna' :  
            self.nome = nome
            self.ID = ID
            self.chavePrivada = SigningKey.from_string(string=binascii.unhexlify(chavePrivada), curve=SECP256k1)
            self.chavePublica = self.chavePrivada.get_verifying_key()
            self.endereco = endereco

        elif processo == 'criar' and nome: 
            self.nome = nome
            self.ID = str(uuid.uuid4())
            self.chavePrivada = SigningKey.generate(curve=SECP256k1)
            self.chavePublica = self.chavePrivada.get_verifying_key()
            self.endereco = self.gerarEndereco()

        else:
            raise TypeError("A criação do eleitor falhou")

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
    def importar(self, dicionario):
        print("Importando...")
        self = Eleitor(
            processo='impotacao_interna',
            nome = dicionario['nome'],
            ID = dicionario['id'],
            chavePrivada=dicionario['chavePrivada'],
            endereco=dicionario['endereco']
        )
        return self

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
        timestamp = str(datetime.now().timestamp())
        dados = ':'.join((self.ID, reqID, timestamp))

        with open('/tmp/reqvoto.json') as f:
            json.dump(
                {
                    'id_eleitor': self.ID,
                    'reqID': reqID,
                    'timestamp': timestamp,
                    'assinatura': self.assinar(binascii.hexlify(dados).decode())
                },
                f
        )


