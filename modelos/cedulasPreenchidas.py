from modelos.cedula import Cedula
import json, random

class CedulasPreenchidas(list):
    urnaID = ''

    def __init__(self, urnaID, cedulas = None):
        urnaID = urnaID

        if cedulas:
            self.importarCedulas(cedulas)

#========================================================================================================
    def importarCedulas(self, cedulas):
        if isinstance(cedulas, list):
            for c in cedulas:
                if isinstance(c, dict):
                    self.append(Cedula(
                        urnaID=c['urnaID'],
                        ID = c['id'],
                        endereco_destino=c['endereco_destino'],
                        assinatura=c['assinatura']
                        )
                    )

#========================================================================================================
    def inserir(self, cedula):
        if isinstance(cedula, Cedula):
            self.append(cedula)
        random.shuffle(self)
        
#========================================================================================================
    def importar(self, arquivo):
        try:
            with open(arquivo, 'r') as f:
                tmp = json.load(f)
                f.close()
                self.importarCedulas(tmp['cedulas'])
        except IOError:
            print('Arquivo de cédulas não localizado, pulando importação')

#========================================================================================================
    def serializar(self):
        return {
            'header': 'cedulasPreenchidas',
            'cedulas': self.serializar()
        }
#========================================================================================================
    def exportar(self, arquivo):
        with open(arquivo, 'w') as f:
            json.dump(self.serializar(), f, indent=4)
            f.close()
