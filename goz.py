#ROBOT VE SENSÖR MANTIĞI

from enum import IntEnum
from abc import ABC,abstractmethod

from sabitler import ReseptorKonum,DuvarDurum,Hareket

#Gözün reseptörleri
class Reseptor:
    def __init__(self,konum_arka=DuvarDurum.KAPALI,konum_sag=DuvarDurum.KAPALI, konum_on=DuvarDurum.KAPALI, konum_sol=DuvarDurum.KAPALI):
        self.__konum_indis=ReseptorKonum(0)#reseptör; sırasıyla tüm konumları tarayacak, indis başlangıçta ilk konumda(SOL) olacak

        self.__deger={ReseptorKonum.ARKA:konum_arka,
                        ReseptorKonum.SAG:konum_sag,
                        ReseptorKonum.ON:konum_on,
                        ReseptorKonum.SOL:konum_sol}       
    
    def __str__(self):
        return f"Sensör : Sol : {self.__deger[ReseptorKonum.SOL]}, Ön : {self.__deger[ReseptorKonum.ON]}, Sağ : {self.__deger[ReseptorKonum.SAG]}, Arka : {self.__deger[ReseptorKonum.ARKA]}"
    
    @property
    def konum_indis(self):
        return self.__konum_indis
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

    def deger_guncelle(self,reseptor_konum,duvar_durum):
        self.__deger[reseptor_konum]=duvar_durum
    def konum_indis_guncelle(self):
        self.__konum_indis=(ReseptorKonum)((self.__konum_indis+1)%len(ReseptorKonum))
    
class Goz(ABC):
    def __init__(self,isim):
        self.__hafiza={} #değişken saklamak için
        self.__isim=isim
    
    @property
    def isim(self):
        return self.__isim
    def isim_degistir(self,isim):
        self.__isim=isim
    @property
    def sola_don(self):
        return Hareket.SOLA_DON
    @property
    def saga_don(self):
        return Hareket.SAGA_DON
    @property
    def ileri_git(self):
        return Hareket.ILERI

    @abstractmethod
    def karar_ver(self,reseptor):
        # Varsayılan olarak hiçbir şey yapma (veya rastgele git)
        # Öğrenci burayı ezecek (override).
        #Bu metod soyuttur. Goz sınıfında içi boştur (pass).
        #Alt sınıflar (BenimRobotum) bunu doldurmak ZORUNDADIR.
        pass