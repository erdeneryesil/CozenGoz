from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.modalview import ModalView #Açılır Pencere
from kivy.uix.label import Label

from kivy.clock import mainthread, Clock

from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

from kivy.properties import ObjectProperty

from grafik_dosya import KaynakYukleyici,GozImaj,ReseptorImaj
from sabitler import AnaPencereSabit, AcilirPencereSabit, AtlasYuklemeBilgi,AcilirPencereTip,AcilirPencereDurum,DosyaTip,GozTip,GozAksiyon,Yon, DikdortgenTip
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
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.background=''
        self.background_color=AcilirPencereSabit.ARKAPLAN_RENK

        self.__tip=None
        self.__durum=None
        self.__saat=None
        self.__dosya_tip=None
        self.__dosya_yukleme_bilgileri=None
        self.__dosya_yukleme_indis=0
        self.auto_dismiss=False
        self.__etiket=Label()
        self.__etiket.color=AcilirPencereSabit.ETIKET_RENK
        #self.__etiket.text="DENEME"

        #self.__etiket.font_name=Oyun.acilirPencereYaziTipiIsim
        #self.__etiket.color=AcilirPencere.etiketRenk
        #self.__etiket.text=AcilirPencere.etiketYazi[self.__tip]
        
        self.bind(pos=self.boyut_ayarla, size=self.boyut_ayarla)    
            
    def dosya_yukleme_baslat(self,dosya_tip,dosya_yukleme_bilgileri):
        self.__dosya_yukleme_indis = 0
        self.__tip=AcilirPencereTip.DOSYA_YUKLEME
        self.__dosya_tip=dosya_tip
        self.__dosya_yukleme_bilgileri=dosya_yukleme_bilgileri
        self.__dosya_yukleme_icin_ayarla()
        self.__saat=Clock.schedule_interval(self.dosya_yukleme_tik_tak,1/60)

    def dosya_yukleme_tik_tak(self, dt):
        if self.__durum==AcilirPencereDurum.ACILMAYA_HAZIR:
            self.open()
        elif self.__durum==AcilirPencereDurum.ACIK:
            self.__durum=AcilirPencereDurum.ETIKET_ACIKLAMA_GUNCELLE
        elif self.__durum==AcilirPencereDurum.ETIKET_ACIKLAMA_GUNCELLE:
            if self.__dosya_yukleme_indis<len(self.__dosya_yukleme_bilgileri):
                # AŞAMA 1: Sadece etiketi güncelle ve DUR
                bilgi=self.__dosya_yukleme_bilgileri[self.__dosya_yukleme_indis]
                self.__etiket.text = bilgi.get(AtlasYuklemeBilgi.ACIKLAMA)
                # Durumu değiştiriyoruz ki bir sonraki 'tiktak'ta yükleme yapılsın
                self.__durum=AcilirPencereDurum.ISLEM_DEVAM_EDIYOR
            else:
                self.__durum=AcilirPencereDurum.ISLEM_BITTI
        elif self.__durum==AcilirPencereDurum.ISLEM_DEVAM_EDIYOR:
            # AŞAMA 2: Ağır olan yükleme işlemini yap
            bilgi = self.__dosya_yukleme_bilgileri[self.__dosya_yukleme_indis]
            imaj_sinif = bilgi.get(AtlasYuklemeBilgi.IMAJ_SINIF)
            aksiyon_sinif = bilgi.get(AtlasYuklemeBilgi.AKSIYON_SINIF)
            tip_sinif = bilgi.get(AtlasYuklemeBilgi.TIP_SINIF)
            yon_sinif = bilgi.get(AtlasYuklemeBilgi.YON_SINIF)
            
            KaynakYukleyici.atlas_dosya(imaj_sinif, aksiyon_sinif, tip_sinif, yon_sinif)
            
            # Yükleme bitti, indisi artır ve tekrar etiket güncelleme moduna dön
            self.__dosya_yukleme_indis+= 1
            self.__durum=AcilirPencereDurum.ETIKET_ACIKLAMA_GUNCELLE

        elif self.__durum==AcilirPencereDurum.ISLEM_BITTI:
            self.dismiss()

        elif self.__durum==AcilirPencereDurum.KAPALI:
            self.__saat.cancel()

    def __tekli_atlas_yukle(self,bilgi):
        aciklama = bilgi.get(AtlasYuklemeBilgi.ACIKLAMA)
        print(aciklama)
        self.__etiket.text = aciklama # Bu artık her dosyada güncellenecek
        
        imaj_sinif = bilgi.get(AtlasYuklemeBilgi.IMAJ_SINIF)
        aksiyon_sinif = bilgi.get(AtlasYuklemeBilgi.AKSIYON_SINIF)
        tip_sinif = bilgi.get(AtlasYuklemeBilgi.TIP_SINIF)
        yon_sinif = bilgi.get(AtlasYuklemeBilgi.YON_SINIF)
        
        # Gerçek yükleme işlemi
        KaynakYukleyici.atlas_dosya(imaj_sinif, aksiyon_sinif, tip_sinif, yon_sinif)

    @mainthread #ayrı bir thread içerisinde nesne oluşturabilmek için fonksiyonun mainthread olması gerekiyor
    def __dosya_yukleme_icin_ayarla(self):
        self.__durum=AcilirPencereDurum.YUKLENIYOR
        yerlesim=BoxLayout(orientation='vertical')

        #self.logo=Image(source=AcilirPencere.logo,allow_stretch=False,keep_ratio=True)
        #self.logo.size_hint=None,None
        #self.logoBoyutAyarla()

        self.__etiket_boyut_ayarla()

        #yerlesim.add_widget(self.logo)
        yerlesim.add_widget(self.__etiket)
        self.add_widget(yerlesim)
        self.__durum=AcilirPencereDurum.ACILMAYA_HAZIR

    def __etiket_boyut_ayarla(self):
        self.__etiket.font_size=self.width*AcilirPencereSabit.ETIKET_BOYUT_ORAN
                          
    def boyut_ayarla(self,*args):
        self.size_hint=None,None
        self.width=Window.width*AcilirPencereSabit.PENCERE_GENISLIK_ORAN
        self.height=Window.height*AcilirPencereSabit.PENCERE_YUKSEKLIK_ORAN

        self.__etiket_boyut_ayarla()
    
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
        self.__yarisma=Yarisma(self.ids.saha)
    
    def yaris_baslat_tiklama(self):
        self.__yarisma.baslat() 

    def on_enter(self, *args):
        self.__dosya_yukleme_baslat()
        
    def __dosya_yukleme_baslat(self):
        #önce dosyalar yüklensin
        goz_atlas_yukleme_bilgi={AtlasYuklemeBilgi.ACIKLAMA:AnaPencereSabit.ACIKLAMA_GOZ_GORSEL_YUKLEME,AtlasYuklemeBilgi.IMAJ_SINIF:GozImaj,AtlasYuklemeBilgi.AKSIYON_SINIF:GozAksiyon,AtlasYuklemeBilgi.TIP_SINIF:GozTip,AtlasYuklemeBilgi.YON_SINIF:Yon}
        reseptor_atlas_yukleme_bilgi={AtlasYuklemeBilgi.ACIKLAMA:AnaPencereSabit.ACIKLAMA_RESEPTOR_GORSEL_YUKLEME,AtlasYuklemeBilgi.IMAJ_SINIF:ReseptorImaj}
        atlas_dosya_bilgileri=[goz_atlas_yukleme_bilgi,reseptor_atlas_yukleme_bilgi]

        dosya_yukleme_pencere=AcilirPencere()

        #dosya yükleme penceresi kapandığında, diğer işlemler başlasın
        dosya_yukleme_pencere.dosya_yukleme_baslat(DosyaTip.ATLAS,atlas_dosya_bilgileri)