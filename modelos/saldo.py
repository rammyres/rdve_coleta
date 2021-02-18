import json
from modelos.transacao import Transacao

class Saldo:
    endereco = ''
    _tipo = ''
    _numero = ''
    saldo = 0
    transacoes = []

#========================================================================================================    
    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, tipo):
        if tipo == 'eleitor' or tipo == 'candidato' or tipo =='urna':
            self._tipo = tipo
        
    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, numero):
        if self.tipo == 'candidato':
            self._numero = numero

#========================================================================================================
    def __init__(self, saldo_json = None, transacao = None):
        # o processo pode ser recuperação (processo = 'recuperar'), com a importação do saldo a partir de um saldo em formato
        # json (saldo json) ou criação de uma nova entrada de saldo (processo = 'criar') e o próximo parametro será uma 
        # transaçção de criação. Além disso poderá ser criada uma transação de movimentação (processo = transferir)

        if saldo_json and transacao:
            raise ValueError("Somente um dos argumentos deve ser preenchido")

        if saldo_json:
            # A criação da partir de dicionário em formato json é pensada para permitir a importação a partir da persistência
            # em arquivos texto. O construtor 'polimorfico' da classe Trasacao permite criar 3 tipos de transações

            self.endereco = saldo_json['endereco']
            self.tipo = saldo_json['tipo']
            if saldo_json['tipo'] == 'candidato':
                self.numero = saldo_json['numero']
            
            for t in saldo_json['transacoes']:
                if t['tipo'] == 'transferir_saldo':
                    tr = Transacao(
                        ID=t['id'],
                        tipo=t['tipo'],
                        endereco_origem=t['endereco_origem'],
                        endereco_destino=t['endereco_destino'],
                        saldo_transferido=t['saldo_transferido'],
                        assinatura=t['assinatura'],
                        Hash=t['hash']
                    )
                if t['tipo'] == 'criar_endereco':
                    if t['tipo_endereco'] == 'eleitor':
                        tr = Transacao(
                            ID = t['id'],
                            tipo = t['tipo'],
                            tipo_endereco=t['tipo_endereco'],
                            assinatura=t['assinatura'],
                            Hash=t['hash']
                        )
                    if t['tipo_endereco'] == t['candidato']:
                        tr = Transacao(
                            ID=t['id'],
                            tipo = t['tipo'],
                            tipo_endereco=t['tipo_endereco'],
                            numero=t['numero'],
                            endereco = t['endereco'],
                            assinatura=t['assinatura'],
                            Hash=t['assinatura']
                        )
                self.inserirTransacao(tr)
            
        if transacao:
            self.endereco = transacao.endereco
            self.tipo = transacao.tipo_endereco
            if transacao.tipo == "candidato":
                self.numero = transacao.numero
            self.inserirTransacao(transacao)
            self.adicionarSaldo(1)
        
#========================================================================================================
    def tranferir(self, transacao):
        if not self.procurarTransacaoPorID(transacao.ID):
            if self.endereco == transacao.endereco_destino:
                self.adicionarSaldo(transacao.saldo_trasnferido)
                self.inserirTransacao(transacao)
            if self.endereco == transacao.endereco_origem:
                self.reduzirSaldo(transacao.saldo_transferido)
                self.inserirTransacao(transacao)
#========================================================================================================
    
    def adicionarSaldo(self, acrescimo):
        self.saldo+= acrescimo
#========================================================================================================

    def reduzirSaldo(self, decrescimo):
        self.saldo -= decrescimo
#========================================================================================================
    def inserirTransacao(self, transacao):
        if transacao.tipo == 'criar_endereco': 
            if transacao.endereco == self.endereco: 
                print(self.procurarTransacaoPorID(transacao.ID))
                if not self.procurarTransacaoPorID(transacao.ID):
                    self.transacoes.append(transacao)
        elif transacao.endereco_origem == self.endereco or transacao.endereco_destino:
            if not self.procurarTransacaoPorID(transacao.ID):
                self.transacoes.append(transacao)    

#========================================================================================================
    def procurarTransacaoPorID(self, id):
        for t in self.transacoes:
            if id == t.ID:
                return self.transacoes.index(t)
        return None
    
#========================================================================================================
    def serializar(self):

        if self.tipo == 'candidato':
            for e in self.transacoes:
                print([e.serializar() for e in self.transacoes])
            dicionario = {
                'endereco': self.endereco,
                'tipo': self.tipo,
                'numero': self.numero,
                'saldo': self.saldo,
                'transacoes': [e.serializar() for e in self.transacoes]
            }
        else:
            dicionario = {
                    'endereco': self.endereco,
                    'tipo': self.tipo,
                    'saldo': self.saldo,
                    'transacoes': [e.serializar() for e in self.transacoes]
                }

        return dicionario