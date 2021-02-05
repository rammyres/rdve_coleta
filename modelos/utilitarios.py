import os

class Utilitarios:
    def remover_seguramente(self, caminho, passagens):
        with open(caminho, "ba+", buffering=0) as arquivo:
            tamanho = arquivo.tell()
        arquivo.close()
            
        with open(caminho, "br+", buffering=0) as arquivo:
            for _ in range(passagens):
                arquivo.seek(0,0)
                arquivo.write(os.urandom(tamanho))
            arquivo.seek(0)
        
        for _ in range(tamanho):
            arquivo.write(b'\x00')
        
        os.remove(caminho) 