#TEMEL VERİ YAPILARI VE DOĞRULAMA ARAÇLARI


class Denetle:
    @staticmethod
    def TurHata(deger,tur):#Bir nesneye atama yapılırken, doğru türde bir değer mi diye kontrol ediliyor
        if not isinstance(deger, tur):
            raise TypeError(f"{tur.__name__} nesnesine, {type(deger).__name__} türünde bir değer atayamazsınız")
    
    @staticmethod
    def BosNesne(nesne,mesaj):
        if nesne is None:
            raise ValueError(mesaj)

#Robotun bulunduğu konum
class Konum:

    def __init__(self,satirNumara,sutunNumara):
        #if satirNumara is None:
            #satirNumara = self.__class__.__baslangicSatirNumara
        #if sutunNumara is None:
            #sutunNumara = self.__class__.__baslangicSutunNumara

        self.__satirNumara=satirNumara
        self.__sutunNumara=sutunNumara
    
    def __str__(self):
        return f"Konum : satır : {self.__satirNumara}, sütun : {self.__sutunNumara}"
    
    @property
    def satirNumara(self):
        return self.__satirNumara
    @property
    def sutunNumara(self):
        return self.__sutunNumara
    
    def satirDegistir(self,degisim,max=99):
        self.__satir+=degisim

    def sutunDegistir(self,degisim,max=99):
        self.__sutun+=degisim

