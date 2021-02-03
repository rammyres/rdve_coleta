from ecdsa import SigningKey, VerifyingKey, SECP256k1
from Crypto.Hash import RIPEMD160, SHA256
import binascii, hashlib, base58, json, uuid

class Eleitor:
    ID = ''
    apelido = ''
    numero = ''
    endereco = ''
    chavePrivada = SigningKey()
    
    def __init__(self, apelido, numero, ID = None, chavePrivada=None, endereco=None):

        self.apelido = apelido
        self.numero = numero

        if chavePrivada and endereco and ID:
            self.ID = ID
            self.chavePrivada = SigningKey.from_string(chavePrivada)
            self.endereco = endereco

        else: 
            self.ID = uuid.uuid4()
            self.chavePrivada = SigningKey.generate(curve=SECP256k1)
            self.endereco = self.gerarEndereco()

        self.chavePublica = self.chavePrivada.verifying_key


    def gerarEndereco(self):
        
        chavePublica = '04' + binascii.hexlify(self.chavePublica.to_string()).decode()
        ripemd160 = RIPEMD160.new()
        hash160 = ripemd160.update(hashlib.sha256(binascii.unhexlify(chavePublica)).digest()).digest()
        enderecoPublico_a = b"\x00" + hash160
        checksum = hashlib.sha256(hashlib.sha256(enderecoPublico_a).digest()).digest()[:4]
        enderecoPublico_b = base58.b58encode(enderecoPublico_a + checksum)

        return enderecoPublico_b.decode()

    def retornaHash(self):
        dados = ':'.join((
            self.apelido,
            self.numero, 
            self.chavePublica,
            self.endereco
        ))

        Hash = SHA256.new()
        Hash.update(dados.decode())
        return Hash.digest()


    def paraJson(self):
        return json.dumps({
            'tipo':'regCandidato',
            'id': self.ID,
            'apelido':self.apelido,
            'numero': self.numero,
            'chavePrivada': self.chavePrivada.to_string,
            'chavePublica': self.chavePublica,
            'endereco':self.endereco,
            'hash': self.retornaHash()
        })