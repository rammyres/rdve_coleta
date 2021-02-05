import json
from modelos.transacao import Transacao

class Saldos:
    endereco = ''
    _tipo = ''
    saldo = 0
    transacoes = []
    
    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, tipo):
        if tipo == 'eleitor' or tipo == 'candidato' or tipo =='urna':
            self._tipo = tipo

    def __init__(self, endereco = None, tipo = None, saldo = None, transacoes = None, dicionario = None):
        if dicionario:
            self.importar(dicionario)
        else:
            self.endereco = endereco
            self.tipo = tipo
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
                endereco_origem=t['endereco_origem']
            )
            transacoes.append(tr)

        self = Saldos(
            endereco=dicionario['endereco'],
            tipo=dicionario['tipo'],
            saldo=dicionario['saldo'],
            transacoes=transacoes
        )
    
    def paraJson(self):
        return json.dumps(
            {
                'endereco': self.endereco,
                'tipo': self.tipo,
                'saldo': self.saldo,
                'transacoes': [e.paraJson() for e in self.transacoes]
            },
            indent=4
        )