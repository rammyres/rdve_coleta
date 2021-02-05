from ecdsa import SigningKey, VerifyingKey, SECP256k1
from Crypto.Hash import RIPEMD160, SHA256
import binascii, hashlib, base58, json, uuid

class Candidato:
    ID = ''
    apelido = ''
    numero = ''
    endereco = ''
    chavePrivada = None
    chavePublica = None
    
    def __init__(self, apelido=None, numero=None, ID = None, chavePrivada=None, endereco=None, dicionario = None):

        if dicionario:
            self.importar(dicionario)

        else:
            self.apelido = apelido
            self.numero = numero

            if chavePrivada and endereco and ID:
                self.ID = ID
                self.chavePrivada = SigningKey.from_string(chavePrivada)
                self.chavePublica = self.chavePrivada.get_verifying_key()
                self.endereco = endereco

            else: 
                self.ID = uuid.uuid4()
                self.chavePrivada = SigningKey.generate(curve=SECP256k1)
                self.chavePublica = self.chavePrivada.get_verifying_key()
                self.endereco = self.gerarEndereco()

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

    def retornaHash(self):
        dados = ':'.join((
            str(self.ID),
            self.apelido,
            self.numero, 
            binascii.hexlify(self.chavePublica.to_string()).decode(),
            self.endereco
        ))

        Hash = SHA256.new()
        Hash.update(dados.encode())
        return Hash.hexdigest()


    def importar(self, dicionario):
        self = Candidato(
            apelido=dicionario['apelido'],
            numero=dicionario['numero'],
            ID=dicionario['id'],
            chavePrivada=dicionario['chavePrivada'],
            endereco=dicionario['endereco']
        )
        return self

    def paraJson(self):
        return json.dumps({
            'tipo':'regCandidato',
            'id': str(self.ID),
            'apelido':self.apelido,
            'numero': self.numero,
            'chavePrivada': binascii.hexlify(self.chavePrivada.to_string()).decode(),
            'chavePublica': binascii.hexlify(self.chavePublica.to_string()).decode(),
            'endereco':self.endereco,
            'hash': self.retornaHash()
        },
        indent=4)