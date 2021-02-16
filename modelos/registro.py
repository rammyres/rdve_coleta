from pymerkle import MerkleTree
from modelos.candidato import Candidato
from modelos.eleitor import Eleitor
from modelos.utilitarios import Utilitarios
import json, io, binascii

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
        if isinstance(elemento, Eleitor) or isinstance(elemento, Candidato):
            if isinstance(elemento, Eleitor):
                self.eleitores.append(elemento)
            if isinstance(elemento, Candidato):
                self.candidatos.append(elemento)
            self.arvore.update(elemento.retornaHash())
    
#========================================================================================================
    def exportar(self, arquivo):
        with open(arquivo, 'w') as f:
            json.dump(
                {
                    'header': 'registros',
                    'raiz': binascii.hexlify(self.arvore.rootHash).decode(),
                    'arvore': self.arvore.serialize(),
                    'eleitores': [e.paraJson() for e in self.eleitores],
                    'candidatos': [c.paraJson() for c in self.candidatos],
                }, 
                f
            )
            f.close()

#========================================================================================================
    def importar(self, arquivo):
        util = Utilitarios()

        if not isinstance(arquivo, io.TextIOWrapper):
            try:
                f = open(arquivo, 'r')
            except IOError:
                print("Arquivo indisponível")
        else:
            f = arquivo
            
        tmp = json.load(f)
        arv = open('/tmp/arv_tmp.json', 'w')
        json.dump(tmp['arvore'], arv)
        arv.close()
        self.arvore = MerkleTree.loadFromFile('/tmp/arv_tmp.json')
        
        eleitores = []
        for e in tmp['eleitores']:
            eleitores.append(Eleitor(e))
        self.eleitores.extend(eleitores)

        candidatos = []
        for e in tmp['candidatos']:
            candidatos.append(Eleitor(e))
        self.candidatos.extend(candidatos)
        
        
        f.close()
        util.remover_seguramente('arv_tmp.json', 5)