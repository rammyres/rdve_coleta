from modelos.registro import Registros
from modelos.transacao import Transacao
from modelos.saldos import Saldos
import json

class UTXO:
    registros = Registros()
    saldos = []

    def __init__(self, arquivo = None, arquivoRegistros = None):
        if arquivo:
            if self.importar(arquivo):
                print("UTXO recuperado")
            else:
                if self.importarDosRegistros(arquivoRegistros):
                    print("Endereços importados a partir dos registros")
            
    def retornarIndicePorEndereco(self, endereco):
        for i in range(len(self.saldos)-1):
            if self.saldos[i].endereco == endereco:
                return i
        return None

    def retornarEnderecoPeloNumero(self, numero):
        for s in self.saldos:
            if s.tipo == 'candidato':
                if s.numero == numero:
                    return s.endereco
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


    def novoEndereco(self, transacao):
        if transacao.tipo == 'criar_endereco':
            if transacao.tipo == 'eleitor':
                self.saldos.append(Saldos(endereco=transacao.endereco,tipo=transacao.tipo_endereco, saldo=1, transacoes = None))
            if transacao.tipo == 'candidato': 
                self.saldos.append(Saldos(endereco=transacao.endereco,tipo=transacao.tipo_endereco, saldo=0, transacoes = None))

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
                'saldos': [s.paraJson() for s in self.saldos]
            }
        )

    def exportar(self, arquivo): 
        with open(arquivo, 'w+') as f:
            json.dump(
                self.paraJson(), f, indent=4
            )

    def importar(self, arquivo):
        try:
            with open(arquivo, 'r') as f:
                self.importarEnderecos(json.load(f))
                return True
        except:
            print("Arquivo não localizado")
            
        return False

    def importarDosRegistros(self, arquivo):
        
        try:
            with open(arquivo, 'r') as f:
                print(f)
                self.registros.importar(f)
                return True               
        except IOError:
            print("Arquivo inexistente")
        except TypeError:
            print("Arquivo inexistente")
            
        return False
            
        

        

        

        