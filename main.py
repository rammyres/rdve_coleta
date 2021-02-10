#!/usr/bin/env python3

import kivy
from kivymd.app import MDApp
import kivy.properties as kyprops
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.uix.vkeyboard import VKeyboard 
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
            with open("/tmp/registros.json", 'r') as f:
                print(f)
                self.registro.importar(f)
                

        # Do something with the file
        except IOError:
            print("Arqivo não localizado")
        
    def novoEleitor(self):        
        eleitor = Eleitor(self.nEleitor.text)
        self.eleitores.append(eleitor)
        self.registro.inserir(eleitor)
        self.registro.exportar('/tmp/registros.json')
        for e in self.eleitores:
            print(e.paraJson())


class TelaCandidatura(Screen):
    candidatos = []
    registro = Registros()
    nCandidato = kyprops.ObjectProperty()
    numCandidato = kyprops.ObjectProperty()

    def iniciar(self):
        try:
            with open("/tmp/registros.json", 'r') as f:
                print(f)
                self.registro.importar(f)
                
        except IOError:
            print("Arquivo não localizado")
        
    def novoCandidato(self):        
        candidato = Candidato(self.nCandidato.text, self.numCandidato.text)
        self.candidatos.append(candidato)
        self.registro.inserir(candidato)
        self.registro.exportar('/tmp/registros.json')
        for c in self.candidatos:
            print(c.paraJson())
    
    

class TelaUrna(Screen):
    pass

class Teclado(VKeyboard):
    pass


class RDVEColetaApp(MDApp):
    Config.set('kivy', 'keyboard_mode', 'systemandmulti')
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
        self.gerenciadorTela.add_widget(TelaUrna(name="TelaUrna"))

        
        self.gerenciadorTela.current='TelaInicial'
        
        return self.gerenciadorTela
        

if __name__ == "__main__":
    RDVEColetaApp().run()