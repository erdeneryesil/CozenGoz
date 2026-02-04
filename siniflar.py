from enum import IntEnum
from abc import ABC, ABCMeta, abstractmethod
import random
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse,Line,Color,Point,Triangle,Rotate,PushMatrix,PopMatrix
from kivy.atlas import Atlas
from kivy.uix.image import Image,CoreImage
from kivy.clock import Clock

class Denetle:
    @staticmethod
    def TurHata(deger,tur):#Bir nesneye atama yapılırken, doğru türde bir değer mi diye kontrol ediliyor
        if not isinstance(deger, tur):
            raise TypeError(f"{tur.__name__} nesnesine, {type(deger).__name__} türünde bir değer atayamazsınız")
    
    @staticmethod
    def BosNesne(nesne,mesaj):
        if nesne is None:
            raise ValueError(mesaj)

class DuvarDurum(IntEnum):
    KAPALI=0
    ACIK=1

#Robotun yapabileceği hamleler
class Hareket(IntEnum):
    SAGA_DON=-1
    ILERI=0
    SOLA_DON=1
    
#Robotun önünün baktığı yön. Robotun varsayılan yönü Yon.UST 
class Yon(IntEnum):#sıralama SOL,ALT,SAG,UST olmalı. Matematiksel işlemler yapılıyor
    SOL=0
    ALT=1
    SAG=2
    UST=3

    __donusAci=90   #her dönüş 90 derece dönmesi anlamına geliyor
    __baslangic=UST
    
    @staticmethod
    def baslangic():
        return Yon.__baslangic
    
    @staticmethod
    def donusAci():
        return Yon.__donusAci
    
    @staticmethod
    def solaDon(yon):
        return Yon((yon+1)%len(Yon))
    
    @staticmethod
    def sagaDon(yon):
        return Yon((yon-1)%len(Yon))
    
    def __str__(self):
        return f"YÖN : {self.name}"

#Robotun bulunduğu konum
class Konum:

    def __init__(self,satirNumara,sutunNumara):
        #if satirNumara is None:
            #satirNumara = self.__class__.__baslangicSatirNumara
        #if sutunNumara is None:
            #sutunNumara = self.__class__.__baslangicSutunNumara

        self.__satirNumara=satirNumara
        self.__sutunNumara=sutunNumara
    
    def __str__(self):
        return f"Konum : satır : {self.__satirNumara}, sütun : {self.__sutunNumara}"
    
    @property
    def satirNumara(self):
        return self.__satirNumara
    @property
    def sutunNumara(self):
        return self.__sutunNumara
    
    def satirDegistir(self,degisim,max=99):
        self.__satir+=degisim

    def sutunDegistir(self,degisim,max=99):
        self.__sutun+=degisim

class Duvar:        
    def __init__(self):#hücreler soldan sağa ya da yukarıdan aşağıda
        self.__durum=DuvarDurum.KAPALI 
            
    @property
    def durum(self):
        return self.__durum
    
    def ac(self):
        self.__durum=DuvarDurum.ACIK
    def kapat(self):
        self.__durum=DuvarDurum.KAPALI
    
class Hucre(Konum):
    __tipBaslangicKey="baslangic"
    __tipBitisKey="bitis"
    __tipYolKey="yol"
    __tipRenkKey="renk"
    __tipUzunlukCarpanKey="uzunlukCarpan"
    __sayiKey="sayı"
    __tip={__tipBaslangicKey:{__tipRenkKey:{"r":245/255,"g":73/255,"b":39/255,"a":1},__tipUzunlukCarpanKey:1},__tipBitisKey:{__tipRenkKey:{"r":219/255,"g":88/255,"b":88/255,"a":1},__tipUzunlukCarpanKey:1},__tipYolKey:{__tipRenkKey:{"r":255/255,"g":247/255,"b":173/255,"a":0.5},__tipUzunlukCarpanKey:0.8}}

    @staticmethod
    def gozTipBaslangicKey():
        return Hucre.__tipBaslangicKey
    @staticmethod
    def gozTipBitisKey():
        return Hucre.__tipBitisKey
    @staticmethod
    def gozTipYolKey():
        return Hucre.__tipYolKey
    @staticmethod
    def gozTipRenkKey():
        return Hucre.__tipRenkKey
    @staticmethod
    def gozTipUzunlukCarpanKey():
        return Hucre.__tipUzunlukCarpanKey
    @staticmethod
    def sayiKey():
        return Hucre.__sayiKey
    @staticmethod
    def gozTip(gozTipKey):
        return Hucre.__tip[gozTipKey]




    def __init__(self,satirNumara,sutunNumara):
        super().__init__(satirNumara,sutunNumara)

    def __eq__(self, digerHucre):# == operatörü ile iki Hucre nesnesinin eşit olup olmadığı sorgulanıyor
        return True if self.satirNumara==digerHucre.satirNumara and self.sutunNumara==digerHucre.sutunNumara else False
    
    def __ne__(self,digerHucre): # != operatörü ile iki Hucre nesnesinin farklı olup olmadığı sorgulanıyor
        return True if self.satirNumara!=digerHucre.satirNumara or self.sutunNumara!=digerHucre.sutunNumara else False

class OnHucre(Hucre):
    def __init__(self,satirNumara,sutunNumara):
        super().__init__(satirNumara,sutunNumara)
        self.__isaret=False
    
    @property
    def isaret(self):
        return self.__isaret
    
    def isaretKoy(self):
        self.__isaret=True
    
    def isaretKaldir(self):
        self.__isaret=False


class DosyaTip(IntEnum):
    ATLAS=0

class AtlasYuklemeBilgi(IntEnum):
    ACIKLAMA=0 #dosya yüklenirken, görüntülenmek istenen açıklama
    IMAJ_SINIF=1
    AKSIYON_SINIF=2
    TIP_SINIF=3
    YON_SINIF=4

class AcilirPencereTip(IntEnum):
    DOSYA_YUKLEME=0

class AcilirPencereDurum(IntEnum):
    YUKLENIYOR=0
    ACILMAYA_HAZIR=1
    ACIK=2
    ETIKET_ACIKLAMA_GUNCELLE = 3 
    ISLEM_DEVAM_EDIYOR=4
    ISLEM_BITTI=5
    KAPALI=6


from kivy.uix.modalview import ModalView #Açılır Pencere
from kivy.uix.label import Label
from kivy.clock import mainthread
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
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

class Yukle:
    @staticmethod
    def AtlasDosya(ImajSinif,AksiyonSinif=None,TipSinif=None,YonSinif=None):
        #ImajSinif.atlasYuklendiGuncelle(False)
    
        # Başlangıçta durum tespiti yaparak döngü içindeki 'if' yükünü azaltıyoruz
        aksiyonlar= AksiyonSinif if AksiyonSinif else [None]
        tipler = TipSinif if TipSinif else [None]
        yonler = YonSinif if YonSinif else [None]
        dizin = ImajSinif.dizin()

        for tip in tipler:
            atlasAd = ImajSinif.atlasDosya() if tip is None else ImajSinif.atlasDosya(tip)
            atlas = Atlas(f"{dizin}/{atlasAd}")
            
            for yon in yonler:
                for aksiyon in aksiyonlar:
                    # Parametre yapısına göre metod seçimi
                    if YonSinif:
                        kareAdNumarasiz = ImajSinif.kareAd(aksiyon,yon)
                        kareSayisi = ImajSinif.kareSayi(aksiyon,yon)
                    else:
                        if aksiyon:
                            kareAdNumarasiz = ImajSinif.kareAd(aksiyon)
                            kareSayisi = ImajSinif.kareSayi(aksiyon)
                        else:
                            kareAdNumarasiz = ImajSinif.kareAd()
                            kareSayisi = ImajSinif.kareSayi()


                    for kareNumara in range(kareSayisi):
                        kareAd = f"{kareAdNumarasiz}{kareNumara}"
                        
                        # Atlas içinden resmi çek ve dönüştür
                        hamKare = CoreImage(atlas[kareAd])
                        
                        # Ekleme işlemini duruma göre yap
                        if TipSinif and YonSinif:
                            ImajSinif.kareEkle(hamKare,aksiyon,tip, yon)
                        else:
                            ImajSinif.kareEkle(hamKare)

        #ImajSinif.atlasYuklendiGuncelle(True)
    
class GozTip(IntEnum):
    GOZ1=1
    GOZ2=2
    GOZ3=3
    GOZ4=4

class GozAksiyon(IntEnum):
    BEKLE=0
    GIT=1
    PATLA=2
    SOLA_DON=3
    SAGA_DON=4

# Kivy'nin Image sınıfının kullandığı metaclass'ı ve ABCMeta'yı birleştiriyoruz
class ImajMeta(type(Image), ABCMeta):
    pass
class Imaj(Image,metaclass=ImajMeta):
    _dizin = None
    _atlasDosya = None
    _kareAd = None
    _kareSayi = None
    _kare = None
    _gecikme = None
    _orijinalBoyut = None
    _boyutOran = None
    _animasyonTekrar = None
    _atlasYuklendi = False


    #Aşağıdaki abstract metotlar alt sınıflar tarafından mutlaka override edilmelidir.
    @classmethod
    @abstractmethod
    def atlasDosya(cls):
        pass
    @classmethod
    @abstractmethod
    def gecikme(cls):
        pass
    @classmethod
    @abstractmethod
    def animasyonTekrar(cls):
        pass
    @classmethod
    @abstractmethod
    def kareAd(cls):
        pass
    @classmethod
    @abstractmethod
    def kareSayi(cls):
        pass
    @classmethod
    @abstractmethod
    def kare(cls,numara):
        pass
    @classmethod
    @abstractmethod
    def kareEkle(cls,hamKare):
        pass
    @classmethod
    @abstractmethod
    def animasyonSure(cls):
        pass
    @abstractmethod
    def _animasyonTikTak(self,dt):
        pass
    @abstractmethod
    def guncelleOlculer(self):
        pass
    @abstractmethod
    def konumla(self):
        pass
    

    @classmethod
    def dizin(cls):
        return cls._dizin
    @classmethod
    def atlasYuklendi(cls):
        return cls._atlasYuklendi
    @classmethod
    def atlasYuklendiGuncelle(cls, deger):
        cls._atlasYuklendi = deger
    @classmethod
    def orijinalBoyut(cls):
        return cls._orijinalBoyut
    @classmethod
    def boyutOran(cls):
        return cls._boyutOran
    
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self._kareSayac=0
        self._animasyonSaat=None
        self._animasyonTamamlandi=False
        self._animasyonBasladi=False
    
    @property
    def animasyonBasladi(self):
        return self._animasyonBasladi
    def animasyonBasladiResetle(self):
        self._animasyonBasladi=False
    @property
    def animasyonTamamlandi(self):
        return self._animasyonTamamlandi
    def animasyonTamamlandiResetle(self):
       self._animasyonTamamlandi=False

    def animasyonSaatDurdur(self):
        if self._animasyonSaat is not None: 
            self._animasyonSaat.cancel()

class ReseptorImaj(Imaj):
    _dizin="assets/reseptor"
    _atlasDosya="reseptor.atlas"

    _kareAd="reseptor-yesil-"
    _kareSayi=8
    _kare=[]
            
    _gecikme=1/60

    _orijinalBoyut=340
    _boyutOran=1#hücre genişliğine oranı
    _atlasYuklendi=False # atlas dosyasının yüklenip yüklenmediğini kontrol edeceğimiz değişken. Yüklendiğine True olacak
    _animasyonTekrar=1 # Animasyon kaç kere çalışacak

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        #self.allow_stretch=True
        #self.fit_mode='contain'
        self.size_hint=(None,None)
        self.opacity=0
        
    @classmethod
    def atlasDosya(cls):
        return cls._atlasDosya
    @classmethod
    def gecikme(cls):
        return cls._gecikme
    @classmethod
    def animasyonTekrar(cls):
        return cls._animasyonTekrar
    @classmethod
    def kareAd(cls):
        return cls._kareAd
    @classmethod
    def kareSayi(cls):
        return cls._kareSayi
    @classmethod
    def kare(cls,numara):
        return cls._kare[numara]
    @classmethod
    def kareEkle(cls,hamKare):
        cls._kare.append(hamKare)
    @classmethod
    def animasyonSure(cls):
        n = cls.kareSayi()
        r = cls.animasyonTekrar()
        delay = cls.gecikme()         
        return n * r * delay
    
    def duvarAcik(self):
        self._animasyonHazirlik()

    def _animasyonHazirlik(self):
        self.texture=ReseptorImaj.kare(0).texture#yeni reseptorAksiyonun, ilk karesi alınıyor. Aksiyon geçişinde, önceki durumun karesi kalmasın diye 
        self._kareSayac=0
        self.opacity=1
        self._animasyonBasladi=True
        if self._animasyonSaat:
            self._animasyonSaat.cancel()
        self._animasyonSaat=Clock.schedule_interval(self._animasyonTikTak,ReseptorImaj.gecikme())
    
    def _animasyonTikTak(self,dt):
        self.texture=ReseptorImaj.kare(self._kareSayac%(ReseptorImaj.kareSayi())).texture
        self._kareSayac+=1


        if self._kareSayac>=ReseptorImaj.kareSayi()*ReseptorImaj.animasyonTekrar():
            self._kareSayac=0
            self._animasyonTamamlandi=True
            self.opacity=0
                
    def guncelleOlculer(self,hucreBoyut):#canvas içerisine çizilecek labirentin genişlik, yükseklik, x, y vs değerleri hesaplanıyor
        self.width=hucreBoyut*ReseptorImaj.boyutOran()
        self.height=self.width
        #self.konumla(hucreX,hucreY,hucreBoyut)

    def konumla(self,gercekYon,hucreX,hucreY,hucreBoyut):
        match gercekYon:
            case Yon.SAG:
                self.center_x=hucreX+hucreBoyut
                self.center_y=hucreY+hucreBoyut/2
            case Yon.ALT:
                self.center_x=hucreX+hucreBoyut/2
                self.center_y=hucreY
            case Yon.SOL:
                self.center_x=hucreX
                self.center_y=hucreY+hucreBoyut/2
            case Yon.UST:
                self.center_x=hucreX+hucreBoyut/2
                self.center_y=hucreY+hucreBoyut           
                    
class GozImaj(Imaj):#animasyon ve çizim işlemlerinin yürütüleceğin sınıf
    _dizin="assets/goz"

    _atlasDosya={GozTip.GOZ1:"goz1.atlas",GozTip.GOZ2:"goz2.atlas",GozTip.GOZ3:"goz3.atlas",GozTip.GOZ4:"goz4.atlas"}
    
    _kareAd={
        Yon.SOL:{GozAksiyon.BEKLE:"sol-bekle-",GozAksiyon.GIT:"sol-git-",GozAksiyon.PATLA:"sol-patla-",GozAksiyon.SOLA_DON:"sol-sola-don-",GozAksiyon.SAGA_DON:"sol-saga-don-"},
        Yon.ALT:{GozAksiyon.BEKLE:"alt-bekle-",GozAksiyon.GIT:"alt-git-",GozAksiyon.PATLA:"alt-patla-",GozAksiyon.SOLA_DON:"alt-sola-don-",GozAksiyon.SAGA_DON:"alt-saga-don-"},
        Yon.SAG:{GozAksiyon.BEKLE:"sag-bekle-",GozAksiyon.GIT:"sag-git-",GozAksiyon.PATLA:"sag-patla-",GozAksiyon.SOLA_DON:"sag-sola-don-",GozAksiyon.SAGA_DON:"sag-saga-don-"},
        Yon.UST:{GozAksiyon.BEKLE:"ust-bekle-",GozAksiyon.GIT:"ust-git-",GozAksiyon.PATLA:"ust-patla-",GozAksiyon.SOLA_DON:"ust-sola-don-",GozAksiyon.SAGA_DON:"ust-saga-don-"},
    }
    _kareSayi={#animasyonların içerdiği resim sayısı.
        Yon.SOL:{GozAksiyon.BEKLE:20,GozAksiyon.GIT:6,GozAksiyon.PATLA:11,GozAksiyon.SOLA_DON:11,GozAksiyon.SAGA_DON:11},
        Yon.ALT:{GozAksiyon.BEKLE:20,GozAksiyon.GIT:6,GozAksiyon.PATLA:9,GozAksiyon.SOLA_DON:11,GozAksiyon.SAGA_DON:11},
        Yon.SAG:{GozAksiyon.BEKLE:20,GozAksiyon.GIT:6,GozAksiyon.PATLA:11,GozAksiyon.SOLA_DON:11,GozAksiyon.SAGA_DON:11},
        Yon.UST:{GozAksiyon.BEKLE:20,GozAksiyon.GIT:6,GozAksiyon.PATLA:9,GozAksiyon.SOLA_DON:11,GozAksiyon.SAGA_DON:11}
    }
    _kare={#animasyonların içerdiği görseller. Yukle.AtlasDosya fonksiyonunda yüklenecek
        GozTip.GOZ1:{
            Yon.SOL:{GozAksiyon.BEKLE:[],GozAksiyon.GIT:[],GozAksiyon.PATLA:[],GozAksiyon.SOLA_DON:[],GozAksiyon.SAGA_DON:[]},
            Yon.ALT:{GozAksiyon.BEKLE:[],GozAksiyon.GIT:[],GozAksiyon.PATLA:[],GozAksiyon.SOLA_DON:[],GozAksiyon.SAGA_DON:[]},
            Yon.SAG:{GozAksiyon.BEKLE:[],GozAksiyon.GIT:[],GozAksiyon.PATLA:[],GozAksiyon.SOLA_DON:[],GozAksiyon.SAGA_DON:[]},
            Yon.UST:{GozAksiyon.BEKLE:[],GozAksiyon.GIT:[],GozAksiyon.PATLA:[],GozAksiyon.SOLA_DON:[],GozAksiyon.SAGA_DON:[]}
        },
        GozTip.GOZ2:{
            Yon.SOL:{GozAksiyon.BEKLE:[],GozAksiyon.GIT:[],GozAksiyon.PATLA:[],GozAksiyon.SOLA_DON:[],GozAksiyon.SAGA_DON:[]},
            Yon.ALT:{GozAksiyon.BEKLE:[],GozAksiyon.GIT:[],GozAksiyon.PATLA:[],GozAksiyon.SOLA_DON:[],GozAksiyon.SAGA_DON:[]},
            Yon.SAG:{GozAksiyon.BEKLE:[],GozAksiyon.GIT:[],GozAksiyon.PATLA:[],GozAksiyon.SOLA_DON:[],GozAksiyon.SAGA_DON:[]},
            Yon.UST:{GozAksiyon.BEKLE:[],GozAksiyon.GIT:[],GozAksiyon.PATLA:[],GozAksiyon.SOLA_DON:[],GozAksiyon.SAGA_DON:[]}
        },
        GozTip.GOZ3:{
            Yon.SOL:{GozAksiyon.BEKLE:[],GozAksiyon.GIT:[],GozAksiyon.PATLA:[],GozAksiyon.SOLA_DON:[],GozAksiyon.SAGA_DON:[]},
            Yon.ALT:{GozAksiyon.BEKLE:[],GozAksiyon.GIT:[],GozAksiyon.PATLA:[],GozAksiyon.SOLA_DON:[],GozAksiyon.SAGA_DON:[]},
            Yon.SAG:{GozAksiyon.BEKLE:[],GozAksiyon.GIT:[],GozAksiyon.PATLA:[],GozAksiyon.SOLA_DON:[],GozAksiyon.SAGA_DON:[]},
            Yon.UST:{GozAksiyon.BEKLE:[],GozAksiyon.GIT:[],GozAksiyon.PATLA:[],GozAksiyon.SOLA_DON:[],GozAksiyon.SAGA_DON:[]}
        },
        GozTip.GOZ4:{
            Yon.SOL:{GozAksiyon.BEKLE:[],GozAksiyon.GIT:[],GozAksiyon.PATLA:[],GozAksiyon.SOLA_DON:[],GozAksiyon.SAGA_DON:[]},
            Yon.ALT:{GozAksiyon.BEKLE:[],GozAksiyon.GIT:[],GozAksiyon.PATLA:[],GozAksiyon.SOLA_DON:[],GozAksiyon.SAGA_DON:[]},
            Yon.SAG:{GozAksiyon.BEKLE:[],GozAksiyon.GIT:[],GozAksiyon.PATLA:[],GozAksiyon.SOLA_DON:[],GozAksiyon.SAGA_DON:[]},
            Yon.UST:{GozAksiyon.BEKLE:[],GozAksiyon.GIT:[],GozAksiyon.PATLA:[],GozAksiyon.SOLA_DON:[],GozAksiyon.SAGA_DON:[]}
        }
        
    }
    _gecikme={GozAksiyon.BEKLE:2/60,GozAksiyon.GIT:2/60,GozAksiyon.PATLA:2/60,GozAksiyon.SOLA_DON:2/60,GozAksiyon.SAGA_DON:2/60}#minimum değer 3/60. Bunun altında bir değer verme

    _orijinalBoyut=563#genişlik,yükseklik aynı
    _boyutOran=1.5#hücre genişliğine oranı
    _atlasYuklendi=False # atlas dosyalarının yüklenip yğklenmediğini kontrol edeceğimiz değişken. Yüklendiğine True olacak
    _animasyonTekrar={GozAksiyon.BEKLE:1,GozAksiyon.GIT:3,GozAksiyon.PATLA:1,GozAksiyon.SOLA_DON:1,GozAksiyon.SAGA_DON:1} # Animasyon kaç kere çalışacak


    
    def __init__(self,tip,yon,**kwargs):
        super().__init__(**kwargs)
        self.__tip=(GozTip)(tip)
        self.__yon=(Yon)(yon)
        self.__aksiyon=None
        self.__yeniYon=None#yön değiştirilirken, animasyon yeni yöne değil, mevcut olana(self.__yon) göre çalıştırılıyor. Animasyon bittikten sonra self.__yon=self.__yeniYon olarak güncellenecek 
        
        self.__gitAdim={Yon.SAG: (0, 0),Yon.SOL: (0, 0),Yon.UST: (0, 0),Yon.ALT: (0, 0)}

        #self.allow_stretch=True
        #self.fit_mode='contain'
        self.size_hint=(None,None)

        self.__aksiyonDegistir(GozAksiyon.BEKLE)#ilk animasyonu başlat

    @classmethod
    def atlasDosya(cls, tip):
        return cls._atlasDosya[tip]
    @classmethod
    def gecikme(cls, aksiyon):
        return cls._gecikme[aksiyon]
    @classmethod
    def animasyonTekrar(cls, aksiyon):
        return cls._animasyonTekrar[aksiyon]
    @classmethod
    def kareAd(cls,aksiyon,yon):
        return cls._kareAd[yon][aksiyon]
    @classmethod
    def kareSayi(cls,aksiyon,yon):
        return cls._kareSayi[yon][aksiyon]
    @classmethod
    def kare(cls,numara,aksiyon,tip,yon):
        return cls._kare[tip][yon][aksiyon][numara]
    @classmethod
    def kareEkle(cls,hamKare,aksiyon,tip,yon):
        cls._kare[tip][yon][aksiyon].append(hamKare)
    @classmethod
    def animasyonSure(cls, aksiyon, yon):
        n = cls.kareSayi(aksiyon, yon)
        r = cls.animasyonTekrar(aksiyon)
        delay = cls.gecikme(aksiyon)
        return n * r * delay



    
    @property
    def tip(self):
        return self.__tip
    @property
    def yon(self):
        return self.__yon
        
    def bekle(self):
        self.__aksiyonDegistir(GozAksiyon.BEKLE)

    def solaDon(self):
        self.__aksiyonDegistir(GozAksiyon.SOLA_DON)
        self.__yeniYon=Yon.solaDon(self.__yon) #dönme animasyonu bittikten sonra self.__yon güncellenecek
                
    def sagaDon(self):
        self.__aksiyonDegistir(GozAksiyon.SAGA_DON)
        self.__yeniYon=Yon.sagaDon(self.__yon) #dönme animasyonu bittikten sonra self.__yon güncellenecek

    def git(self):
        self.__aksiyonDegistir(GozAksiyon.GIT)

    @property
    def aksiyon(self):
        return self.__aksiyon
    
    def __aksiyonDegistir(self,aksiyon):
        #bir aksiyon tamamlanmadan, diğer bir aksiyona geçilmek istenirse...
        if self.__aksiyon not in (None,GozAksiyon.BEKLE):
            return
            
        self.__aksiyon=aksiyon
        self._animasyonHazirlik()
    
    def _animasyonHazirlik(self):
        self.texture=GozImaj.kare(0,self.__aksiyon,self.__tip,self.__yon).texture#yeni aksiyonun, ilk karesi alınıyor. Aksiyon geçişinde, önceki durumun karesi kalmasın diye 
        self._kareSayac=0    
        self._animasyonBasladi=True    
        if self._animasyonSaat:
            self._animasyonSaat.cancel()
        self._animasyonSaat=Clock.schedule_interval(self._animasyonTikTak,GozImaj.gecikme(self.__aksiyon))

    
    def _animasyonTikTak(self,dt):
        self.texture=GozImaj.kare(self._kareSayac%(GozImaj.kareSayi(self.__aksiyon,self.__yon)),self.__aksiyon,self.__tip,self.__yon).texture
        self._kareSayac+=1

        if self.__aksiyon==GozAksiyon.GIT:
            dx,dy=self.__gitAdim[self.__yon]
            self.center_x+=dx
            self.center_y+=dy

        if self._kareSayac>=GozImaj.kareSayi(self.__aksiyon,self.__yon)*GozImaj.animasyonTekrar(self.__aksiyon):
            self._kareSayac=0
            self._animasyonTamamlandi=True
            if self.__aksiyon==GozAksiyon.GIT:
                pass
            elif self.__aksiyon==GozAksiyon.SOLA_DON or self.__aksiyon==GozAksiyon.SAGA_DON:
                self.__yon=self.__yeniYon
                
            self.__aksiyon=GozAksiyon.BEKLE
            self._animasyonHazirlik()

    def guncelleOlculer(self,hucreX,hucreY,hucreBoyut):#canvas içerisine çizilecek labirentin genişlik, yükseklik, x, y vs değerleri hesaplanıyor
        self.width=hucreBoyut*GozImaj.boyutOran()
        self.height=self.width

        self.konumla(hucreX,hucreY,hucreBoyut)

        gitAdimSag=hucreBoyut/(GozImaj.kareSayi(GozAksiyon.GIT,Yon.SAG)*GozImaj.animasyonTekrar(GozAksiyon.GIT))
        gitAdimSol=hucreBoyut/(GozImaj.kareSayi(GozAksiyon.GIT,Yon.SOL)*GozImaj.animasyonTekrar(GozAksiyon.GIT))
        gitAdimUst=hucreBoyut/(GozImaj.kareSayi(GozAksiyon.GIT,Yon.UST)*GozImaj.animasyonTekrar(GozAksiyon.GIT))
        gitAdimAlt=hucreBoyut/(GozImaj.kareSayi(GozAksiyon.GIT,Yon.ALT)*GozImaj.animasyonTekrar(GozAksiyon.GIT))

        self.__gitAdim={Yon.SAG: (gitAdimSag, 0),Yon.SOL: (-gitAdimSol, 0),Yon.UST: (0, gitAdimUst),Yon.ALT: (0, -gitAdimAlt)}

    def konumla(self,hucreX,hucreY,hucreBoyut):
        self.center_x=hucreX+hucreBoyut/2
        self.center_y=hucreY+hucreBoyut/2
                
#reseptörler, gözün neresinde bulunabilir
class ReseptorKonum(IntEnum):#sıralama SOL,ARKA,SAG,ON olmalı. Matematiksel işlemler yapılıyor    
    SOL=0   #Yon.SOL'a tekabül ediyor
    ARKA=1  #Yon.ALT'a tekabül ediyor
    SAG=2   #Yon.SAG'a tekabül ediyor
    ON=3    #Yon.UST'a tekabül ediyor

#Gözün reseptörleri
class Reseptor:
    def __init__(self,konumArka=DuvarDurum.KAPALI,konumSag=DuvarDurum.KAPALI, konumOn=DuvarDurum.KAPALI, konumSol=DuvarDurum.KAPALI):
        self.__konumIndis=ReseptorKonum(0)#reseptör; sırasıyla tüm konumları tarayacak, indis başlangıçta ilk konumda(SOL) olacak

        self.__deger={ReseptorKonum.ARKA:konumArka,
                        ReseptorKonum.SAG:konumSag,
                        ReseptorKonum.ON:konumOn,
                        ReseptorKonum.SOL:konumSol}       
    
    def __str__(self):
        return f"Sensör : Sol : {self.__deger[ReseptorKonum.SOL]}, Ön : {self.__deger[ReseptorKonum.ON]}, Sağ : {self.__deger[ReseptorKonum.SAG]}, Arka : {self.__deger[ReseptorKonum.ARKA]}"
    
    @property
    def konumIndis(self):
        return self.__konumIndis
    @property 
    def sol(self):
        return self.__deger[ReseptorKonum.SOL]
    @property 
    def sag(self):
        return self.__deger[ReseptorKonum.SAG]
    @property 
    def on(self):
        return self.__deger[ReseptorKonum.ON]
    @property 
    def arka(self):
        return self.__deger[ReseptorKonum.ARKA]

    def degerGuncelle(self,reseptorKonum,duvarDurum):
        self.__deger[reseptorKonum]=duvarDurum
    def konumIndisGuncelle(self):
        self.__konumIndis=(ReseptorKonum)((self.__konumIndis+1)%len(ReseptorKonum))
    
class Goz(ABC):
    def __init__(self,isim):
        self.__hafiza={} #değişken saklamak için
        self.__isim=isim
    
    @property
    def isim(self):
        return self.__isim
    def isimDegistir(self,isim):
        self.__isim=isim
    @property
    def solaDon(self):
        return Hareket.SOLA_DON
    @property
    def sagaDon(self):
        return Hareket.SAGA_DON
    @property
    def ileriGit(self):
        return Hareket.ILERI

    @abstractmethod
    def kararVer(self,reseptor):
        """
        Bu fonksiyon her adımda çağrılır.
        reseptor_verisi: {'on': Zemin.DUVAR, 'sol': Zemin.BOS, ...}
        Geriye Yon.ILERI, Yon.SAGA_DON veya Yon.SOLA_DON döndürmelidir.
        """
        # Varsayılan olarak hiçbir şey yapma (veya rastgele git)
        # Öğrenci burayı ezecek (override).
        #Bu metod soyuttur. Goz sınıfında içi boştur (pass).
        #Alt sınıflar (BenimRobotum) bunu doldurmak ZORUNDADIR.
        pass
 
class LabirentTip(IntEnum):
    KARE=0
    YATAY=1
    DIKEY=2
    def __str__(self):
        return f"Labirent Tipi : {self.name}"
    
    @staticmethod
    def belirle(satirSayi,sutunSayi):
        if satirSayi>sutunSayi:
            return LabirentTip.DIKEY
        elif sutunSayi>satirSayi:
            return LabirentTip.YATAY
        else:
            return LabirentTip.KARE

class Labirent:   
    def __init__(self,satirSayi,sutunSayi):
        #çizim ile ilgili özellikler
        self.__satirAnahtar="satir"
        self.__sutunAnahtar="sutun"
        self.__genislik=-1
        self.__yukseklik=-1
        self.__merkezX=-1
        self.__merkezY=-1
        self.__solUstX=-1
        self.__solUstY=-1
        self.__kenarlikRenk=(1,1,1,1)
        self.__kenarlikKalinlik=0
        self.__hucreKenarUzunluk=-1

        self.__satirSayi=satirSayi
        self.__sutunSayi=sutunSayi
        self.__tip=LabirentTip.belirle(self.__satirSayi,self.__sutunSayi)
        self.__baslangicSatirNumara=-1
        self.__baslangicSutunNumara=-1
        self.__bitisSatirNumara=-1
        self.__bitisSutunNumara=-1

        self.__rastgeleBaslangicBitisBelirle()

        self.__minimumCozumUzunlugu=self.__satirSayi*self.__sutunSayi*0.5
        self.__cozumYolu=[]
        self.__olustur()
        
        self.__hucreler=self.__olusturHucreler()
        
    @property
    def baslangicHucre(self):
        return self.__hucreler[self.__baslangicSatirNumara][self.__baslangicSutunNumara]
    @property
    def bitisHucre(self):
        return self.__hucreler[self.__bitisSatirNumara][self.__bitisSutunNumara]
    @property
    def hucreKenarUzunluk(self):
        return self.__hucreKenarUzunluk
    def hucre(self,satirNumara,sutunNumara):
        if satirNumara<0 or satirNumara>=self.__satirSayi or sutunNumara<0 or sutunNumara>=self.__sutunSayi:
            return None
        return self.__hucreler[satirNumara][sutunNumara]
    
    def komsuHucreler(self,hucre):

        komsuHucreler={Yon.SOL:None,Yon.ALT:None,Yon.SAG:None,Yon.UST:None,Hucre.sayiKey():0}
        if hucre.satirNumara+1<self.__satirSayi:#altında komşu var mı
            komsuHucreler[Yon.ALT]=self.__hucreler[hucre.satirNumara+1][hucre.sutunNumara]
            komsuHucreler[Hucre.sayiKey()]+=1
        
        if hucre.satirNumara-1>=0:#üstünde satir var mı
            komsuHucreler[Yon.UST]=self.__hucreler[hucre.satirNumara-1][hucre.sutunNumara]
            komsuHucreler[Hucre.sayiKey()]+=1
        
        if hucre.sutunNumara+1<self.__sutunSayi:#sağında komşu var mı
            komsuHucreler[Yon.SAG]=self.__hucreler[hucre.satirNumara][hucre.sutunNumara+1]
            komsuHucreler[Hucre.sayiKey()]+=1

        if hucre.sutunNumara-1>=0:#solunda komşu var mı
            komsuHucreler[Yon.SOL]=self.__hucreler[hucre.satirNumara][hucre.sutunNumara-1]
            komsuHucreler[Hucre.sayiKey()]+=1
        return komsuHucreler

    def duvar(self,hucre1,hucre2):
        if hucre1 is None or hucre2 is None:#Eğer satır ya da sutun numarası labirentin sınırları dışındaysa, KAPALI bir duvar dönsün 
            return Duvar()   
                
        if hucre1.satirNumara==hucre2.satirNumara:#aynı satırdaki hücreler arasındaki bir duvar ise
            if hucre2.sutunNumara<hucre1.sutunNumara:#hücre2 küçük indisli ise
                return self.__duvarlar[self.__satirAnahtar][hucre2.satirNumara][hucre2.sutunNumara]
            return self.__duvarlar[self.__satirAnahtar][hucre1.satirNumara][hucre1.sutunNumara]#hücre1 küçük indisli ise
        else:#aynı sütundaki hücreler arasındaki bir duvar ise
            if hucre2.satirNumara<hucre1.satirNumara:#hücre2 küçük indisli ise
                return self.__duvarlar[self.__sutunAnahtar][hucre2.sutunNumara][hucre2.satirNumara]    
            return self.__duvarlar[self.__sutunAnahtar][hucre1.sutunNumara][hucre1.satirNumara]#hücre1 küçük indisli ise

    def hucreXY(self,hucre):#konumu verilen hücreye, robotu çizebilmek için gerekli koordinatlar ve boyut        
        x=self.__solUstX+self.__hucreKenarUzunluk*hucre.sutunNumara+self.__kenarlikKalinlik+self.__hucreKenarUzunluk/2-self.__hucreKenarUzunluk/2        
        y=self.__solUstY-self.__hucreKenarUzunluk*(1+hucre.satirNumara)+self.__kenarlikKalinlik+self.__hucreKenarUzunluk/2-self.__hucreKenarUzunluk/2
        return (x,y)
        
    def __hucreTipKey(self,hucre):# hucrenin gozTip key (__tipBaslangicKey="baslangic",__tipBitisKey="bitis",__tipYolKey="yol") bilgisini döndürür
        if hucre==self.baslangicHucre:
            return Hucre.gozTipBaslangicKey()
        elif hucre==self.bitisHucre:
            return Hucre.gozTipBitisKey()
        else:
            return Hucre.gozTipYolKey()

    def ciz(self):
        Color(rgba=self.__kenarlikRenk)
        self.__cizCerceve(self.__genislik, self.__yukseklik, self.__merkezX, self.__merkezY)
        self.__cizDuvar(self.__solUstX, self.__solUstY,self.__hucreKenarUzunluk)

        hucreTip=Hucre.gozTip(Hucre.gozTipYolKey())
        #for hucre in self.__cozumYolu:
            #self.__boyaHucre(self.__solUstX, self.__solUstY,hucre,hucreTip[Hucre.gozTipUzunlukCarpanKey()],hucreTip[Hucre.gozTipRenkKey()])

        #hucreTip=Hucre.gozTip(Hucre.gozTipBaslangicKey())
        #self.__boyaHucre(self.__solUstX, self.__solUstY,Konum(self.__baslangicSatirNumara,self.__baslangicSutunNumara),hucreTip[Hucre.gozTipUzunlukCarpanKey()],hucreTip[Hucre.gozTipRenkKey()])
            
        hucreTip=Hucre.gozTip(Hucre.gozTipBitisKey())
        self.__boyaHucre(self.__solUstX, self.__solUstY,Konum(self.__bitisSatirNumara,self.__bitisSutunNumara),hucreTip[Hucre.gozTipUzunlukCarpanKey()],hucreTip[Hucre.gozTipRenkKey()])
           
    def guncelleOlculer(self,yarisAlaniX,yarisAlaniY,yarisAlaniGenislik,yarisAlaniYukseklik):#canvas içerisine çizilecek labirentin genişlik, yükseklik, x, y vs değerleri hesaplanıyor
        genislikOlcek=yarisAlaniGenislik/self.__sutunSayi
        yukseklikOlcek=yarisAlaniYukseklik/self.__satirSayi
        olcekFaktor=min(genislikOlcek,yukseklikOlcek)

        self.__genislik=self.__sutunSayi*olcekFaktor
        self.__yukseklik=self.__satirSayi*olcekFaktor

        self.__merkezX=yarisAlaniX+yarisAlaniGenislik/2
        self.__merkezY=yarisAlaniY+yarisAlaniYukseklik/2

        self.__solUstX=self.__merkezX - self.__genislik / 2
        self.__solUstY=self.__merkezY + self.__yukseklik / 2

        self.__kenarlikKalinlik=self.__genislik/300#self.__genislik/400
        self.__hucreKenarUzunluk=self.__genislik/self.__sutunSayi
    
    def __olustur(self):
         
        while(len(self.__cozumYolu)<self.__minimumCozumUzunlugu):
            #self.__butunDuvarlariKapat()
            #self.__butunOnHucrelerIsaretKaldir()

            self.__hucreler=self.__olusturOnHucreler()
            self.__duvarlar=self.__olusturDuvarlar()
            self.__cozumYolu=[]

            hucreYigin=[]
            hucreYigin.append(self.__hucreler[self.__baslangicSatirNumara][self.__baslangicSutunNumara])#ilk hücreyi yığına ekle
            #print("başlangıç :",len(self.__cozumYolu))
            while(not self.__butunOnHucrelerIsaretlendi()):
                hucre=hucreYigin[-1]#stack'in en üstündeki hücre
                hucre.isaretKoy()
                rastgeleKomsuHucre=self.__secRastgeleKomsuHucre(hucre)
                if rastgeleKomsuHucre:
                    rastgeleKomsuHucre.isaretKoy()
                    self.__acDuvar(hucre,rastgeleKomsuHucre)
                    hucreYigin.append(rastgeleKomsuHucre)
                    if rastgeleKomsuHucre.satirNumara==self.__bitisSatirNumara and rastgeleKomsuHucre.sutunNumara==self.__bitisSutunNumara:
                        #baslangicHucre=hucreYigin[0]
                        #bitisHucre=hucreYigin[0-1]
                        #print(f"buldu: {baslangicHucre.satirNumara},{baslangicHucre.sutunNumara} - {bitisHucre.satirNumara},{bitisHucre.sutunNumara}")
                        for hucre in hucreYigin:
                            self.__cozumYolu.append(Hucre(hucre.satirNumara,hucre.sutunNumara))
                else:
                    hucreYigin.pop()
        
            #print("bitiş : ",len(self.__cozumYolu))

    def __secRastgeleKomsuHucre(self,hucre):
        komsuHucreler=self.komsuHucreler(hucre)
        
        if komsuHucreler[Hucre.sayiKey()]==0:
            return None
        
        tumKomsuHucrelerIsaretli=True
        for yon in Yon:
            if komsuHucreler[yon]:
                if not komsuHucreler[yon].isaret:
                    tumKomsuHucrelerIsaretli=False
                    break
        
        if tumKomsuHucrelerIsaretli:
            return None
    
        while(True):
            rastgeleYon=random.choice(list(Yon))
            rastgeleKomsuHucre=komsuHucreler[rastgeleYon]
            if rastgeleKomsuHucre:
                if not rastgeleKomsuHucre.isaret:
                    return rastgeleKomsuHucre
        
    def __butunOnHucrelerIsaretlendi(self):
        for satirNumara in range(self.__satirSayi):
            for sutunNumara in range(self.__sutunSayi):
                if not self.__hucreler[satirNumara][sutunNumara].isaret:
                    return False
        return True
    def __butunOnHucrelerIsaretKaldir(self):
        for satirNumara in range(self.__satirSayi):
            for sutunNumara in range(self.__sutunSayi):
                self.__hucreler[satirNumara][sutunNumara].isaretKaldir()
    
    def __olusturOnHucreler(self):
        onHucreler=[]
        for satirNumara in range(self.__satirSayi):
            satir=[]
            for sutunNumara in range(self.__sutunSayi):
                hucre=OnHucre(satirNumara,sutunNumara)
                satir.append(hucre)
            onHucreler.append(satir)
        return onHucreler
    
    def __olusturHucreler(self):#OnHucre nesnelerini, Hucre nesnelerine dönüştürür 
        hucreler=[]
        for satirNumara in range(self.__satirSayi):
            satir=[]
            for sutunNumara in range(self.__sutunSayi):
                onHucre=self.__hucreler[satirNumara][sutunNumara]
                hucre=Hucre(onHucre.satirNumara,onHucre.sutunNumara)
                satir.append(hucre)
            hucreler.append(satir)
        return hucreler
    
    def __olusturDuvarlar(self):
        duvarlar={self.__satirAnahtar:[],self.__sutunAnahtar:[]}
        #satırlarda bulunan duvarlar oluşturuluyor
        for satirNumara in range(self.__satirSayi):
            satirDuvarlar=[]
            for sutunNumara in range(self.__sutunSayi-1):
                duvar=Duvar()
                satirDuvarlar.append(duvar)
            duvarlar[self.__satirAnahtar].append(satirDuvarlar)

                
        #sutunlarda bulunan duvarlar oluşturuluyor
        for sutunNumara in range(self.__sutunSayi):
            sutunDuvarlar=[]
            for satirNumara in range(self.__satirSayi-1):
                duvar=Duvar()
                sutunDuvarlar.append(duvar)
            duvarlar[self.__sutunAnahtar].append(sutunDuvarlar)

        return duvarlar
    
    def __acDuvar(self,hucre1,hucre2):
        self.duvar(hucre1,hucre2).ac()

    def __butunDuvarlariKapat(self):
        #satırlarda bulunan duvarlar kapatılıyor
        for satirNumara in range(self.__satirSayi):
            for sutunNumara in range(self.__sutunSayi-1):
                self.__duvarlar[self.__satirAnahtar][satirNumara][sutunNumara].kapat()
                
        for sutunNumara in range(self.__sutunSayi):
            for satirNumara in range(self.__satirSayi-1):
                self.__duvarlar[self.__sutunAnahtar][sutunNumara][satirNumara].kapat()
    
    def __rastgeleBaslangicBitisBelirle(self):#labirentin başlangıç ve bitiş hücreleri rastgele belirleniyor
        if self.__tip==LabirentTip.KARE:
            labirentTip=random.choice([LabirentTip.YATAY,LabirentTip.DIKEY])
        else:
            labirentTip=self.__tip


        match labirentTip:
            case LabirentTip.YATAY:
                self.__baslangicSutunNumara=0
                self.__bitisSutunNumara=self.__sutunSayi-1
                self.__baslangicSatirNumara=random.randint(0,self.__satirSayi-1)
                self.__bitisSatirNumara=random.randint(0,self.__satirSayi-1)
            case LabirentTip.DIKEY:
                self.__baslangicSatirNumara=0
                self.__bitisSatirNumara=self.__satirSayi-1
                self.__baslangicSutunNumara=random.randint(0,self.__sutunSayi-1)
                self.__bitisSutunNumara=random.randint(0,self.__sutunSayi-1)

    def __cizCerceve(self,genislik,yukseklik,labirentMerkezX, labirentMerkezY):
        Line(close="True", width=self.__kenarlikKalinlik,rectangle=(labirentMerkezX - genislik / 2, labirentMerkezY - yukseklik / 2, genislik, yukseklik))
    
    def __cizDuvar(self,labirentSolUstX,labirentSolUstY,hucreKenarUzunluk):
        for satirNumara in range(self.__satirSayi):
            for sutunNumara in range(self.__sutunSayi-1):
                duvar=self.duvar(self.__hucreler[satirNumara][sutunNumara],self.__hucreler[satirNumara][sutunNumara+1])
                if duvar.durum==DuvarDurum.KAPALI:
                    x=labirentSolUstX+hucreKenarUzunluk*(sutunNumara+1)
                    y1=labirentSolUstY-hucreKenarUzunluk*satirNumara
                    y2=y1-hucreKenarUzunluk
                    Line(width=self.__kenarlikKalinlik,points=(x,y1,x,y2))

        for sutunNumara in range(self.__sutunSayi):
            for satirNumara in range(self.__satirSayi-1):
                duvar=self.duvar(self.__hucreler[satirNumara][sutunNumara],self.__hucreler[satirNumara+1][sutunNumara])
                if duvar.durum==DuvarDurum.KAPALI:
                    x1=labirentSolUstX+hucreKenarUzunluk*sutunNumara
                    y=labirentSolUstY-hucreKenarUzunluk*(satirNumara+1)
                    x2=x1+hucreKenarUzunluk
                    Line(width=self.__kenarlikKalinlik,points=(x1,y,x2,y))

    def __boyaHucre(self,labirentSolUstX,labirentSolUstY,konum,uzunlukCarpan,renk):
        Color(renk["r"],renk["g"],renk["b"],renk["a"])
        hucre=self.__hucreler[konum.satirNumara][konum.sutunNumara]

        x=labirentSolUstX+self.__hucreKenarUzunluk*hucre.sutunNumara+self.__kenarlikKalinlik+self.__hucreKenarUzunluk/2-uzunlukCarpan*self.__hucreKenarUzunluk/2
        y=labirentSolUstY-self.__hucreKenarUzunluk*(1+hucre.satirNumara)+self.__kenarlikKalinlik+self.__hucreKenarUzunluk/2-uzunlukCarpan*self.__hucreKenarUzunluk/2

        boyut=uzunlukCarpan*self.__hucreKenarUzunluk-2*self.__kenarlikKalinlik
        Ellipse(size=(boyut,boyut),pos=(x,y))
        
    #def __maksimumMesafe(self):#labirentin birbirlerine en uzak olan hücrelerin arasındaki mesafe
        #return self.__satirSayi-1+self.__sutunSayi-1
    
    #def __mesafeHesapla(self,satirNumara1,sutunNumara1,satirNumara2,sutunNumara2):
        #return abs(satirNumara1-satirNumara2)+abs(sutunNumara1-sutunNumara2)
