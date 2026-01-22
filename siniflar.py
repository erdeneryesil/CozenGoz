from enum import IntEnum
from abc import ABC, abstractmethod
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

#Sensörler, robotun neresinde bulunabilir
class ReseptorKonum(IntEnum):#sıralama SOL,ARKA,SAG,ON olmalı. Matematiksel işlemler yapılıyor    
    SOL=0   #Yon.SOL'a tekabül ediyor
    ARKA=1  #Yon.ALT'a tekabül ediyor
    SAG=2   #Yon.SAG'a tekabül ediyor
    ON=3    #Yon.UST'a tekabül ediyor

#Gözün reseptörleri
class Reseptor:
    def __init__(self,konumArka=DuvarDurum.KAPALI,konumSag=DuvarDurum.KAPALI, konumOn=DuvarDurum.KAPALI, konumSol=DuvarDurum.KAPALI):
        self.__deger={ReseptorKonum.ARKA.name:konumArka,
                        ReseptorKonum.SAG.name:konumSag,
                        ReseptorKonum.ON.name:konumOn,
                        ReseptorKonum.SOL.name:konumSol}
        
    
    def __str__(self):
        return f"Sensör : Sol : {self.__deger[ReseptorKonum.SOL.name]}, Ön : {self.__deger[ReseptorKonum.ON.name]}, Sağ : {self.__deger[ReseptorKonum.SAG.name]}, Arka : {self.__deger[ReseptorKonum.ARKA.name]}"
    
    @property
    def deger(self):
        return self.__deger
    
    @property 
    def sol(self):
        return self.__deger[ReseptorKonum.SOL.name]
    @property 
    def sag(self):
        return self.__deger[ReseptorKonum.SAG.name]
    @property 
    def on(self):
        return self.__deger[ReseptorKonum.ON.name]
    @property 
    def arka(self):
        return self.__deger[ReseptorKonum.ARKA.name]

class ReseptorAksiyon(IntEnum):
    ARANIYOR=0
    DUVAR_ACIK=1
    DUVAR_KAPALI=2

class ReseptorImaj(Image):
    __dizin="assets/reseptor"
    __atlasDosya="reseptor.atlas"

    __kareAd={ReseptorAksiyon.ARANIYOR:"reseptor-beyaz-",ReseptorAksiyon.DUVAR_ACIK:"reseptor-yesil-",ReseptorAksiyon.DUVAR_KAPALI:"reseptor-kirmizi"}
    __kareSayi=13
    __kare={ReseptorAksiyon.ARANIYOR:[],ReseptorAksiyon.DUVAR_ACIK:[],ReseptorAksiyon.DUVAR_KAPALI:[]}
            
    __gecikme={ReseptorAksiyon.ARANIYOR:5/60,ReseptorAksiyon.DUVAR_ACIK:5/60,ReseptorAksiyon.DUVAR_KAPALI:5/60}

    __orijinalBoyut=340
    __boyutOran=1#hücre genişliğine oranı
    __atlasYuklendi=False # atlas dosyasının yüklenip yüklenmediğini kontrol edeceğimiz değişken. Yüklendiğine True olacak
    __animasyonTekrar={ReseptorAksiyon.ARANIYOR:1,ReseptorAksiyon.DUVAR_ACIK:1,ReseptorAksiyon.DUVAR_KAPALI:1} # Animasyon kaç kere çalışacak

    @staticmethod
    def dizin():
        return ReseptorImaj.__dizin
    @staticmethod
    def atlasDosya():
        return ReseptorImaj.__atlasDosya
    @staticmethod
    def kareSayi():
        return ReseptorImaj.__kareSayi
    @staticmethod
    def kareAd(reseptorAksiyon):
        Denetle.TurHata(reseptorAksiyon,ReseptorAksiyon)
        return ReseptorImaj.__kareAd[reseptorAksiyon]
    @staticmethod
    def kare(reseptorAksiyon,numara):
        Denetle.TurHata(reseptorAksiyon,ReseptorAksiyon)
        return ReseptorImaj.__kare[reseptorAksiyon][numara]
    @staticmethod
    def kareEkle(reseptorAksiyon,kare):
        Denetle.TurHata(reseptorAksiyon,ReseptorAksiyon)
        return ReseptorImaj.__kare[reseptorAksiyon].append(kare)
    @staticmethod
    def gecikme(reseptorAksiyon):
        Denetle.TurHata(reseptorAksiyon,ReseptorAksiyon)
        return ReseptorImaj.__gecikme[reseptorAksiyon]
    @staticmethod
    def orijinalBoyut():
        return ReseptorImaj.__orijinalBoyut
    @staticmethod
    def boyutOran():
        return ReseptorImaj.__boyutOran
    @staticmethod
    def atlasYuklendi():
        return ReseptorImaj.__atlasYuklendi
    @staticmethod
    def atlasYuklendiGuncelle(deger):
        ReseptorImaj.__atlasYuklendi=deger
    @staticmethod
    def animasyonTekrar(reseptorAksiyon):
        Denetle.TurHata(reseptorAksiyon,ReseptorAksiyon)
        return ReseptorImaj.__animasyonTekrar[reseptorAksiyon]

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.__reseptorAksiyon=None
        self.__kareSayac=0
        self.__animasyonSaat=None
        #self.__aksiyonBitti=False

        #self.allow_stretch=True
        #self.fit_mode='contain'
        self.size_hint=(None,None)
    
    #@property
    #def reseptorAksiyon(self):
        #return self.__reseptorAksiyon

    #@property
    #def aksiyonBitti(self):
        #return self.__aksiyonBitti
    
    #def aksiyonBittiSifirla(self):
       #self.__aksiyonBitti=False 

    def __reseptorAksiyonDegistir(self,reseptorAksiyon):
        self.__reseptorAksiyon=reseptorAksiyon
        self.__animasyonHazirlik()
    
    def __animasyonHazirlik(self):
        self.texture=ReseptorImaj.kare(self.__reseptorAksiyon,0).texture#yeni reseptorAksiyonun, ilk karesi alınıyor. Aksiyon geçişinde, önceki durumun karesi kalmasın diye 
        self.__kareSayac=0
        if self.__animasyonSaat:
            self.__animasyonSaat.cancel()
        self.__animasyonSaat=Clock.schedule_interval(self.animasyonTikTak,ReseptorImaj.gecikme(self.__reseptorAksiyon))


        '''self.texture=Nine.kare[self.durum][0].texture#yeni durumun, ilk karesi alınıyor. Durum geçişinde, önceki durumun karesi kalmasın diye 
        self.BoyutAyarla()
        self.KonumAyarla()

        if self.durum=='tokmakla':
            self.tokmakVurdu=False
        elif self.durum=='ateş et':
            self.mermiAdet-=1
            self.silahGosterge.MermiAdetDegistir(self.mermiAdet)
            if self.mermiAdet==0:
                self.tufekVar=False
                self.silahGosterge.DurumDegistir('tokmak')
        elif self.durum.split('-')[0]=='zıpla':#eğer durum, zıpla-tüfekli ya da zıpla-tüfeksiz ise
            self.ziplaHiz=self.ziplaHizOrijinal[self.durum]


        self.kareSayac=0
        if self.animasyonSaat:
            self.animasyonSaat.cancel()
        self.animasyonSaat=Clock.schedule_interval(self.animasyonTikTak,Nine.gecikme[self.durum])'''
    
    def animasyonTikTak(self,dt):
        self.texture=ReseptorImaj.kare(self.__reseptorAksiyon,self.__kareSayac%(ReseptorImaj.kareSayi())).texture
        self.__kareSayac+=1

        if self.__reseptorAksiyon==GozAksiyon.GIT:
            dx,dy=self.__gitAdim[self.__yon]
            self.x+=dx#0.7 denemek için. GIT aksiyonu bittiğinde, tam hücreniin ortasına konumlandırılsın.
            self.y+=dy

        if self.__kareSayac>=ReseptorImaj.kareSayi(self.__yon,self.__reseptorAksiyon)*ReseptorImaj.animasyonTekrar(self.__reseptorAksiyon):
            self.__kareSayac=0
            #self.__aksiyonBitti=True
            if self.__reseptorAksiyon==GozAksiyon.GIT:
                pass
            elif self.__reseptorAksiyon==GozAksiyon.SOLA_DON or self.__reseptorAksiyon==GozAksiyon.SAGA_DON:
                self.__yon=self.__yeniYon
                
            self.__reseptorAksiyon=GozAksiyon.BEKLE
            self.__animasyonHazirlik()


        '''if self.durum!='gidiş':
            self.texture=Mermi.kare[self.durum][self.kareSayac].texture
            self.kareSayac+=1
        if Mermi.kareSayisi[self.durum]>1 and self.kareSayac+1==Mermi.kareSayisi[self.durum]: #'gidiş' gibi tek resimli durumlarda animasyonun bigozTip bitmediğini kontrol etmeye gerek yok 
            if self.durum=='patlama':
                self.DurumDegistir('gidiş')
            elif self.durum=='vurma':
                self.sil=True
                self.animasyonSaat.cancel()'''

    def guncelleOlculer(self,hucreX,hucreY,hucreBoyut):#canvas içerisine çizilecek labirentin genişlik, yükseklik, x, y vs değerleri hesaplanıyor
        self.width=hucreBoyut*GozImaj.genislikOran()
        self.height=self.width*GozImaj.orijinalYukseklik()/GozImaj.orijinalGenislik()
        self.konumla(hucreX,hucreY,hucreBoyut)

        gitAdimSag=(int)(hucreBoyut/(GozImaj.kareSayi(Yon.SAG,GozAksiyon.GIT)*GozImaj.animasyonTekrar(GozAksiyon.GIT)))
        gitAdimSol=(int)(hucreBoyut/(GozImaj.kareSayi(Yon.SOL,GozAksiyon.GIT)*GozImaj.animasyonTekrar(GozAksiyon.GIT)))
        gitAdimUst=(int)(hucreBoyut/(GozImaj.kareSayi(Yon.UST,GozAksiyon.GIT)*GozImaj.animasyonTekrar(GozAksiyon.GIT)))
        gitAdimAlt=(int)(hucreBoyut/(GozImaj.kareSayi(Yon.ALT,GozAksiyon.GIT)*GozImaj.animasyonTekrar(GozAksiyon.GIT)))

        self.__gitAdim={Yon.SAG: (gitAdimSag, 0),Yon.SOL: (-gitAdimSol, 0),Yon.UST: (0, gitAdimUst),Yon.ALT: (0, -gitAdimAlt)}
    
    def konumla(self,hucreX,hucreY,hucreBoyut):
        self.center_x=hucreX+hucreBoyut/2
        self.center_y=hucreY+hucreBoyut/2


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
    __tip={__tipBaslangicKey:{__tipRenkKey:{"r":245/255,"g":73/255,"b":39/255,"a":1},__tipUzunlukCarpanKey:1},__tipBitisKey:{__tipRenkKey:{"r":88/255,"g":219/255,"b":88/255,"a":1},__tipUzunlukCarpanKey:1},__tipYolKey:{__tipRenkKey:{"r":255/255,"g":247/255,"b":173/255,"a":0.5},__tipUzunlukCarpanKey:0.8}}
    __xKey="x"
    __yKey="y"
    __boyutKey="boyut"

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
    @staticmethod
    def xKey():
        return Hucre.__xKey
    @staticmethod
    def yKey():
        return Hucre.__yKey
    @staticmethod
    def boyutKey():
        return Hucre.__boyutKey

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

class Yukle:
    @staticmethod
    def AtlasDosya(Sinif,gozTip=None):
        Denetle.TurHata(gozTip,GozTip)
        if gozTip:
            atlasDosyaAd=Sinif.dizin()+'/'+Sinif.atlasDosya(gozTip)
            atlasDosya=Atlas(atlasDosyaAd)
        else:
            pass
 
        if gozTip:Sinif.atlasYuklendiGuncelle(gozTip,False)
        #else:Sinif.atlasYuklendiGuncelle=False

        if gozTip:
            for yon in Yon:
                for aksiyon in GozAksiyon:
                    kareAdNumarasiz=Sinif.kareAd(yon,aksiyon)
                    for kareNumara in range(Sinif.kareSayi(yon,aksiyon)):
                        kareAd=kareAdNumarasiz+str(kareNumara)
                        hamKare=CoreImage(atlasDosya[kareAd])#.atlas dosyası içindeki, resimler teker teker ele alınıyor
                        Sinif.kareEkle(gozTip,yon,aksiyon,hamKare)
        else:pass

        if gozTip:Sinif.atlasYuklendiGuncelle(gozTip,True)
        #else:Sinif.atlasYuklendi=True
        
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


class GozImaj(Image):#animasyon ve çizim işlemlerinin yürütüleceğin sınıf
    __dizin="assets/goz"

    __atlasDosya={
        GozTip.GOZ1:"goz1.atlas",
        GozTip.GOZ2:"goz2.atlas",
        GozTip.GOZ3:"goz3.atlas",
        GozTip.GOZ4:"goz4.atlas"
    }
    __kareAd={
        Yon.SOL:{GozAksiyon.BEKLE:"sol-bekle-",GozAksiyon.GIT:"sol-git-",GozAksiyon.PATLA:"sol-patla-",GozAksiyon.SOLA_DON:"sol-sola-don-",GozAksiyon.SAGA_DON:"sol-saga-don-"},
        Yon.ALT:{GozAksiyon.BEKLE:"alt-bekle-",GozAksiyon.GIT:"alt-git-",GozAksiyon.PATLA:"alt-patla-",GozAksiyon.SOLA_DON:"alt-sola-don-",GozAksiyon.SAGA_DON:"alt-saga-don-"},
        Yon.SAG:{GozAksiyon.BEKLE:"sag-bekle-",GozAksiyon.GIT:"sag-git-",GozAksiyon.PATLA:"sag-patla-",GozAksiyon.SOLA_DON:"sag-sola-don-",GozAksiyon.SAGA_DON:"sag-saga-don-"},
        Yon.UST:{GozAksiyon.BEKLE:"ust-bekle-",GozAksiyon.GIT:"ust-git-",GozAksiyon.PATLA:"ust-patla-",GozAksiyon.SOLA_DON:"ust-sola-don-",GozAksiyon.SAGA_DON:"ust-saga-don-"},
    }
    __kareSayi={#animasyonların içerdiği resim sayısı.
        Yon.SOL:{GozAksiyon.BEKLE:20,GozAksiyon.GIT:6,GozAksiyon.PATLA:11,GozAksiyon.SOLA_DON:11,GozAksiyon.SAGA_DON:11},
        Yon.ALT:{GozAksiyon.BEKLE:20,GozAksiyon.GIT:6,GozAksiyon.PATLA:9,GozAksiyon.SOLA_DON:11,GozAksiyon.SAGA_DON:11},
        Yon.SAG:{GozAksiyon.BEKLE:20,GozAksiyon.GIT:6,GozAksiyon.PATLA:11,GozAksiyon.SOLA_DON:11,GozAksiyon.SAGA_DON:11},
        Yon.UST:{GozAksiyon.BEKLE:20,GozAksiyon.GIT:6,GozAksiyon.PATLA:9,GozAksiyon.SOLA_DON:11,GozAksiyon.SAGA_DON:11}
    }
    __kare={#animasyonların içerdiği görseller. Yukle.AtlasDosya fonksiyonunda yüklenecek
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
    __gecikme={GozAksiyon.BEKLE:1/60,GozAksiyon.GIT:1/60,GozAksiyon.PATLA:1/60,GozAksiyon.SOLA_DON:1/60,GozAksiyon.SAGA_DON:1/60}

    __orijinalBoyut=563#genişlik,yükseklik aynı
    __boyutOran=1.5#hücre genişliğine oranı
    __atlasYuklendi={GozTip.GOZ1:False,GozTip.GOZ2:False,GozTip.GOZ3:False,GozTip.GOZ4:False} # atlas dosyalarının yüklenip yğklenmediğini kontrol edeceğimiz değişken. Yüklendiğine True olacak
    __animasyonTekrar={GozAksiyon.BEKLE:1,GozAksiyon.GIT:3,GozAksiyon.PATLA:1,GozAksiyon.SOLA_DON:1,GozAksiyon.SAGA_DON:1} # Animasyon kaç kere çalışacak

    @staticmethod
    def dizin():
        return GozImaj.__dizin
    @staticmethod
    def atlasDosya(tip):
        Denetle.TurHata(tip,GozTip)
        return GozImaj.__atlasDosya[tip]
    @staticmethod
    def kareSayi(yon,aksiyon):
        Denetle.TurHata(yon,Yon)
        Denetle.TurHata(aksiyon,GozAksiyon)
        return GozImaj.__kareSayi[yon][aksiyon]
    @staticmethod
    def kareAd(yon,aksiyon):
        Denetle.TurHata(yon,Yon)
        Denetle.TurHata(aksiyon,GozAksiyon)
        return GozImaj.__kareAd[yon][aksiyon]
    @staticmethod
    def kare(tip,yon,aksiyon,numara):
        Denetle.TurHata(tip,GozTip)
        Denetle.TurHata(yon,Yon)
        Denetle.TurHata(aksiyon,GozAksiyon)
        return GozImaj.__kare[tip][yon][aksiyon][numara]
    @staticmethod
    def kareEkle(tip,yon,aksiyon,kare):
        Denetle.TurHata(tip,GozTip)
        Denetle.TurHata(yon,Yon)
        Denetle.TurHata(aksiyon,GozAksiyon)
        return GozImaj.__kare[tip][yon][aksiyon].append(kare)
    @staticmethod
    def gecikme(aksiyon):
        Denetle.TurHata(aksiyon,GozAksiyon)
        return GozImaj.__gecikme[aksiyon]
    @staticmethod
    def orijinalBoyut():
        return GozImaj.__orijinalBoyut
    @staticmethod
    def boyutOran():
        return GozImaj.__boyutOran
    @staticmethod
    def atlasYuklendi(tip):
        Denetle.TurHata(tip,GozTip)
        return GozImaj.__atlasYuklendi[tip.name]
    @staticmethod
    def atlasYuklendiGuncelle(tip,deger):
        Denetle.TurHata(tip,GozTip)
        GozImaj.__atlasYuklendi[tip]=deger
    @staticmethod
    def animasyonTekrar(aksiyon):
        Denetle.TurHata(aksiyon,GozAksiyon)
        return GozImaj.__animasyonTekrar[aksiyon]
    
    def __init__(self,tip,yon,**kwargs):
        super().__init__(**kwargs)
        self.__tip=(GozTip)(tip)
        self.__yon=(Yon)(yon)
        self.__yeniYon=None#yön değiştirilirken, animasyon yeni yöne değil, mevcut olana(self.__yon) göre çalıştırılıyor. Animasyon bittikten sonra self.__yon=self.__yeniYon olarak güncellenecek 
        self.__aksiyon=GozAksiyon.BEKLE
        self.__kareSayac=0
        self.__animasyonSaat=None
        self.__gitAdim={Yon.SAG: (0, 0),Yon.SOL: (0, 0),Yon.UST: (0, 0),Yon.ALT: (0, 0)}
        self.__aksiyonBitti=False

        #self.allow_stretch=True
        #self.fit_mode='contain'
        self.size_hint=(None,None)

        self.__aksiyonDegistir(self.__aksiyon)#ilk animasyonu başlat
        #self.texture=GozImaj.kare(self.__tip,self.__yon,self.__aksiyon,0).texture

    @property
    def tip(self):
        return self.__tip
    @property
    def aksiyon(self):
        return self.__aksiyon
    @property
    def yon(self):
        return self.__yon

    @property
    def aksiyonBitti(self):
        return self.__aksiyonBitti
    
    def aksiyonBittiSifirla(self):
       self.__aksiyonBitti=False 
    
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

    def __aksiyonDegistir(self,aksiyon):
        #bir aksiyon tamamlanmadan, diğer bir aksiyona geçilmek istenirse...
        if self.__aksiyon!=GozAksiyon.BEKLE:
            return
            
        self.__aksiyon=aksiyon
        self.__animasyonHazirlik()
    
    def __animasyonHazirlik(self):
        self.texture=GozImaj.kare(self.__tip,self.__yon,self.__aksiyon,0).texture#yeni aksiyonun, ilk karesi alınıyor. Aksiyon geçişinde, önceki durumun karesi kalmasın diye 
        self.__kareSayac=0
        if self.__animasyonSaat:
            self.__animasyonSaat.cancel()
        self.__animasyonSaat=Clock.schedule_interval(self.animasyonTikTak,GozImaj.gecikme(self.__aksiyon))


        '''self.texture=Nine.kare[self.durum][0].texture#yeni durumun, ilk karesi alınıyor. Durum geçişinde, önceki durumun karesi kalmasın diye 
        self.BoyutAyarla()
        self.KonumAyarla()

        if self.durum=='tokmakla':
            self.tokmakVurdu=False
        elif self.durum=='ateş et':
            self.mermiAdet-=1
            self.silahGosterge.MermiAdetDegistir(self.mermiAdet)
            if self.mermiAdet==0:
                self.tufekVar=False
                self.silahGosterge.DurumDegistir('tokmak')
        elif self.durum.split('-')[0]=='zıpla':#eğer durum, zıpla-tüfekli ya da zıpla-tüfeksiz ise
            self.ziplaHiz=self.ziplaHizOrijinal[self.durum]


        self.kareSayac=0
        if self.animasyonSaat:
            self.animasyonSaat.cancel()
        self.animasyonSaat=Clock.schedule_interval(self.animasyonTikTak,Nine.gecikme[self.durum])'''
    
    def animasyonTikTak(self,dt):
        self.texture=GozImaj.kare(self.__tip,self.__yon,self.__aksiyon,self.__kareSayac%(GozImaj.kareSayi(self.__yon,self.__aksiyon))).texture
        self.__kareSayac+=1

        if self.__aksiyon==GozAksiyon.GIT:
            dx,dy=self.__gitAdim[self.__yon]
            self.center_x+=dx
            self.center_y+=dy

        if self.__kareSayac>=GozImaj.kareSayi(self.__yon,self.__aksiyon)*GozImaj.animasyonTekrar(self.__aksiyon):
            self.__kareSayac=0
            self.__aksiyonBitti=True
            if self.__aksiyon==GozAksiyon.GIT:
                pass
            elif self.__aksiyon==GozAksiyon.SOLA_DON or self.__aksiyon==GozAksiyon.SAGA_DON:
                self.__yon=self.__yeniYon
                
            self.__aksiyon=GozAksiyon.BEKLE
            self.__animasyonHazirlik()


        '''if self.durum!='gidiş':
            self.texture=Mermi.kare[self.durum][self.kareSayac].texture
            self.kareSayac+=1
        if Mermi.kareSayisi[self.durum]>1 and self.kareSayac+1==Mermi.kareSayisi[self.durum]: #'gidiş' gibi tek resimli durumlarda animasyonun tip bitmediğini kontrol etmeye gerek yok 
            if self.durum=='patlama':
                self.DurumDegistir('gidiş')
            elif self.durum=='vurma':
                self.sil=True
                self.animasyonSaat.cancel()'''

    def guncelleOlculer(self,hucreX,hucreY,hucreBoyut):#canvas içerisine çizilecek labirentin genişlik, yükseklik, x, y vs değerleri hesaplanıyor
        self.width=hucreBoyut*GozImaj.boyutOran()
        self.height=self.width

        self.konumla(hucreX,hucreY,hucreBoyut)

        gitAdimSag=hucreBoyut/(GozImaj.kareSayi(Yon.SAG,GozAksiyon.GIT)*GozImaj.animasyonTekrar(GozAksiyon.GIT))
        gitAdimSol=hucreBoyut/(GozImaj.kareSayi(Yon.SOL,GozAksiyon.GIT)*GozImaj.animasyonTekrar(GozAksiyon.GIT))
        gitAdimUst=hucreBoyut/(GozImaj.kareSayi(Yon.UST,GozAksiyon.GIT)*GozImaj.animasyonTekrar(GozAksiyon.GIT))
        gitAdimAlt=hucreBoyut/(GozImaj.kareSayi(Yon.ALT,GozAksiyon.GIT)*GozImaj.animasyonTekrar(GozAksiyon.GIT))

        self.__gitAdim={Yon.SAG: (gitAdimSag, 0),Yon.SOL: (-gitAdimSol, 0),Yon.UST: (0, gitAdimUst),Yon.ALT: (0, -gitAdimAlt)}

    
    def konumla(self,hucreX,hucreY,hucreBoyut):
        self.center_x=hucreX+hucreBoyut/2
        self.center_y=hucreY+hucreBoyut/2


        

        
        

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

        

        #self.__hucreler=self.__olusturOnHucreler() #olustur metodunda oluşturuluyor
        #self.__duvarlar=self.__olusturDuvarlar() #olustur metodunda oluşturuluyor

        self.__rastgeleBaslangicBitisBelirle()

        self.__minimumCozumUzunlugu=self.__satirSayi*self.__sutunSayi*0.5
        self.__cozumYolu=[]
        self.__olustur()
        
        #from pympler.asizeof import asizeof

        #print(asizeof(self.__hucreler[0][0])*self.__satirSayi*self.__sutunSayi/1024)
        self.__hucreler=self.__olusturHucreler()
        #print(asizeof(self.__hucreler[0][0])*self.__satirSayi*self.__sutunSayi/1024)
    
    def reseptorGonder(self,yon,konum):
        deger={ReseptorKonum.ARKA.name:DuvarDurum.KAPALI,ReseptorKonum.SAG.name:DuvarDurum.KAPALI, ReseptorKonum.ON.name:DuvarDurum.KAPALI, ReseptorKonum.SOL.name:DuvarDurum.KAPALI}
        komsuHucreler=self.komsuHucreler(konum)
    
        yonFark=yon-Yon.baslangic()#Robotun başlangıç yönü Yon.UST, eğer farklı bir yöne dönmüşse, bu yön ile Yon.UST arasındaki fark
        for robotYon in Yon:
            gercekYon=Yon((robotYon+yonFark)%len(Yon)).name
            if komsuHucreler[gercekYon]:
                deger[ReseptorKonum(robotYon).name]=self.duvar(konum,komsuHucreler[gercekYon]).durum
            else:
                deger[ReseptorKonum(robotYon).name]=DuvarDurum.KAPALI

        return Reseptor(deger[ReseptorKonum.ARKA.name],deger[ReseptorKonum.SAG.name],deger[ReseptorKonum.ON.name],deger[ReseptorKonum.SOL.name])

    #@property
    #def satirSayi(self):
        #return self.__satirSayi
    #@property
    #def sutunSayi(self):
        #return self.__sutunSayi
    
    @property
    def baslangicHucre(self):
        return self.__hucreler[self.__baslangicSatirNumara][self.__baslangicSutunNumara]

    @property
    def bitisHucre(self):
        return self.__hucreler[self.__bitisSatirNumara][self.__bitisSutunNumara]
    
    def hucre(self,satirNumara,sutunNumara):
        return self.__hucreler[satirNumara][sutunNumara]
    
    def komsuHucreler(self,hucre):

        komsuHucreler={Yon.SOL.name:None,Yon.ALT.name:None,Yon.SAG.name:None,Yon.UST.name:None,Hucre.sayiKey():0}
        if hucre.satirNumara+1<self.__satirSayi:#altında komşu var mı
            komsuHucreler[Yon.ALT.name]=self.__hucreler[hucre.satirNumara+1][hucre.sutunNumara]
            komsuHucreler[Hucre.sayiKey()]+=1
        
        if hucre.satirNumara-1>=0:#üstünde satir var mı
            komsuHucreler[Yon.UST.name]=self.__hucreler[hucre.satirNumara-1][hucre.sutunNumara]
            komsuHucreler[Hucre.sayiKey()]+=1
        
        if hucre.sutunNumara+1<self.__sutunSayi:#sağında komşu var mı
            komsuHucreler[Yon.SAG.name]=self.__hucreler[hucre.satirNumara][hucre.sutunNumara+1]
            komsuHucreler[Hucre.sayiKey()]+=1

        if hucre.sutunNumara-1>=0:#solunda komşu var mı
            komsuHucreler[Yon.SOL.name]=self.__hucreler[hucre.satirNumara][hucre.sutunNumara-1]
            komsuHucreler[Hucre.sayiKey()]+=1
        return komsuHucreler

    def duvar(self,hucre1,hucre2):
        satirUygunDegil = (hucre1.satirNumara<0 or hucre1.satirNumara>=self.__satirSayi) or ((hucre2.satirNumara<0 or hucre2.satirNumara>=self.__satirSayi))
        sutunUygunDegil = (hucre1.sutunNumara<0 or hucre1.sutunNumara>=self.__sutunSayi) or ((hucre2.sutunNumara<0 or hucre2.sutunNumara>=self.__sutunSayi))

        if satirUygunDegil or sutunUygunDegil:#Eğer satır ya da sutun numarası labirentin sınırları dışındaysa, KAPALI bir duvar dönsün 
            return Duvar()   
        
        if hucre1.satirNumara==hucre2.satirNumara:#aynı satırdaki hücreler arasındaki bir duvar ise
            if hucre2.sutunNumara<hucre1.sutunNumara:#hücre2 küçük indisli ise
                return self.__duvarlar[self.__satirAnahtar][hucre2.satirNumara][hucre2.sutunNumara]
            return self.__duvarlar[self.__satirAnahtar][hucre1.satirNumara][hucre1.sutunNumara]#hücre1 küçük indisli ise
        else:#aynı sütundaki hücreler arasındaki bir duvar ise
            if hucre2.satirNumara<hucre1.satirNumara:#hücre2 küçük indisli ise
                return self.__duvarlar[self.__sutunAnahtar][hucre2.sutunNumara][hucre2.satirNumara]    
            return self.__duvarlar[self.__sutunAnahtar][hucre1.sutunNumara][hucre1.satirNumara]#hücre1 küçük indisli ise

    def hucreXYBoyut(self,hucre,yon):#konumu verilen hücreye, robotu çizebilmek için gerekli koordinatlar ve boyut
        hucreTipKey=self.__hucreTipKey(hucre)
        hucreTip=Hucre.gozTip(hucreTipKey)
        uzunlukCarpan=hucreTip[Hucre.gozTipUzunlukCarpanKey()]
        
        x=self.__solUstX+self.__hucreKenarUzunluk*hucre.sutunNumara+self.__kenarlikKalinlik+self.__hucreKenarUzunluk/2-uzunlukCarpan*self.__hucreKenarUzunluk/2
        y=self.__solUstY-self.__hucreKenarUzunluk*(1+hucre.satirNumara)+self.__kenarlikKalinlik+self.__hucreKenarUzunluk/2-uzunlukCarpan*self.__hucreKenarUzunluk/2

        boyut=uzunlukCarpan*self.__hucreKenarUzunluk-2*self.__kenarlikKalinlik

        #yonFark=yon-Yon.baslangic()#Robotun başlangıç yönü Yon.UST, eğer farklı bir yöne dönmüşse, bu yön ile Yon.UST arasındaki fark
        #aci=Yon.donusAci()*yonFark

        return {Hucre.xKey():x,Hucre.yKey():y,Hucre.boyutKey():boyut}
        
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

        self.__kenarlikKalinlik=self.__genislik/400
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
            if komsuHucreler[yon.name]:
                if not komsuHucreler[yon.name].isaret:
                    tumKomsuHucrelerIsaretli=False
                    break
        
        if tumKomsuHucrelerIsaretli:
            return None
    
        while(True):
            rastgeleYon=random.choice(list(Yon))
            rastgeleKomsuHucre=komsuHucreler[rastgeleYon.name]
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
