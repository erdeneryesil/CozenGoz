#DÜNYA VE ÇEVRE

#from enum import IntEnum
import random
#from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Ellipse, Fbo


from temel import Konum#,Denetle
from sabitler import EkranSabit,HucreSabit,LabirentSabit,AnimasyonSabit,DikdortgenTip,DuvarDurum,Yon,GozTip,GozAksiyon,Hareket,Yon,DuvarDurum,ReseptorKonum
from yarismaci import BenimGozum
from goz import Reseptor

from grafik_pencere_dosya import LabirentStatikImaj,GozImaj,ReseptorImaj

class Hucre(Konum):
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
        self.__satirSayi=satirSayi
        self.__sutunSayi=sutunSayi

        self.__minimumCozumUzunlugu=self.__satirSayi*self.__sutunSayi*LabirentSabit.MINIMUM_COZUM_UZUNLUGU_ORAN
        self.__tip=DikdortgenTip.belirle(self.__sutunSayi,self.__satirSayi)

        self.__kenarlikKalinlik=-1
        self.__hucreKenarUzunluk=-1
        self.__baslangicSatirNumara=-1
        self.__baslangicSutunNumara=-1
        self.__bitisSatirNumara=-1
        self.__bitisSutunNumara=-1
        self.__cozumYolu=[]
        self.__hucreler=[]
        self.__imaj=None

        rastgeleDeger=self.__rastgeleBaslangicBitisBelirle()
        self.__baslangicSatirNumara=rastgeleDeger[LabirentSabit.BASLANGIC_SATIR_NUMARA_ANAHTAR]
        self.__baslangicSutunNumara=rastgeleDeger[LabirentSabit.BASLANGIC_SUTUN_NUMARA_ANAHTAR]
        self.__bitisSatirNumara=rastgeleDeger[LabirentSabit.BITIS_SATIR_NUMARA_ANAHTAR]
        self.__bitisSutunNumara=rastgeleDeger[LabirentSabit.BITIS_SUTUN_NUMARA_ANAHTAR]
        
        self.__cozumYolu=self.__olusturCozumYolu()
        self.__hucreler=self.__olusturHucreler()


        self.__imaj=LabirentStatikImaj(self)
        self.__imaj.texture.save("labirent_sablonu.png")


    @property
    def satirSayi(self):
        return self.__satirSayi
    @property
    def sutunSayi(self):
        return self.__sutunSayi
    @property
    def baslangicSatirNumara(self):
        return self.__baslangicSatirNumara
    @property
    def baslangicSutunNumara(self):
        return self.__baslangicSutunNumara
    @property
    def bitisSatirNumara(self):
        return self.__bitisSatirNumara
    @property
    def bitisSutunNumara(self):
        return self.__bitisSutunNumara
    
    @property
    def baslangicHucre(self):
        return self.__hucreler[self.__baslangicSatirNumara][self.__baslangicSutunNumara]
    @property
    def bitisHucre(self):
        return self.__hucreler[self.__bitisSatirNumara][self.__bitisSutunNumara]
    @property
    def cozumYoluUzunluk(self):#çözüm yolu kaç tane Hücre içeriyor
        return len(self.__cozumYolu)
    @property
    def hucreKenarUzunluk(self):
        return self.__hucreKenarUzunluk
    @property
    def kenarlikKalinlik(self):
        return self.__kenarlikKalinlik
    @property
    def imaj(self):
        return self.__imaj
    @property
    def imajGenislik(self):#width ile imajın gerçek boyutu dönmüyor, norm_image_size ile gerçek değeri alabiliyoruz
        return self.__imaj.norm_image_size[0]
    @property
    def imajYukseklik(self):#height ile imajın gerçek boyutu dönmüyor, norm_image_size ile gerçek değeri alabiliyoruz
        return self.__imaj.norm_image_size[1]
    @property
    def tip(self):
        return self.__tip
    
    def cozumYoluHucre(self,numara):
        return self.__cozumYolu[numara]

    def hucre(self,satirNumara,sutunNumara):
        if satirNumara<0 or satirNumara>=self.__satirSayi or sutunNumara<0 or sutunNumara>=self.__sutunSayi:
            return None
        return self.__hucreler[satirNumara][sutunNumara]
    
    def komsuHucreler(self,hucre):
        komsuHucreler={Yon.SOL:None,Yon.ALT:None,Yon.SAG:None,Yon.UST:None,HucreSabit.SAYI_ANAHTAR:0}
        if hucre.satirNumara+1<self.__satirSayi:#altında komşu var mı
            komsuHucreler[Yon.ALT]=self.__hucreler[hucre.satirNumara+1][hucre.sutunNumara]
            komsuHucreler[HucreSabit.SAYI_ANAHTAR]+=1
        
        if hucre.satirNumara-1>=0:#üstünde satir var mı
            komsuHucreler[Yon.UST]=self.__hucreler[hucre.satirNumara-1][hucre.sutunNumara]
            komsuHucreler[HucreSabit.SAYI_ANAHTAR]+=1
        
        if hucre.sutunNumara+1<self.__sutunSayi:#sağında komşu var mı
            komsuHucreler[Yon.SAG]=self.__hucreler[hucre.satirNumara][hucre.sutunNumara+1]
            komsuHucreler[HucreSabit.SAYI_ANAHTAR]+=1

        if hucre.sutunNumara-1>=0:#solunda komşu var mı
            komsuHucreler[Yon.SOL]=self.__hucreler[hucre.satirNumara][hucre.sutunNumara-1]
            komsuHucreler[HucreSabit.SAYI_ANAHTAR]+=1
        return komsuHucreler

    def duvar(self,hucre1,hucre2):
        if hucre1 is None or hucre2 is None:#Eğer satır ya da sutun numarası labirentin sınırları dışındaysa, KAPALI bir duvar dönsün 
            return Duvar()   
                
        if hucre1.satirNumara==hucre2.satirNumara:#aynı satırdaki hücreler arasındaki bir duvar ise
            if hucre2.sutunNumara<hucre1.sutunNumara:#hücre2 küçük indisli ise
                return self.__duvarlar[LabirentSabit.SATIR_ANAHTAR][hucre2.satirNumara][hucre2.sutunNumara]
            return self.__duvarlar[LabirentSabit.SATIR_ANAHTAR][hucre1.satirNumara][hucre1.sutunNumara]#hücre1 küçük indisli ise
        else:#aynı sütundaki hücreler arasındaki bir duvar ise
            if hucre2.satirNumara<hucre1.satirNumara:#hücre2 küçük indisli ise
                return self.__duvarlar[LabirentSabit.SUTUN_ANAHTAR][hucre2.sutunNumara][hucre2.satirNumara]    
            return self.__duvarlar[LabirentSabit.SUTUN_ANAHTAR][hucre1.sutunNumara][hucre1.satirNumara]#hücre1 küçük indisli ise

    def hucreXY(self,hucre,saha):#konumu verilen hücreye, robotu çizebilmek için gerekli koordinatlar   
        genislik,yukseklik=self.olcekle(saha.width,saha.height)
        solX=self.imaj.solXRender(saha)
        ustY=self.imaj.ustYRender(saha)
        x=solX+self.__kenarlikKalinlik/2+(self.__hucreKenarUzunluk-self.__kenarlikKalinlik/2)*hucre.sutunNumara   
        y=ustY-self.__hucreKenarUzunluk*(1+hucre.satirNumara)+self.__kenarlikKalinlik+self.__hucreKenarUzunluk/2-self.__hucreKenarUzunluk/2

        return (x,y)

    def hesaplaHucreKenarUzunluk(self,genislik=None,yukseklik=None):
        if genislik is None:
            genislik=self.__imaj.guncelGenislikRender
        
        if yukseklik is None:
            yukseklik=self.__imaj.guncelYukseklikRender

            
        if self.__tip==DikdortgenTip.YATAY:
            return genislik/self.__sutunSayi
        return yukseklik/self.__satirSayi
        
    def olcekle(self,sahaGenislik,sahaYukseklik):#sahanın boyutlarına göre ölçeklenmiş genişlik, yükseklik değerlerini döndürür
        genislikOlcek=sahaGenislik/self.__sutunSayi
        yukseklikOlcek=sahaYukseklik/self.__satirSayi
        olcekFaktor=min(genislikOlcek,yukseklikOlcek)

        return (self.__sutunSayi*olcekFaktor,self.__satirSayi*olcekFaktor)

    def guncelleOlculer(self,saha):#canvas içerisine çizilecek labirentin genişlik, yükseklik, x, y vs değerleri hesaplanıyor        
        
        genislik,yukseklik=self.olcekle(saha.width,saha.height)

        self.__imaj.size=(genislik,yukseklik)
        self.__imaj.pos=(self.__imaj.solXImageWidget(saha),self.__imaj.ustYImageWidget(saha)-yukseklik)
        
        self.__kenarlikKalinlik=self.__guncelleKenarlikKalinlik(saha.width,saha.height)
        
        self.__hucreKenarUzunluk=self.hesaplaHucreKenarUzunluk()

        print(self.__hucreKenarUzunluk/self.__kenarlikKalinlik)
        
        #from grafik_pencere_dosya import StatikImaj
        #i=StatikImaj()
        #i._gercekDegerlerHesapla()
        #self.__orijinalKenarlikKalinlik=self.__orijinalGenislikImageWidget/EkranSabit.LABIRENT_KENARLIK_KALINLIK_ORAN
        #print(self.__imaj.orijinalKenarlikKalinlik,self.__kenarlikKalinlik)
        #print(self.__imaj.genislikImageWidget/self.kenarlikKalinlik)


        #print(self.__kenarlikKalinlik,self.__imaj.genislikRender)
        #print(solX,self.__imaj.solX(saha))
        #print(saha.width,genislik,saha.height,yukseklik)
        #print(genislik,self.__imaj.genislik,self.__imaj.width)
        #print(yukseklik,self.__imaj.yukseklik,self.__imaj.height)
        
    def __guncelleKenarlikKalinlik(self,sahaGenislik,sahaYukseklik):
        if self.__tip==DikdortgenTip.YATAY:
            return self.__imaj.guncelYukseklikRender/EkranSabit.LABIRENT_KENARLIK_KALINLIK_ORAN
        elif self.__tip==DikdortgenTip.DIKEY:
            return self.__imaj.guncelGenislikRender/EkranSabit.LABIRENT_KENARLIK_KALINLIK_ORAN
        else:
            if sahaGenislik>sahaYukseklik:
                return (self.satirSayi/sahaYukseklik)*(self.__imaj.guncelGenislikRender/EkranSabit.LABIRENT_KENARLIK_KALINLIK_ORAN)
            else:
                return (self.satirSayi/sahaGenislik)*(self.__imaj.guncelGenislikRender/EkranSabit.LABIRENT_KENARLIK_KALINLIK_ORAN)/sahaGenislik
    def __olusturCozumYolu(self):
         
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
        
        return hucreYigin
    
    def __secRastgeleKomsuHucre(self,hucre):
        komsuHucreler=self.komsuHucreler(hucre)
        
        if komsuHucreler[HucreSabit.SAYI_ANAHTAR]==0:
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
        duvarlar={LabirentSabit.SATIR_ANAHTAR:[],LabirentSabit.SUTUN_ANAHTAR:[]}
        #satırlarda bulunan duvarlar oluşturuluyor
        for satirNumara in range(self.__satirSayi):
            satirDuvarlar=[]
            for sutunNumara in range(self.__sutunSayi-1):
                duvar=Duvar()
                satirDuvarlar.append(duvar)
            duvarlar[LabirentSabit.SATIR_ANAHTAR].append(satirDuvarlar)

                
        #sutunlarda bulunan duvarlar oluşturuluyor
        for sutunNumara in range(self.__sutunSayi):
            sutunDuvarlar=[]
            for satirNumara in range(self.__satirSayi-1):
                duvar=Duvar()
                sutunDuvarlar.append(duvar)
            duvarlar[LabirentSabit.SUTUN_ANAHTAR].append(sutunDuvarlar)

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
                self.__duvarlar[LabirentSabit.SUTUN_ANAHTAR][sutunNumara][satirNumara].kapat()
    
    def __rastgeleBaslangicBitisBelirle(self):#labirentin başlangıç ve bitiş hücreleri rastgele belirleniyor

        if self.__tip==DikdortgenTip.YATAY:
            baslangicSutunNumara=0
            bitisSutunNumara=self.__sutunSayi-1
            baslangicSatirNumara=random.randint(0,self.__satirSayi-1)
            bitisSatirNumara=random.randint(0,self.__satirSayi-1)
        else:
            baslangicSatirNumara=0
            bitisSatirNumara=self.__satirSayi-1
            baslangicSutunNumara=random.randint(0,self.__sutunSayi-1)
            bitisSutunNumara=random.randint(0,self.__sutunSayi-1)

        return {LabirentSabit.BASLANGIC_SATIR_NUMARA_ANAHTAR:baslangicSatirNumara,
            LabirentSabit.BASLANGIC_SUTUN_NUMARA_ANAHTAR:baslangicSutunNumara,
            LabirentSabit.BITIS_SATIR_NUMARA_ANAHTAR:bitisSatirNumara,
            LabirentSabit.BITIS_SUTUN_NUMARA_ANAHTAR:bitisSutunNumara}
    

        
    #def __maksimumMesafe(self):#labirentin birbirlerine en uzak olan hücrelerin arasındaki mesafe
        #return self.__satirSayi-1+self.__sutunSayi-1
    
    #def __mesafeHesapla(self,satirNumara1,sutunNumara1,satirNumara2,sutunNumara2):
        #return abs(satirNumara1-satirNumara2)+abs(sutunNumara1-sutunNumara2)

class Saha(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
                
        self.__labirent=Labirent(8,8)#Labirent(20,5)
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
        self.__yarismaSaat=Clock.schedule_once(self.geriSayim,AnimasyonSabit.GERI_SAYIM_GECIKME)


    def geriSayim(self,dt):
        self.__yarismaSaat=Clock.schedule_once(self.yarisTikTak,AnimasyonSabit.ANIMASYON_GECIKME)

    def yarisTikTak(self,dt):   
               
        if self.__gozImaj.aksiyon!=GozAksiyon.BEKLE:
            self.__yarismaSaat=Clock.schedule_once(self.yarisTikTak,AnimasyonSabit.ANIMASYON_GECIKME)
            return
        
        if self.__gozHucre==self.__labirent.bitisHucre:           
            print("bitti")
            return
                    
        
        if not self.__reseptorGuncellendi:
            animasyonSure=self.__reseptorGuncelle()
            self.__yarismaSaat=Clock.schedule_once(self.yarisTikTak, animasyonSure+AnimasyonSabit.EPSILON if animasyonSure > 0 else AnimasyonSabit.ANIMASYON_GECIKME)
            return

        
        if self.__gozImaj.animasyonTamamlandi:
            self.__gozImaj.animasyonBasladiResetle()
            self.__gozImaj.animasyonTamamlandiResetle()
            x, y = self.__labirent.hucreXY(self.__gozHucre,self.__saha)
            self.__gozImaj.konumla(x, y, self.__labirent.hucreKenarUzunluk,self.__labirent.kenarlikKalinlik)
            self.__reseptorGuncellendi = False

            with self.__saha.canvas:
                from kivy.graphics import Color, Line, Ellipse,Rectangle, Fbo#, RenderContext, Scale, Translate
                Color(0,0,0,1)
                boyut=self.__labirent.kenarlikKalinlik
                solX=self.__labirent.imaj.solXRender(self.__saha)
                ustY=self.__labirent.imaj.ustYRender(self.__saha)
                sagX=solX+self.__labirent.imaj.guncelGenislikRender
                altY=ustY-self.__labirent.imaj.guncelYukseklikRender
                
                #Rectangle(size=(boyut,boyut),pos=(self.__labirent.imaj.solXImageWidget(self.__saha),self.__labirent.imaj.ustYImageWidget(self.__saha)))
                x=self.__labirent.imaj.solXImageWidget(self.__saha)
                y=self.__labirent.imaj.ustYImageWidget(self.__saha)
                Line(width=boyut,points=(x,y-100,x+100,y-100))
                

                #print(self.__labirent.kenarlikKalinlik)
                #Rectangle(size=(boyut,boyut),pos=(solX-boyut/2,ustY-boyut/2))
                #Rectangle(size=(boyut,boyut),pos=(sagX-boyut/2,ustY-boyut/2))
                #Rectangle(size=(boyut,boyut),pos=(solX-boyut/2,altY-boyut/2))
                #Rectangle(size=(boyut,boyut),pos=(sagX-boyut/2,altY-boyut/2))


                x=solX+self.__labirent.kenarlikKalinlik/2
                y=ustY-self.__labirent.kenarlikKalinlik/2
                #Rectangle(size=(boyut,boyut),pos=(x-boyut/2,y-boyut/2))

                x=solX+self.__labirent.kenarlikKalinlik+self.__labirent.hucreKenarUzunluk
                y=ustY-self.__labirent.kenarlikKalinlik
                #Line(width=(boyut),points=(x-boyut/2,y-boyut/2,x+boyut/2,y-boyut/2))
                #Rectangle(size=(10,10),pos=(x,y))



                
            gozHareket = self.__goz.kararVer(self.__reseptor)
            animasyonSure=self.__gozHareketUygula(gozHareket)
            
            self.__yarismaSaat=Clock.schedule_once(self.yarisTikTak, animasyonSure+AnimasyonSabit.EPSILON)
            return
        
        self.__yarismaSaat=Clock.schedule_once(self.yarisTikTak, AnimasyonSabit.ANIMASYON_GECIKME)
        
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
        
        self.__gozImaj.guncelleOlculer(x,y,self.__labirent.hucreKenarUzunluk,self.__labirent.kenarlikKalinlik)
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

