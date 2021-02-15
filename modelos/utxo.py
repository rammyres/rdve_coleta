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
            utxo_eleitores = Saldos(processo = 'criar', transacao=e.transacaoCriacao())
        for c in self.registros.candidatos:
            utxo_candidatos = Saldos(processo='criar', transacao =c.transacaoCriacao())

        self.saldos.extend(utxo_candidatos)
        self.saldos.extend(utxo_eleitores)


    def novoEndereco(self, transacao):
        if transacao.tipo == 'criar_endereco':
            self.saldos.append(Saldos(processo='criar', transacao =transacao))
            

    def transferirSaldo(self, endereco_origem, endereco_destino, assinatura, saldo_transferido):
        tr = Transacao(tipo='transferir_saldo',
                       endereco_destino=endereco_destino, 
                       endereco_origem=endereco_origem,
                       saldo_transferido = saldo_transferido,
                       assinatura=assinatura)
        self.saldos[self.retornarIndicePorEndereco(endereco_origem)].tranferir(tr)
        self.saldos[self.retornarIndicePorEndereco(endereco_destino)].tranferir(tr)
        

    def paraJson(self):
        print([s for s in self.saldos])
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
            
        

        

        

        