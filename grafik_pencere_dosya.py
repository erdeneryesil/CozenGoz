#KIVY PENCERE, DOSYA VE GRAFİK YÖNETİMİ

from abc import ABCMeta, abstractmethod

from kivy.uix.image import Image,CoreImage
from kivy.clock import Clock
from kivy.atlas import Atlas
from kivy.graphics import Color, Line, Ellipse, Fbo, Rectangle

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

        #ilk oluşturulan görsele ait nitelikler
        self._gercekGenislikImageWidget=-1
        self._gercekYukseklikImageWidget=-1
        self._gercekGenislikRender=-1
        self._gercekYukseklikRender=-1
        self._gercekSolX=-1
        self._gercekAltY=-1
        self._gercekUstY=-1

    def _gercekDegerlerHesapla(self):
        raise NotImplementedError("_gercek değerler, alt sınıflarda hesaplanmalıdır!")
    def _textureOlustur(self):
        raise NotImplementedError("texture oluşturma işlemi alt sınıflarda yapılmalıdır")
    
    @property
    def gercekGenislikImageWidget(self):
        return self._gercekGenislikImageWidget
    @property
    def gercekYukseklikImageWidget(self):
        return self._gercekYukseklikImageWidget
    @property
    def gercekGenislikRender(self):
        return self._gercekGenislikRender
    @property
    def gercekYukseklikRender(self):
        return self._gercekYukseklikRender
    
    #guncelGenislikImageWidget,guncelYukseklikImageWidget,solXImageWidget,ustYImageWidget değerleri; görselin bir Widget olarak sahip olduğu değerlerdir. Kenar boşlukları dahildir
    @property
    def guncelGenislikImageWidget(self):
        return self.size[0]
    @property
    def guncelYukseklikImageWidget(self):
        return self.size[1]
    def solXImageWidget(self,ebeveyn):#ebeveyn:içinde bulunduğu widget
        return ebeveyn.x+(ebeveyn.width-self.guncelGenislikImageWidget)/2
    def ustYImageWidget(self,ebeveyn):#ebeveyn:içinde bulunduğu widget
        return self.guncelYukseklikImageWidget+ebeveyn.y+(ebeveyn.height-self.guncelYukseklikImageWidget)/2
    
    #guncelGenislikRender,guncelYukseklikRender,solXRender,ustYRender değerleri; görselin gerçek çizim değerleridir. Kenar boşluklarından arındırılmıştır
    @property
    def guncelGenislikRender(self):
        return self.norm_image_size[0]
    @property
    def guncelYukseklikRender(self):
        return self.norm_image_size[1]
    
    def solXRender(self,ebeveyn):
        return ebeveyn.x+(ebeveyn.width-self.guncelGenislikRender)/2
    def ustYRender(self,ebeveyn):
        return self.guncelYukseklikRender+ebeveyn.y+(ebeveyn.height-self.guncelYukseklikRender)/2
    

class LabirentStatikImaj(StatikImaj):
    def __init__(self,labirent,**kwargs):
        super().__init__(**kwargs)

        self.__labirent=labirent
        
        self.__gercekKenarlikKalinlik=-1
        self.__gercekHucreKenarUzunluk=-1
        self.__guncelKenarlikKalinlik=-1
        self.__guncelHucreKenarUzunluk=-1

        self._gercekDegerlerHesapla()
        self.texture=self._textureOlustur()

    @property
    def gercekKenarlikKalinlik(self):
        return self.__gercekKenarlikKalinlik
    @property
    def gercekHucreKenarUzunluk(self):
        return self.__gercekHucreKenarUzunluk
    @property
    def guncelHucreKenarUzunluk(self):
        return self.__guncelHucreKenarUzunluk
    @property
    def guncelKenarlikKalinlik(self):
        return self.__guncelKenarlikKalinlik

    def guncelleOlculer(self,saha):#canvas içerisine çizilecek labirentin genişlik, yükseklik, x, y vs değerleri hesaplanıyor        
        
        genislik,yukseklik=self.__olcekle(saha.width,saha.height)

        self.size=(genislik,yukseklik)
        self.pos=(self.solXImageWidget(saha),self.ustYImageWidget(saha)-yukseklik)
        
        
        
        match self.__labirent.tip:
            case DikdortgenTip.YATAY:
                self.__guncelKenarlikKalinlik=self.__hesaplaKenarlikKalinlik(self.guncelYukseklikRender)
                self.__guncelHucreKenarUzunluk=self.__hesaplaHucreKenarUzunluk(self.guncelGenislikRender,self.__labirent.sutunSayi,self.__guncelKenarlikKalinlik)

            case DikdortgenTip.DIKEY:
                self.__guncelKenarlikKalinlik=self.__hesaplaKenarlikKalinlik(self.guncelGenislikRender)
                self.__guncelHucreKenarUzunluk=self.__hesaplaHucreKenarUzunluk(self.guncelYukseklikRender,self.__labirent.satirSayi,self.__guncelKenarlikKalinlik)
            case DikdortgenTip.KARE:
                self.__guncelKenarlikKalinlik=self.__hesaplaKenarlikKalinlik(self.guncelGenislikRender)
                self.__guncelHucreKenarUzunluk=self.__hesaplaHucreKenarUzunluk(self.guncelYukseklikRender,self.__labirent.satirSayi,self.__guncelKenarlikKalinlik)

        #print(self.__guncelHucreKenarUzunluk/self.__guncelKenarlikKalinlik)
        
        #from grafik_pencere_dosya import StatikImaj
        #i=StatikImaj()
        #i._gercekDegerlerHesapla()
        #self.__orijinalKenarlikKalinlik=self.__orijinalGenislikImageWidget/EkranSabit.LABIRENT_KENARLIK_KALINLIK_ORAN
        #print(self.orijinalKenarlikKalinlik,self.__guncelKenarlikKalinlik)
        #print(self.genislikImageWidget/self.kenarlikKalinlik)


        #print(self.__guncelKenarlikKalinlik,self.genislikRender)
        #print(solX,self.solX(saha))
        #print(saha.width,genislik,saha.height,yukseklik)
        #print(genislik,self.genislik,self.width)
        #print(yukseklik,self.yukseklik,self.height)

    def hucreXY(self,hucre,saha):#konumu verilen hücreye, robotu çizebilmek için gerekli koordinatlar   
        solX=self.solXRender(saha)
        ustY=self.ustYRender(saha)
        x=solX+self.__guncelKenarlikKalinlik+hucre.sutunNumara*(self.__guncelHucreKenarUzunluk)   
        y=ustY-self.__guncelKenarlikKalinlik-self.__guncelHucreKenarUzunluk
        

        return (x,y)

    def _gercekDegerlerHesapla(self):#niteliklerin değerleri hesaplanıyor
        maks=EkranSabit.maksSahaBoyut(self.__labirent.tip)
        maksSahaGenislik=maks[EkranSabit.MAKS_SAHA_GENISLIK_ANAHTAR]
        maksSahaYukseklik=maks[EkranSabit.MAKS_SAHA_YUKSEKLIK_ANAHTAR]

        '''_gercekGenislikImageWidget,_gercekYukseklikImageWidget ve _gercekGenislikRender,_gercekYukseklikRender değişkenleri ile alakalı açıklama:

        Image nesneleri bir widget içerisinde görüntülenirken, içinde bulunduğu widget nesnesine göre boyutlandırılıp, konumlandırılabiliyor.
        Fakat gerçek boyut(size,width,height) ve konum(pos,x,y) verileri yanıltıcı değerler içerebiliyor.

        size Niteliği (Widget(Image) Boyutu) (_gercekGenislikImageWidget,_gercekYukseklikImageWidget değişkenleri)
        Tanım: Image nesnesinin (yani UI üzerindeki widget sınırlarının) genişlik ve yükseklik değeridir.
        Davranış: Bu, Image nesnesinin arayüzde kapladığı toplam kutu boyutudur.
        Özellik: İstediğiniz gibi manuel olarak (size: 400, 300 şeklinde) değiştirebilirsiniz. Resmin en-boy oranına (aspect ratio) uyup uymadığına bakılmaksızın doğrudan widget'ın sınırlarını belirler.

        norm_image_size Niteliği (Normalize Edilmiş Resim Boyutu) (_gercekGenislikRender,_gercekYukseklikRender değişkenleri)
        Tanım: Resmin, allow_stretch=True ve keep_ratio=True (varsayılan değerlerdir) kurallarına bağlı kalarak, widget sınırları (size) içine sığdırıldığı gerçek render (çizim) boyutudur.
        Davranış:
        Kivy, resmin gercek oranını (en/boy oranını) bozmamak için resmi ölçeklendirir.
        Eğer widget'ınızın en-boy oranı ile resmin gercek en-boy oranı birebir aynı değilse, norm_image_size değeri size değerinden küçük olacaktır.
        Boş kalan kısımlar ise şeffaf alanlar olarak kalır (veya resim bu boyutta çizilir).'''
        

        self._gercekGenislikImageWidget,self._gercekYukseklikImageWidget=self.__olcekle(maksSahaGenislik,maksSahaYukseklik)#labirentin çizileceği alanın genişlik ve yükseklik
        
        # alt-üst(2+2), sol-sağ(2+2) taraflardan kenarlık kalınlığının 2 katı kadar küçültme yapılacak
        #texture ait  genişlik ve yükseklik, canvas'a göre küçültülecek. Fakat bu küçültmenin oranı genişlik ve yüksekliğe göre aynı olmalı (*self._gercekYukseklikImageWidget/canvasGenislik)
        if self.__labirent.tip==DikdortgenTip.YATAY:
            self.__gercekKenarlikKalinlik=self.__hesaplaKenarlikKalinlik(self._gercekYukseklikImageWidget)
        elif self.__labirent.tip==DikdortgenTip.DIKEY:   
            self.__gercekKenarlikKalinlik=self.__hesaplaKenarlikKalinlik(self._gercekGenislikImageWidget)
        elif self.__labirent.tip==DikdortgenTip.KARE:
            self.__gercekKenarlikKalinlik=self.__hesaplaKenarlikKalinlik(self._gercekGenislikImageWidget)





        hucreBoyutGenisligeGore=self.__hesaplaHucreKenarUzunluk(self._gercekGenislikImageWidget,self.__labirent.sutunSayi,self.__gercekKenarlikKalinlik)
        hucreBoyutYuksekligeGore=self.__hesaplaHucreKenarUzunluk(self._gercekYukseklikImageWidget,self.__labirent.satirSayi,self.__gercekKenarlikKalinlik)            

        if hucreBoyutYuksekligeGore<hucreBoyutGenisligeGore:
            self.__gercekHucreKenarUzunluk=hucreBoyutYuksekligeGore
            self._gercekYukseklikRender=self._gercekYukseklikImageWidget-EkranSabit.TEXTURE_KUCULTME_CARPAN_2_KENAR*self.__gercekKenarlikKalinlik
            self._gercekGenislikRender=self._gercekYukseklikRender*self._gercekGenislikImageWidget/self._gercekYukseklikImageWidget
        else:
            self.__gercekHucreKenarUzunluk=hucreBoyutGenisligeGore
            self._gercekGenislikRender=self._gercekGenislikImageWidget-EkranSabit.TEXTURE_KUCULTME_CARPAN_2_KENAR*self.__gercekKenarlikKalinlik
            self._gercekYukseklikRender=self._gercekGenislikRender*self._gercekYukseklikImageWidget/self._gercekGenislikImageWidget

        self._gercekSolX=self.__gercekKenarlikKalinlik+(self._gercekGenislikImageWidget-self._gercekGenislikRender)/2
        self._gercekAltY=((self._gercekYukseklikImageWidget-self.gercekYukseklikRender)/2)+self.__gercekKenarlikKalinlik
        self._gercekUstY=self._gercekYukseklikImageWidget-self.__gercekKenarlikKalinlik-((self._gercekYukseklikImageWidget-self.gercekYukseklikRender)/2)



    def _textureOlustur(self):
        #labirent görselini, maks boyutlara göre bir kez oluşturup, sonrasında ölçekleniyor

        #solX=EkranSabit.TEXTURE_KUCULTME_CARPAN_2_KENAR*self.__gercekKenarlikKalinlik+self.__gercekKenarlikKalinlik#self.__gercekKenarlikKalinlik#EkranSabit.TEXTURE_KUCULTME_CARPAN_1_KENAR*self.__gercekKenarlikKalinlik
        #ustY=self._gercekYukseklikRender-self.__gercekKenarlikKalinlik

        
        fbo = Fbo(size=(self._gercekGenislikImageWidget, self._gercekYukseklikImageWidget))
        #fbo = Fbo(size=(self._gercekGenislikRender, self._gercekYukseklikRender))
        



        # Kivy Fbo varsayılan olarak transparan gelebilir. Arka planı temizliyoruz.
        fbo.clear_buffer()


        # 2. Çizim komutlarını Fbo canvas'ına ekliyoruz
        with fbo:


            
            # Kenarlık rengi ve çerçeve çizimi
            textureX = self._gercekSolX
            textureY = self._gercekUstY-self._gercekYukseklikRender+2*self.__gercekKenarlikKalinlik


            Color(rgba=LabirentSabit.KENARLIK_RENK)
            self.__cizCerceve(self._gercekSolX,self._gercekAltY,self._gercekGenislikRender,self._gercekYukseklikRender)

            # Duvarların çizimi
            self.__cizDuvar(self._gercekSolX,self._gercekUstY)
            
            # Çözüm yolu veya Başlangıç/Bitiş hücrelerinin boyanması
            hucreTip=HucreSabit.TIP[HucreSabit.TIP_YOL_ANAHTAR]
            #for hucre in self.__cozumYolu:
                #self.__boyaHucre(labirent,solX,ustY,hucre,hucreTip[HucreSabit.TIP_UZUNLUK_CARPAN_ANAHTAR],hucreTip[HucreSabit.TIP_RENK_ANAHTAR])
            for hucreNumara in range(self.__labirent.cozumYoluUzunluk):
                pass#self.__boyaHucre(solX,ustY,self.__labirent.cozumYoluHucre(hucreNumara),hucreTip[HucreSabit.TIP_UZUNLUK_CARPAN_ANAHTAR],hucreTip[HucreSabit.TIP_RENK_ANAHTAR])


            hucreTip=HucreSabit.TIP[HucreSabit.TIP_BASLANGIC_ANAHTAR]
            pass#self.__boyaHucre(solX,ustY,Konum(self.__labirent.baslangicSatirNumara,self.__labirent.baslangicSutunNumara),hucreTip[HucreSabit.TIP_UZUNLUK_CARPAN_ANAHTAR],hucreTip[HucreSabit.TIP_RENK_ANAHTAR])
            
            hucreTip=HucreSabit.TIP[HucreSabit.TIP_BITIS_ANAHTAR]
            pass#self.__boyaHucre(solX,ustY,Konum(self.__labirent.bitisSatirNumara,self.__labirent.bitisSutunNumara),hucreTip[HucreSabit.TIP_UZUNLUK_CARPAN_ANAHTAR],hucreTip[HucreSabit.TIP_RENK_ANAHTAR])



            Color(1,1,1,1)
            #Rectangle(size=(self.__gercekKenarlikKalinlik,self.__gercekKenarlikKalinlik),pos=(self._gercekSolX-self.__gercekKenarlikKalinlik/2,self._gercekUstY-self.__gercekKenarlikKalinlik))
            x=self._gercekSolX
            y=self._gercekUstY
            Line(width=self.__gercekKenarlikKalinlik,points=(x,self._gercekUstY,x+self.__gercekKenarlikKalinlik,self._gercekUstY))
            Line(width=self.__gercekKenarlikKalinlik,points=(x,self._gercekAltY,x+self.__gercekKenarlikKalinlik,self._gercekAltY))

            Color(0,0,0,1)
            Rectangle(size=(2*self.__gercekKenarlikKalinlik,2*self.__gercekKenarlikKalinlik),pos=(self._gercekSolX-self.__gercekKenarlikKalinlik,self._gercekUstY-self.__gercekKenarlikKalinlik))

        # 3. Fbo üzerindeki çizimleri ekrana yansıtılmaya hazır bir doku (texture) olarak çekiyoruz
        fbo.draw()

        return fbo.texture

    def __olcekle(self,sahaGenislik,sahaYukseklik):#sahanın boyutlarına göre ölçeklenmiş genişlik, yükseklik değerlerini döndürür
        genislikOlcek=sahaGenislik/self.__labirent.sutunSayi
        yukseklikOlcek=sahaYukseklik/self.__labirent.satirSayi
        olcekFaktor=min(genislikOlcek,yukseklikOlcek)

        return (self.__labirent.sutunSayi*olcekFaktor,self.__labirent.satirSayi*olcekFaktor)

    def __cizCerceve(self,x,y,genislik,yukseklik):
                
        Line(close="True", width=self.__gercekKenarlikKalinlik,rectangle=(x,y, genislik-2*self.__gercekKenarlikKalinlik, yukseklik-2*self.__gercekKenarlikKalinlik))

    def __cizDuvar(self,solX,ustY):



        Color(0,0,0,1)
        for satirNumara in range(self.__labirent.satirSayi):
            for sutunNumara in range(self.__labirent.sutunSayi-1):
                duvar=self.__labirent.duvar(self.__labirent.hucre(satirNumara,sutunNumara),self.__labirent.hucre(satirNumara,sutunNumara+1))
                if duvar.durum==DuvarDurum.KAPALI:
                    #x=solX+self.__gercekHucreKenarUzunluk*(sutunNumara+1)
                    
                    x=solX+1*self.__gercekKenarlikKalinlik+(self.__gercekHucreKenarUzunluk+2*self.__gercekKenarlikKalinlik)*(sutunNumara+1)                    
                    y1=ustY-(1*self.__gercekKenarlikKalinlik)-(2*self.__gercekKenarlikKalinlik+self.__gercekHucreKenarUzunluk)*satirNumara
                    y2=y1-self.__gercekKenarlikKalinlik-self.__gercekHucreKenarUzunluk
                    #Line(width=self.__gercekKenarlikKalinlik,points=(x,y1,x,y2))

        for sutunNumara in range(self.__labirent.sutunSayi):
            for satirNumara in range(self.__labirent.satirSayi-1):
                duvar=self.__labirent.duvar(self.__labirent.hucre(satirNumara,sutunNumara),self.__labirent.hucre(satirNumara+1,sutunNumara))
                if duvar.durum==DuvarDurum.KAPALI:
                    x1=solX+1*self.__gercekKenarlikKalinlik+(self.__gercekHucreKenarUzunluk+2*self.__gercekKenarlikKalinlik)*sutunNumara
                    y=ustY-(1*self.__gercekKenarlikKalinlik)-(2*self.__gercekKenarlikKalinlik+self.__gercekHucreKenarUzunluk)*(satirNumara+1)
                    x2=x1+self.__gercekHucreKenarUzunluk+self.__gercekKenarlikKalinlik
                    Line(width=self.__gercekKenarlikKalinlik,points=(x1,y,x2,y))


    def __boyaHucre(self,solX,ustY,konum,uzunlukCarpan,renk):
        Color(renk["r"],renk["g"],renk["b"],renk["a"])
        
        hucre=self.__labirent.hucre(konum.satirNumara,konum.sutunNumara)

        x=solX+self.__gercekHucreKenarUzunluk*hucre.sutunNumara+self.__gercekKenarlikKalinlik+self.__gercekHucreKenarUzunluk/2-uzunlukCarpan*self.__gercekHucreKenarUzunluk/2
        y=ustY-self.__gercekKenarlikKalinlik*2-self.__gercekHucreKenarUzunluk*(1+hucre.satirNumara)+self.__gercekKenarlikKalinlik+self.__gercekHucreKenarUzunluk/2-uzunlukCarpan*self.__gercekHucreKenarUzunluk/2

        olcu=uzunlukCarpan*self.__gercekHucreKenarUzunluk-2*self.__gercekKenarlikKalinlik
        Ellipse(size=(olcu,olcu),pos=(x,y))

    def __hesaplaKenarlikKalinlik(self,olcu):#olcu; genişlik ya da yükseklik olacaktır
        return olcu/EkranSabit.LABIRENT_KENARLIK_KALINLIK_ORAN
            
        '''match self.__labirent.tip:
            case DikdortgenTip.YATAY:
                return self.guncelYukseklikRender/EkranSabit.LABIRENT_KENARLIK_KALINLIK_ORAN
            case DikdortgenTip.DIKEY:
                return self.guncelGenislikRender/EkranSabit.LABIRENT_KENARLIK_KALINLIK_ORAN
            case DikdortgenTip.KARE:
                return self.guncelGenislikRender/EkranSabit.LABIRENT_KENARLIK_KALINLIK_ORAN'''

    def __hesaplaHucreKenarUzunluk(self,olcu,hucreSayi,kenarlikKalinlik):#olcu; genişlik ya da yükseklik. hucreSayi; satır ya da sütun sayısı
        return (olcu-(hucreSayi+1)*2*kenarlikKalinlik)/(hucreSayi)
        return olcu/hucreSayi


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
