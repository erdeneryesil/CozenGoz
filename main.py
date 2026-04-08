from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')

# Manuel konumlandırmayı aktif et
Config.set('graphics', 'position', 'custom')

# Sol ve Üst koordinatları belirle
# Örneğin 2. monitörünüz ana monitörün sağındaysa ve ana monitör 1920px genişliğindeyse:
Config.set('graphics', 'left', '1920') 
Config.set('graphics', 'top', '0')
#Config.set('graphics', 'left', '2180') 
#Config.set('graphics', 'top', '1')

import time

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout

from temel import Denetle
from labirent import Labirent
from goz import Reseptor
from yarismaci import BenimGozum

from pencereler import AnaPencere


Builder.load_file('dizayn.kv')




    

class Uygulama(App):
    def build(self):
        self.title="ÇözenGöz"
        #self.roboLabirent=CozenGoz()
        #return self.roboLabirent
        self.anaPencere=AnaPencere()
        return self.anaPencere
    



if __name__=="__main__":    
    Uygulama().run()