# SABİT VE GLOBAL SINIFLAR


from enum import IntEnum

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
