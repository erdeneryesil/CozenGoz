


from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.modalview import ModalView #Açılır Pencere
from kivy.uix.label import Label

from kivy.clock import mainthread, Clock

from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

from grafik_pencere_dosya import Yukle,GozImaj,ReseptorImaj
from sabitler import AtlasYuklemeBilgi,AcilirPencereTip,AcilirPencereDurum,YarisAnimasyon,DosyaTip,GozTip,GozAksiyon,Hareket,Yon,DuvarDurum,ReseptorKonum
from labirent import Yarisma

class PencereYonetici(ScreenManager):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        

class AcilirPencere(ModalView):
    #logo='assets/sahne/logo.png'
    #logoOrijinalGenislik=2000
    #logoOrijinalYukseklik=2116

    #Her açılır pencere tipi için yalnızca tek bir Label nesnesi kullanılacak
    #etiketBoyutOran={'dosya yükle pencere':.05,'seviye yükle pencere':.05,'oyun başlat pencere':.15,'oyun kaybetti pencere':.15,'oyun kazandı pencere':.15}#Etiketin, yazı boyutunun pencere yüksekliğine oranı
    #etiketYazi={'dosya yükle pencere':u'DOSYALAR Y\u00dbKLEN\u00ceYOR','seviye yükle pencere':u'OYUN Y\u00dbKLEN\u00ceYOR','oyun başlat pencere':u'SEV\u00ceYE ','oyun kaybetti pencere':u'OYUN B\u00ceTT\u00ce','oyun kazandı pencere':u'TEBR\u00ceKLER'}

    __PENCERE_GENISLIK_ORAN=.9     #Açılır pencerenin genişliğinin, ana pencerenin genişliğine oranı
    __PENCERE_YUKSEKLIK_ORAN=.9    #Açılır pencerenin yüksekliğinin, ana pencerenin yüksekliğine oranı
    __ETIKET_BOYUT_ORAN=.03         #Etiket yazı boyutunun, açılır pencerenin genişliğine oranı
    __ETIKET_RENK=[.694,.157,.157,1]       #etiketin yazı rengi
    __ARKAPLAN_RENK=[.8,.8,.8,.7]

    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.background=''
        self.background_color=AcilirPencere.__ARKAPLAN_RENK

        self.__tip=None
        self.__durum=None
        self.__saat=None
        self.__dosyaTip=None
        self.__dosyaBilgiler=None
        self.__dosyaYuklemeIndis=0
        self.auto_dismiss=False
        self.__etiket=Label()
        self.__etiket.color=self.__ETIKET_RENK
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
        self.__etiket.font_size=self.width*self.__ETIKET_BOYUT_ORAN
                          
    def boyutAyarla(self,*args):
        self.size_hint=None,None
        self.width=Window.width*self.__PENCERE_GENISLIK_ORAN
        self.height=Window.height*self.__PENCERE_YUKSEKLIK_ORAN

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


class AnaPencere(Screen):
    def __init__(self,**kwargs):
        super().__init__()

        self.yarisma=Yarisma(self.ids.saha)
        

    def yarisBaslatClick(self):
        self.yarisma.baslat() 

    def on_enter(self, *args):
        self.__dosyaYuklemeBaslat()
        
    
    def __dosyaYuklemeBaslat(self):
        #önce dosyalar yüklensin
        gozAtlasYuklemeBilgi={AtlasYuklemeBilgi.ACIKLAMA:"Göz görselleri yükleniyor",AtlasYuklemeBilgi.IMAJ_SINIF:GozImaj,AtlasYuklemeBilgi.AKSIYON_SINIF:GozAksiyon,AtlasYuklemeBilgi.TIP_SINIF:GozTip,AtlasYuklemeBilgi.YON_SINIF:Yon}
        reseptorAtlasYuklemeBilgi={AtlasYuklemeBilgi.ACIKLAMA:"Reseptör görselleri yükleniyor",AtlasYuklemeBilgi.IMAJ_SINIF:ReseptorImaj}
        atlasDosyaBilgiler=[gozAtlasYuklemeBilgi,reseptorAtlasYuklemeBilgi]

        dosyaYuklemePencere=AcilirPencere()

        #dosya yükleme penceresi kapandığında, diğer işlemler başlasın
        dosyaYuklemePencere.dosyaYuklemeBaslat(DosyaTip.ATLAS,atlasDosyaBilgiler)

        



