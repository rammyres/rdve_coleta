#!/usr/bin/env python3

import kivy
from kivymd.app import MDApp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen

class TelaColeta(Screen):
    pass

class TelaAlistamento(Screen):
    pass

class TesteLeitor(Screen):
    pass

class TelaUrna(Screen):
    pass


class RDVEColetaApp(MDApp):
           
    def build(self):
        # self.theme_cls.primary_palette = "BlueGray"
        self.gerenciadorTela = ScreenManager()
        self.gerenciadorTela.add_widget(TelaColeta(name='TelaInicial'))
        self.gerenciadorTela.add_widget(TelaAlistamento(name='TelaAlistamento'))
        # self.gerenciadorTela.add_widget(TesteLeitor(name='TesteLeitor'))
        # self.gerenciadorTela.add_widget(TelaQREleitor(name='TelaQREleitor'))

        self.gerenciadorTela.current='TelaInicial'
        
        return self.gerenciadorTela
        

if __name__ == "__main__":
    RDVEColetaApp().run()