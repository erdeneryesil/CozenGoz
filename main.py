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

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from siniflar import DosyaTip,AtlasYuklemeBilgi,AcilirPencere,Labirent,GozImaj,Reseptor,ReseptorImaj,ReseptorKonum,Yon,Hareket,Denetle,Hucre,Konum,DuvarDurum,GozTip,GozAksiyon,Yukle
from yarismaci import BenimGozum
import time
from kivy.graphics import Ellipse,Line,Color,Point,Triangle,Rotate,PushMatrix,PopMatrix






Builder.load_file('dizayn.kv')

    
class CozenGoz(FloatLayout):
    # Epsilon Değeri (Hassas Zamanlama Payı)
    __epsilon=1/120

    __animasyonGecikme=1/60
    __geriSayimGecikme=1

    @staticmethod
    def epsilon():
        return CozenGoz.__epsilon 
    @staticmethod
    def animasyonGecikme():
        return CozenGoz.__animasyonGecikme
    @staticmethod
    def geriSayimGecikme():
        return CozenGoz.__geriSayimGecikme 
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        #önce dosyalar yüklensin
        gozAtlasYuklemeBilgi={AtlasYuklemeBilgi.ACIKLAMA:"Göz görselleri yükleniyor",AtlasYuklemeBilgi.IMAJ_SINIF:GozImaj,AtlasYuklemeBilgi.AKSIYON_SINIF:GozAksiyon,AtlasYuklemeBilgi.TIP_SINIF:GozTip,AtlasYuklemeBilgi.YON_SINIF:Yon}
        reseptorAtlasYuklemeBilgi={AtlasYuklemeBilgi.ACIKLAMA:"Reseptör görselleri yükleniyor",AtlasYuklemeBilgi.IMAJ_SINIF:ReseptorImaj}
        atlasDosyaBilgiler=[gozAtlasYuklemeBilgi,reseptorAtlasYuklemeBilgi]




        


        self.dosyaYuklemePencere=AcilirPencere()

        #dosya yükleme penceresi kapandığında, diğer işlemler başlasın
        self.dosyaYuklemePencere.bind(on_dismiss=self.baslangicIslemleri)

        self.dosyaYuklemePencere.dosyaYuklemeBaslat(DosyaTip.ATLAS,atlasDosyaBilgiler)

        
        #Yukle.AtlasDosya(GozImaj,GozAksiyon,GozTip,Yon)
        #Yukle.AtlasDosya(ReseptorImaj)
        

    def baslangicIslemleri(self,instance):
        self.__yarisSaat=None
        self.labirent=None
        self.gozHucre=None
        self.goz=None
        self.gozImaj=None
        self.reseptor=None
        self.reseptorImaj=None
        self.reseptorGuncellendi=None
        
        self.yarisAlaniWidget=self.ids.yarisAlaniWidget
        self.yarisAlaniWidget.bind(pos=self.guncelleCanvas, size=self.guncelleCanvas)
                
        self.labirent=Labirent(3,3)
        goz1=BenimGozum("ROBOT1")
        self.goz=goz1
        self.gozImaj=GozImaj(GozTip.GOZ1,Yon.baslangic())

        self.gozHucre=self.labirent.baslangicHucre
        
        self.reseptor=Reseptor()
        self.reseptorImaj=ReseptorImaj()

        self.add_widget(self.gozImaj)
        self.add_widget(self.reseptorImaj)

        Clock.schedule_once(lambda dt: self.guncelleCanvas(self.yarisAlaniWidget), 0) #pencere açılması tamamlandığında, boyutların güncellenmesi için
        self.yarisBaslat()
        


    def yarisBaslat(self):
        self.reseptorGuncellendi=False
        self.oyunBitti=False
        self.gozHucre=self.labirent.baslangicHucre
        self.gozImaj.bekle()

        #animasyonSure=GozImaj.animasyonSure(GozAksiyon.BEKLE, self.gozImaj.yon)
        self.__yarisSaat=Clock.schedule_once(self.geriSayim,CozenGoz.geriSayimGecikme())

    def geriSayim(self,dt):
        self.__yarisSaat=Clock.schedule_once(self.yarisTikTak,CozenGoz.animasyonGecikme())

    def yarisTikTak(self,dt):          
        
        if self.gozImaj.aksiyon!=GozAksiyon.BEKLE:
            self.__yarisSaat=Clock.schedule_once(self.yarisTikTak,CozenGoz.animasyonGecikme())
            return
        
        if self.gozHucre==self.labirent.bitisHucre:           
            print("bitti")
            return
                    
        
        if not self.reseptorGuncellendi:
            animasyonSure=self.__reseptorGuncelle()
            self.__yarisSaat=Clock.schedule_once(self.yarisTikTak, animasyonSure+CozenGoz.epsilon() if animasyonSure > 0 else CozenGoz.animasyonGecikme())
            return

        
        if self.gozImaj.animasyonTamamlandi:
            self.gozImaj.animasyonBasladiResetle()
            self.gozImaj.animasyonTamamlandiResetle()
            x, y = self.labirent.hucreXY(self.gozHucre)
            self.gozImaj.konumla(x, y, self.labirent.hucreKenarUzunluk)
            self.reseptorGuncellendi = False
            
            
            gozHareket = self.goz.kararVer(self.reseptor)
            animasyonSure=self.__gozHareketUygula(gozHareket)
            
            self.__yarisSaat=Clock.schedule_once(self.yarisTikTak, animasyonSure+CozenGoz.epsilon())
            return
         

        
        self.__yarisSaat=Clock.schedule_once(self.yarisTikTak, CozenGoz.animasyonGecikme())
        
        
        
        
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
                    self.gozHucre=self.labirent.hucre(hucreSatirNumara,hucreSutunNumara)
                    self.gozImaj.git()
                else:
                    print("HÖSTT")
                    #self.gozImaj.bekle()

        return GozImaj.animasyonSure(self.gozImaj.aksiyon, self.gozImaj.yon)

    def guncelleCanvas(self,*args):
        if self.labirent is None:return

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
               
        yonFark = self.gozImaj.yon - Yon.baslangic()
        gercekReseptorKonum=ReseptorKonum((self.reseptor.konumIndis+yonFark)%len(ReseptorKonum))
        hucreX,hucreY=self.labirent.hucreXY(self.gozHucre)

        komsuHucreler = self.labirent.komsuHucreler(self.gozHucre)
        hedefHucre = komsuHucreler.get(Yon(gercekReseptorKonum))
        
        duvarDurum = DuvarDurum.KAPALI
        if hedefHucre:
            duvarDurum = self.labirent.duvar(self.gozHucre, hedefHucre).durum
        self.reseptor.degerGuncelle(self.reseptor.konumIndis, duvarDurum)

        if duvarDurum==DuvarDurum.ACIK:
            if not self.reseptorImaj.animasyonBasladi:
                self.reseptorImaj.animasyonTamamlandiResetle()
                self.reseptorImaj.konumla(gercekReseptorKonum,hucreX,hucreY,self.labirent.hucreKenarUzunluk)
            
                self.reseptorImaj.duvarAcik()
            
                return ReseptorImaj.animasyonSure()
            
            if self.reseptorImaj.animasyonTamamlandi:
                self.reseptorImaj.animasyonBasladiResetle()
                self.reseptor.konumIndisGuncelle()

                if self.reseptor.konumIndis == 0:
                    self.reseptorGuncellendi = True

        else:
            self.reseptor.konumIndisGuncelle()

            if self.reseptor.konumIndis == 0:
                self.reseptorGuncellendi = True

        return 0


class Uygulama(App):
    def build(self):
        self.title="ÇözenGöz"
        self.roboLabirent=CozenGoz()
        return self.roboLabirent

    



if __name__=="__main__":    
    Uygulama().run()