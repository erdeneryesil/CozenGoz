from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from siniflar import Labirent,GozImaj,ReseptorImaj,ReseptorAksiyon,Yon,Hareket,Denetle,Hucre,Konum,DuvarDurum,GozTip,GozAksiyon,Yukle
from yarismaci import BenimGozum

from kivy.graphics import Ellipse,Line,Color,Point,Triangle,Rotate,PushMatrix,PopMatrix

from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')

# Manuel konumlandırmayı aktif et
Config.set('graphics', 'position', 'custom')

# Sol ve Üst koordinatları belirle
# Örneğin 2. monitörünüz ana monitörün sağındaysa ve ana monitör 1920px genişliğindeyse:
Config.set('graphics', 'left', '1920') 
Config.set('graphics', 'top', '0')


Builder.load_file('dizayn.kv')

    
class CozenGoz(FloatLayout):

    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)


        Yukle.AtlasDosya(GozImaj,GozAksiyon,GozTip,Yon)
        Yukle.AtlasDosya(ReseptorImaj,ReseptorAksiyon)
        


    

        self.__yarisSaat=None
        self.labirent=None
        self.goz=None
        self.gozImaj=None
        self.gozHucre=None
        self.reseptorImaj=None
        
        self.yarisAlaniWidget=self.ids.yarisAlaniWidget
        self.yarisAlaniWidget.bind(pos=self.guncelleCanvas, size=self.guncelleCanvas)
        
        goz1=BenimGozum("ROBOT1")


        

        self.labirent=Labirent(5,5)
        #print(self.labirent.baslangicHucre)

        self.goz=goz1
        self.gozHucre=self.labirent.baslangicHucre
        self.gozImaj=GozImaj(GozTip.GOZ1,Yon.baslangic())
        self.reseptorImaj=ReseptorImaj()

        self.add_widget(self.gozImaj)
        self.add_widget(self.reseptorImaj)



        self.__yarisSaat=Clock.schedule_interval(self.yarisTikTak,1/60)



    def yarisTikTak(self,dt):   

        if self.gozImaj.aksiyon!=GozAksiyon.BEKLE:
            pass
        else:
            if self.gozImaj.aksiyonBitti:
                hucreParam=self.labirent.hucreXYBoyut(self.gozHucre,self.gozImaj.yon)
                hucreX=hucreParam[Hucre.xKey()]
                hucreY=hucreParam[Hucre.yKey()]
                hucreBoyut=hucreParam[Hucre.boyutKey()]
                self.gozImaj.konumla(hucreX,hucreY,hucreBoyut)
                self.gozImaj.aksiyonBittiSifirla()
            
                reseptor=self.labirent.reseptorGonder(self.gozImaj.yon,self.gozHucre)
                robotHareket=self.goz.kararVer(reseptor)
                self.gozHareketUygula(robotHareket)
        

    
    def gozHareketUygula(self,hareket):
        match hareket:
            case Hareket.SOLA_DON:
                self.gozImaj.solaDon()#.yon=Yon((self.gozImaj.yon+1)%len(Yon))
                print("sola döndü")
            case Hareket.SAGA_DON:
                self.gozImaj.sagaDon()#.yon=Yon((self.gozImaj.yon-1)%len(Yon))
                print("sağa döndü")
            case Hareket.ILERI:
                hucreSatirNumara=self.gozHucre.satirNumara
                hucreSutunNumara=self.gozHucre.sutunNumara
                match self.gozImaj.yon:
                    case Yon.SAG:
                        hucreSutunNumara+=1
                    case Yon.SOL:
                        hucreSutunNumara-=1
                    case Yon.ALT:
                        hucreSatirNumara+=1
                    case Yon.UST:
                        hucreSatirNumara-=1
                
                duvar=self.labirent.duvar(self.gozHucre,self.labirent.hucre(hucreSatirNumara,hucreSutunNumara))
                if duvar.durum==DuvarDurum.ACIK:   
                    print("ileri gitti")                 
                    self.gozHucre=self.labirent.hucre(hucreSatirNumara,hucreSutunNumara)
                    self.gozImaj.git()
                else:
                    print("DUVAR KAPALI")


    def guncelleCanvas(self,*args):
        Denetle.TurHata(yarisAlani:=args[0],Widget)

        self.labirent.guncelleOlculer(yarisAlani.x,yarisAlani.y,yarisAlani.width,yarisAlani.height)
        
        canvas=yarisAlani.canvas#yarışın çizildiği canvas
        canvas.clear()
        with canvas:
            self.labirent.ciz()

        hucreCizimParam=self.labirent.hucreXYBoyut(self.gozHucre,self.gozImaj.yon)
        hucreX=hucreCizimParam[Hucre.xKey()]
        hucreY=hucreCizimParam[Hucre.yKey()]
        hucreBoyut=hucreCizimParam[Hucre.boyutKey()]

        self.gozImaj.guncelleOlculer(hucreX,hucreY,hucreBoyut)

                    
        

class Uygulama(App):
    def build(self):
        self.roboLabirent=CozenGoz()
        return self.roboLabirent

    



if __name__=="__main__":    
    Uygulama().run()