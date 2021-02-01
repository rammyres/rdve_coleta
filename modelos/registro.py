import pymerkletree
import candidato, eleitor

class Registros(List):

    def inserir(self, elemento):
        if isinstance(elemento, eleitor) or isinstance(elemento, candidato):
            self.append(elemento)
