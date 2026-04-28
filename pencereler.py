
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.modalview import ModalView #Açılır Pencere
from kivy.uix.label import Label
from kivy.clock import mainthread
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

from grafik_pencere_dosya import Yukle,GozImaj,ReseptorImaj
from sabitler import AtlasYuklemeBilgi,AcilirPencereTip,AcilirPencereDurum,YarisAnimasyon,DosyaTip,GozTip,GozAksiyon,Hareket,Yon,DuvarDurum,ReseptorKonum
from yarismaci import BenimGozum
from goz import Reseptor
from labirent import Labirent
from temel import Denetle

class PencereYonetici(ScreenManager):
    def __init__(self,**kwargs):
        super().__init__()
        

class AcilirPencere(ModalView):
    #logo='assets/sahne/logo.png'
    #logoOrijinalGenislik=2000
    #logoOrijinalYukseklik=2116

    #Her açılır pencere tipi için yalnızca tek bir Label nesnesi kullanılacak
    #etiketBoyutOran={'dosya yükle pencere':.05,'seviye yükle pencere':.05,'oyun başlat pencere':.15,'oyun kaybetti pencere':.15,'oyun kazandı pencere':.15}#Etiketin, yazı boyutunun pencere yüksekliğine oranı
    #etiketYazi={'dosya yükle pencere':u'DOSYALAR Y\u00dbKLEN\u00ceYOR','seviye yükle pencere':u'OYUN Y\u00dbKLEN\u00ceYOR','oyun başlat pencere':u'SEV\u00ceYE ','oyun kaybetti pencere':u'OYUN B\u00ceTT\u00ce','oyun kazandı pencere':u'TEBR\u00ceKLER'}

    __pencereGenislikOran=.9     #Açılır pencerenin genişliğinin, ana pencerenin genişliğine oranı
    __pencereYukseklikOran=.9    #Açılır pencerenin yüksekliğinin, ana pencerenin yüksekliğine oranı
    __etiketBoyutOran=.03         #Etiket yazı boyutunun, açılır pencerenin genişliğine oranı
    ___etiketRenk=[.694,.157,.157,1]       #etiketin yazı rengi


    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.background=''
        self.background_color=[.8,.8,.8,.7]

        self.__tip=None
        self.__durum=None
        self.__saat=None
        self.__dosyaTip=None
        self.__dosyaBilgiler=None
        self.__dosyaYuklemeIndis=0
        self.auto_dismiss=False
        self.__etiket=Label()
        self.__etiket.color=self.___etiketRenk
        #self.__etiket.text="DENEME"


        #self.__etiket.font_name=Oyun.acilirPencereYaziTipiIsim
        #self.__etiket.color=AcilirPencere.etiketRenk
        #self.__etiket.text=AcilirPencere.etiketYazi[self.__tip]
        
        self.bind(pos=self.boyutAyarla, size=self.boyutAyarla)

        
            
    def dosyaYuklemeBaslat(self,dosyaTip,dosyaYuklemeBilgiler):
        self.__dosyaYuklemeIndis = 0
        self.__tip=AcilirPencereTip.DOSYA_YUKLEME
        self.__dosyaTip=dosyaTip
        self.__dosyaYuklemeBilgiler=dosyaYuklemeBilgiler
        self.__dosyaYuklemeIcinAyarla()
        self.__saat=Clock.schedule_interval(self.dosyaYuklemeTikTak,1/60)

    def dosyaYuklemeTikTak(self, dt):
        if self.__durum==AcilirPencereDurum.ACILMAYA_HAZIR:
            self.open()
        elif self.__durum==AcilirPencereDurum.ACIK:
            self.__durum=AcilirPencereDurum.ETIKET_ACIKLAMA_GUNCELLE
        elif self.__durum==AcilirPencereDurum.ETIKET_ACIKLAMA_GUNCELLE:
            if self.__dosyaYuklemeIndis<len(self.__dosyaYuklemeBilgiler):
                # AŞAMA 1: Sadece etiketi güncelle ve DUR
                bilgi=self.__dosyaYuklemeBilgiler[self.__dosyaYuklemeIndis]
                self.__etiket.text = bilgi.get(AtlasYuklemeBilgi.ACIKLAMA)
                # Durumu değiştiriyoruz ki bir sonraki 'tiktak'ta yükleme yapılsın
                self.__durum=AcilirPencereDurum.ISLEM_DEVAM_EDIYOR
            else:
                self.__durum=AcilirPencereDurum.ISLEM_BITTI
        elif self.__durum==AcilirPencereDurum.ISLEM_DEVAM_EDIYOR:
            # AŞAMA 2: Ağır olan yükleme işlemini yap
            bilgi = self.__dosyaYuklemeBilgiler[self.__dosyaYuklemeIndis]
            imajSinif = bilgi.get(AtlasYuklemeBilgi.IMAJ_SINIF)
            aksiyonSinif = bilgi.get(AtlasYuklemeBilgi.AKSIYON_SINIF)
            tipSinif = bilgi.get(AtlasYuklemeBilgi.TIP_SINIF)
            yonSinif = bilgi.get(AtlasYuklemeBilgi.YON_SINIF)
            
            Yukle.AtlasDosya(imajSinif, aksiyonSinif, tipSinif, yonSinif)
            
            # Yükleme bitti, indisi artır ve tekrar etiket güncelleme moduna dön
            self.__dosyaYuklemeIndis+= 1
            self.__durum=AcilirPencereDurum.ETIKET_ACIKLAMA_GUNCELLE

        elif self.__durum==AcilirPencereDurum.ISLEM_BITTI:
            self.dismiss()

        elif self.__durum==AcilirPencereDurum.KAPALI:
            self.__saat.cancel()


    def __tekliAtlasYukle(self,bilgi):
        aciklama = bilgi.get(AtlasYuklemeBilgi.ACIKLAMA)
        print(aciklama)
        self.__etiket.text = aciklama # Bu artık her dosyada güncellenecek
        
        imajSinif = bilgi.get(AtlasYuklemeBilgi.IMAJ_SINIF)
        aksiyonSinif = bilgi.get(AtlasYuklemeBilgi.AKSIYON_SINIF)
        tipSinif = bilgi.get(AtlasYuklemeBilgi.TIP_SINIF)
        yonSinif = bilgi.get(AtlasYuklemeBilgi.YON_SINIF)
        
        # Gerçek yükleme işlemi
        Yukle.AtlasDosya(imajSinif, aksiyonSinif, tipSinif, yonSinif)




    @mainthread #ayrı bir thread içerisinde nesne oluşturabilmek için fonksiyonun mainthread olması gerekiyor
    def __dosyaYuklemeIcinAyarla(self):
        self.__durum=AcilirPencereDurum.YUKLENIYOR
        yerlesim=BoxLayout(orientation='vertical')


        #self.logo=Image(source=AcilirPencere.logo,allow_stretch=False,keep_ratio=True)
        #self.logo.size_hint=None,None
        #self.logoBoyutAyarla()

        self.__etiketBoyutAyarla()

        #yerlesim.add_widget(self.logo)
        yerlesim.add_widget(self.__etiket)
        self.add_widget(yerlesim)
        self.__durum=AcilirPencereDurum.ACILMAYA_HAZIR

    def __etiketBoyutAyarla(self):
        self.__etiket.font_size=self.width*self.__etiketBoyutOran
                          
    def boyutAyarla(self,*args):
        self.size_hint=None,None
        self.width=Window.width*self.__pencereGenislikOran
        self.height=Window.height*self.__pencereYukseklikOran

        self.__etiketBoyutAyarla()
    

    def on_pre_open(self):
        self.__durum=AcilirPencereDurum.ACIK
        return super().on_pre_open()

    #def on_pre_dismiss(self):
        #self.__durum=AcilirPencereDurum.KAPALI
        #return super().on_pre_dismiss()
    
    def on_dismiss(self):
        self.__durum=AcilirPencereDurum.KAPALI
        return super().on_dismiss()

class DenemePencere(Screen):
    pass

class AnaPencere(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        print("asd")
        
        self.yarisPencere=None
    
    def denemeClick(self):
        denemePencere=DenemePencere()

        self.yarisPencere=YarisPencere()
        self.manager.current=self.yarisPencere.name
        

class YarisPencere(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
    
    def on_enter(self, *args):
        self.__dosyaYuklemeBaslat()
    
    def __dosyaYuklemeBaslat(self):
        #önce dosyalar yüklensin
        gozAtlasYuklemeBilgi={AtlasYuklemeBilgi.ACIKLAMA:"Göz görselleri yükleniyor",AtlasYuklemeBilgi.IMAJ_SINIF:GozImaj,AtlasYuklemeBilgi.AKSIYON_SINIF:GozAksiyon,AtlasYuklemeBilgi.TIP_SINIF:GozTip,AtlasYuklemeBilgi.YON_SINIF:Yon}
        reseptorAtlasYuklemeBilgi={AtlasYuklemeBilgi.ACIKLAMA:"Reseptör görselleri yükleniyor",AtlasYuklemeBilgi.IMAJ_SINIF:ReseptorImaj}
        atlasDosyaBilgiler=[gozAtlasYuklemeBilgi,reseptorAtlasYuklemeBilgi]

        dosyaYuklemePencere=AcilirPencere()

        #dosya yükleme penceresi kapandığında, diğer işlemler başlasın
        dosyaYuklemePencere.bind(on_dismiss=self.baslangicIslemleri)
        dosyaYuklemePencere.dosyaYuklemeBaslat(DosyaTip.ATLAS,atlasDosyaBilgiler)
        
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
        self.__yarisSaat=Clock.schedule_once(self.geriSayim,YarisAnimasyon.geriSayimGecikme())

    def geriSayim(self,dt):
        self.__yarisSaat=Clock.schedule_once(self.yarisTikTak,YarisAnimasyon.animasyonGecikme())

    def yarisTikTak(self,dt):          
        
        if self.gozImaj.aksiyon!=GozAksiyon.BEKLE:
            self.__yarisSaat=Clock.schedule_once(self.yarisTikTak,YarisAnimasyon.animasyonGecikme())
            return
        
        if self.gozHucre==self.labirent.bitisHucre:           
            print("bitti")
            return
                    
        
        if not self.reseptorGuncellendi:
            animasyonSure=self.__reseptorGuncelle()
            self.__yarisSaat=Clock.schedule_once(self.yarisTikTak, animasyonSure+YarisAnimasyon.epsilon() if animasyonSure > 0 else YarisAnimasyon.animasyonGecikme())
            return

        
        if self.gozImaj.animasyonTamamlandi:
            self.gozImaj.animasyonBasladiResetle()
            self.gozImaj.animasyonTamamlandiResetle()
            x, y = self.labirent.hucreXY(self.gozHucre)
            self.gozImaj.konumla(x, y, self.labirent.hucreKenarUzunluk)
            self.reseptorGuncellendi = False
            
            
            gozHareket = self.goz.kararVer(self.reseptor)
            animasyonSure=self.__gozHareketUygula(gozHareket)
            
            self.__yarisSaat=Clock.schedule_once(self.yarisTikTak, animasyonSure+YarisAnimasyon.epsilon())
            return
        
        self.__yarisSaat=Clock.schedule_once(self.yarisTikTak, YarisAnimasyon.animasyonGecikme())
        
        
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


