#ROBOT VE SENSÖR MANTIĞI


from enum import IntEnum
from abc import ABC,abstractmethod

from sabitler import ReseptorKonum,DuvarDurum,Hareket

#Gözün reseptörleri
class Reseptor:
    def __init__(self,konumArka=DuvarDurum.KAPALI,konumSag=DuvarDurum.KAPALI, konumOn=DuvarDurum.KAPALI, konumSol=DuvarDurum.KAPALI):
        self.__konumIndis=ReseptorKonum(0)#reseptör; sırasıyla tüm konumları tarayacak, indis başlangıçta ilk konumda(SOL) olacak

        self.__deger={ReseptorKonum.ARKA:konumArka,
                        ReseptorKonum.SAG:konumSag,
                        ReseptorKonum.ON:konumOn,
                        ReseptorKonum.SOL:konumSol}       
    
    def __str__(self):
        return f"Sensör : Sol : {self.__deger[ReseptorKonum.SOL]}, Ön : {self.__deger[ReseptorKonum.ON]}, Sağ : {self.__deger[ReseptorKonum.SAG]}, Arka : {self.__deger[ReseptorKonum.ARKA]}"
    
    @property
    def konumIndis(self):
        return self.__konumIndis
    @property 
    def sol(self):
        return self.__deger[ReseptorKonum.SOL]
    @property 
    def sag(self):
        return self.__deger[ReseptorKonum.SAG]
    @property 
    def on(self):
        return self.__deger[ReseptorKonum.ON]
    @property 
    def arka(self):
        return self.__deger[ReseptorKonum.ARKA]

    def degerGuncelle(self,reseptorKonum,duvarDurum):
        self.__deger[reseptorKonum]=duvarDurum
    def konumIndisGuncelle(self):
        self.__konumIndis=(ReseptorKonum)((self.__konumIndis+1)%len(ReseptorKonum))
    
class Goz(ABC):
    def __init__(self,isim):
        self.__hafiza={} #değişken saklamak için
        self.__isim=isim
    
    @property
    def isim(self):
        return self.__isim
    def isimDegistir(self,isim):
        self.__isim=isim
    @property
    def solaDon(self):
        return Hareket.SOLA_DON
    @property
    def sagaDon(self):
        return Hareket.SAGA_DON
    @property
    def ileriGit(self):
        return Hareket.ILERI

    @abstractmethod
    def kararVer(self,reseptor):
        """
        Bu fonksiyon her adımda çağrılır.
        reseptor_verisi: {'on': Zemin.DUVAR, 'sol': Zemin.BOS, ...}
        Geriye Yon.ILERI, Yon.SAGA_DON veya Yon.SOLA_DON döndürmelidir.
        """
        # Varsayılan olarak hiçbir şey yapma (veya rastgele git)
        # Öğrenci burayı ezecek (override).
        #Bu metod soyuttur. Goz sınıfında içi boştur (pass).
        #Alt sınıflar (BenimRobotum) bunu doldurmak ZORUNDADIR.
        pass