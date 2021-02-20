from modelos.registro import Registros
from modelos.transacao import Transacao
from modelos.saldo import Saldo
import json, uuid

class UTXO:
    ID = ''
    saldos = []

    def __init__(self, arquivoUTXO = None):

        if arquivoUTXO:
            try:
                with open(arquivoUTXO, 'r') as f:
                    tmp = json.load(f)
                    f.close()

                self.ID = tmp['id']
                print([Saldo(saldo_json=e) for e in tmp['saldos']])
                self.saldos = [Saldo(saldo_json=e) for e in tmp['saldos']]
            except IOError:
                print("Arquivo UTXO não localizado, pulando")
            # except KeyError:
            #     print("Arquivo UTXO inválido, pulando importação")

        if not arquivoUTXO:
            self.ID = str(uuid.uuid4())

#========================================================================================================
    def retornarIndicePorEndereco(self, endereco):
        a = None
        for i in range(0, len(self.saldos)):
        
            if (self.saldos[i].endereco == endereco):
                a = i
        print(a)
        return a

#========================================================================================================
    def retornarEnderecoPeloNumero(self, numero):
        for s in self.saldos:
            if s.tipo == 'candidato':
                if s.numero == numero:
                    return s.endereco
        return None

#========================================================================================================
    def importarEnderecos(self, saldos):        
        tmp = [Saldo(saldo_json=e) for e in saldos['saldos']]
        
        self.saldos.extend(tmp)

#========================================================================================================
    def novoEndereco(self, transacao):
        if transacao.tipo == 'criar_endereco':
            if not self.retornarIndicePorEndereco(transacao.endereco):
                self.saldos.append(Saldo(transacao=transacao))
            
#========================================================================================================
    def transferirSaldo(self, endereco_origem, endereco_destino, assinatura, saldo_transferido):
        tr = Transacao(tipo='transferir_saldo',
                       endereco_destino=endereco_destino, 
                       endereco_origem=endereco_origem,
                       saldo_transferido = saldo_transferido,
                       assinatura=assinatura)
        print(endereco_origem)
        print(tr)
        for s in self.saldos:
            print(s.endereco)
        self.saldos[self.retornarIndicePorEndereco(endereco_origem)].tranferir(tr)
        self.saldos[self.retornarIndicePorEndereco(endereco_destino)].tranferir(tr)
        
#========================================================================================================
    def serializar(self):
        print([s.serializar() for s in self.saldos])

        return {
                'header': 'utxo',
                'id': self.ID,
                'saldos': [s.serializar() for s in self.saldos]
            }
        
#========================================================================================================
    def exportar(self, arquivo): 
        with open(arquivo, 'w+') as f:
            json.dump(
                self.serializar(), f, indent=4
            )