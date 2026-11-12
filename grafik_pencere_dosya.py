#KIVY PENCERE, DOSYA VE GRAFİK YÖNETİMİ

from abc import ABCMeta, abstractmethod

from kivy.uix.image import Image,CoreImage
from kivy.clock import Clock
from kivy.atlas import Atlas
from kivy.graphics import Color, Line, Ellipse, Fbo, Rectangle

from sabitler import DuvarDurum,HucreSabit,EkranSabit,LabirentSabit,ImajTip,ImajSabit,GozTip,GozAksiyon,Yon,DikdortgenTip,HucreNokta
from temel import Konum

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

class StatikImaj(Image):
    #Canvas imajın tamamı, kenar boşlukları dahil
    #Render imajın içeriği, kenar boşluklarından arındırılmış hali

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.allow_stretch=True
        self.keep_ratio=True

        #ilk oluşturulan görsele ait nitelikler. Canvas çizim alanı(kenar boşlukları içerir), Render çizimin kendisi(kenar boşlukları içermez)
        self._gercekGenislikCanvas=-1
        self._gercekYukseklikCanvas=-1
        self._gercekGenislikRender=-1
        self._gercekYukseklikRender=-1
        self._gercekSolXRender=-1
        self._gercekAltYRender=-1
        self._gercekUstYRender=-1

    def _gercekDegerlerHesapla(self):
        raise NotImplementedError("_gercek değerler, alt sınıflarda hesaplanmalıdır!")
    def _textureOlustur(self):
        raise NotImplementedError("texture oluşturma işlemi alt sınıflarda yapılmalıdır")
    
    
    #_guncelGenislikCanvas,_guncelYukseklikCanvas,_guncelSolXCanvas,_guncelUstYCanvas değerleri; görselin bir Widget olarak sahip olduğu değerlerdir. Kenar boşlukları dahildir
    @property
    def _guncelGenislikCanvas(self):
        return self.size[0]
    @property
    def _guncelYukseklikCanvas(self):
        return self.size[1]
    def _guncelSolXCanvas(self,ebeveyn):#ebeveyn:içinde bulunduğu widget
        return ebeveyn.x+(ebeveyn.width-self._guncelGenislikCanvas)/2
    def _guncelAltYCanvas(self,ebeveyn):#ebeveyn:içinde bulunduğu widget
        return ebeveyn.y+(ebeveyn.height-self._guncelYukseklikCanvas)/2
    def _guncelUstYCanvas(self,ebeveyn):#ebeveyn:içinde bulunduğu widget
        return ebeveyn.y+self._guncelYukseklikCanvas+(ebeveyn.height-self._guncelYukseklikCanvas)/2
    
    
    #_guncelGenislikRender,_guncelYukseklikRender,_guncelSolXRender,_guncelUstYRender değerleri; görselin gerçek çizim değerleridir. Kenar boşluklarından arındırılmıştır
    @property
    def _guncelGenislikRender(self):
        return self._guncelGenislikCanvas*(self._gercekGenislikRender/self._gercekGenislikCanvas)
    @property
    def _guncelYukseklikRender(self):
        return self._guncelYukseklikCanvas*(self._gercekYukseklikRender/self._gercekYukseklikCanvas)
    
    def _guncelSolXRender(self,ebeveyn):
        return self._guncelSolXCanvas(ebeveyn)+(self._guncelGenislikCanvas-self._guncelGenislikRender)/2#kenarlık kalınlığı hesaba dahil edilmiyor
    def _guncelAltYRender(self,ebeveyn):
        return self._guncelAltYCanvas(ebeveyn)+(self._guncelYukseklikCanvas-self._guncelYukseklikRender)/2#kenarlık kalınlığı hesaba dahil edilmiyor
    def _guncelUstYRender(self,ebeveyn):
        return self._guncelUstYCanvas(ebeveyn)-(self._guncelYukseklikCanvas-self._guncelYukseklikRender)/2#kenarlık kalınlığı hesaba dahil edilmiyor
    
    

class LabirentStatikImaj(StatikImaj):
    #Canvas imajın tamamı, kenar boşlukları dahil
    #Render imajın içeriği, kenar boşluklarından arındırılmış hali
    def __init__(self,labirent,**kwargs):
        super().__init__(**kwargs)

        self.__labirent=labirent
        
        self._gercekKenarlikYarim=-1
        self._gercekHucreBoyut=-1
        self._guncelKenarlikYarim=-1
        self._guncelHucreBoyut=-1

        self._gercekDegerlerHesapla()
        self.texture=self._textureOlustur()

    @property
    def _gercekKenarlikTam(self):
        return 2*self._gercekKenarlikYarim

    @property   #public
    def guncelHucreBoyut(self):
        return self._guncelHucreBoyut
    @property   #public
    def guncelKenarlikTam(self):
        return 2*self._guncelKenarlikYarim

    def guncelleOlculer(self,saha):#canvas içerisine çizilecek labirentin genişlik, yükseklik, x, y vs değerleri hesaplanıyor        
        
        genislik,yukseklik=self.__olcekle(saha.width,saha.height)

        self.size=(genislik,yukseklik)
        self.pos=(self._guncelSolXCanvas(saha),self._guncelUstYCanvas(saha)-yukseklik)
        
        if self.__labirent.tip==DikdortgenTip.YATAY:
            self._guncelKenarlikYarim=self.__hesaplaKenarlikYarim(self._guncelGenislikCanvas,self.__labirent.sutunSayi)
        else:
            self._guncelKenarlikYarim=self.__hesaplaKenarlikYarim(self._guncelYukseklikCanvas,self.__labirent.satirSayi)

        self._guncelHucreBoyut=self.__hesaplaHucreBoyut(self._guncelGenislikRender,self.__labirent.sutunSayi,self.guncelKenarlikTam)

    def hucreXY(self,hucreNokta,hucre,saha=None):#konumu verilen hücreye; robotu, sensörleri vs. çizebilmek için gerekli koordinatlar   
        if saha is None:#texture oluşturulur iken
            solX=self._gercekSolXRender
            ustY=self._gercekUstYRender
            altY=self._gercekAltYRender
            genislik=self._gercekGenislikRender
            yukselik=self._gercekYukseklikRender
            hucreBoyut=self._gercekHucreBoyut
            kenarlikYarim=self._gercekKenarlikYarim
        else:        
            solX=self._guncelSolXRender(saha)
            ustY=self._guncelUstYRender(saha)
            altY=self._guncelAltYRender(saha)
            genislik=self._guncelGenislikRender
            yukselik=self._guncelYukseklikRender
            hucreBoyut=self._guncelHucreBoyut
            kenarlikYarim=self._guncelKenarlikYarim

        temelSolX=solX+(hucre.sutunNumara)*(genislik/self.__labirent.sutunSayi)
        temelSagX=solX+(hucre.sutunNumara+1)*(genislik/self.__labirent.sutunSayi)
        temelUstY=ustY-(hucre.satirNumara+1)*(yukselik/self.__labirent.satirSayi)
        temelAltY=altY+(self.__labirent.satirSayi-hucre.satirNumara)*(yukselik/self.__labirent.satirSayi)

            
        match hucreNokta:
            case HucreNokta.MERKEZ:
                x=temelSolX+hucreBoyut/2+kenarlikYarim
                y=temelUstY+hucreBoyut/2+kenarlikYarim
            case HucreNokta.SOL_ALT:
                x=temelSolX+kenarlikYarim
                y=temelUstY+kenarlikYarim
            case HucreNokta.SOL:
                x=temelSolX
                y=temelUstY+hucreBoyut/2+kenarlikYarim
            case HucreNokta.ALT:
                x=temelSolX+hucreBoyut/2+kenarlikYarim
                y=temelUstY
            case HucreNokta.SAG:
                x=temelSagX
                y=temelUstY+hucreBoyut/2+kenarlikYarim
            case HucreNokta.UST:
                x=temelSolX+hucreBoyut/2+kenarlikYarim
                y=temelAltY
            case HucreNokta.SAG_ALT:
                x=temelSagX-kenarlikYarim
                y=temelUstY+kenarlikYarim

        return (x,y)
        

    def _gercekDegerlerHesapla(self):#niteliklerin değerleri hesaplanıyor
        maks=EkranSabit.maksSahaBoyut(self.__labirent.tip)
        maksSahaGenislik=maks[EkranSabit.MAKS_SAHA_GENISLIK_ANAHTAR]
        maksSahaYukseklik=maks[EkranSabit.MAKS_SAHA_YUKSEKLIK_ANAHTAR]       

        self._gercekGenislikCanvas,self._gercekYukseklikCanvas=self.__olcekle(maksSahaGenislik,maksSahaYukseklik)#labirentin çizileceği alanın genişlik ve yükseklik
        
        if self.__labirent.tip==DikdortgenTip.YATAY:
            self._gercekKenarlikYarim=self.__hesaplaKenarlikYarim(self._gercekGenislikCanvas,self.__labirent.sutunSayi)
            self._gercekYukseklikRender=self._gercekYukseklikCanvas-EkranSabit.RENDER_KUCULTME_CARPAN*self._gercekKenarlikTam
            self._gercekGenislikRender=self._gercekYukseklikRender*self._gercekGenislikCanvas/self._gercekYukseklikCanvas
        else:
            self._gercekKenarlikYarim=self.__hesaplaKenarlikYarim(self._gercekYukseklikCanvas,self.__labirent.satirSayi)
            self._gercekGenislikRender=self._gercekGenislikCanvas-EkranSabit.RENDER_KUCULTME_CARPAN*self._gercekKenarlikTam
            self._gercekYukseklikRender=self._gercekGenislikRender*self._gercekYukseklikCanvas/self._gercekGenislikCanvas

        

        #hucreBoyutGenisligeGore=self.__hesaplaHucreBoyut(self._gercekGenislikCanvas,self.__labirent.sutunSayi,self._gercekKenarlikTam)
        #hucreBoyutYuksekligeGore=self.__hesaplaHucreBoyut(self._gercekYukseklikCanvas,self.__labirent.satirSayi,self._gercekKenarlikTam)            

        '''if hucreBoyutYuksekligeGore<hucreBoyutGenisligeGore:
            print("asd")
            self._gercekYukseklikRender=self._gercekYukseklikCanvas-EkranSabit.RENDER_KUCULTME_CARPAN*self._gercekKenarlikTam
            self._gercekGenislikRender=self._gercekYukseklikRender*self._gercekGenislikCanvas/self._gercekYukseklikCanvas
        else:
            print("99")
            self._gercekGenislikRender=self._gercekGenislikCanvas-EkranSabit.RENDER_KUCULTME_CARPAN*self._gercekKenarlikTam
            self._gercekYukseklikRender=self._gercekGenislikRender*self._gercekYukseklikCanvas/self._gercekGenislikCanvas
        '''


        #self._gercekGenislikRender+=self._gercekKenarlikTam
        #self._gercekYukseklikRender+=self._gercekKenarlikTam

        self._gercekHucreBoyut=self.__hesaplaHucreBoyut(self._gercekGenislikRender,self.__labirent.sutunSayi,self._gercekKenarlikTam)
        #print(self.__labirent.sutunSayi*self._gercekHucreBoyut+self._gercekKenarlikTam*(self.__labirent.sutunSayi+1),self._gercekGenislikRender)
        #print(self.__labirent.satirSayi*self._gercekHucreBoyut+self._gercekKenarlikTam*(self.__labirent.satirSayi+1),self._gercekYukseklikRender)

        self._gercekSolXRender=(self._gercekGenislikCanvas-self._gercekGenislikRender)/2    #labirentin sol kenarının ortası (kenarlığın ortası)   
        self._gercekAltYRender=((self._gercekYukseklikCanvas-self._gercekYukseklikRender)/2) #labirentin alt kenarının ortası (kenarlığın ortası)
        self._gercekUstYRender=self._gercekYukseklikCanvas-((self._gercekYukseklikCanvas-self._gercekYukseklikRender)/2) #labirentin üst kenarının ortası (kenarlığın ortası)
    
    def __izgaraCiz(self):#deneme amaçlı
        Color(1,1,1,1)

        #labirentin köşeleri
        olcu=self._gercekKenarlikTam

        x=self._gercekSolXRender
        y=self._gercekUstYRender-100
        Rectangle(size=(olcu,olcu),pos=(x-olcu/2,y-olcu/2))#sol-üst

        x=self._gercekSolXRender
        y=self._gercekAltYRender
        Rectangle(size=(olcu,olcu),pos=(x-olcu/2,y-olcu/2))#sol-alt

        x=self._gercekSolXRender+self._gercekGenislikRender
        y=self._gercekAltYRender
        Rectangle(size=(olcu,olcu),pos=(x-olcu/2,y-olcu/2))#sağ-alt
        
        x=self._gercekSolXRender+self._gercekGenislikRender
        y=self._gercekUstYRender
        Rectangle(size=(olcu,olcu),pos=(x-olcu/2,y-olcu/2))#sağ-üst

        #imajın köşeleri
        x=0
        y=0
        #Rectangle(size=(olcu,olcu),pos=(x-olcu/2,y-olcu/2))#sol-alt

        x=self._gercekGenislikCanvas
        y=0
        #Rectangle(size=(olcu,olcu),pos=(x-olcu/2,y-olcu/2))#sağ-alt

        x=self._gercekGenislikCanvas
        y=self._gercekYukseklikCanvas
        #Rectangle(size=(olcu,olcu),pos=(x-olcu/2,y-olcu/2))#sağ-üst

        x=0
        y=self._gercekYukseklikCanvas
        #Rectangle(size=(olcu,olcu),pos=(x-olcu/2,y-olcu/2))#sol-üst

        
        
        #sütunlar
        for i in range(0,self.__labirent.sutunSayi+1):
            x=self._gercekSolXRender+i*(self._gercekHucreBoyut+self._gercekKenarlikTam)

            yUst=self._gercekUstYRender
            yAlt=self._gercekAltYRender
            
            Color(.5,.5,.5,1)
            #Rectangle(size=(olcu,olcu),pos=(x-olcu/2,yUst-olcu/2))
            #Rectangle(size=(olcu,olcu),pos=(x-olcu/2,yAlt-olcu/2))
            
            Color(.3,.3,.3,1)
            Line(width=olcu/2,points=(x,yUst,x,yAlt))

        #satırlar
        for i in range(1,self.__labirent.satirSayi):
            xSol=self._gercekSolXRender
            xSag=self._gercekSolXRender+self._gercekGenislikRender
            y=self._gercekAltYRender+i*(self._gercekHucreBoyut+self._gercekKenarlikTam)

            Color(.5,.5,.5,1)          
            #Rectangle(size=(olcu,olcu),pos=(xSol-olcu/2,y-olcu/2)) 
            #Rectangle(size=(olcu,olcu),pos=(xSag-olcu/2,y-olcu/2))

            Color(.3,.3,.3,1)
            Line(width=olcu/2,points=(xSol,y,xSag,y))

    def _textureOlustur(self):
        #labirent görselini, maks boyutlara göre bir kez oluşturup, sonrasında ölçekleniyor
        fbo = Fbo(size=(self._gercekGenislikCanvas, self._gercekYukseklikCanvas))
        
        # Kivy Fbo varsayılan olarak transparan gelebilir. Arka planı temizliyoruz.
        fbo.clear_buffer()

        with fbo:
            #self.__izgaraCiz()

            Color(rgba=LabirentSabit.KENARLIK_RENK)
            self.__cizCerceve()

            # Duvarların çizimi
            self.__cizDuvar()
            
            # Çözüm yolu veya Başlangıç/Bitiş hücrelerinin boyanması
            hucreTip=HucreSabit.TIP[HucreSabit.TIP_YOL_ANAHTAR]
            for hucreNumara in range(self.__labirent.cozumYoluUzunluk):
                self.__boyaHucre(self.__labirent.cozumYoluHucre(hucreNumara),hucreTip[HucreSabit.TIP_UZUNLUK_CARPAN_ANAHTAR],hucreTip[HucreSabit.TIP_RENK_ANAHTAR])

            hucreTip=HucreSabit.TIP[HucreSabit.TIP_BASLANGIC_ANAHTAR]
            self.__boyaHucre(Konum(self.__labirent.baslangicSatirNumara,self.__labirent.baslangicSutunNumara),hucreTip[HucreSabit.TIP_UZUNLUK_CARPAN_ANAHTAR],hucreTip[HucreSabit.TIP_RENK_ANAHTAR])

            hucreTip=HucreSabit.TIP[HucreSabit.TIP_BITIS_ANAHTAR]
            self.__boyaHucre(Konum(self.__labirent.bitisSatirNumara,self.__labirent.bitisSutunNumara),hucreTip[HucreSabit.TIP_UZUNLUK_CARPAN_ANAHTAR],hucreTip[HucreSabit.TIP_RENK_ANAHTAR])

        fbo.draw()

        return fbo.texture

    def __olcekle(self,sahaGenislik,sahaYukseklik):#sahanın boyutlarına göre ölçeklenmiş genişlik, yükseklik değerlerini döndürür
        genislikOlcek=sahaGenislik/self.__labirent.sutunSayi
        yukseklikOlcek=sahaYukseklik/self.__labirent.satirSayi
        olcekFaktor=min(genislikOlcek,yukseklikOlcek)

        return (self.__labirent.sutunSayi*olcekFaktor,self.__labirent.satirSayi*olcekFaktor)

    def __cizCerceve(self):
        Line(close="True", width=self._gercekKenarlikYarim,rectangle=(self._gercekSolXRender,self._gercekAltYRender, self._gercekGenislikRender, self._gercekYukseklikRender))

    def __cizDuvar(self):
        for satirNumara in range(self.__labirent.satirSayi):
            for sutunNumara in range(self.__labirent.sutunSayi-1):
                duvar=self.__labirent.duvar(self.__labirent.hucre(satirNumara,sutunNumara),self.__labirent.hucre(satirNumara,sutunNumara+1))
                if duvar.durum==DuvarDurum.KAPALI:
                    x,y=self.hucreXY(HucreNokta.SOL_ALT,self.__labirent.hucre(satirNumara,sutunNumara+1))    
                    x-=self._gercekKenarlikYarim           
                    y1=y+self._gercekHucreBoyut+self._gercekKenarlikYarim
                    y2=y-self._gercekKenarlikYarim                    
                    Line(width=self._gercekKenarlikYarim,points=(x,y1,x,y2))

        for sutunNumara in range(self.__labirent.sutunSayi):
            for satirNumara in range(self.__labirent.satirSayi-1):
                duvar=self.__labirent.duvar(self.__labirent.hucre(satirNumara,sutunNumara),self.__labirent.hucre(satirNumara+1,sutunNumara))
                if duvar.durum==DuvarDurum.KAPALI:
                    x,y=self.hucreXY(HucreNokta.SOL_ALT,self.__labirent.hucre(satirNumara,sutunNumara))
                    y-=self._gercekKenarlikYarim
                    x1=x-self._gercekKenarlikYarim
                    x2=x+self._gercekHucreBoyut+self._gercekKenarlikYarim
                    Line(width=self._gercekKenarlikYarim,points=(x1,y,x2,y))

    def __boyaHucre(self,konum,uzunlukCarpan,renk):
        Color(rgba=renk)        
        olcu=uzunlukCarpan*self._gercekHucreBoyut

        hucre=self.__labirent.hucre(konum.satirNumara,konum.sutunNumara)        
        x,y=self.hucreXY(HucreNokta.MERKEZ,hucre)
        x-=(olcu/2)
        y-=(olcu/2)

        Ellipse(size=(olcu,olcu),pos=(x,y))

    def __hesaplaKenarlikYarim(self,olcu,hucreSayi):#olcu; genişlik ya da yükseklik. hucreSayi; satır ya da sütun sayısı
        return (olcu/EkranSabit.LABIRENT_KENARLIK_YARIM_ORAN)/hucreSayi
            

    def __hesaplaHucreBoyut(self,olcu,hucreSayi,kenarlikTam):#olcu; genişlik ya da yükseklik. hucreSayi; satır ya da sütun sayısı
        return (olcu+kenarlikTam-(hucreSayi+1)*kenarlikTam)/(hucreSayi)
    
class AnimasyonImaj(Image):
    #SABİTLER
    _DIZIN = None
    _ATLAS_DOSYA = None
    _KARE_AD = None
    _KARE_SAYI = None
    _GECIKME = None
    _ORIJINAL_BOYUT = None
    _BOYUT_ORAN = None
    _ANIMASYON_TEKRAR = None

    _kare= None
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
        return cls._DIZIN
    @classmethod
    def atlasYuklendi(cls):
        return cls._atlasYuklendi
    @classmethod
    def atlasYuklendiGuncelle(cls, deger):
        cls._atlasYuklendi = deger
    @classmethod
    def orijinalBoyut(cls):
        return cls._ORIJINAL_BOYUT
    @classmethod
    def boyutOran(cls):
        return cls._BOYUT_ORAN
    
    
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

class ReseptorImaj(AnimasyonImaj):
    #SABİTLER
    _DIZIN=ImajSabit.DIZIN[ImajTip.RESEPTOR_IMAJ]
    _ATLAS_DOSYA=ImajSabit.ATLAS_DOSYA[ImajTip.RESEPTOR_IMAJ]
    _KARE_AD=ImajSabit.KARE_AD[ImajTip.RESEPTOR_IMAJ]
    _KARE_SAYI=ImajSabit.KARE_SAYI[ImajTip.RESEPTOR_IMAJ]
    _GECIKME=ImajSabit.GECIKME[ImajTip.RESEPTOR_IMAJ]
    _ORIJINAL_BOYUT=ImajSabit.ORIJINAL_BOYUT[ImajTip.RESEPTOR_IMAJ]
    _BOYUT_ORAN=ImajSabit.BOYUT_ORAN[ImajTip.RESEPTOR_IMAJ]#hücre genişliğine oranı
    _ANIMASYON_TEKRAR=ImajSabit.ANIMASYON_TEKRAR[ImajTip.RESEPTOR_IMAJ] # Animasyon kaç kere çalışacak
    
    _kare=ImajSabit.BOS_KARE[ImajTip.RESEPTOR_IMAJ]
    _atlasYuklendi=False # atlas dosyasının yüklenip yüklenmediğini kontrol edeceğimiz değişken. Yüklendiğine True olacak

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        #self.allow_stretch=True
        #self.fit_mode='contain'
        self.size_hint=(None,None)
        self.opacity=0
        
    @classmethod
    def atlasDosya(cls):
        return cls._ATLAS_DOSYA
    @classmethod
    def gecikme(cls):
        return cls._GECIKME
    @classmethod
    def animasyonTekrar(cls):
        return cls._ANIMASYON_TEKRAR
    @classmethod
    def kareAd(cls):
        return cls._KARE_AD
    @classmethod
    def kareSayi(cls):
        return cls._KARE_SAYI
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

    def konumla(self,x,y):
        self.center_x=x
        self.center_y=y
      
                    
class GozImaj(AnimasyonImaj):#animasyon ve çizim işlemlerinin yürütüleceğin sınıf
    _DIZIN=ImajSabit.DIZIN[ImajTip.GOZ_IMAJ]
    _ATLAS_DOSYA=ImajSabit.ATLAS_DOSYA[ImajTip.GOZ_IMAJ]
    _KARE_AD=ImajSabit.KARE_AD[ImajTip.GOZ_IMAJ]
    _KARE_SAYI=ImajSabit.KARE_SAYI[ImajTip.GOZ_IMAJ]
    _GECIKME=ImajSabit.GECIKME[ImajTip.GOZ_IMAJ]
    _ORIJINAL_BOYUT=ImajSabit.ORIJINAL_BOYUT[ImajTip.GOZ_IMAJ]
    _BOYUT_ORAN=ImajSabit.BOYUT_ORAN[ImajTip.GOZ_IMAJ]
    _ANIMASYON_TEKRAR=ImajSabit.ANIMASYON_TEKRAR[ImajTip.GOZ_IMAJ]

    _atlasYuklendi=False # atlas dosyalarının yüklenip yğklenmediğini kontrol edeceğimiz değişken. Yüklendiğine True olacak
    _kare=ImajSabit.BOS_KARE[ImajTip.GOZ_IMAJ]

    
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
        return cls._ATLAS_DOSYA[tip]
    @classmethod
    def gecikme(cls, aksiyon):
        return cls._GECIKME[aksiyon]
    @classmethod
    def animasyonTekrar(cls, aksiyon):
        return cls._ANIMASYON_TEKRAR[aksiyon]
    @classmethod
    def kareAd(cls,aksiyon,yon):
        return cls._KARE_AD[yon][aksiyon]
    @classmethod
    def kareSayi(cls,aksiyon,yon):
        return cls._KARE_SAYI[yon][aksiyon]
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
        

    def guncelleOlculer(self,hucreX,hucreY,hucreBoyut,kenarlikTam):#canvas içerisine çizilecek labirentin genişlik, yükseklik, x, y vs değerleri hesaplanıyor
        self.width=hucreBoyut*GozImaj.boyutOran()
        self.height=self.width
        
        self.konumla(hucreX,hucreY)

        
        gitAdimSag=(hucreBoyut+kenarlikTam)/(GozImaj.kareSayi(GozAksiyon.GIT,Yon.SAG)*GozImaj.animasyonTekrar(GozAksiyon.GIT))
        gitAdimSol=(hucreBoyut+kenarlikTam)/(GozImaj.kareSayi(GozAksiyon.GIT,Yon.SOL)*GozImaj.animasyonTekrar(GozAksiyon.GIT))
        gitAdimUst=(hucreBoyut+kenarlikTam)/(GozImaj.kareSayi(GozAksiyon.GIT,Yon.UST)*GozImaj.animasyonTekrar(GozAksiyon.GIT))
        gitAdimAlt=(hucreBoyut+kenarlikTam)/(GozImaj.kareSayi(GozAksiyon.GIT,Yon.ALT)*GozImaj.animasyonTekrar(GozAksiyon.GIT))


        self.__gitAdim={Yon.SAG: (gitAdimSag, 0),Yon.SOL: (-gitAdimSol, 0),Yon.UST: (0, gitAdimUst),Yon.ALT: (0, -gitAdimAlt)}

    def konumla(self,x,y):
        self.center_x=x
        self.center_y=y


        
        
        
