#TEMEL VERİ YAPILARI VE DOĞRULAMA ARAÇLARI

class Denetle:
    @staticmethod
    def tur_hata(deger,tur):#Bir nesneye atama yapılırken, doğru türde bir değer mi diye kontrol ediliyor
        if not isinstance(deger, tur):
            raise TypeError(f"{tur.__name__} nesnesine, {type(deger).__name__} türünde bir değer atayamazsınız")
    
    @staticmethod
    def bos_nesne(nesne,mesaj):
        if nesne is None:
            raise ValueError(mesaj)

#Robotun bulunduğu konum
class Konum:
    def __init__(self,satir_numarasi,sutun_numarasi):
        #if satir_numarasi is None:
            #satir_numarasi = self.__class__.__baslangic_satir_numarasi
        #if sutun_numarasi is None:
            #sutun_numarasi = self.__class__.__baslangic_sutun_numarasi

        self.__satir_numarasi=satir_numarasi
        self.__sutun_numarasi=sutun_numarasi
    
    def __str__(self):
        return f"Konum : satır : {self.__satir_numarasi}, sütun : {self.__sutun_numarasi}"
    
    @property
    def satir_numarasi(self):
        return self.__satir_numarasi
    @property
    def sutun_numarasi(self):
        return self.__sutun_numarasi
    
    def satir_degistir(self,degisim):
        self.__satir_numarasi+=degisim

    def sutun_degistir(self,degisim):
        self.__sutun_numarasi+=degisim