import json, uuid
from hashlib import sha256

class Transacao:
    ID = '' # gerado automaticamente
    tipo = '' # tipo de transação, pode ser criar_endereco ou transferir_saldo
    tipo_endereco = '' # tipo do endereço criado, no caso de transação criar_endereco
                       # podem ser eleitor, candidato ou urna
    endereco = '' # endereco criado 
    endereco_origem = '' # para transações transferir_saldo é o endereço que fornecerá
                         # saldo para o endereco_destino
    endereco_destino = '' 
    saldo_transferido = 0 # por padrão o saldo a ser transferido é 0
    assinatura = '' # assinatura referente a transação de criaçao de endereço é gerada pelo usuário
    Hash = ''

    def __init__(self, tipo = None, 
                       endereco = None, 
                       tipo_endereco = None,
                       numero = None,
                       endereco_origem = None, 
                       endereco_destino = None, 
                       saldo_transferido = None, 
                       assinatura = None):

        self.ID = str(uuid.uuid4())
        if tipo == 'criar_endereco':
            self.tipo = tipo
            self.endereco = endereco
            self.tipo_endereco = tipo_endereco
            if self.tipo_endereco == 'candidato':
                self.numero = numero
        if tipo == 'transferir_saldo':
            self.endereco_destino = endereco_destino
            self.endereco_origem = endereco_origem
            self.saldo_transferido = saldo_transferido

        self.assinatura = assinatura


    def dados(self): 
        # Os dados utilizados para gerar os hashes serão automaticamente selecionados, 
        # dependendo do tipo de transação
        dados = ''
        if self.tipo == 'criar_endereco':
            if self.tipo_endereco == 'eleitor':
                dados = ':'.join(
                    (
                    self.ID, 
                    self.endereco, 
                    self.tipo_endereco,
                    self.assinatura
                    )
                )
            if self.tipo_endereco == 'candidato':
                dados = ':'.join(
                    (
                    self.ID, 
                    self.endereco, 
                    self.numero,
                    self.tipo_endereco,
                    self.assinatura
                    )
                )

        if self.tipo == 'transferir_saldo':
            dados = ':'.join(
            (
                self.ID,
                self.endereco_origem,
                self.endereco_destino,
                self.saldo_transferido,
                self.assinatura
            )
        )

        print(dados)

        return dados
        
    def gerarHash(self):
        h = sha256()
        h.update(self.dados().encode())
        return h.hexdigest()
    
    def paraJson(self):
        dicionario = {}
        if self.tipo == 'transferir_saldo':
            dicionario = json.dumps(
                {
                    'id': self.ID,
                    'tipo': self.tipo,
                    'endereco_origem': self.endereco_destino,
                    'endereco_destino': self.endereco_destino,
                    'saldo_transferido': self.saldo_transferido,
                    'assinatura': self.assinatura,
                    'hash': self.Hash
                }, indent=4
            )
        if self.tipo == 'criar_endereco':
            if self.tipo_endereco == 'eleitor':
                dicionario = json.dumps(
                    {
                    'id' : self.ID,
                    'tipo': self.tipo,
                    'tipo_endereco': self.tipo_endereco,
                    'endereco': self.endereco,
                    'assinatura': self.assinatura,
                    'hash': self.Hash
                    }
                )
            if self.tipo_endereco == 'candidato':
                dicionario = json.dumps(
                    {
                    'id' : self.ID,
                    'tipo': self.tipo,
                    'tipo_endereco': self.tipo_endereco,
                    'numero': self.numero,
                    'endereco': self.endereco,
                    'assinatura': self.assinatura,
                    'hash': self.Hash
                    }
                )
        return dicionario