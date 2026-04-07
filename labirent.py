#DÜNYA VE ÇEVRE


from enum import IntEnum
import random

from kivy.graphics import Ellipse,Line,Color

from temel import Konum
from sabitler import LabirentTip,DuvarDurum,Yon


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
