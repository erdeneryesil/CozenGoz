#KIVY PENCERE, DOSYA VE GRAFİK YÖNETİMİ


from abc import ABCMeta, abstractmethod

from kivy.uix.image import Image,CoreImage
from kivy.clock import Clock
from kivy.atlas import Atlas

from sabitler import GozTip,GozAksiyon,Yon,AcilirPencereTip,AcilirPencereDurum,AtlasYuklemeBilgi




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
