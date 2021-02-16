import json
from modelos.transacao import Transacao

class Saldos:
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
    def __init__(self, processo, saldo_json = None, transacao = None):
        # o processo pode ser recuperação (processo = 'recuperar'), com a importação do saldo a partir de um saldo em formato
        # json (saldo json) ou criação de uma nova entrada de saldo (processo = 'criar') e o próximo parametro será uma 
        # transaçção de criação. Além disso poderá ser criada uma transação de movimentação (processo = transferir)

        if processo == "recuperar":
            if saldo_json:
                self.importar(saldo_json)
        if processo == "criar" and transacao:
            self.endereco = transacao.endereco
            self.tipo = transacao.tipo_endereco
            if transacao.tipo == "candidato":
                self.numero = transacao.numero
        
#========================================================================================================
    def tranferir(self, transacao):
        if not self.procurarTransacaoPorID(transacao.ID):
            if self.endereco == transacao.endereco_destino:
                self.adicionarSaldo(transacao.saldo_trasnferido)
                self.transacoes.append(transacao)
            if self.endereco == transacao.endereco_origem:
                self.reduzirSaldo(transacao.saldo_transferido)
                self.transacoes.append(transacao)
#========================================================================================================
    
    def adicionarSaldo(self, acrescimo):
        self.saldo+= acrescimo
#========================================================================================================

    def reduzirSaldo(self, decrescimo):
        self.saldo -= decrescimo

#========================================================================================================
    def importar(self, dicionario):
        print(dicionario)
        self = Saldos(processo='criar')
        self.endereco = dicionario['endereco']
        self.tipo = dicionario['tipo']
        self.saldo = dicionario['saldo']

        if dicionario['tipo'] == 'candidato':
            self.numero = dicionario['numero']

        for t in dicionario['transacoes']:
            tr = Transacao()
            tr.importar(t)
            self.transacoes.append(tr)

        print(self.paraJson())

#========================================================================================================
    def procurarTransacaoPorID(self, id):
        for t in self.transacoes:
            if id == t.ID:
                return self.transacoes.index(t)
        return None
    
#========================================================================================================
    def paraJson(self):

        if self.tipo == 'candidato':
            for e in self.transacoes:
                print(e.paraJson())
            dicionario = json.dumps(
            {
                'endereco': self.endereco,
                'tipo': self.tipo,
                'numero': self.numero,
                'saldo': self.saldo,
                'transacoes': [e.paraJson() for e in self.transacoes]
            }, 
            indent=4
            )
        else:
            dicionario = json.dumps(
                {
                    'endereco': self.endereco,
                    'tipo': self.tipo,
                    'saldo': self.saldo,
                    'transacoes': [e.paraJson() for e in self.transacoes]
                }
            )

        return dicionario