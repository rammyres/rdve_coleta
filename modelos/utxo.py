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

    def novoEndereco(self, endereco, tipo, saldo):
        self.saldos.append(Saldos(endereco=endereco,tipo=tipo, saldo=0, transacoes = None))

    def transferirSaldo(self, endereco_origem, endereco_destino, assinatura, saldo_transferido):
        tr = Transacao(endereco_destino=endereco_destino, 
                       endereco_origem=endereco_origem,
                       saldo_transferido = saldo_transferido,
                       assinatura= assinatura)
        self.saldos[self.retornarIndicePorEndereco(endereco_origem)].reduzirSaldo(saldo_transferido)
        self.saldos[self.retornarIndicePorEndereco(endereco_destino)].adicionarSaldo(saldo_transferido)
        self.saldos[self.retornarIndicePorEndereco(endereco_destino)].transacoes.append(tr)

    def paraJson(self):
        return json.dumps(
            {
                'header': 'utxo',
                'saldos': [s.paraJson for s in self.saldos]
            }
        )

        

        

        

        