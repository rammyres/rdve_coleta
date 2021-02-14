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


    def __init__(self, endereco = None, tipo = None, numero = None, saldo = None, transacoes = None, dicionario = None):
        if dicionario:
            self.importar(dicionario)
        else:
            self.endereco = endereco
            self.tipo = tipo
            self.numero = numero
            self.adicionarSaldo(saldo)
            self.transacoes.extend(transacoes)

    def adicionarSaldo(self, transacao):
        if self.tipo == 'eleitor':
            if self.saldo == 0 and (self.saldo+transacao.saldo == 1):
                self.saldo += transacao.saldo
        else:
            self.saldo += transacao.saldo

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