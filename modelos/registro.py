from pymerkle import MerkleTree
from modelos.candidato import Candidato
from modelos.eleitor import Eleitor
from modelos.utilitarios import Utilitarios
import json, io, binascii, os

class Registros:
    arvore = MerkleTree()
    eleitores = []
    candidatos = []

    def __init__(self, elementos = None, arvore = None):
        if elementos:
            for e in elementos:
                self.inserir(e)
        if arvore:
            with open('tmp', 'w') as f:
                json.dump(arvore, f)
                self.arvore = MerkleTree.loadFromFile(f)
                f.close()

#========================================================================================================
    def inserir(self, elemento):
        print(elemento.serializar())
        if isinstance(elemento, Eleitor) or isinstance(elemento, Candidato):
            if isinstance(elemento, Eleitor):
                self.eleitores.append(elemento)
            if isinstance(elemento, Candidato):
                self.candidatos.append(elemento)

            print(elemento.Hash)
            self.arvore.update(digest=elemento.Hash)
    
#========================================================================================================
    def exportar(self, arquivo):
        with open(arquivo, 'w') as f:
            json.dump(
                {
                    'header': 'registros',
                    'raiz': binascii.hexlify(self.arvore.rootHash).decode(),
                    'arvore': self.arvore.serialize(),
                    'eleitores': [e.serializar() for e in self.eleitores],
                    'candidatos': [c.serializar() for c in self.candidatos],
                }, 
                f, indent=4
            )
            f.close()

#========================================================================================================
    def importar(self, arquivo):
        util = Utilitarios()
        
        if os.path.exists(arquivo):
            try:
                with open(arquivo, 'r+') as f:
                
                    tmp = json.load(f)
                
                    arv = open('/tmp/arv_tmp.json', 'w')
                    json.dump(tmp['arvore'], arv)
                    arv.close()
                    self.arvore = MerkleTree.loadFromFile('/tmp/arv_tmp.json')
                    
                    for e in tmp['eleitores']:
                        try:
                            print("Importando {}".format(e))
                            self.inserir(Eleitor(processo = 'importar', dicionario=e))
                        except TypeError:
                            print("Eleitor inválido, pulando")
                    
                    for c in tmp['candidatos']:
                        try: 
                            print("Importando {}".format(c))
                            self.inserir(Candidato(processo='importar', dicionario=c))
                        except TypeError:
                            print("Candidato inválido, pulando")
                    
                    util.remover_seguramente('arv_tmp.json', 5)
                f.close()

            except IOError:
                print("Arquivo indisponível")
            except ValueError:
                print('Arquivo de registros inválido, criando novos registros')
            else:
                print("Arquivo não localizado")
        
        