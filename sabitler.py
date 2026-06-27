# SABİT VE GLOBAL SINIFLAR


from enum import IntEnum


    
class EkranSabit:
    #uygulama ekranının max boyutları
    __MAX_GENISLIK=3840
    __MAX_YUKSEKLIK=2160
    
    #solPanel,yarismaPanel,sagPanel genişlik oranları
    __SOL_PANEL_GENISLIK_ORAN=.15
    __YARISMA_PANEL_GENISLIK_ORAN=.7 #aynı zamanda, sahanın; ekran genişliğine oranı.
    __SAG_PANEL_GENISLIK_ORAN=.15

    #yarışma panelinde; sahanın altında ve üstünde alan bırakıldı
    __SAHA_YUKSEKLIK_ORAN=.8
    __SAHA_UST_YUKSEKLIK_ORAN=.1
    __SAHA_ALT_YUKSEKLIK_ORAN=.1

    #labirent çizimi ile alakalı değerler
    __LABIRENT_KENARLIK_KALINLIK_ORAN=300

    #saha max boyutlarında iken, sahip olduğu ölçü ve koordinatlar
    __MAX_SAHA_GENISLIK=__MAX_GENISLIK*__YARISMA_PANEL_GENISLIK_ORAN
    __MAX_SAHA_YUKSEKLIK=__MAX_YUKSEKLIK*__SAHA_YUKSEKLIK_ORAN
    __MAX_SAHA_KENARLIK_KALINLIK=__MAX_GENISLIK*__YARISMA_PANEL_GENISLIK_ORAN/__LABIRENT_KENARLIK_KALINLIK_ORAN

    @staticmethod
    def maxSahaHucreKenarUzunluk(sutunSayi):
        return EkranSabit.__MAX_SAHA_GENISLIK/sutunSayi
    
    @staticmethod
    def maxGenislik():
        return EkranSabit.__MAX_GENISLIK
    @staticmethod
    def maxYukseklik():
        return EkranSabit.__MAX_YUKSEKLIK
    
    @staticmethod
    def solPanelGenislikOran():
        return EkranSabit.__SOL_PANEL_GENISLIK_ORAN
    @staticmethod
    def yarismaPanelGenislikOran():
        return EkranSabit.__YARISMA_PANEL_GENISLIK_ORAN
    @staticmethod
    def sagPanelGenislikOran():
        return EkranSabit.__SAG_PANEL_GENISLIK_ORAN
    

    @staticmethod
    def sahaYukseklikOran():
        return EkranSabit.__SAHA_YUKSEKLIK_ORAN
    @staticmethod
    def sahaUstYukseklikOran():
        return EkranSabit.__SAHA_UST_YUKSEKLIK_ORAN
    @staticmethod
    def sahaAltYukseklikOran():
        return EkranSabit.__SAHA_ALT_YUKSEKLIK_ORAN
    
    @staticmethod
    def labirentKenarlikKalinlikOran():
        return EkranSabit.__LABIRENT_KENARLIK_KALINLIK_ORAN
    
    @staticmethod
    def maxSahaGenislik():
        return EkranSabit.__MAX_SAHA_GENISLIK
    @staticmethod
    def maxSahaYukseklik():
        return EkranSabit.__MAX_SAHA_YUKSEKLIK
    @staticmethod
    def maxSahaX():
        return EkranSabit.__maxSahaX
    @staticmethod
    def maxSahaY():
        return EkranSabit.__maxSahaY
    @staticmethod
    def maxSahaNerkezX():
        return EkranSabit.__maxSahaNerkezX
    @staticmethod
    def maxSahaNerkezY():
        return EkranSabit.__maxSahaNerkezY
    @staticmethod
    def maxSahaSolUstX():
        return EkranSabit.__maxSahaSolUstX
    @staticmethod
    def maxSahaSolUstY():
        return EkranSabit.__maxSahaSolUstY
    @staticmethod
    def maxSahaKenarlikKalinlik():
        return EkranSabit.__MAX_SAHA_KENARLIK_KALINLIK


    
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

#reseptörler, gözün neresinde bulunabilir
class ReseptorKonum(IntEnum):#sıralama SOL,ARKA,SAG,ON olmalı. Matematiksel işlemler yapılıyor    
    SOL=0   #Yon.SOL'a tekabül ediyor
    ARKA=1  #Yon.ALT'a tekabül ediyor
    SAG=2   #Yon.SAG'a tekabül ediyor
    ON=3    #Yon.UST'a tekabül ediyor

#Robotun önünün baktığı yön. Robotun varsayılan yönü Yon.UST 
class Yon(IntEnum):#sıralama SOL,ALT,SAG,UST olmalı. Matematiksel işlemler yapılıyor
    SOL=0
    ALT=1
    SAG=2
    UST=3

    __DONUS_ACI=90   #her dönüş 90 derece dönmesi anlamına geliyor
    __BASLANGIC=UST
    
    @staticmethod
    def baslangic():
        return Yon.__BASLANGIC
    
    @staticmethod
    def donusAci():
        return Yon.__DONUS_ACI
    
    @staticmethod
    def solaDon(yon):
        return Yon((yon+1)%len(Yon))
    
    @staticmethod
    def sagaDon(yon):
        return Yon((yon-1)%len(Yon))
    
    def __str__(self):
        return f"YÖN : {self.name}"

#Robotun yapabileceği hamleler
class Hareket(IntEnum):
    SAGA_DON=-1
    ILERI=0
    SOLA_DON=1

class DuvarDurum(IntEnum):
    KAPALI=0
    ACIK=1

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

#Yarışmadaki animasyona ilişkin sabit değerler
class YarisAnimasyon:
    #SABİTLER

    # Epsilon Değeri (Hassas Zamanlama Payı)
    __EPSILON=1/120

    __ANIMASYON_GECIKME=1/60
    __GERI_SAYIM_GECIKME=1

    @staticmethod
    def epsilon():
        return YarisAnimasyon.__EPSILON 
    @staticmethod
    def animasyonGecikme():
        return YarisAnimasyon.__ANIMASYON_GECIKME
    @staticmethod
    def geriSayimGecikme():
        return YarisAnimasyon.__GERI_SAYIM_GECIKME 