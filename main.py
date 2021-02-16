#!/usr/bin/env python3

import kivy
from kivymd.app import MDApp
import kivy.properties as kyprops
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from modelos.eleitor import Eleitor
from modelos.candidato import Candidato
from modelos.registro import Registros
from modelos.utilitarios import Utilitarios
from modelos.utxo import UTXO

#========================================================================================================
#========================================================================================================
class TelaColeta(Screen):
    pass

#========================================================================================================
#========================================================================================================
class TelaAlistamento(Screen):
    registro = Registros()
    utxo = UTXO(arquivo='/tmp/utxo.json')
    eleitores = []
    nEleitor = kyprops.ObjectProperty()

    def iniciar(self):
        try:
            with open("/tmp/registros.json", 'r') as f:
                print(f)
                self.registro.importar(f)
                
        except IOError:
            print("Arqivo não localizado")
        
    def novoEleitor(self):        
        eleitor = Eleitor(self.nEleitor.text)
        self.eleitores.append(eleitor)
        self.registro.inserir(eleitor)
        self.utxo.novoEndereco(eleitor.transacaoCriacao())
        self.registro.exportar('/tmp/registros.json')
        self.utxo.exportar(arquivo='/tmp/utxo.json')
        for e in self.eleitores:
            print(e.paraJson())

#========================================================================================================
#========================================================================================================

class TelaCandidatura(Screen):
    candidatos = []
    utxo = UTXO(arquivo='/tmp/utxo.json')
    registro = Registros()
    nCandidato = kyprops.ObjectProperty()
    numCandidato = kyprops.ObjectProperty()

#========================================================================================================
    def iniciar(self):
        try:
            with open("/tmp/registros.json", 'r') as f:
                print(f)
                self.registro.importar(f)
                
        except IOError:
            print("Arquivo não localizado")

#========================================================================================================
    def novoCandidato(self):        
        candidato = Candidato(self.nCandidato.text, self.numCandidato.text)
        self.candidatos.append(candidato)
        self.registro.inserir(candidato)
        self.utxo.novoEndereco(candidato.transacaoCriacao())
        print(self.utxo.paraJson())
        self.registro.exportar('/tmp/registros.json')
        self.utxo.exportar(arquivo='/tmp/utxo.json')
        for c in self.candidatos:
            print(c.paraJson())

#========================================================================================================        
#========================================================================================================
class Content(BoxLayout):
    pass
#========================================================================================================        
#========================================================================================================
class TelaUrna(Screen):
    # eleitor = Eleitor()
    eleitores = []
    candidatos = []
    numCandidato = kyprops.ObjectProperty()
    
    def ao_tocar(self, texto): 
        self.numCandidato.text += texto

#========================================================================================================
    def corrige(self):
        self.numCandidato.text = ''

#========================================================================================================
    def ao_editar(self):
        print(self.numCandidato.text)

#========================================================================================================
#========================================================================================================
class RDVEColetaApp(MDApp):
    
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