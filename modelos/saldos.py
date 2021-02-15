import json
from modelos.transacao import Transacao

class Saldos:
    endereco = ''
    _tipo = ''
    _numero = ''
    saldo = 0
    transacoes = []

    
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


    def __init__(self, processo, saldo_json = None, transacao_criacao = None):
        # o processo pode ser recuperação (processo = 'recuperar'), com a importação do saldo a partir de um saldo em formato
        # json (saldo json) ou criação de uma nova entrada de saldo (processo = 'criar') e o próximo parametro será uma 
        # transaçção de criação 

        if processo == "recuperar":
            if saldo_json:
                self.importar(saldo_json)
        if processo == "criar" and transacao_criacao:
            self.endereco = transacao_criacao.endereco
            self.tipo = tipo
            self.numero = numero
            self.adicionarSaldo(saldo)
            if transacoes:
                self.transacoes.extend(transacoes)

    def adicionarSaldo(self, transacao = None):

        print(transacao)
        
        if self.tipo == 'eleitor':
            if saldo: 
                if self.saldo == 0 and (self.saldo+saldo == 1):
                    self.saldo += saldo
            if transacao:
                if self.saldo == 0 and self.saldo+transacao.saldo == 1:
                    self.saldo += transacao.saldo
                
        else:
            if saldo:
                self.saldo += saldo
            if transacao:
                self.saldo += transacao.saldo
        
        if transacao:
            self.transacoes.append(transacao)

    def reduzirSaldo(self, decrescimo):
        self.saldo -= decrescimo

    def importar(self, dicionario):
        transacoes = []
        for t in dicionario['transacoes']:
            tr = Transacao(
                endereco_destino=t['endereco_destino'],
                endereco_origem=t['endereco_origem'],
                saldo_transferido=t['saldo_transferido'],
                assinatura=t['assinatura']
            )
            transacoes.append(tr)

        if dicionario["tipo"] == 'candidato': 
            self = Saldos(
                endereco=dicionario['endereco'],
                tipo=dicionario['tipo'],
                numero=dicionario['numero'],
                saldo=dicionario['saldo'],
                transacoes=transacoes
            )
        else:
            self = Saldos(
                endereco=dicionario['endereco'],
                tipo=dicionario['tipo'],
                saldo=dicionario['saldo'],
                transacoes=transacoes
            )
    
    def paraJson(self):

        if self.tipo == 'candidato':
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
            }, 
            indent=4
            )

        return dicionario