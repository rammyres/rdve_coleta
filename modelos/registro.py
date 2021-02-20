from pymerkle import MerkleTree
from modelos.candidato import Candidato
from modelos.eleitor import Eleitor
from modelos.utilitarios import Utilitarios
from tqdm import tqdm
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

#=======================================================================================================#
# Verifica se o elemento com ID e endereco especificados já existe nos registros, a fim de evitar 
# duplicidade nos registros 
#=======================================================================================================#
    def existeRegistro(self, ID, endereco):
        for e in self.eleitores:
            if e.ID == ID and e.endereco == endereco:
                return True
        for c in self.candidatos:
            if c.ID == ID and c.endereco == endereco:
                return True

        return False

#=======================================================================================================#
# Insere um elemento nas listas de eleitores ou candidatos                                              #
#=======================================================================================================#
    def inserir(self, elemento):

        if not self.existeRegistro(elemento.ID, elemento.endereco):
            if isinstance(elemento, Eleitor) or isinstance(elemento, Candidato):
                if isinstance(elemento, Eleitor):
                    self.eleitores.append(elemento)
                if isinstance(elemento, Candidato):
                    self.candidatos.append(elemento)

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
    def retornaEnderecoPeloNumero(self, numero):
        for c in self.candidatos:
            if c.numero == numero:
                return c.endereco
        return None
#========================================================================================================
    def retornaEnderecoPeloID(self, ID):
        for e in self.eleitores:
            if e.ID == ID:
                return e.endereco
        return None

#========================================================================================================
    def importar(self, arquivo):
        util = Utilitarios()
        
        if os.path.exists(arquivo):
            try:
                with open(arquivo, 'r+') as f:
                
                    tmp = json.load(f)
                
                    with open('/tmp/arv_tmp.json', 'w') as arv:
                        json.dump(tmp['arvore'], arv)
                        arv.close()
                    self.arvore = MerkleTree.loadFromFile('/tmp/arv_tmp.json')

                    for e in tqdm(tmp['eleitores']):
                        
                        try:
                            eleitor = Eleitor(
                                nome = e['nome'],
                                ID=e['id'],
                                chavePrivada=e['chavePrivada'],
                                chavePublica=e['chavePublica'],
                                endereco=e['endereco']
                            )
                            self.inserir(eleitor)
                            
                        except TypeError:
                            print("Eleitor inválido, pulando")
                    
                    for c in tqdm(tmp['candidatos']):
                        try: 
                            candidato = Candidato(
                                            ID=c['id'],
                                            apelido=c['apelido'],
                                            numero=c['numero'],
                                            chavePrivada=c['chavePrivada'],
                                            chavePublica=c['chavePublica'],
                                            endereco=c['endereco'])
                                
                            self.inserir(candidato)
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