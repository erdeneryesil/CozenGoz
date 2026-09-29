#KIVY PENCERE, DOSYA VE GRAFİK YÖNETİMİ

from abc import ABCMeta, abstractmethod

from kivy.uix.image import Image,CoreImage
from kivy.clock import Clock
from kivy.atlas import Atlas
from kivy.graphics import Color, Line, Ellipse, Fbo

from sabitler import DuvarDurum,HucreSabit,EkranSabit,LabirentSabit,ImajTip,ImajSabit,GozTip,GozAksiyon,Yon,DikdortgenTip
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
    '''Image nesneleri bir widget içerisinde görüntülenirken, içinde bulunduğu widget nesnesine göre boyutlandırılıp, konumlandırılabiliyor.
    Fakat gerçek boyut(size,width,height) ve konum(pos,x,y) verileri yanıltıcı değerler içerebiliyor.

    size Niteliği (Widget Boyutu)
    Tanım: Image nesnesinin (yani UI üzerindeki widget sınırlarının) genişlik ve yükseklik değeridir.
    Davranış: Bu, Image nesnesinin arayüzde kapladığı toplam kutu boyutudur.
    Özellik: İstediğiniz gibi manuel olarak (size: 400, 300 şeklinde) değiştirebilirsiniz. Resmin en-boy oranına (aspect ratio) uyup uymadığına bakılmaksızın doğrudan widget'ın sınırlarını belirler.

    norm_image_size Niteliği (Normalize Edilmiş Resim Boyutu)
    Tanım: Resmin, allow_stretch=True ve keep_ratio=True (varsayılan değerlerdir) kurallarına bağlı kalarak, widget sınırları (size) içine sığdırıldığı gerçek render (çizim) boyutudur.
    Davranış:
    Kivy, resmin orijinal oranını (en/boy oranını) bozmamak için resmi ölçeklendirir.
    Eğer widget'ınızın en-boy oranı ile resmin orijinal en-boy oranı birebir aynı değilse, norm_image_size değeri size değerinden küçük olacaktır.
    Boş kalan kısımlar ise şeffaf alanlar olarak kalır (veya resim bu boyutta çizilir).

    Bu sebeple Labirent gibi statik görsellerin; ölçeklendirme, konumlandırma gibi işlemlerden sonra boyut ve konum bilgilerine sağlıklı olarak ulaşabilmek için bu sınıf kullanılacak '''
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.allow_stretch=True
        self.keep_ratio=True

    #genislikImageWidget,yukseklikImageWidget,solXImageWidget,ustYImageWidget değerleri; görselin bir Widget olarak sahip olduğu değerlerdir. Kenar boşlukları dahildir
    @property
    def genislikImageWidget(self):
        return self.size[0]
    @property
    def yukseklikImageWidget(self):
        return self.size[1]
    def solXImageWidget(self,ebeveyn):#ebeveyn:içinde bulunduğu widget
        return ebeveyn.x+(ebeveyn.width-self.genislikImageWidget)/2
    def ustYImageWidget(self,ebeveyn):#ebeveyn:içinde bulunduğu widget
        return self.yukseklikImageWidget+ebeveyn.y+(ebeveyn.height-self.yukseklikImageWidget)/2
    
    #genislikRender,yukseklikRender,solXRender,ustYRender değerleri; görselin gerçek çizim değerleridir. Kenar boşluklarından arındırılmıştır
    @property
    def genislikRender(self):
        return self.norm_image_size[0]
    @property
    def yukseklikRender(self):
        return self.norm_image_size[1]
    def solXRender(self,ebeveyn):
        return ebeveyn.x+(ebeveyn.width-self.genislikRender)/2
    def ustYRender(self,ebeveyn):
        return self.yukseklikRender+ebeveyn.y+(ebeveyn.height-self.yukseklikRender)/2
    

    def ebeveynX(self,ebeveyn):#ebeveyn:içinde bulunduğu widget
        return ebeveyn.x
    def ebeveynW(self,ebeveyn):#ebeveyn:içinde bulunduğu widget
        return ebeveyn.width
    def ebeveynY(self,ebeveyn):#ebeveyn:içinde bulunduğu widget
        return ebeveyn.y
    def ebeveynH(self,ebeveyn):#ebeveyn:içinde bulunduğu widget
        return ebeveyn.height
    

class LabirentStatikImaj(StatikImaj):
    def __init__(self,labirent,**kwargs):
        super().__init__(**kwargs)

        #ilk oluşturulan Labirent görseline ait nitelikler
        self.__orijinalGenislikImageWidget=-1
        self.__orijinalYukseklikImageWidget=-1
        self.__orijinalGenislikRender=-1
        self.__orijinalYukseklikRender=-1
        self.__orijinalKenarlikKalinlik=-1
        self.__orijinalHucreKenarUzunluk=-1
        
        self.__orijinalDegerlerHesapla(labirent)

        self.texture=self.__textureOlustur(labirent)


    @property
    def orijinalGenislikImageWidget(self):
        return self.__orijinalGenislikImageWidget
    @property
    def orijinalYukseklikImageWidget(self):
        return self.__orijinalYukseklikImageWidget
    @property
    def orijinalGenislikRender(self):
        return self.__orijinalGenislikRender
    @property
    def orijinalYukseklikRender(self):
        return self.__orijinalYukseklikRender
    @property
    def orijinalKenarlikKalinlik(self):
        return self.__orijinalKenarlikKalinlik
    @property
    def orijinalHucreKenarUzunluk(self):
        return self.__orijinalHucreKenarUzunluk

    
    def __orijinalDegerlerHesapla(self,labirent):#niteliklerin değerleri hesaplanıyor
        maks=EkranSabit.maksSahaKenarlik(labirent.tip)
        maksSahaGenislik=maks[EkranSabit.MAKS_SAHA_GENISLIK_ANAHTAR]
        maksSahaYukseklik=maks[EkranSabit.MAKS_SAHA_YUKSEKLIK_ANAHTAR]
        self.__orijinalKenarlikKalinlik=maks[EkranSabit.MAKS_KENARLIK_KALINLIK_ANAHTAR]

        '''__orijinalGenislikImageWidget,__orijinalYukseklikImageWidget ve __orijinalGenislikRender,__orijinalYukseklikRender değişkenleri ile alakalı açıklama:

        Image nesneleri bir widget içerisinde görüntülenirken, içinde bulunduğu widget nesnesine göre boyutlandırılıp, konumlandırılabiliyor.
        Fakat gerçek boyut(size,width,height) ve konum(pos,x,y) verileri yanıltıcı değerler içerebiliyor.

        size Niteliği (Widget(Image) Boyutu) (__orijinalGenislikImageWidget,__orijinalYukseklikImageWidget değişkenleri)
        Tanım: Image nesnesinin (yani UI üzerindeki widget sınırlarının) genişlik ve yükseklik değeridir.
        Davranış: Bu, Image nesnesinin arayüzde kapladığı toplam kutu boyutudur.
        Özellik: İstediğiniz gibi manuel olarak (size: 400, 300 şeklinde) değiştirebilirsiniz. Resmin en-boy oranına (aspect ratio) uyup uymadığına bakılmaksızın doğrudan widget'ın sınırlarını belirler.

        norm_image_size Niteliği (Normalize Edilmiş Resim Boyutu) (__orijinalGenislikRender,__orijinalYukseklikRender değişkenleri)
        Tanım: Resmin, allow_stretch=True ve keep_ratio=True (varsayılan değerlerdir) kurallarına bağlı kalarak, widget sınırları (size) içine sığdırıldığı gerçek render (çizim) boyutudur.
        Davranış:
        Kivy, resmin orijinal oranını (en/boy oranını) bozmamak için resmi ölçeklendirir.
        Eğer widget'ınızın en-boy oranı ile resmin orijinal en-boy oranı birebir aynı değilse, norm_image_size değeri size değerinden küçük olacaktır.
        Boş kalan kısımlar ise şeffaf alanlar olarak kalır (veya resim bu boyutta çizilir).'''
        

        self.__orijinalGenislikImageWidget,self.__orijinalYukseklikImageWidget=labirent.olcekle(maksSahaGenislik,maksSahaYukseklik)#labirentin çizileceği alanın genişlik ve yükseklik

        # alt-üst(2+2), sol-sağ(2+2) taraflardan kenarlık kalınlığının 2 katı kadar küçültme yapılacak
        #texture ait  genişlik ve yükseklik, canvas'a göre küçültülecek. Fakat bu küçültmenin oranı genişlik ve yüksekliğe göre aynı olmalı (*self.__orijinalYukseklikImageWidget/canvasGenislik)
        if labirent.tip==DikdortgenTip.DIKEY:            
            self.__orijinalYukseklikRender=self.__orijinalYukseklikImageWidget-EkranSabit.TEXTURE_KUCULTME_CARPAN_2_KENAR*self.__orijinalKenarlikKalinlik   
            self.__orijinalGenislikRender=self.__orijinalYukseklikRender*self.__orijinalGenislikImageWidget/self.__orijinalYukseklikImageWidget
            self.__orijinalGenislikImageWidget+=(self.__orijinalYukseklikImageWidget/self.__orijinalGenislikImageWidget)/EkranSabit.TEXTURE_KUCULTME_CARPAN_2_KENAR*self.__orijinalKenarlikKalinlik
        elif labirent.tip==DikdortgenTip.YATAY:
            self.__orijinalGenislikRender=self.__orijinalGenislikImageWidget-(EkranSabit.TEXTURE_KUCULTME_CARPAN_2_KENAR)*self.__orijinalKenarlikKalinlik
            self.__orijinalYukseklikRender=self.__orijinalGenislikRender*self.__orijinalYukseklikImageWidget/self.__orijinalGenislikImageWidget
            self.__orijinalYukseklikImageWidget+=(self.__orijinalGenislikImageWidget/self.__orijinalYukseklikImageWidget)/EkranSabit.TEXTURE_KUCULTME_CARPAN_2_KENAR*self.__orijinalKenarlikKalinlik
        elif labirent.tip==DikdortgenTip.KARE:
            self.__orijinalGenislikRender=self.__orijinalGenislikImageWidget-(EkranSabit.TEXTURE_KUCULTME_CARPAN_2_KENAR)*self.__orijinalKenarlikKalinlik
            self.__orijinalYukseklikRender=self.__orijinalGenislikRender*self.__orijinalYukseklikImageWidget/self.__orijinalGenislikImageWidget
            #self.__orijinalGenislikImageWidget+=(self.__orijinalYukseklikImageWidget/self.__orijinalGenislikImageWidget)/EkranSabit.TEXTURE_KUCULTME_CARPAN_2_KENAR*self.__orijinalKenarlikKalinlik
            #self.__orijinalYukseklikImageWidget+=(self.__orijinalGenislikImageWidget/self.__orijinalYukseklikImageWidget)/EkranSabit.TEXTURE_KUCULTME_CARPAN_2_KENAR*self.__orijinalKenarlikKalinlik

        self.__orijinalHucreKenarUzunluk=labirent.hesaplaHucreKenarUzunluk(self.__orijinalGenislikRender,self.__orijinalYukseklikRender)

    def __textureOlustur(self,labirent):
        #labirent görselini, maks boyutlara göre bir kez oluşturup, sonrasında ölçekleniyor

        solX=EkranSabit.TEXTURE_KUCULTME_CARPAN_1_KENAR*self.__orijinalKenarlikKalinlik
        #ustY=self.__orijinalYukseklikRender+EkranSabit.TEXTURE_KUCULTME_CARPAN_1_KENAR*self.__orijinalKenarlikKalinlik*self.__orijinalYukseklikImageWidget/self.__orijinalGenislikImageWidget 
        ustY=self.__orijinalYukseklikRender+EkranSabit.TEXTURE_KUCULTME_CARPAN_1_KENAR*self.__orijinalKenarlikKalinlik

        
        fbo = Fbo(size=(self.__orijinalGenislikImageWidget, self.__orijinalYukseklikImageWidget))

        # Kivy Fbo varsayılan olarak transparan gelebilir. Arka planı temizliyoruz.
        fbo.clear_buffer()

        # 2. Çizim komutlarını Fbo canvas'ına ekliyoruz
        with fbo:
            # Kenarlık rengi ve çerçeve çizimi
            textureX = solX
            textureY = EkranSabit.TEXTURE_KUCULTME_CARPAN_1_KENAR*self.__orijinalKenarlikKalinlik


            Color(rgba=LabirentSabit.KENARLIK_RENK)
            self.__cizCerceve(textureX,textureY,self.__orijinalGenislikRender,self.__orijinalYukseklikRender)

            # Duvarların çizimi
            self.__cizDuvar(labirent,solX,ustY)
            
            # Çözüm yolu veya Başlangıç/Bitiş hücrelerinin boyanması
            hucreTip=HucreSabit.TIP[HucreSabit.TIP_YOL_ANAHTAR]
            #for hucre in self.__cozumYolu:
                #self.__boyaHucre(labirent,solX,ustY,hucre,hucreTip[HucreSabit.TIP_UZUNLUK_CARPAN_ANAHTAR],hucreTip[HucreSabit.TIP_RENK_ANAHTAR])
            for hucreNumara in range(labirent.cozumYoluUzunluk):
                self.__boyaHucre(labirent,solX,ustY,labirent.cozumYoluHucre(hucreNumara),hucreTip[HucreSabit.TIP_UZUNLUK_CARPAN_ANAHTAR],hucreTip[HucreSabit.TIP_RENK_ANAHTAR])


            hucreTip=HucreSabit.TIP[HucreSabit.TIP_BASLANGIC_ANAHTAR]
            self.__boyaHucre(labirent,solX,ustY,Konum(labirent.baslangicSatirNumara,labirent.baslangicSutunNumara),hucreTip[HucreSabit.TIP_UZUNLUK_CARPAN_ANAHTAR],hucreTip[HucreSabit.TIP_RENK_ANAHTAR])
            
            hucreTip=HucreSabit.TIP[HucreSabit.TIP_BITIS_ANAHTAR]
            self.__boyaHucre(labirent,solX,ustY,Konum(labirent.bitisSatirNumara,labirent.bitisSutunNumara),hucreTip[HucreSabit.TIP_UZUNLUK_CARPAN_ANAHTAR],hucreTip[HucreSabit.TIP_RENK_ANAHTAR])

        # 3. Fbo üzerindeki çizimleri ekrana yansıtılmaya hazır bir doku (texture) olarak çekiyoruz
        fbo.draw()

        return fbo.texture

    def __cizCerceve(self,x,y,genislik,yukseklik):        
        Line(close="True", width=self.__orijinalKenarlikKalinlik,rectangle=(x,y, genislik, yukseklik))

    def __cizDuvar(self,labirent,solX,ustY):
        for satirNumara in range(labirent.satirSayi):
            for sutunNumara in range(labirent.sutunSayi-1):
                duvar=labirent.duvar(labirent.hucre(satirNumara,sutunNumara),labirent.hucre(satirNumara,sutunNumara+1))
                if duvar.durum==DuvarDurum.KAPALI:
                    x=solX+self.__orijinalHucreKenarUzunluk*(sutunNumara+1)
                    y1=ustY-self.__orijinalHucreKenarUzunluk*satirNumara
                    y2=y1-self.__orijinalHucreKenarUzunluk
                    Line(width=self.__orijinalKenarlikKalinlik,points=(x,y1,x,y2))

        for sutunNumara in range(labirent.sutunSayi):
            for satirNumara in range(labirent.satirSayi-1):
                duvar=labirent.duvar(labirent.hucre(satirNumara,sutunNumara),labirent.hucre(satirNumara+1,sutunNumara))
                if duvar.durum==DuvarDurum.KAPALI:
                    x1=solX+self.__orijinalHucreKenarUzunluk*sutunNumara
                    y=ustY-self.__orijinalHucreKenarUzunluk*(satirNumara+1)
                    x2=x1+self.__orijinalHucreKenarUzunluk
                    Line(width=self.__orijinalKenarlikKalinlik,points=(x1,y,x2,y))

    def __boyaHucre(self,labirent,solX,ustY,konum,uzunlukCarpan,renk):
        Color(renk["r"],renk["g"],renk["b"],renk["a"])
        
        hucre=labirent.hucre(konum.satirNumara,konum.sutunNumara)

        x=solX+self.__orijinalHucreKenarUzunluk*hucre.sutunNumara+self.__orijinalKenarlikKalinlik+self.__orijinalHucreKenarUzunluk/2-uzunlukCarpan*self.__orijinalHucreKenarUzunluk/2
        y=ustY-self.__orijinalHucreKenarUzunluk*(1+hucre.satirNumara)+self.__orijinalKenarlikKalinlik+self.__orijinalHucreKenarUzunluk/2-uzunlukCarpan*self.__orijinalHucreKenarUzunluk/2

        boyut=uzunlukCarpan*self.__orijinalHucreKenarUzunluk-2*self.__orijinalKenarlikKalinlik
        Ellipse(size=(boyut,boyut),pos=(x,y))



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
        




    def guncelleOlculer(self,hucreX,hucreY,hucreBoyut,kenarlikKalinlik):#canvas içerisine çizilecek labirentin genişlik, yükseklik, x, y vs değerleri hesaplanıyor
        self.width=hucreBoyut*GozImaj.boyutOran()
        self.height=self.width
        
        self.konumla(hucreX,hucreY,hucreBoyut,kenarlikKalinlik)

        gitAdimSag=hucreBoyut/(GozImaj.kareSayi(GozAksiyon.GIT,Yon.SAG)*GozImaj.animasyonTekrar(GozAksiyon.GIT))
        gitAdimSol=hucreBoyut/(GozImaj.kareSayi(GozAksiyon.GIT,Yon.SOL)*GozImaj.animasyonTekrar(GozAksiyon.GIT))
        gitAdimUst=hucreBoyut/(GozImaj.kareSayi(GozAksiyon.GIT,Yon.UST)*GozImaj.animasyonTekrar(GozAksiyon.GIT))
        gitAdimAlt=hucreBoyut/(GozImaj.kareSayi(GozAksiyon.GIT,Yon.ALT)*GozImaj.animasyonTekrar(GozAksiyon.GIT))

        self.__gitAdim={Yon.SAG: (gitAdimSag, 0),Yon.SOL: (-gitAdimSol, 0),Yon.UST: (0, gitAdimUst),Yon.ALT: (0, -gitAdimAlt)}

    def konumla(self,hucreX,hucreY,hucreBoyut,kenarlikKalinlik):
        self.center_x=hucreX+hucreBoyut/2+kenarlikKalinlik/2
        self.center_y=hucreY+hucreBoyut/2+kenarlikKalinlik/2
