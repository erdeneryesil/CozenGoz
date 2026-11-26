#KIVY DOSYA VE GRAFİK YÖNETİMİ

from abc import ABCMeta, abstractmethod

from kivy.uix.image import Image,CoreImage
from kivy.clock import Clock
from kivy.atlas import Atlas
from kivy.graphics import Color, Line, Ellipse, Fbo, Rectangle

from sabitler import DuvarDurum,HucreSabit,EkranSabit,LabirentSabit,ImajTip,ImajSabit,GozTip,GozAksiyon,Yon,DikdortgenTip,HucreNokta
from temel import Konum

class KaynakYukleyici:
    @staticmethod
    def atlas_dosya(imaj_sinif,aksiyon_sinif=None,tip_sinif=None,yon_sinif=None):
        #imaj_sinif.atlas_yuklendi_guncelle(False)
    
        # Başlangıçta durum tespiti yaparak döngü içindeki 'if' yükünü azaltıyoruz
        aksiyonlar= aksiyon_sinif if aksiyon_sinif else [None]
        tipler = tip_sinif if tip_sinif else [None]
        yonler = yon_sinif if yon_sinif else [None]
        dizin = imaj_sinif.dizin()
        
        for tip in tipler:
            atlas_ad = imaj_sinif.atlas_dosya() if tip is None else imaj_sinif.atlas_dosya(tip)
            atlas = Atlas(f"{dizin}/{atlas_ad}")

            for yon in yonler:
                for aksiyon in aksiyonlar:
                    # Parametre yapısına göre metod seçimi
                    if yon_sinif:
                        kare_ad_numarasiz = imaj_sinif.kare_ad(aksiyon,yon)
                        kare_sayisi = imaj_sinif.kare_sayisi(aksiyon,yon)
                    else:
                        if aksiyon:
                            kare_ad_numarasiz = imaj_sinif.kare_ad(aksiyon)
                            kare_sayisi = imaj_sinif.kare_sayisi(aksiyon)
                        else:
                            kare_ad_numarasiz = imaj_sinif.kare_ad()
                            kare_sayisi = imaj_sinif.kare_sayisi()

                    for kare_numara in range(kare_sayisi):
                        kare_ad = f"{kare_ad_numarasiz}{kare_numara}"
                        
                        # Atlas içinden resmi çek ve dönüştür
                        ham_kare = CoreImage(atlas[kare_ad])
                        
                        # Ekleme işlemini duruma göre yap
                        if tip_sinif and yon_sinif:
                            imaj_sinif.kare_ekle(ham_kare,aksiyon,tip, yon)
                        else:
                            imaj_sinif.kare_ekle(ham_kare)

class StatikImaj(Image):
    #Canvas imajın tamamı, kenar boşlukları dahil
    #Render imajın içeriği, kenar boşluklarından arındırılmış hali

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.allow_stretch=True
        self.keep_ratio=True

        #ilk oluşturulan görsele ait nitelikler. Canvas çizim alanı(kenar boşlukları içerir), Render çizimin kendisi(kenar boşlukları içermez)
        self._gercek_genislik_canvas=-1
        self._gercek_yukseklik_canvas=-1
        self._gercek_genislik_render=-1
        self._gercek_yukseklik_render=-1
        self._gercek_sol_x_render=-1
        self._gercek_alt_y_render=-1
        self._gercek_ust_y_render=-1

    def _gercek_degerler_hesapla(self):
        raise NotImplementedError("_gercek değerler, alt sınıflarda hesaplanmalıdır!")
    def _texture_olustur(self):
        raise NotImplementedError("texture oluşturma işlemi alt sınıflarda yapılmalıdır")
    
    #_guncel_genislik_canvas,_guncel_yukseklik_canvas,_guncel_sol_x_canvas,_guncel_ust_y_canvas değerleri; görselin bir Widget olarak sahip olduğu değerlerdir. Kenar boşlukları dahildir
    @property
    def _guncel_genislik_canvas(self):
        return self.size[0]
    @property
    def _guncel_yukseklik_canvas(self):
        return self.size[1]
    def _guncel_sol_x_canvas(self,ebeveyn):#ebeveyn:içinde bulunduğu widget
        return ebeveyn.x+(ebeveyn.width-self._guncel_genislik_canvas)/2
    def _guncel_alt_y_canvas(self,ebeveyn):#ebeveyn:içinde bulunduğu widget
        return ebeveyn.y+(ebeveyn.height-self._guncel_yukseklik_canvas)/2
    def _guncel_ust_y_canvas(self,ebeveyn):#ebeveyn:içinde bulunduğu widget
        return ebeveyn.y+self._guncel_yukseklik_canvas+(ebeveyn.height-self._guncel_yukseklik_canvas)/2
    
    #_guncel_genislik_render,_guncel_yukseklik_render,_guncel_sol_x_render,_guncel_ust_y_render değerleri; görselin gerçek çizim değerleridir. Kenar boşluklarından arındırılmıştır
    @property
    def _guncel_genislik_render(self):
        return self._guncel_genislik_canvas*(self._gercek_genislik_render/self._gercek_genislik_canvas)
    @property
    def _guncel_yukseklik_render(self):
        return self._guncel_yukseklik_canvas*(self._gercek_yukseklik_render/self._gercek_yukseklik_canvas)
    
    def _guncel_sol_x_render(self,ebeveyn):
        return self._guncel_sol_x_canvas(ebeveyn)+(self._guncel_genislik_canvas-self._guncel_genislik_render)/2#kenarlık kalınlığı hesaba dahil edilmiyor
    def _guncel_alt_y_render(self,ebeveyn):
        return self._guncel_alt_y_canvas(ebeveyn)+(self._guncel_yukseklik_canvas-self._guncel_yukseklik_render)/2#kenarlık kalınlığı hesaba dahil edilmiyor
    def _guncel_ust_y_render(self,ebeveyn):
        return self._guncel_ust_y_canvas(ebeveyn)-(self._guncel_yukseklik_canvas-self._guncel_yukseklik_render)/2#kenarlık kalınlığı hesaba dahil edilmiyor
    
class LabirentStatikImaj(StatikImaj):
    #Canvas imajın tamamı, kenar boşlukları dahil
    #Render imajın içeriği, kenar boşluklarından arındırılmış hali
    def __init__(self,labirent,**kwargs):
        super().__init__(**kwargs)

        self.__labirent=labirent
        
        self._gercek_kenarlik_yarim=-1
        self._gercek_hucre_boyut=-1
        self._guncel_kenarlik_yarim=-1
        self._guncel_hucre_boyut=-1

        self._gercek_degerler_hesapla()
        self.texture=self._texture_olustur()

    @property
    def _gercek_kenarlik_tam(self):
        return 2*self._gercek_kenarlik_yarim

    @property   #public
    def guncel_hucre_boyut(self):
        return self._guncel_hucre_boyut
    
    @property   #public
    def guncel_kenarlik_tam(self):
        return 2*self._guncel_kenarlik_yarim

    def guncelle_olculer(self,saha):#canvas içerisine çizilecek labirentin genişlik, yükseklik, x, y vs değerleri hesaplanıyor        
        genislik,yukseklik=self.__olcekle(saha.width,saha.height)

        self.size=(genislik,yukseklik)
        self.pos=(self._guncel_sol_x_canvas(saha),self._guncel_ust_y_canvas(saha)-yukseklik)
        
        if self.__labirent.dikdortgen_tip==DikdortgenTip.YATAY:
            self._guncel_kenarlik_yarim=self.__hesapla_kenarlik_yarim(self._guncel_genislik_canvas,self.__labirent.sutun_sayisi)
        else:
            self._guncel_kenarlik_yarim=self.__hesapla_kenarlik_yarim(self._guncel_yukseklik_canvas,self.__labirent.satir_sayisi)

        self._guncel_hucre_boyut=self.__hesapla_hucre_boyut(self._guncel_genislik_render,self.__labirent.sutun_sayisi,self.guncel_kenarlik_tam)

    def hucre_x_y(self,hucre_nokta,hucre,saha=None):#konumu verilen hücreye; robotu, sensörleri vs. çizebilmek için gerekli koordinatlar   
        if saha is None:#texture oluşturulur iken
            sol_x=self._gercek_sol_x_render
            ust_y=self._gercek_ust_y_render
            alt_y=self._gercek_alt_y_render
            genislik=self._gercek_genislik_render
            yukseklik=self._gercek_yukseklik_render
            hucre_boyut=self._gercek_hucre_boyut
            kenarlik_yarim=self._gercek_kenarlik_yarim
        else:        
            sol_x=self._guncel_sol_x_render(saha)
            ust_y=self._guncel_ust_y_render(saha)
            alt_y=self._guncel_alt_y_render(saha)
            genislik=self._guncel_genislik_render
            yukseklik=self._guncel_yukseklik_render
            hucre_boyut=self._guncel_hucre_boyut
            kenarlik_yarim=self._guncel_kenarlik_yarim

        temel_sol_x=sol_x+(hucre.sutun_numarasi)*(genislik/self.__labirent.sutun_sayisi)
        temel_sag_x=sol_x+(hucre.sutun_numarasi+1)*(genislik/self.__labirent.sutun_sayisi)
        temel_ust_y=ust_y-(hucre.satir_numarasi+1)*(yukseklik/self.__labirent.satir_sayisi)
        temel_alt_y=alt_y+(self.__labirent.satir_sayisi-hucre.satir_numarasi)*(yukseklik/self.__labirent.satir_sayisi)

        match hucre_nokta:
            case HucreNokta.MERKEZ:
                x=temel_sol_x+hucre_boyut/2+kenarlik_yarim
                y=temel_ust_y+hucre_boyut/2+kenarlik_yarim
            case HucreNokta.SOL_ALT:
                x=temel_sol_x+kenarlik_yarim
                y=temel_ust_y+kenarlik_yarim
            case HucreNokta.SOL:
                x=temel_sol_x
                y=temel_ust_y+hucre_boyut/2+kenarlik_yarim
            case HucreNokta.ALT:
                x=temel_sol_x+hucre_boyut/2+kenarlik_yarim
                y=temel_ust_y
            case HucreNokta.SAG:
                x=temel_sag_x
                y=temel_ust_y+hucre_boyut/2+kenarlik_yarim
            case HucreNokta.UST:
                x=temel_sol_x+hucre_boyut/2+kenarlik_yarim
                y=temel_alt_y
            case HucreNokta.SAG_ALT:
                x=temel_sag_x-kenarlik_yarim
                y=temel_ust_y+kenarlik_yarim

        return (x,y)
        
    def _gercek_degerler_hesapla(self):#niteliklerin değerleri hesaplanıyor
        maks=EkranSabit.maks_saha_boyut(self.__labirent.dikdortgen_tip)
        maks_saha_genislik=maks[EkranSabit.MAKS_SAHA_GENISLIK_ANAHTAR]
        maks_saha_yukseklik=maks[EkranSabit.MAKS_SAHA_YUKSEKLIK_ANAHTAR]       

        self._gercek_genislik_canvas,self._gercek_yukseklik_canvas=self.__olcekle(maks_saha_genislik,maks_saha_yukseklik)#labirentin çizileceği alanın genişlik ve yükseklik
        
        if self.__labirent.dikdortgen_tip==DikdortgenTip.YATAY:
            self._gercek_kenarlik_yarim=self.__hesapla_kenarlik_yarim(self._gercek_genislik_canvas,self.__labirent.sutun_sayisi)
            print(self._gercek_yukseklik_canvas,self._gercek_kenarlik_yarim)
        else:
            self._gercek_kenarlik_yarim=self.__hesapla_kenarlik_yarim(self._gercek_yukseklik_canvas,self.__labirent.satir_sayisi)
            print(self._gercek_genislik_canvas,self._gercek_kenarlik_yarim)

        hucre_boyut_genislige_gore=self.__hesapla_hucre_boyut(self._gercek_genislik_canvas,self.__labirent.sutun_sayisi,self._gercek_kenarlik_tam)
        hucre_boyut_yukseklige_gore=self.__hesapla_hucre_boyut(self._gercek_yukseklik_canvas,self.__labirent.satir_sayisi,self._gercek_kenarlik_tam)            

        if hucre_boyut_yukseklige_gore<hucre_boyut_genislige_gore:
            self._gercek_yukseklik_render=self._gercek_yukseklik_canvas-EkranSabit.RENDER_KUCULTME_CARPAN*self._gercek_kenarlik_tam
            self._gercek_genislik_render=self._gercek_yukseklik_render*self._gercek_genislik_canvas/self._gercek_yukseklik_canvas
        else:
            self._gercek_genislik_render=self._gercek_genislik_canvas-EkranSabit.RENDER_KUCULTME_CARPAN*self._gercek_kenarlik_tam
            self._gercek_yukseklik_render=self._gercek_genislik_render*self._gercek_yukseklik_canvas/self._gercek_genislik_canvas

        self._gercek_hucre_boyut=self.__hesapla_hucre_boyut(self._gercek_genislik_render,self.__labirent.sutun_sayisi,self._gercek_kenarlik_tam)

        self._gercek_sol_x_render=(self._gercek_genislik_canvas-self._gercek_genislik_render)/2    #labirentin sol kenarının ortası (kenarlığın ortası)   
        self._gercek_alt_y_render=((self._gercek_yukseklik_canvas-self._gercek_yukseklik_render)/2) #labirentin alt kenarının ortası (kenarlığın ortası)
        self._gercek_ust_y_render=self._gercek_yukseklik_canvas-((self._gercek_yukseklik_canvas-self._gercek_yukseklik_render)/2) #labirentin üst kenarının ortası (kenarlığın ortası)

    def _texture_olustur(self):
        #labirent görselini, maks boyutlara göre bir kez oluşturup, sonrasında ölçekleniyor
        fbo = Fbo(size=(self._gercek_genislik_canvas, self._gercek_yukseklik_canvas))
        
        # Kivy Fbo varsayılan olarak transparan gelebilir. Arka planı temizliyoruz.
        fbo.clear_buffer()

        with fbo:
            #self.__izgara_ciz()
            #Color(0.07, 0.09, 0.12, 1)
            Color(rgba=LabirentSabit.KENARLIK_RENK)
            self.__ciz_cerceve()

            # Duvarların çizimi
            self.__ciz_duvar()
            
            # Çözüm yolu veya Başlangıç/Bitiş hücrelerinin boyanması
            hucre_tip=HucreSabit.TIP[HucreSabit.TIP_YOL_ANAHTAR]
            for hucre_numara in range(self.__labirent.cozum_yolu_uzunlugu):
                self.__boya_hucre(self.__labirent.cozum_yolu_hucre(hucre_numara),hucre_tip[HucreSabit.TIP_UZUNLUK_CARPAN_ANAHTAR],hucre_tip[HucreSabit.TIP_RENK_ANAHTAR])

            hucre_tip=HucreSabit.TIP[HucreSabit.TIP_BASLANGIC_ANAHTAR]
            self.__boya_hucre(Konum(self.__labirent.baslangic_satir_numarasi,self.__labirent.baslangic_sutun_numarasi),hucre_tip[HucreSabit.TIP_UZUNLUK_CARPAN_ANAHTAR],hucre_tip[HucreSabit.TIP_RENK_ANAHTAR])

            hucre_tip=HucreSabit.TIP[HucreSabit.TIP_BITIS_ANAHTAR]
            self.__boya_hucre(Konum(self.__labirent.bitis_satir_numara,self.__labirent.bitis_sutun_numara),hucre_tip[HucreSabit.TIP_UZUNLUK_CARPAN_ANAHTAR],hucre_tip[HucreSabit.TIP_RENK_ANAHTAR])

        fbo.draw()

        return fbo.texture

    def __olcekle(self,saha_genislik,saha_yukseklik):#sahanın boyutlarına göre ölçeklenmiş genişlik, yükseklik değerlerini döndürür
        genislik_olcek=saha_genislik/self.__labirent.sutun_sayisi
        yukseklik_olcek=saha_yukseklik/self.__labirent.satir_sayisi
        olcek_faktor=min(genislik_olcek,yukseklik_olcek)

        return (self.__labirent.sutun_sayisi*olcek_faktor,self.__labirent.satir_sayisi*olcek_faktor)

    def __ciz_cerceve(self):
        Line(close="True", width=self._gercek_kenarlik_yarim,rectangle=(self._gercek_sol_x_render,self._gercek_alt_y_render, self._gercek_genislik_render, self._gercek_yukseklik_render))

    def __ciz_duvar(self):
        for satir_numarasi in range(self.__labirent.satir_sayisi):
            for sutun_numarasi in range(self.__labirent.sutun_sayisi-1):
                duvar=self.__labirent.duvar(self.__labirent.hucre(satir_numarasi,sutun_numarasi),self.__labirent.hucre(satir_numarasi,sutun_numarasi+1))
                if duvar.durum==DuvarDurum.KAPALI:
                    x,y=self.hucre_x_y(HucreNokta.SOL_ALT,self.__labirent.hucre(satir_numarasi,sutun_numarasi+1))    
                    x-=self._gercek_kenarlik_yarim           
                    y1=y+self._gercek_hucre_boyut+self._gercek_kenarlik_yarim
                    y2=y-self._gercek_kenarlik_yarim                    
                    Line(width=self._gercek_kenarlik_yarim,points=(x,y1,x,y2))

        for sutun_numarasi in range(self.__labirent.sutun_sayisi):
            for satir_numarasi in range(self.__labirent.satir_sayisi-1):
                duvar=self.__labirent.duvar(self.__labirent.hucre(satir_numarasi,sutun_numarasi),self.__labirent.hucre(satir_numarasi+1,sutun_numarasi))
                if duvar.durum==DuvarDurum.KAPALI:
                    x,y=self.hucre_x_y(HucreNokta.SOL_ALT,self.__labirent.hucre(satir_numarasi,sutun_numarasi))
                    y-=self._gercek_kenarlik_yarim
                    x1=x-self._gercek_kenarlik_yarim
                    x2=x+self._gercek_hucre_boyut+self._gercek_kenarlik_yarim
                    Line(width=self._gercek_kenarlik_yarim,points=(x1,y,x2,y))

    def __boya_hucre(self,konum,uzunluk_carpan,renk):
        Color(rgba=renk)        
        olcu=uzunluk_carpan*self._gercek_hucre_boyut

        hucre=self.__labirent.hucre(konum.satir_numarasi,konum.sutun_numarasi)        
        x,y=self.hucre_x_y(HucreNokta.MERKEZ,hucre)
        x-=(olcu/2)
        y-=(olcu/2)

        Ellipse(size=(olcu,olcu),pos=(x,y))

    def __hesapla_kenarlik_yarim(self,olcu,hucre_sayisi):#olcu; genişlik ya da yükseklik. hucre_sayisi; satır ya da sütun sayısı
        return (olcu/EkranSabit.LABIRENT_KENARLIK_YARIM_ORAN)/hucre_sayisi
            
    def __hesapla_hucre_boyut(self,olcu,hucre_sayisi,kenarlik_tam):#olcu; genişlik ya da yükseklik. hucre_sayisi; satır ya da sütun sayısı
        return (olcu+kenarlik_tam-(hucre_sayisi+1)*kenarlik_tam)/(hucre_sayisi)
    
class AnimasyonImaj(Image):
    #SABİTLER
    _DIZIN = None
    _ATLAS_DOSYA = None
    _KARE_AD = None
    _KARE_SAYISI = None
    _GECIKME = None
    _ORIJINAL_BOYUT = None
    _BOYUT_ORAN = None
    _ANIMASYON_TEKRAR = None

    _kare= None
    _atlas_yuklendi = False

    #Aşağıdaki abstract metotlar alt sınıflar tarafından mutlaka override edilmelidir.
    @classmethod
    @abstractmethod
    def atlas_dosya(cls):
        pass
    @classmethod
    @abstractmethod
    def gecikme(cls):
        pass
    @classmethod
    @abstractmethod
    def animasyon_tekrar(cls):
        pass
    @classmethod
    @abstractmethod
    def kare_ad(cls):
        pass
    @classmethod
    @abstractmethod
    def kare_sayisi(cls):
        pass
    @classmethod
    @abstractmethod
    def kare(cls,numara):
        pass
    @classmethod
    @abstractmethod
    def kare_ekle(cls,ham_kare):
        pass
    @classmethod
    @abstractmethod
    def animasyon_suresi(cls):
        pass
    @abstractmethod
    def _animasyon_tik_tak(self,dt):
        pass
    @abstractmethod
    def guncelle_olculer(self):
        pass
    @abstractmethod
    def konumla(self):
        pass

    @classmethod
    def dizin(cls):
        return cls._DIZIN
    @classmethod
    def atlas_yuklendi(cls):
        return cls._atlas_yuklendi
    @classmethod
    def atlas_yuklendi_guncelle(cls, deger):
        cls._atlas_yuklendi = deger
    @classmethod
    def orijinal_boyut(cls):
        return cls._ORIJINAL_BOYUT
    @classmethod
    def boyut_oran(cls):
        return cls._BOYUT_ORAN
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self._kare_sayac=0
        self._animasyon_saat=None
        self._animasyon_tamamlandi=False
        self._animasyon_basladi=False
    
    @property
    def animasyon_basladi(self):
        return self._animasyon_basladi
    def animasyon_basladi_resetle(self):
        self._animasyon_basladi=False
    @property
    def animasyon_tamamlandi(self):
        return self._animasyon_tamamlandi
    def animasyon_tamamlandi_resetle(self):
       self._animasyon_tamamlandi=False

    def animasyon_saat_durdur(self):
        if self._animasyon_saat is not None: 
            self._animasyon_saat.cancel()

class ReseptorImaj(AnimasyonImaj):
    #SABİTLER
    _DIZIN=ImajSabit.DIZIN[ImajTip.RESEPTOR_IMAJ]
    _ATLAS_DOSYA=ImajSabit.ATLAS_DOSYA[ImajTip.RESEPTOR_IMAJ]
    _KARE_AD=ImajSabit.KARE_AD[ImajTip.RESEPTOR_IMAJ]
    _KARE_SAYISI=ImajSabit.KARE_SAYISI[ImajTip.RESEPTOR_IMAJ]
    _GECIKME=ImajSabit.GECIKME[ImajTip.RESEPTOR_IMAJ]
    _ORIJINAL_BOYUT=ImajSabit.ORIJINAL_BOYUT[ImajTip.RESEPTOR_IMAJ]
    _BOYUT_ORAN=ImajSabit.BOYUT_ORAN[ImajTip.RESEPTOR_IMAJ]#hücre genişliğine oranı
    _ANIMASYON_TEKRAR=ImajSabit.ANIMASYON_TEKRAR[ImajTip.RESEPTOR_IMAJ] # Animasyon kaç kere çalışacak
    
    _kare=ImajSabit.BOS_KARE[ImajTip.RESEPTOR_IMAJ]
    _atlas_yuklendi=False # atlas dosyasının yüklenip yüklenmediğini kontrol edeceğimiz değişken. Yüklendiğine True olacak

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        #self.allow_stretch=True
        #self.fit_mode='contain'
        self.size_hint=(None,None)
        self.opacity=0
        
    @classmethod
    def atlas_dosya(cls):
        return cls._ATLAS_DOSYA
    @classmethod
    def gecikme(cls):
        return cls._GECIKME
    @classmethod
    def animasyon_tekrar(cls):
        return cls._ANIMASYON_TEKRAR
    @classmethod
    def kare_ad(cls):
        return cls._KARE_AD
    @classmethod
    def kare_sayisi(cls):
        return cls._KARE_SAYISI
    @classmethod
    def kare(cls,numara):
        return cls._kare[numara]
    @classmethod
    def kare_ekle(cls,ham_kare):
        cls._kare.append(ham_kare)
    @classmethod
    def animasyon_suresi(cls):
        n = cls.kare_sayisi()
        r = cls.animasyon_tekrar()
        delay = cls.gecikme()         
        return n * r * delay
    
    def duvar_acik(self):
        self._animasyon_hazirlik()

    def _animasyon_hazirlik(self):
        self.texture=ReseptorImaj.kare(0).texture#yeni reseptorAksiyonun, ilk karesi alınıyor. Aksiyon geçişinde, önceki durumun karesi kalmasın diye 
        self._kare_sayac=0
        self.opacity=1
        self._animasyon_basladi=True
        if self._animasyon_saat:
            self._animasyon_saat.cancel()
        self._animasyon_saat=Clock.schedule_interval(self._animasyon_tik_tak,ReseptorImaj.gecikme())
    
    def _animasyon_tik_tak(self,dt):
        self.texture=ReseptorImaj.kare(self._kare_sayac%(ReseptorImaj.kare_sayisi())).texture
        self._kare_sayac+=1

        if self._kare_sayac>=ReseptorImaj.kare_sayisi()*ReseptorImaj.animasyon_tekrar():
            self._kare_sayac=0
            self._animasyon_tamamlandi=True
            self.opacity=0
                
    def guncelle_olculer(self,hucre_boyut):#canvas içerisine çizilecek labirentin genişlik, yükseklik, x, y vs değerleri hesaplanıyor
        self.width=hucre_boyut*ReseptorImaj.boyut_oran()
        self.height=self.width
        #self.konumla(hucre_x,hucre_y,hucre_boyut)

    def konumla(self,x,y):
        self.center_x=x
        self.center_y=y
                    
class GozImaj(AnimasyonImaj):#animasyon ve çizim işlemlerinin yürütüleceğin sınıf
    _DIZIN=ImajSabit.DIZIN[ImajTip.GOZ_IMAJ]
    _ATLAS_DOSYA=ImajSabit.ATLAS_DOSYA[ImajTip.GOZ_IMAJ]
    _KARE_AD=ImajSabit.KARE_AD[ImajTip.GOZ_IMAJ]
    _KARE_SAYISI=ImajSabit.KARE_SAYISI[ImajTip.GOZ_IMAJ]
    _GECIKME=ImajSabit.GECIKME[ImajTip.GOZ_IMAJ]
    _ORIJINAL_BOYUT=ImajSabit.ORIJINAL_BOYUT[ImajTip.GOZ_IMAJ]
    _BOYUT_ORAN=ImajSabit.BOYUT_ORAN[ImajTip.GOZ_IMAJ]
    _ANIMASYON_TEKRAR=ImajSabit.ANIMASYON_TEKRAR[ImajTip.GOZ_IMAJ]

    _atlas_yuklendi=False # atlas dosyalarının yüklenip yğklenmediğini kontrol edeceğimiz değişken. Yüklendiğine True olacak
    _kare=ImajSabit.BOS_KARE[ImajTip.GOZ_IMAJ]

    def __init__(self,tip,yon,**kwargs):
        super().__init__(**kwargs)
        self.__dikdortgen_tip=(GozTip)(tip)
        self.__yon=(Yon)(yon)
        self.__aksiyon=None
        self.__yeni_yon=None#yön değiştirilirken, animasyon yeni yöne değil, mevcut olana(self.__yon) göre çalıştırılıyor. Animasyon bittikten sonra self.__yon=self.__yeni_yon olarak güncellenecek 
        
        self.__git_adim={Yon.SAG: (0, 0),Yon.SOL: (0, 0),Yon.UST: (0, 0),Yon.ALT: (0, 0)}

        #self.allow_stretch=True
        #self.fit_mode='contain'
        self.size_hint=(None,None)

        self.__aksiyon_degistir(GozAksiyon.BEKLE)#ilk animasyonu başlat

    @classmethod
    def atlas_dosya(cls, tip):
        return cls._ATLAS_DOSYA[tip]
    @classmethod
    def gecikme(cls, aksiyon):
        return cls._GECIKME[aksiyon]
    @classmethod
    def animasyon_tekrar(cls, aksiyon):
        return cls._ANIMASYON_TEKRAR[aksiyon]
    @classmethod
    def kare_ad(cls,aksiyon,yon):
        return cls._KARE_AD[yon][aksiyon]
    @classmethod
    def kare_sayisi(cls,aksiyon,yon):
        return cls._KARE_SAYISI[yon][aksiyon]
    @classmethod
    def kare(cls,numara,aksiyon,tip,yon):
        return cls._kare[tip][yon][aksiyon][numara]
    @classmethod
    def kare_ekle(cls,ham_kare,aksiyon,tip,yon):
        cls._kare[tip][yon][aksiyon].append(ham_kare)
    @classmethod
    def animasyon_suresi(cls, aksiyon, yon):
        n = cls.kare_sayisi(aksiyon, yon)
        r = cls.animasyon_tekrar(aksiyon)
        delay = cls.gecikme(aksiyon)
        return n * r * delay

    @property
    def dikdortgen_tip(self):
        return self.__dikdortgen_tip
    @property
    def yon(self):
        return self.__yon
        
    def bekle(self):
        self.__aksiyon_degistir(GozAksiyon.BEKLE)

    def sola_don(self):
        self.__aksiyon_degistir(GozAksiyon.SOLA_DON)
        self.__yeni_yon=Yon.sola_don(self.__yon) #dönme animasyonu bittikten sonra self.__yon güncellenecek
                
    def saga_don(self):
        self.__aksiyon_degistir(GozAksiyon.SAGA_DON)
        self.__yeni_yon=Yon.saga_don(self.__yon) #dönme animasyonu bittikten sonra self.__yon güncellenecek

    def git(self):
        self.__aksiyon_degistir(GozAksiyon.GIT)

    @property
    def aksiyon(self):
        return self.__aksiyon
    
    def __aksiyon_degistir(self,aksiyon):
        #bir aksiyon tamamlanmadan, diğer bir aksiyona geçilmek istenirse...
        if self.__aksiyon not in (None,GozAksiyon.BEKLE):
            return
            
        self.__aksiyon=aksiyon
        self._animasyon_hazirlik()
    
    def _animasyon_hazirlik(self):
        self.texture=GozImaj.kare(0,self.__aksiyon,self.__dikdortgen_tip,self.__yon).texture#yeni aksiyonun, ilk karesi alınıyor. Aksiyon geçişinde, önceki durumun karesi kalmasın diye 
        self._kare_sayac=0    
        self._animasyon_basladi=True    
        if self._animasyon_saat:
            self._animasyon_saat.cancel()
        self._animasyon_saat=Clock.schedule_interval(self._animasyon_tik_tak,GozImaj.gecikme(self.__aksiyon))

    def _animasyon_tik_tak(self,dt):
        self.texture=GozImaj.kare(self._kare_sayac%(GozImaj.kare_sayisi(self.__aksiyon,self.__yon)),self.__aksiyon,self.__dikdortgen_tip,self.__yon).texture
        self._kare_sayac+=1

        if self.__aksiyon==GozAksiyon.GIT:
            d_x,d_y=self.__git_adim[self.__yon]
            self.center_x+=d_x
            self.center_y+=d_y

        if self._kare_sayac>=GozImaj.kare_sayisi(self.__aksiyon,self.__yon)*GozImaj.animasyon_tekrar(self.__aksiyon):
            self._kare_sayac=0
            self._animasyon_tamamlandi=True
            if self.__aksiyon==GozAksiyon.GIT:
                pass
            elif self.__aksiyon==GozAksiyon.SOLA_DON or self.__aksiyon==GozAksiyon.SAGA_DON:
                self.__yon=self.__yeni_yon
                
            self.__aksiyon=GozAksiyon.BEKLE
            self._animasyon_hazirlik()
        
    def guncelle_olculer(self,hucre_x,hucre_y,hucre_boyut,kenarlik_tam):#canvas içerisine çizilecek labirentin genişlik, yükseklik, x, y vs değerleri hesaplanıyor
        self.width=hucre_boyut*GozImaj.boyut_oran()
        self.height=self.width
        
        self.konumla(hucre_x,hucre_y)

        git_adim_sag=(hucre_boyut+kenarlik_tam)/(GozImaj.kare_sayisi(GozAksiyon.GIT,Yon.SAG)*GozImaj.animasyon_tekrar(GozAksiyon.GIT))
        git_adim_sol=(hucre_boyut+kenarlik_tam)/(GozImaj.kare_sayisi(GozAksiyon.GIT,Yon.SOL)*GozImaj.animasyon_tekrar(GozAksiyon.GIT))
        git_adim_ust=(hucre_boyut+kenarlik_tam)/(GozImaj.kare_sayisi(GozAksiyon.GIT,Yon.UST)*GozImaj.animasyon_tekrar(GozAksiyon.GIT))
        git_adim_alt=(hucre_boyut+kenarlik_tam)/(GozImaj.kare_sayisi(GozAksiyon.GIT,Yon.ALT)*GozImaj.animasyon_tekrar(GozAksiyon.GIT))

        self.__git_adim={Yon.SAG: (git_adim_sag, 0),Yon.SOL: (-git_adim_sol, 0),Yon.UST: (0, git_adim_ust),Yon.ALT: (0, -git_adim_alt)}

    def konumla(self,x,y):
        self.center_x=x
        self.center_y=y