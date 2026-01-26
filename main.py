from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from siniflar import Labirent,GozImaj,Reseptor,ReseptorImaj,ReseptorAksiyon,ReseptorKonum,ReseptorAsama,Yon,Hareket,Denetle,Hucre,Konum,DuvarDurum,GozTip,GozAksiyon,Yukle
from yarismaci import BenimGozum
import time
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
        self.gozHucre=None
        self.goz=None
        self.gozImaj=None
        self.reseptor=None
        self.reseptorImaj=None
        self.reseptorGuncellendi=True
        
        self.yarisAlaniWidget=self.ids.yarisAlaniWidget
        self.yarisAlaniWidget.bind(pos=self.guncelleCanvas, size=self.guncelleCanvas)
        
        goz1=BenimGozum("ROBOT1")


        

        self.labirent=Labirent(5,5)
        self.gozHucre=self.labirent.baslangicHucre

        self.goz=goz1
        self.gozImaj=GozImaj(GozTip.GOZ1,Yon.baslangic())
        
        self.reseptor=Reseptor()
        self.reseptorImaj=ReseptorImaj()

        self.add_widget(self.gozImaj)
        self.add_widget(self.reseptorImaj)


        self.__yarisSaat=Clock.schedule_interval(self.yarisTikTak,1/60)
        


    def yarisTikTak(self,dt):    
         
        if self.gozImaj.aksiyon!=GozAksiyon.BEKLE:
            return
        
        if not self.reseptorGuncellendi:
            self.__reseptorGuncelle()
            return

        if not self.gozImaj.aksiyonBasladi:
            self.gozImaj.aksiyonTamamlandiResetle()
            gozHareket = self.goz.kararVer(self.reseptor)
            self.__gozHareketUygula(gozHareket)
            return

        if self.gozImaj.aksiyonTamamlandi:
            self.gozImaj.aksiyonBasladiResetle()
            x, y = self.labirent.hucreXY(self.gozHucre)
            self.gozImaj.konumla(x, y, self.labirent.hucreKenarUzunluk)
            
            self.reseptorGuncellendi = False
        



          

    
    def __gozHareketUygula(self,hareket):
        match hareket:
            case Hareket.SOLA_DON:
                self.gozImaj.solaDon()#.yon=Yon((self.gozImaj.yon+1)%len(Yon))
                #print("sola döndü")
            case Hareket.SAGA_DON:
                self.gozImaj.sagaDon()#.yon=Yon((self.gozImaj.yon-1)%len(Yon))
                #print("sağa döndü")
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
                    #print("ileri gitti")                 
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

        x,y=self.labirent.hucreXY(self.gozHucre)

        self.gozImaj.guncelleOlculer(x,y,self.labirent.hucreKenarUzunluk)
        self.reseptorImaj.guncelleOlculer(self.labirent.hucreKenarUzunluk)

    def __reseptorGuncelle(self):
        if self.reseptorGuncellendi:
            print(self.reseptorGuncellendi)
        
        if self.reseptor.asama == ReseptorAsama.BOSTA:
            self.reseptor.asamaGuncelle()
            return
        


        yonFark = self.gozImaj.yon - Yon.baslangic()
        gercekReseptorKonum=ReseptorKonum((self.reseptor.konumIndis+yonFark)%len(ReseptorKonum))
        hucreX,hucreY=self.labirent.hucreXY(self.gozHucre)

        
        if self.reseptor.asama == ReseptorAsama.TARAMA:
            if not self.reseptorImaj.aksiyonBasladi:
                self.reseptorImaj.aksiyonTamamlandiResetle()
                self.reseptorImaj.konumla(gercekReseptorKonum,hucreX,hucreY,self.labirent.hucreKenarUzunluk)
                self.reseptorImaj.tara()
                return
            if self.reseptorImaj.aksiyonTamamlandi:
                self.reseptorImaj.aksiyonBasladiResetle()
                self.reseptor.asamaGuncelle()
                return

        if self.reseptor.asama == ReseptorAsama.SONUC:
            komsuHucreler = self.labirent.komsuHucreler(self.gozHucre)
            hedefHucre = komsuHucreler.get(Yon(gercekReseptorKonum))
            
            duvarDurum = DuvarDurum.KAPALI
            if hedefHucre:
                duvarDurum = self.labirent.duvar(self.gozHucre, hedefHucre).durum
            self.reseptor.degerGuncelle(self.reseptor.konumIndis, duvarDurum)

            if not self.reseptorImaj.aksiyonBasladi:
                self.reseptorImaj.aksiyonTamamlandiResetle()
                self.reseptorImaj.konumla(gercekReseptorKonum,hucreX,hucreY,self.labirent.hucreKenarUzunluk)
                if duvarDurum==DuvarDurum.ACIK:
                    self.reseptorImaj.duvarAcik()
                else:
                    self.reseptorImaj.duvarKapali()
                return
            
            if self.reseptorImaj.aksiyonTamamlandi:
                self.reseptorImaj.aksiyonBasladiResetle()
                self.reseptor.konumIndisGuncelle()
                
                if self.reseptor.konumIndis == 0:
                    self.reseptorGuncellendi = True

                self.reseptor.asamaGuncelle()





    
            
            
        

class Uygulama(App):
    def build(self):
        self.roboLabirent=CozenGoz()
        return self.roboLabirent

    



if __name__=="__main__":    
    Uygulama().run()