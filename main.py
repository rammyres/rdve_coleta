#!/usr/bin/env python3

import kivy
from kivymd.app import MDApp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen

class TelaColeta(Screen):
    pass

# class TelaQREleitor(Screen):
#     pass
# class TesteLeitor(Screen):
#     pass


class RDVEColetaApp(MDApp):
           
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        gerenciadorTela = ScreenManager()
        gerenciadorTela.add_widget(TelaColeta(name='TelaInicial'))
        # gerenciadorTela.add_widget(TesteLeitor(name='Teste'))
        # gerenciadorTela.add_widget(TelaQREleitor(name='TelaQREleitor'))

        gerenciadorTela.current='TelaInicial'
        return TelaColeta()
        

if __name__ == "__main__":
    RDVEColetaApp().run()