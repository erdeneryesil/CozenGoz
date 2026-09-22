# SABİT VE GLOBAL SINIFLAR

from enum import IntEnum

#IntEnum SINIFLAR

class ImajTip(IntEnum):
    GOZ_IMAJ=0
    RESEPTOR_IMAJ=1
    
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

class DikdortgenTip(IntEnum):#labirent ya da sahanın tipini belirlemek amacıyla kullanılıyor
    KARE=0
    YATAY=1
    DIKEY=2
    def __str__(self):
        return f"Tip : {self.name}"
    
    @staticmethod
    def belirle(genislik,yukseklik):#labirent için genislik:sütun sayısı, yukseklik=satır sayısı
        if yukseklik>genislik:
            return DikdortgenTip.DIKEY
        elif genislik>yukseklik:
            return DikdortgenTip.YATAY
        else:
            return DikdortgenTip.KARE
        
#SABİT DEĞERLERİ İÇEREN STATİK SINIFLAR
class SabitMetaClass(type):#sadece sabit değerleri içerecek olan statik sınıflar, bu sınıftan metaclass ile kalıtım alacak
    """Sınıf seviyesindeki özniteliklerin değiştirilmesini veya silinmesini engeller."""
    def __setattr__(cls, name, value):
        raise AttributeError(f"'{cls.__name__}' statik bir sınıftır; '{name}' sabiti değiştirilemez.")

    def __delattr__(cls, name):
        raise AttributeError(f"'{cls.__name__}' statik bir sınıftır; '{name}' sabiti silinemez.")

class ImajSabit(metaclass=SabitMetaClass):
    DIZIN={ImajTip.RESEPTOR_IMAJ:"assets/reseptor",ImajTip.GOZ_IMAJ:"assets/goz"}
    ATLAS_DOSYA={
                    ImajTip.RESEPTOR_IMAJ:"reseptor.atlas",
                    ImajTip.GOZ_IMAJ:{GozTip.GOZ1:"goz1.atlas",GozTip.GOZ2:"goz2.atlas",GozTip.GOZ3:"goz3.atlas",GozTip.GOZ4:"goz4.atlas"}
                }
    KARE_AD={
                ImajTip.RESEPTOR_IMAJ:"reseptor-yesil-",
                ImajTip.GOZ_IMAJ:{
                    Yon.SOL:{GozAksiyon.BEKLE:"sol-bekle-",GozAksiyon.GIT:"sol-git-",GozAksiyon.PATLA:"sol-patla-",GozAksiyon.SOLA_DON:"sol-sola-don-",GozAksiyon.SAGA_DON:"sol-saga-don-"},
                    Yon.ALT:{GozAksiyon.BEKLE:"alt-bekle-",GozAksiyon.GIT:"alt-git-",GozAksiyon.PATLA:"alt-patla-",GozAksiyon.SOLA_DON:"alt-sola-don-",GozAksiyon.SAGA_DON:"alt-saga-don-"},
                    Yon.SAG:{GozAksiyon.BEKLE:"sag-bekle-",GozAksiyon.GIT:"sag-git-",GozAksiyon.PATLA:"sag-patla-",GozAksiyon.SOLA_DON:"sag-sola-don-",GozAksiyon.SAGA_DON:"sag-saga-don-"},
                    Yon.UST:{GozAksiyon.BEKLE:"ust-bekle-",GozAksiyon.GIT:"ust-git-",GozAksiyon.PATLA:"ust-patla-",GozAksiyon.SOLA_DON:"ust-sola-don-",GozAksiyon.SAGA_DON:"ust-saga-don-"},
                }
            }
    KARE_SAYI={
                ImajTip.RESEPTOR_IMAJ:8,
                ImajTip.GOZ_IMAJ:{#animasyonların içerdiği resim sayısı.
                    Yon.SOL:{GozAksiyon.BEKLE:20,GozAksiyon.GIT:6,GozAksiyon.PATLA:11,GozAksiyon.SOLA_DON:11,GozAksiyon.SAGA_DON:11},
                    Yon.ALT:{GozAksiyon.BEKLE:20,GozAksiyon.GIT:6,GozAksiyon.PATLA:9,GozAksiyon.SOLA_DON:11,GozAksiyon.SAGA_DON:11},
                    Yon.SAG:{GozAksiyon.BEKLE:20,GozAksiyon.GIT:6,GozAksiyon.PATLA:11,GozAksiyon.SOLA_DON:11,GozAksiyon.SAGA_DON:11},
                    Yon.UST:{GozAksiyon.BEKLE:20,GozAksiyon.GIT:6,GozAksiyon.PATLA:9,GozAksiyon.SOLA_DON:11,GozAksiyon.SAGA_DON:11}
                }
            }
    GECIKME={
                ImajTip.RESEPTOR_IMAJ:1/60,
                ImajTip.GOZ_IMAJ:{GozAksiyon.BEKLE:2/60,GozAksiyon.GIT:2/60,GozAksiyon.PATLA:2/60,GozAksiyon.SOLA_DON:2/60,GozAksiyon.SAGA_DON:2/60}#minimum değer 3/60. Bunun altında bir değer verme
            }
    ORIJINAL_BOYUT={ImajTip.RESEPTOR_IMAJ:340,ImajTip.GOZ_IMAJ:563}#genişlik,yükseklik aynı
    BOYUT_ORAN={ImajTip.RESEPTOR_IMAJ:1,ImajTip.GOZ_IMAJ:1.5}#hücre genişliğine oranı
    ANIMASYON_TEKRAR={
                ImajTip.RESEPTOR_IMAJ:1,
                ImajTip.GOZ_IMAJ:{GozAksiyon.BEKLE:1,GozAksiyon.GIT:3,GozAksiyon.PATLA:1,GozAksiyon.SOLA_DON:1,GozAksiyon.SAGA_DON:1}
    } # Animasyon kaç kere çalışacak
    
    BOS_KARE={
                ImajTip.RESEPTOR_IMAJ:[],
                ImajTip.GOZ_IMAJ:{#animasyonların içerdiği görseller. Yukle.AtlasDosya fonksiyonunda yüklenecek
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
            }

class HucreSabit(metaclass=SabitMetaClass):
    TIP_BASLANGIC_KEY="baslangic"
    TIP_BITIS_KEY="bitis"
    TIP_YOL_KEY="yol"
    TIP_RENK_KEY="renk"
    TIP_UZUNLUK_CARPAN_KEY="uzunlukCarpan"
    SAYI_KEY="sayı"
    TIP={
        TIP_BASLANGIC_KEY:{
            TIP_RENK_KEY:{"r":245/255,"g":73/255,"b":39/255,"a":1},
            TIP_UZUNLUK_CARPAN_KEY:1},
        TIP_BITIS_KEY:{
            TIP_RENK_KEY:{"r":219/255,"g":88/255,"b":88/255,"a":1},
            TIP_UZUNLUK_CARPAN_KEY:1},
        TIP_YOL_KEY:{
            TIP_RENK_KEY:{"r":255/255,"g":247/255,"b":173/255,"a":0.5},
            TIP_UZUNLUK_CARPAN_KEY:1.0}
        }

class EkranSabit(metaclass=SabitMetaClass):

    MAKS_SAHA_GENISLIK_KEY="MAKS_SAHA_GENISLIK"
    MAKS_SAHA_YUKSEKLIK_KEY="MAKS_SAHA_YUKSEKLIK"
    MAKS_KENARLIK_KALINLIK_KEY="MAKS_KENARLIK_KALINLIK"
    
    #ekranın alabileceği maks genişlik, yükseklik değerleri
    MAKS_EKRAN_GENISLIK_YATAY=3840
    MAKS_EKRAN_YUKSEKLIK_YATAY=2160
    MAKS_EKRAN_GENISLIK_DIKEY=2160
    MAKS_EKRAN_YUKSEKLIK_DIKEY=3840
    MAKS_EKRAN_GENISLIK_KARE=3840
    MAKS_EKRAN_YUKSEKLIK_KARE=3840
                
    #solPanel,yarismaPanel,sagPanel genişlik oranları
    SOL_PANEL_GENISLIK_ORAN=.15
    SAHA_GENISLIK_ORAN=.7 #aynı zamanda, sahanın; ekran genişliğine oranı.
    SAG_PANEL_GENISLIK_ORAN=.15

    #yarışma panelinde; sahanın altında ve üstünde alan bırakıldı
    SAHA_YUKSEKLIK_ORAN=.8
    SAHA_UST_YUKSEKLIK_ORAN=.1
    SAHA_ALT_YUKSEKLIK_ORAN=.1

    #labirent çizimi ile alakalı değerler
    LABIRENT_KENARLIK_KALINLIK_ORAN=100

    #labirent görseli için : alt-üst(2+2), sol-sağ(2+2) taraflardan kenarlık kalınlığının 2 katı kadar küçültme yapılacak
    TEXTURE_KUCULTME_CARPAN_2_KENAR=2
    TEXTURE_KUCULTME_CARPAN_1_KENAR=1

    def maksSahaKenarlik(labirentTip):#sahanın maks w-h, kenarlık kalınlık maks değerleri döndürür
        match labirentTip:
            case DikdortgenTip.YATAY:
                maksEkranGenislik=EkranSabit.MAKS_EKRAN_GENISLIK_YATAY
                maksEkranYukseklik=EkranSabit.MAKS_EKRAN_YUKSEKLIK_YATAY
                maksKenarlikKalinlik=maksEkranYukseklik*EkranSabit.SAHA_YUKSEKLIK_ORAN/EkranSabit.LABIRENT_KENARLIK_KALINLIK_ORAN
            case DikdortgenTip.DIKEY:
                maksEkranGenislik=EkranSabit.MAKS_EKRAN_GENISLIK_DIKEY
                maksEkranYukseklik=EkranSabit.MAKS_EKRAN_YUKSEKLIK_DIKEY
                maksKenarlikKalinlik=maksEkranGenislik*EkranSabit.SAHA_GENISLIK_ORAN/EkranSabit.LABIRENT_KENARLIK_KALINLIK_ORAN
            case DikdortgenTip.KARE:
                maksEkranGenislik=EkranSabit.MAKS_EKRAN_GENISLIK_KARE
                maksEkranYukseklik=EkranSabit.MAKS_EKRAN_YUKSEKLIK_KARE
                maksKenarlikKalinlik=maksEkranGenislik*EkranSabit.SAHA_GENISLIK_ORAN/EkranSabit.LABIRENT_KENARLIK_KALINLIK_ORAN

        
        maksSahaGenislik=maksEkranGenislik*EkranSabit.SAHA_GENISLIK_ORAN
        maksSahaYukseklik=maksEkranYukseklik*EkranSabit.SAHA_YUKSEKLIK_ORAN

        return {EkranSabit.MAKS_SAHA_GENISLIK_KEY:maksSahaGenislik,
            EkranSabit.MAKS_SAHA_YUKSEKLIK_KEY:maksSahaYukseklik,
            EkranSabit.MAKS_KENARLIK_KALINLIK_KEY:maksKenarlikKalinlik}
    

class LabirentSabit(metaclass=SabitMetaClass):
    KENARLIK_RENK=(1,0,0,1)
    MINIMUM_COZUM_UZUNLUGU_ORAN=0.5
    SATIR_ANAHTAR="satir"
    SUTUN_ANAHTAR="sutun"

#Yarışmadaki animasyona ilişkin sabit değerler
class AnimasyonSabit(metaclass=SabitMetaClass):
    # Epsilon Değeri (Hassas Zamanlama Payı)
    EPSILON=1/120

    ANIMASYON_GECIKME=1/60
    GERI_SAYIM_GECIKME=1

class AnaPencereSabit(metaclass=SabitMetaClass):
    ACIKLAMA_GOZ_GORSEL_YUKLEME="Göz görselleri yükleniyor"
    ACIKLAMA_RESEPTOR_GORSEL_YUKLEME="Reseptör görselleri yükleniyor"

class AcilirPencereSabit(metaclass=SabitMetaClass):
    PENCERE_GENISLIK_ORAN=.9     #Açılır pencerenin genişliğinin, ana pencerenin genişliğine oranı
    PENCERE_YUKSEKLIK_ORAN=.9    #Açılır pencerenin yüksekliğinin, ana pencerenin yüksekliğine oranı
    ETIKET_BOYUT_ORAN=.03         #Etiket yazı boyutunun, açılır pencerenin genişliğine oranı
    ETIKET_RENK=[.694,.157,.157,1]       #etiketin yazı rengi
    ARKAPLAN_RENK=[.8,.8,.8,.7]

