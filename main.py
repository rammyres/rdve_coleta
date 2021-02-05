#!/usr/bin/env python3

import kivy
from kivymd.app import MDApp
import kivy.properties as kyprops
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from modelos.eleitor import Eleitor
from modelos.candidato import Candidato
from modelos.registro import Registros
from modelos.utilitarios import Utilitarios

class TelaColeta(Screen):
    pass

class TelaAlistamento(Screen):
    registro = Registros()
    eleitores = []
    nEleitor = kyprops.ObjectProperty()

    def iniciar(self):
        try:
            f = open("/tmp/registros.json")
            f.close()
            self.registro.importar("/tmp/registros.json")

        # Do something with the file
        except IOError:
            print("File not accessible")
        finally:
            f.close()
    
    def novoEleitor(self):        
        eleitor = Eleitor(self.nEleitor.text)
        self.eleitores.append(eleitor)
        self.registro.inserir(eleitor)
        self.registro.exportar('/tmp/registros.json')
        for e in self.eleitores:
            print(e.paraJson())
        


class TelaCandidatura(Screen):
    Candidatos = []
    nCandidato = kyprops.ObjectProperty()
    numCandidato = kyprops.ObjectProperty()
    
    def novoCandidato(self):
        
        candidato = Candidato(self.nCandidato.text, self.numCandidato.text)
        self.Candidatos.append(candidato)
        for c in self.Candidatos:
            print(c.paraJson())

class TelaUrna(Screen):
    pass


class RDVEColetaApp(MDApp):

    eleitores = []
    candidatos = []
    
    
    def novoCandidato(self, apelido, numero):
        candidato = Candidato(apelido, numero)
        self.candidadtos.append(candidato)
           
    def build(self):
        
        self.gerenciadorTela = ScreenManager()
        self.gerenciadorTela.add_widget(TelaColeta(name='TelaInicial'))
        self.gerenciadorTela.add_widget(TelaAlistamento(name='TelaAlistamento'))
        self.gerenciadorTela.add_widget(TelaCandidatura(name = 'TelaCandidatura'))

        
        self.gerenciadorTela.current='TelaInicial'
        
        return self.gerenciadorTela
        

if __name__ == "__main__":
    RDVEColetaApp().run()