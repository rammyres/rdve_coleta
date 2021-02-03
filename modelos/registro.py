from pymerkle import MerkleTree
from utilitarios import Utilitarios
import candidato, eleitor, utilitarios, json

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

    def inserir(self, elemento):
        if isinstance(elemento, eleitor) or isinstance(elemento, candidato):
            if isinstance(elemento, eleitor):
                self.eleitores.append(elemento)
            if isinstance(elemento, candidato):
                self.candidatos.append(elemento)
            self.arvore.update(elemento.retornaHash())
    
    def exportar(self, arquivo):
        with open(arquivo, 'w') as f:
            json.dump(
                {
                    'header': 'registros',
                    'raiz': self.arvore.rootHash,
                    'arvore': self.arvore.toJSONString(),
                    'eleitores': [e.paraJson() for e in self.eleitores],
                    'candidatos': [c.paraJson() for c in self.candidatos],
                }, 
                f
            )
            f.close()

    def importar(self, arquivo):
        util = Utilitarios()
        with open(arquivo, 'r') as f:
            tmp = json.load(f)
            arv = open('arv_tmp.json', 'w')
            json.dump(tmp['arvore'], arv)
            arv.close()
            self.arvore = MerkleTree.loadFromFile('arv_tmp.json')
            self.eleitores.extend(tmp['eleitores'])
            self.candidatos.extend(tmp['candidatos'])
        f.close()
        util.remover_seguramente('arv_tmp.json', 5)