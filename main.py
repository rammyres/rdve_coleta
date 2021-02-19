#!/usr/bin/env python3

import kivy
from kivymd.app import MDApp
import kivy.properties as kyprops
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem
from kivy.utils import get_color_from_hex
from kivymd.color_definitions import colors
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
class TelaSeletor(Screen):
    registros = Registros()
    registros.importar('/tmp/registros.json')
    utxo = UTXO()
    eleitor = None

    sv = ScrollView()
    ml = MDList()

#========================================================================================================
    def iniciar(self):

        if len(self.registros.eleitores)>0:
            
            self.sv.remove_widget(self.ml)
            self.remove_widget(self.sv)
            self.ml.clear_widgets()
            
            for e in self.registros.eleitores:
                self.ml.add_widget(
                    TwoLineListItem(
                        text=e.nome,
                        secondary_text = e.ID,
                        on_release = self.ao_clicar
                    ),
                                        
                )
        if len(self.registros.eleitores)==0:
            self.ml.add_widget(
                    OneLineListItem(
                        text="Nenhum eleitor"
                    )
                )
        self.sv.add_widget(self.ml)
        self.add_widget(self.sv)
        

        botaoVoltar = MDFillRoundFlatButton(
            text='Voltar',
            md_bg_color = get_color_from_hex(colors['LightBlue']['500']),
            on_press = self.telaInicial,
            pos_hint = {'x': 0.1, 'y': 0.1}
        )
        self.add_widget(botaoVoltar)

#========================================================================================================
    def telaInicial(self, b):
        self.manager.current = 'TelaInicial'
#========================================================================================================
    def buscarEleitorPorID(self, ID):
        for eleitor in self.registros.eleitores:
            if eleitor.ID == ID:
                return eleitor
        return None


#========================================================================================================
    def ao_clicar(self, item):
        self.eleitor = self.buscarEleitorPorID(item.secondary_text)
        self.requererVoto()
        self.manager.current = 'TelaUrna'

#========================================================================================================
    def requererVoto(self):
        if self.eleitor:
            self.eleitor.requererVoto()

#========================================================================================================
class TelaAlistamento(Screen):
    registros = Registros()
    utxo = None
    nEleitor = kyprops.ObjectProperty()

    def iniciar(self):
        self.registros.importar('/tmp/registros.json')

#========================================================================================================        
    def novoEleitor(self):
        self.utxo = UTXO(arquivoUTXO='/tmp/utxo.json')        
        eleitor = Eleitor(nome=self.nEleitor.text)
        self.registros.inserir(eleitor)
        self.utxo.novoEndereco(eleitor.transacaoCriacao())
        self.registros.exportar('/tmp/registros.json')
        self.utxo.exportar(arquivo='/tmp/utxo.json')
        self.nEleitor.text = ''

#========================================================================================================
#========================================================================================================

class TelaCandidatura(Screen):
    utxo = UTXO(arquivoUTXO='/tmp/utxo.json')
    registro = Registros()
    nCandidato = kyprops.ObjectProperty()
    numCandidato = kyprops.ObjectProperty()

#========================================================================================================
    def iniciar(self):
        self.registro.importar(arquivo='/tmp/registros.json')

#========================================================================================================
    def novoCandidato(self):        
        candidato = Candidato(apelido = self.nCandidato.text, 
                              numero = self.numCandidato.text)
        self.registro.inserir(candidato)
        self.utxo.novoEndereco(candidato.transacaoCriacao())
        self.registro.exportar('/tmp/registros.json')
        self.utxo.exportar(arquivo='/tmp/utxo.json')
        self.nCandidato.text = ''
        self.numCandidato.text = ''

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
        self.gerenciadorTela.add_widget(TelaSeletor(name="TelaSeletor"))

        
        self.gerenciadorTela.current='TelaInicial'
        
        return self.gerenciadorTela
        

if __name__ == "__main__":
    RDVEColetaApp().run()