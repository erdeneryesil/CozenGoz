#DÜNYA VE ÇEVRE


from enum import IntEnum
import random
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.image import Image

from kivy.graphics import Color, Line, Ellipse, Fbo, RenderContext, Scale, Translate


from temel import Konum,Denetle
from sabitler import LabirentTip,DuvarDurum,Yon,YarisAnimasyon,GozTip,GozAksiyon,Hareket,Yon,DuvarDurum,ReseptorKonum,EkranSabit
from yarismaci import BenimGozum
from goz import Reseptor

from grafik_pencere_dosya import GozImaj,ReseptorImaj


class Hucre(Konum):
    #SABİTLER
    __TIP_BASLANGIC_KEY="baslangic"
    __TIP_BITIS_KEY="bitis"
    __TIP_YOL_KEY="yol"
    __TIP_RENK_KEY="renk"
    __TIP_UZUNLUK_CARPAN_KEY="uzunlukCarpan"
    __SAYI_KEY="sayı"
    __TIP={__TIP_BASLANGIC_KEY:{__TIP_RENK_KEY:{"r":245/255,"g":73/255,"b":39/255,"a":1},__TIP_UZUNLUK_CARPAN_KEY:1},__TIP_BITIS_KEY:{__TIP_RENK_KEY:{"r":219/255,"g":88/255,"b":88/255,"a":1},__TIP_UZUNLUK_CARPAN_KEY:1},__TIP_YOL_KEY:{__TIP_RENK_KEY:{"r":255/255,"g":247/255,"b":173/255,"a":0.5},__TIP_UZUNLUK_CARPAN_KEY:1.0}}

    @staticmethod
    def gozTipBaslangicKey():
        return Hucre.__TIP_BASLANGIC_KEY
    @staticmethod
    def gozTipBitisKey():
        return Hucre.__TIP_BITIS_KEY
    @staticmethod
    def gozTipYolKey():
        return Hucre.__TIP_YOL_KEY
    @staticmethod
    def gozTipRenkKey():
        return Hucre.__TIP_RENK_KEY
    @staticmethod
    def gozTipUzunlukCarpanKey():
        return Hucre.__TIP_UZUNLUK_CARPAN_KEY
    @staticmethod
    def sayiKey():
        return Hucre.__SAYI_KEY
    @staticmethod
    def gozTip(gozTipKey):
        return Hucre.__TIP[gozTipKey]




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

class Labirent:
    #SABİTLER
    __KENARLIK_RENK=(1,0,0,1)
    __MINIMUM_COZUM_UZUNLUGU_ORAN=0.5
    __SATIR_ANAHTAR="satir"
    __SUTUN_ANAHTAR="sutun"

    def __init__(self,satirSayi,sutunSayi):
        #çizim ile ilgili özellikler
        self.__kenarlikKalinlik=None
        self.__hucreKenarUzunluk=None
        self.__texture=None
        self.__imaj=None

        self.__satirSayi=satirSayi
        self.__sutunSayi=sutunSayi
        self.__TIP=LabirentTip.belirle(self.__satirSayi,self.__sutunSayi)
        self.__baslangicSatirNumara=None
        self.__baslangicSutunNumara=None
        self.__bitisSatirNumara=None
        self.__bitisSutunNumara=None

        self.__rastgeleBaslangicBitisBelirle()

        self.__minimumCozumUzunlugu=self.__satirSayi*self.__sutunSayi*Labirent.__MINIMUM_COZUM_UZUNLUGU_ORAN
        self.__cozumYolu=[]
        self.__olustur()
        
        self.__hucreler=self.__olusturHucreler()

        self.__texture=self.__textureOlustur()
        #self.__imaj = Image(allow_stretch=True, keep_ratio=True)
        self.__imaj = Image()
        self.__imaj.size_hint=(None,None)
        self.__imaj.texture = self.__texture

        self.__texture.save("labirent_sablonu.png")
        
    @property
    def baslangicHucre(self):
        return self.__hucreler[self.__baslangicSatirNumara][self.__baslangicSutunNumara]
    @property
    def bitisHucre(self):
        return self.__hucreler[self.__bitisSatirNumara][self.__bitisSutunNumara]
    @property
    def hucreKenarUzunluk(self):
        return self.__hucreKenarUzunluk
    @property
    def imaj(self):
        return self.__imaj
    
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
                return self.__duvarlar[Labirent.__SATIR_ANAHTAR][hucre2.satirNumara][hucre2.sutunNumara]
            return self.__duvarlar[Labirent.__SATIR_ANAHTAR][hucre1.satirNumara][hucre1.sutunNumara]#hücre1 küçük indisli ise
        else:#aynı sütundaki hücreler arasındaki bir duvar ise
            if hucre2.satirNumara<hucre1.satirNumara:#hücre2 küçük indisli ise
                return self.__duvarlar[Labirent.__SUTUN_ANAHTAR][hucre2.sutunNumara][hucre2.satirNumara]    
            return self.__duvarlar[Labirent.__SUTUN_ANAHTAR][hucre1.sutunNumara][hucre1.satirNumara]#hücre1 küçük indisli ise


    def hucreXY(self,hucre,saha):#konumu verilen hücreye, robotu çizebilmek için gerekli koordinatlar ve boyut
        genislik,yukseklik=self.__hesaplaGenislikYukseklik(saha.width,saha.height)
        solUstX,solUstY=self.__hesaplaSolUstXY(saha,genislik,yukseklik)
        x=solUstX+self.__hucreKenarUzunluk*hucre.sutunNumara+self.__kenarlikKalinlik+self.__hucreKenarUzunluk/2-self.__hucreKenarUzunluk/2        
        y=solUstY-self.__hucreKenarUzunluk*(1+hucre.satirNumara)+self.__kenarlikKalinlik+self.__hucreKenarUzunluk/2-self.__hucreKenarUzunluk/2
        return (x,y)
    
    def __hucreTipKey(self,hucre):# hucrenin gozTip key (__TIP_BASLANGIC_KEY="baslangic",__TIP_BITIS_KEY="bitis",__TIP_YOL_KEY="yol") bilgisini döndürür
        if hucre==self.baslangicHucre:
            return Hucre.gozTipBaslangicKey()
        elif hucre==self.bitisHucre:
            return Hucre.gozTipBitisKey()
        else:
            return Hucre.gozTipYolKey()

    def __textureOlustur(self):
        #labirent görselini, max boyutlara göre bir kez oluşturup, sonrasında boyutları ölçekleyeceğiz
        
        self.__kenarlikKalinlik=EkranSabit.maxSahaKenarlikKalinlik()

        canvasGenislik,canvasYukseklik=self.__hesaplaGenislikYukseklik(EkranSabit.maxSahaGenislik(),EkranSabit.maxSahaYukseklik())#labirentin çizileceği alanın genişlik ve yükseklik
        
        # alt-üst(2+2), sol-sağ(2+2) taraflardan kenarlık kalınlığının 2 katı kadar küçültme yapılacak
        kucultmeCarpan2Kenar=4
        kucultmeCarpan1Kenar=2
        #texture ait  genişlik ve yükseklik, canvas'a göre küçültülecek. Fakat bu küçültmenin oranı genişlik ve yüksekliğe göre aynı olmalı (*canvasYukseklik/canvasGenislik)
        textureGenislik=canvasGenislik-kucultmeCarpan2Kenar*self.__kenarlikKalinlik                                    #labirentin genişliği
        textureYukseklik=canvasYukseklik-kucultmeCarpan2Kenar*self.__kenarlikKalinlik*canvasYukseklik/canvasGenislik   #labirentin yüksekliği

        solUstX=kucultmeCarpan1Kenar*self.__kenarlikKalinlik
        solUstY=textureYukseklik+kucultmeCarpan1Kenar*self.__kenarlikKalinlik*canvasYukseklik/canvasGenislik 

        self.__hucreKenarUzunluk=self.__hesaplaHucreKenarUzunluk(textureGenislik,textureYukseklik)

        fbo = Fbo(size=(canvasGenislik, canvasYukseklik))

        # Kivy Fbo varsayılan olarak transparan gelebilir. Arka planı temizliyoruz.
        fbo.clear_buffer()

        # 2. Çizim komutlarını Fbo canvas'ına ekliyoruz
        with fbo:
            # Kenarlık rengi ve çerçeve çizimi
            textureX = solUstX
            textureY = kucultmeCarpan1Kenar*self.__kenarlikKalinlik*canvasYukseklik/canvasGenislik

            Color(rgba=Labirent.__KENARLIK_RENK)
            self.__cizCerceve(textureX,textureY,textureGenislik,textureYukseklik)

            # Duvarların çizimi
            self.__cizDuvar(solUstX,solUstY)
            
            # Çözüm yolu veya Başlangıç/Bitiş hücrelerinin boyanması
            hucreTip=Hucre.gozTip(Hucre.gozTipYolKey())
            for hucre in self.__cozumYolu:
                self.__boyaHucre(solUstX,solUstY,hucre,hucreTip[Hucre.gozTipUzunlukCarpanKey()],hucreTip[Hucre.gozTipRenkKey()])


            hucreTip=Hucre.gozTip(Hucre.gozTipBaslangicKey())
            self.__boyaHucre(solUstX,solUstY,Konum(self.__baslangicSatirNumara,self.__baslangicSutunNumara),hucreTip[Hucre.gozTipUzunlukCarpanKey()],hucreTip[Hucre.gozTipRenkKey()])
            
            hucreTip=Hucre.gozTip(Hucre.gozTipBitisKey())
            self.__boyaHucre(solUstX,solUstY,Konum(self.__bitisSatirNumara,self.__bitisSutunNumara),hucreTip[Hucre.gozTipUzunlukCarpanKey()],hucreTip[Hucre.gozTipRenkKey()])

        # 3. Fbo üzerindeki çizimleri ekrana yansıtılmaya hazır bir doku (texture) olarak çekiyoruz
        fbo.draw()
        return fbo.texture

    
    def __cizCerceve(self,x,y,genislik,yukseklik):        
        Line(close="True", width=self.__kenarlikKalinlik,rectangle=(x,y, genislik, yukseklik))

    def __cizDuvar(self,solUstX,solUstY):
        for satirNumara in range(self.__satirSayi):
            for sutunNumara in range(self.__sutunSayi-1):
                duvar=self.duvar(self.__hucreler[satirNumara][sutunNumara],self.__hucreler[satirNumara][sutunNumara+1])
                if duvar.durum==DuvarDurum.KAPALI:
                    x=solUstX+self.__hucreKenarUzunluk*(sutunNumara+1)
                    y1=solUstY-self.__hucreKenarUzunluk*satirNumara
                    y2=y1-self.__hucreKenarUzunluk
                    Line(width=self.__kenarlikKalinlik,points=(x,y1,x,y2))

        for sutunNumara in range(self.__sutunSayi):
            for satirNumara in range(self.__satirSayi-1):
                duvar=self.duvar(self.__hucreler[satirNumara][sutunNumara],self.__hucreler[satirNumara+1][sutunNumara])
                if duvar.durum==DuvarDurum.KAPALI:
                    x1=solUstX+self.__hucreKenarUzunluk*sutunNumara
                    y=solUstY-self.__hucreKenarUzunluk*(satirNumara+1)
                    x2=x1+self.__hucreKenarUzunluk
                    Line(width=self.__kenarlikKalinlik,points=(x1,y,x2,y))

    def __boyaHucre(self,solUstX,solUstY,konum,uzunlukCarpan,renk):
        Color(renk["r"],renk["g"],renk["b"],renk["a"])
        
        hucre=self.__hucreler[konum.satirNumara][konum.sutunNumara]

        x=solUstX+self.__hucreKenarUzunluk*hucre.sutunNumara+self.__kenarlikKalinlik+self.__hucreKenarUzunluk/2-uzunlukCarpan*self.__hucreKenarUzunluk/2
        y=solUstY-self.__hucreKenarUzunluk*(1+hucre.satirNumara)+self.__kenarlikKalinlik+self.__hucreKenarUzunluk/2-uzunlukCarpan*self.__hucreKenarUzunluk/2

        boyut=uzunlukCarpan*self.__hucreKenarUzunluk-2*self.__kenarlikKalinlik
        Ellipse(size=(boyut,boyut),pos=(x,y))


    def guncelleOlculer(self,saha):#canvas içerisine çizilecek labirentin genişlik, yükseklik, x, y vs değerleri hesaplanıyor        
        
        genislik,yukseklik=self.__hesaplaGenislikYukseklik(saha.width,saha.height)

        solUstX,solUstY=self.__hesaplaSolUstXY(saha,genislik,yukseklik)

        self.__kenarlikKalinlik=genislik/EkranSabit.labirentKenarlikKalinlikOran()
        self.__hucreKenarUzunluk=genislik/self.__sutunSayi
        self.__hucreKenarUzunluk=self.__hesaplaHucreKenarUzunluk(genislik,yukseklik)
        
        self.__imaj.size=(genislik,yukseklik)
        self.__imaj.pos=(solUstX,solUstY-yukseklik)

    def __hesaplaHucreKenarUzunluk(self,genislik,yukseklik):
        if self.__TIP==LabirentTip.YATAY:
            return genislik/self.__sutunSayi
        return yukseklik/self.__satirSayi
        
        
        

    def __hesaplaKenarlikKalinlik(self):
        pass

    def __hesaplaGenislikYukseklik(self,sahaGenislik,sahaYukseklik):
        genislikOlcek=sahaGenislik/self.__sutunSayi
        yukseklikOlcek=sahaYukseklik/self.__satirSayi
        olcekFaktor=min(genislikOlcek,yukseklikOlcek)

        return (self.__sutunSayi*olcekFaktor,self.__satirSayi*olcekFaktor)
    
    def __hesaplaSolUstXY(self,saha,labirentGenislik,labirentYukseklik):
        return (saha.x+saha.width/2-labirentGenislik/2,saha.y+saha.height/2 + labirentYukseklik / 2)
        

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
        duvarlar={Labirent.__SATIR_ANAHTAR:[],Labirent.__SUTUN_ANAHTAR:[]}
        #satırlarda bulunan duvarlar oluşturuluyor
        for satirNumara in range(self.__satirSayi):
            satirDuvarlar=[]
            for sutunNumara in range(self.__sutunSayi-1):
                duvar=Duvar()
                satirDuvarlar.append(duvar)
            duvarlar[Labirent.__SATIR_ANAHTAR].append(satirDuvarlar)

                
        #sutunlarda bulunan duvarlar oluşturuluyor
        for sutunNumara in range(self.__sutunSayi):
            sutunDuvarlar=[]
            for satirNumara in range(self.__satirSayi-1):
                duvar=Duvar()
                sutunDuvarlar.append(duvar)
            duvarlar[Labirent.__SUTUN_ANAHTAR].append(sutunDuvarlar)

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
                self.__duvarlar[Labirent.__SUTUN_ANAHTAR][sutunNumara][satirNumara].kapat()
    
    def __rastgeleBaslangicBitisBelirle(self):#labirentin başlangıç ve bitiş hücreleri rastgele belirleniyor
        if self.__TIP==LabirentTip.KARE:
            labirentTip=random.choice([LabirentTip.YATAY,LabirentTip.DIKEY])
        else:
            labirentTip=self.__TIP


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


        
    #def __maksimumMesafe(self):#labirentin birbirlerine en uzak olan hücrelerin arasındaki mesafe
        #return self.__satirSayi-1+self.__sutunSayi-1
    
    #def __mesafeHesapla(self,satirNumara1,sutunNumara1,satirNumara2,sutunNumara2):
        #return abs(satirNumara1-satirNumara2)+abs(sutunNumara1-sutunNumara2)

class Yarisma:
    def __init__(self,saha):
        self.__saha=saha # yarışmanın yapılacağı Widget nesnesi
        
        self.__yarismaSaat=None
        self.__labirent=None
        self.__gozHucre=None
        self.__goz=None
        self.__gozImaj=None
        self.__reseptor=None
        self.__reseptorImaj=None
        self.__reseptorGuncellendi=None
        
    def __baslangicIslemleri(self):

        self.__saha.bind(pos=self.guncelleOlculer, size=self.guncelleOlculer)
                
        self.__labirent=Labirent(5,5)
        goz1=BenimGozum("ROBOT1")
        self.__goz=goz1
        self.__gozImaj=GozImaj(GozTip.GOZ1,Yon.baslangic())

        self.__gozHucre=self.__labirent.baslangicHucre
        
        self.__reseptor=Reseptor()
        self.__reseptorImaj=ReseptorImaj()


        self.__saha.add_widget(self.__labirent.imaj)
        self.__saha.add_widget(self.__gozImaj)
        self.__saha.add_widget(self.__reseptorImaj)
        

        Clock.schedule_once(lambda dt: self.guncelleOlculer(self.__saha), 0) #pencere açılması tamamlandığında, boyutların güncellenmesi için
    
    def baslat(self):
        self.__baslangicIslemleri()

        self.__reseptorGuncellendi=False
        self.oyunBitti=False
        self.__gozHucre=self.__labirent.baslangicHucre
        self.__gozImaj.bekle()

        #animasyonSure=GozImaj.animasyonSure(GozAksiyon.BEKLE, self.__gozImaj.yon)
        self.__yarismaSaat=Clock.schedule_once(self.geriSayim,YarisAnimasyon.geriSayimGecikme())


    def geriSayim(self,dt):
        self.__yarismaSaat=Clock.schedule_once(self.yarisTikTak,YarisAnimasyon.animasyonGecikme())

    def yarisTikTak(self,dt):          
        if self.__gozImaj.aksiyon!=GozAksiyon.BEKLE:
            self.__yarismaSaat=Clock.schedule_once(self.yarisTikTak,YarisAnimasyon.animasyonGecikme())
            return
        
        if self.__gozHucre==self.__labirent.bitisHucre:           
            print("bitti")
            return
                    
        
        if not self.__reseptorGuncellendi:
            animasyonSure=self.__reseptorGuncelle()
            self.__yarismaSaat=Clock.schedule_once(self.yarisTikTak, animasyonSure+YarisAnimasyon.epsilon() if animasyonSure > 0 else YarisAnimasyon.animasyonGecikme())
            return

        
        if self.__gozImaj.animasyonTamamlandi:
            self.__gozImaj.animasyonBasladiResetle()
            self.__gozImaj.animasyonTamamlandiResetle()
            x, y = self.__labirent.hucreXY(self.__gozHucre,self.__saha)
            self.__gozImaj.konumla(x, y, self.__labirent.hucreKenarUzunluk)
            self.__reseptorGuncellendi = False
            
            
            gozHareket = self.__goz.kararVer(self.__reseptor)
            animasyonSure=self.__gozHareketUygula(gozHareket)
            
            self.__yarismaSaat=Clock.schedule_once(self.yarisTikTak, animasyonSure+YarisAnimasyon.epsilon())
            return
        
        self.__yarismaSaat=Clock.schedule_once(self.yarisTikTak, YarisAnimasyon.animasyonGecikme())
        
    def __gozHareketUygula(self,hareket):
        match hareket:
            case Hareket.SOLA_DON:
                self.__gozImaj.solaDon()#.yon=Yon((self.__gozImaj.yon+1)%len(Yon))
                #print("sola döndü")
            case Hareket.SAGA_DON:
                self.__gozImaj.sagaDon()#.yon=Yon((self.__gozImaj.yon-1)%len(Yon))
                #print("sağa döndü")
            case Hareket.ILERI:
                hucreSatirNumara=self.__gozHucre.satirNumara
                hucreSutunNumara=self.__gozHucre.sutunNumara
                match self.__gozImaj.yon:
                    case Yon.SAG:
                        hucreSutunNumara+=1
                    case Yon.SOL:
                        hucreSutunNumara-=1
                    case Yon.ALT:
                        hucreSatirNumara+=1
                    case Yon.UST:
                        hucreSatirNumara-=1
                
                duvar=self.__labirent.duvar(self.__gozHucre,self.__labirent.hucre(hucreSatirNumara,hucreSutunNumara))
                
                if duvar.durum==DuvarDurum.ACIK:   
                    self.__gozHucre=self.__labirent.hucre(hucreSatirNumara,hucreSutunNumara)
                    self.__gozImaj.git()
                else:
                    print("HÖSTT")
                    #self.__gozImaj.bekle()

        return GozImaj.animasyonSure(self.__gozImaj.aksiyon, self.__gozImaj.yon)

    def guncelleOlculer(self,*args):

        if self.__labirent is None:
            return
            
        self.__labirent.guncelleOlculer(self.__saha)
        
        x,y=self.__labirent.hucreXY(self.__gozHucre,self.__saha)
        
        self.__gozImaj.guncelleOlculer(x,y,self.__labirent.hucreKenarUzunluk)
        self.__reseptorImaj.guncelleOlculer(self.__labirent.hucreKenarUzunluk)

    def __reseptorGuncelle(self):
               
        yonFark = self.__gozImaj.yon - Yon.baslangic()
        gercekReseptorKonum=ReseptorKonum((self.__reseptor.konumIndis+yonFark)%len(ReseptorKonum))
        hucreX,hucreY=self.__labirent.hucreXY(self.__gozHucre,self.__saha)

        komsuHucreler = self.__labirent.komsuHucreler(self.__gozHucre)
        hedefHucre = komsuHucreler.get(Yon(gercekReseptorKonum))
        
        duvarDurum = DuvarDurum.KAPALI
        if hedefHucre:
            duvarDurum = self.__labirent.duvar(self.__gozHucre, hedefHucre).durum
        self.__reseptor.degerGuncelle(self.__reseptor.konumIndis, duvarDurum)

        if duvarDurum==DuvarDurum.ACIK:
            if not self.__reseptorImaj.animasyonBasladi:
                self.__reseptorImaj.animasyonTamamlandiResetle()
                self.__reseptorImaj.konumla(gercekReseptorKonum,hucreX,hucreY,self.__labirent.hucreKenarUzunluk)
            
                self.__reseptorImaj.duvarAcik()
            
                return ReseptorImaj.animasyonSure()
            
            if self.__reseptorImaj.animasyonTamamlandi:
                self.__reseptorImaj.animasyonBasladiResetle()
                self.__reseptor.konumIndisGuncelle()

                if self.__reseptor.konumIndis == 0:
                    self.__reseptorGuncellendi = True

        else:
            self.__reseptor.konumIndisGuncelle()

            if self.__reseptor.konumIndis == 0:
                self.__reseptorGuncellendi = True

        return 0

