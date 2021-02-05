from modelos.registro import Registros
from modelos.transacao import Transacao
from modelos.saldos import Saldos
import json

class UTXO:
    registros = Registros()
    saldos = []

    def __init__(self):
        try:
            with open("/tmp/registros.json", 'r') as f:
                print(f)
                self.registros.importar(f)
        except IOError:
            print("Arquivo inexistente")

    def retornarIndicePorEndereco(self, endereco):
        for i in range(len(self.saldos)-1):
            if self.saldos[i].endereco == endereco:
                return i
        return None
    
    def importarEnderecos(self, registros):
        for e in self.registros.eleitores:
            utxo_eleitores = Saldos(
                endereco=e.endereco,
                tipo='eleitor',
                saldo=e.saldo,            
            )
        for c in self.registros.candidatos:
            utxo_candidatos = Saldos(
                endereco=c.endereco,
                tipo='candidato',
                saldo=c.saldo,            
            )

        self.saldos.extend(utxo_candidatos)
        self.saldos.extend(utxo_eleitores)

    def transferirSaldo(self, endereco_origem, endereco_destino):
        tr = Transacao(endereco_destino=endereco_destino, endereco_origem=endereco_origem)
        self.saldos[self.retornarIndicePorEndereco(endereco_origem)].reduzirSaldo(1)
        self.saldos[self.retornarIndicePorEndereco(endereco_destino)].adicionarSaldo(tr)

    def paraJson(self):
        return json.dumps(
            {
                'header': 'utxo',
                'saldos': [s.paraJson for s in self.saldos]
            }
        )

        

        

        

        