#DÜNYA VE ÇEVRE

#from enum import IntEnum
import random
#from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Ellipse, Fbo


from temel import Konum#,Denetle
from sabitler import HucreSabit,HucreNokta,LabirentSabit,AnimasyonSabit,DikdortgenTip,DuvarDurum,Yon,GozTip,GozAksiyon,Hareket,Yon,ReseptorKonum
from yarismaci import BenimGozum
from goz import Reseptor

from grafik_dosya import LabirentStatikImaj,GozImaj,ReseptorImaj

class Hucre(Konum):
    def __init__(self,satir_numarasi,sutun_numarasi):
        super().__init__(satir_numarasi,sutun_numarasi)

    def __eq__(self, diger_hucre):# == operatörü ile iki Hucre nesnesinin eşit olup olmadığı sorgulanıyor
        return True if self.satir_numarasi==diger_hucre.satir_numarasi and self.sutun_numarasi==diger_hucre.sutun_numarasi else False
    
    def __ne__(self,diger_hucre): # != operatörü ile iki Hucre nesnesinin farklı olup olmadığı sorgulanıyor
        return True if self.satir_numarasi!=diger_hucre.satir_numarasi or self.sutun_numarasi!=diger_hucre.sutun_numarasi else False

class TaslakHucre(Hucre):
    def __init__(self,satir_numarasi,sutun_numarasi):
        super().__init__(satir_numarasi,sutun_numarasi)
        self.__isaret=False
    
    @property
    def isaret(self):
        return self.__isaret
    
    def isaret_koy(self):
        self.__isaret=True
    
    def isaret_kaldir(self):
        self.__isaret=False

class Duvar:        
    def __init__(self):#hücreler soldan sağa ya da yukarıdan aşağıda
        self.__durum=DuvarDurum.KAPALI 
            
    @property
    def durum(self):
        return self.__durum
    
    def ac(self):
        self.__durum=DuvarDurum.ACIK
    def kapat(self):
        self.__durum=DuvarDurum.KAPALI

class Labirent:
    def __init__(self,satir_sayisi,sutun_sayisi):
        self.__satir_sayisi=satir_sayisi
        self.__sutun_sayisi=sutun_sayisi

        self.__minimum_cozum_uzunlugu=self.__satir_sayisi*self.__sutun_sayisi*LabirentSabit.MINIMUM_COZUM_UZUNLUGU_ORAN
        self.__tip=DikdortgenTip.belirle(self.__sutun_sayisi,self.__satir_sayisi)

        self.__baslangic_satir_numara=-1
        self.__baslangic_sutun_numara=-1
        self.__bitis_satir_numara=-1
        self.__bitis_sutun_numara=-1

        self.__taslak_hucreler=[]        #labirent oluşturulduktan sonra bu nesne silinecek (del)
        self.__taslak_hucre_duvarlar=[]   #labirent oluşturulduktan sonra bu nesne silinecek (del)
        
        self.__hucreler=[]
        self.__duvarlar=[]
        self.__cozum_yolu=[]

        rastgele_deger=self.__rastgele_baslangic_bitis_belirle()
        self.__baslangic_satir_numara=rastgele_deger[LabirentSabit.BASLANGIC_SATIR_NUMARA_ANAHTAR]
        self.__baslangic_sutun_numara=rastgele_deger[LabirentSabit.BASLANGIC_SUTUN_NUMARA_ANAHTAR]
        self.__bitis_satir_numara=rastgele_deger[LabirentSabit.BITIS_SATIR_NUMARA_ANAHTAR]
        self.__bitis_sutun_numara=rastgele_deger[LabirentSabit.BITIS_SUTUN_NUMARA_ANAHTAR]
        
        self.__cozum_yolu=self.__olustur_cozum_yolu()
        self.__hucreler=self.__olustur_hucreler()
        self.__duvarlar=self.__olustur_duvarlar()

        del self.__taslak_hucre_duvarlar
        del self.__taslak_hucreler

    @property
    def satir_sayisi(self):
        return self.__satir_sayisi
    @property
    def sutun_sayisi(self):
        return self.__sutun_sayisi
    @property
    def baslangic_satir_numarasi(self):
        return self.__baslangic_satir_numara
    @property
    def baslangic_sutun_numarasi(self):
        return self.__baslangic_sutun_numara
    @property
    def bitis_satir_numara(self):
        return self.__bitis_satir_numara
    @property
    def bitis_sutun_numara(self):
        return self.__bitis_sutun_numara
    
    @property
    def baslangic_hucre(self):
        return self.__hucreler[self.__baslangic_satir_numara][self.__baslangic_sutun_numara]
    @property
    def bitis_hucre(self):
        return self.__hucreler[self.__bitis_satir_numara][self.__bitis_sutun_numara]
    @property
    def cozum_yolu_uzunlugu(self):#çözüm yolu kaç tane Hücre içeriyor
        return len(self.__cozum_yolu)
    @property
    def tip(self):
        return self.__tip
    
    def cozum_yolu_hucre(self,numara):
        return self.__cozum_yolu[numara]

    def hucre(self,satir_numarasi,sutun_numarasi):
        if satir_numarasi<0 or satir_numarasi>=self.__satir_sayisi or sutun_numarasi<0 or sutun_numarasi>=self.__sutun_sayisi:
            return None
        return self.__hucreler[satir_numarasi][sutun_numarasi]
    
    def komsu_hucreler(self,hucre,taslak_hucre_mi=False):#taslak_hucre_mi=ön hücre mi(self.__taslak_hucreler) yoksa, oluşturulmuş labirentin hücreleri mi(self.__hucre)
        hucreler=self.__taslak_hucreler if taslak_hucre_mi else self.__hucreler

        komsu_hucreler={Yon.SOL:None,Yon.ALT:None,Yon.SAG:None,Yon.UST:None,HucreSabit.SAYI_ANAHTAR:0}
        if hucre.satir_numarasi+1<self.__satir_sayisi:#altında komşu var mı
            komsu_hucreler[Yon.ALT]=hucreler[hucre.satir_numarasi+1][hucre.sutun_numarasi]
            komsu_hucreler[HucreSabit.SAYI_ANAHTAR]+=1
        
        if hucre.satir_numarasi-1>=0:#üstünde satir var mı
            komsu_hucreler[Yon.UST]=hucreler[hucre.satir_numarasi-1][hucre.sutun_numarasi]
            komsu_hucreler[HucreSabit.SAYI_ANAHTAR]+=1
        
        if hucre.sutun_numarasi+1<self.__sutun_sayisi:#sağında komşu var mı
            komsu_hucreler[Yon.SAG]=hucreler[hucre.satir_numarasi][hucre.sutun_numarasi+1]
            komsu_hucreler[HucreSabit.SAYI_ANAHTAR]+=1

        if hucre.sutun_numarasi-1>=0:#solunda komşu var mı
            komsu_hucreler[Yon.SOL]=hucreler[hucre.satir_numarasi][hucre.sutun_numarasi-1]
            komsu_hucreler[HucreSabit.SAYI_ANAHTAR]+=1
        return komsu_hucreler

    def duvar(self,hucre1,hucre2,taslak_hucre_duvar_mi=False):#taslak_hucre_duvar_mi=ön hücrenin duvarı mı(self.__taslak_hucre_duvarlar) yoksa, oluşturulmuş labirentin hücrelerinin duvarları mı(self.__duvarlar)
        duvarlar=self.__taslak_hucre_duvarlar if taslak_hucre_duvar_mi else self.__duvarlar
            
        if hucre1 is None or hucre2 is None:#Eğer satır ya da sutun numarası labirentin sınırları dışındaysa, KAPALI bir duvar dönsün 
            return Duvar()   
                
        if hucre1.satir_numarasi==hucre2.satir_numarasi:#aynı satırdaki hücreler arasındaki bir duvar ise
            if hucre2.sutun_numarasi<hucre1.sutun_numarasi:#hücre2 küçük indisli ise
                return duvarlar[LabirentSabit.SATIR_ANAHTAR][hucre2.satir_numarasi][hucre2.sutun_numarasi]
            return duvarlar[LabirentSabit.SATIR_ANAHTAR][hucre1.satir_numarasi][hucre1.sutun_numarasi]#hücre1 küçük indisli ise
        else:#aynı sütundaki hücreler arasındaki bir duvar ise
            if hucre2.satir_numarasi<hucre1.satir_numarasi:#hücre2 küçük indisli ise
                return duvarlar[LabirentSabit.SUTUN_ANAHTAR][hucre2.sutun_numarasi][hucre2.satir_numarasi]    
            return duvarlar[LabirentSabit.SUTUN_ANAHTAR][hucre1.sutun_numarasi][hucre1.satir_numarasi]#hücre1 küçük indisli ise

    def __olustur_cozum_yolu(self):
        cozum_yolu=[]
        hucre_yigin=[]
        while(len(cozum_yolu)<self.__minimum_cozum_uzunlugu):

            self.__taslak_hucreler=self.__olustur_taslak_hucreler()
            self.__taslak_hucre_duvarlar=self.__olustur_taslak_hucre_duvarlar()
            
            cozum_yolu=[]
            hucre_yigin=[]
            hucre_yigin.append(self.__taslak_hucreler[self.__baslangic_satir_numara][self.__baslangic_sutun_numara])#ilk hücreyi yığına ekle

            while(not self.__taslak_hucreler_isaretlendi()):
                hucre=hucre_yigin[-1]#stack'in en üstündeki hücre
                hucre.isaret_koy()
                rastgele_komsu_hucre=self.__sec_rastgele_komsu_hucre(hucre)
                if rastgele_komsu_hucre:
                    rastgele_komsu_hucre.isaret_koy()
                    self.__ac_duvar(hucre,rastgele_komsu_hucre)
                    hucre_yigin.append(rastgele_komsu_hucre)

                    if rastgele_komsu_hucre.satir_numarasi==self.__bitis_satir_numara and rastgele_komsu_hucre.sutun_numarasi==self.__bitis_sutun_numara:
                        for hucre in hucre_yigin:
                            cozum_yolu.append(Hucre(hucre.satir_numarasi,hucre.sutun_numarasi))
                else:
                    hucre_yigin.pop()
        
        return cozum_yolu
    
    def __sec_rastgele_komsu_hucre(self,hucre):
        komsu_hucreler=self.komsu_hucreler(hucre,True)
        
        if komsu_hucreler[HucreSabit.SAYI_ANAHTAR]==0:
            return None
        
        tum_komsu_hucreler_isaretli=True
        for yon in Yon:
            if komsu_hucreler[yon]:
                if not komsu_hucreler[yon].isaret:
                    tum_komsu_hucreler_isaretli=False
                    break
        
        if tum_komsu_hucreler_isaretli:
            return None
    
        while(True):
            rastgele_yon=random.choice(list(Yon))
            rastgele_komsu_hucre=komsu_hucreler[rastgele_yon]
            if rastgele_komsu_hucre:
                if not rastgele_komsu_hucre.isaret:
                    return rastgele_komsu_hucre
        
    def __taslak_hucreler_isaretlendi(self):
        for satir_numarasi in range(self.__satir_sayisi):
            for sutun_numarasi in range(self.__sutun_sayisi):
                if not self.__taslak_hucreler[satir_numarasi][sutun_numarasi].isaret:
                    return False
        return True
    
    def __olustur_taslak_hucreler(self):
        taslak_hucreler=[]
        for satir_numarasi in range(self.__satir_sayisi):
            satir=[]
            for sutun_numarasi in range(self.__sutun_sayisi):
                hucre=TaslakHucre(satir_numarasi,sutun_numarasi)
                satir.append(hucre)
            taslak_hucreler.append(satir)
        return taslak_hucreler
    
    def __olustur_hucreler(self):#self.__taslak_hucreler nesnesindeki ön hücreleri, self.__hucreler nesnesine aktar 
        return self.__taslak_hucreler

    def __olustur_taslak_hucre_duvarlar(self):
        duvarlar={LabirentSabit.SATIR_ANAHTAR:[],LabirentSabit.SUTUN_ANAHTAR:[]}
        #satırlarda bulunan duvarlar oluşturuluyor
        for satir_numarasi in range(self.__satir_sayisi):
            satir_duvarlar=[]
            for sutun_numarasi in range(self.__sutun_sayisi-1):
                duvar=Duvar()
                satir_duvarlar.append(duvar)
            duvarlar[LabirentSabit.SATIR_ANAHTAR].append(satir_duvarlar)

        #sutunlarda bulunan duvarlar oluşturuluyor
        for sutun_numarasi in range(self.__sutun_sayisi):
            sutun_duvarlar=[]
            for satir_numarasi in range(self.__satir_sayisi-1):
                duvar=Duvar()
                sutun_duvarlar.append(duvar)
            duvarlar[LabirentSabit.SUTUN_ANAHTAR].append(sutun_duvarlar)

        return duvarlar
    
    def __olustur_duvarlar(self):#self.__taslak_hucre_duvarlar nesnesindeki duvarları self.__duvarlar içerisine aktar
        return self.__taslak_hucre_duvarlar

    def __ac_duvar(self,hucre1,hucre2):
        self.duvar(hucre1,hucre2,True).ac()

    def __butun_duvarlari_kapat(self):
        #satırlarda bulunan duvarlar kapatılıyor
        for satir_numarasi in range(self.__satir_sayisi):
            for sutun_numarasi in range(self.__sutun_sayisi-1):
                self.__duvarlar[LabirentSabit.SATIR_ANAHTAR][satir_numarasi][sutun_numarasi].kapat()
                
        for sutun_numarasi in range(self.__sutun_sayisi):
            for satir_numarasi in range(self.__satir_sayisi-1):
                self.__duvarlar[LabirentSabit.SUTUN_ANAHTAR][sutun_numarasi][satir_numarasi].kapat()
    
    def __rastgele_baslangic_bitis_belirle(self):#labirentin başlangıç ve bitiş hücreleri rastgele belirleniyor

        if self.__tip==DikdortgenTip.YATAY:
            baslangic_sutun_numarasi=0
            bitis_sutun_numara=self.__sutun_sayisi-1
            baslangic_satir_numarasi=random.randint(0,self.__satir_sayisi-1)
            bitis_satir_numara=random.randint(0,self.__satir_sayisi-1)
        else:
            baslangic_satir_numarasi=0
            bitis_satir_numara=self.__satir_sayisi-1
            baslangic_sutun_numarasi=random.randint(0,self.__sutun_sayisi-1)
            bitis_sutun_numara=random.randint(0,self.__sutun_sayisi-1)

        return {LabirentSabit.BASLANGIC_SATIR_NUMARA_ANAHTAR:baslangic_satir_numarasi,
            LabirentSabit.BASLANGIC_SUTUN_NUMARA_ANAHTAR:baslangic_sutun_numarasi,
            LabirentSabit.BITIS_SATIR_NUMARA_ANAHTAR:bitis_satir_numara,
            LabirentSabit.BITIS_SUTUN_NUMARA_ANAHTAR:bitis_sutun_numara}
        
    #def __maksimum_mesafe(self):#labirentin birbirlerine en uzak olan hücrelerin arasındaki mesafe
        #return self.__satir_sayisi-1+self.__sutun_sayisi-1
    
    #def __mesafe_hesapla(self,satir_numara1,sutun_numara1,satir_numara2,sutun_numara2):
        #return abs(satir_numara1-satir_numara2)+abs(sutun_numara1-sutun_numara2)

class Saha(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Yarisma:
    def __init__(self,saha):
        self.__saha=saha # yarışmanın yapılacağı Widget nesnesi
        
        self.__yarisma_saat=None
        self.__oyun_bitti=None
        self.__labirent=None
        self.__labirent_imaj=None
        self.__goz_hucre=None
        self.__goz=None
        self.__goz_imaj=None
        self.__reseptor=None
        self.__reseptor_imaj=None
        self.__reseptor_guncellendi=None
        
    def __baslangic_islemleri(self):

        self.__saha.bind(pos=self.guncelle_olculer, size=self.guncelle_olculer)
                
        self.__labirent=Labirent(10,15)#Labirent(20,5)
        self.__labirent_imaj=LabirentStatikImaj(self.__labirent)
        self.__labirent_imaj.texture.save("labirent_sablonu.png")
    
        goz1=BenimGozum("ROBOT1")
        self.__goz=goz1
        self.__goz_imaj=GozImaj(GozTip.GOZ1,Yon.baslangic())

        self.__goz_hucre=self.__labirent.baslangic_hucre
        
        self.__reseptor=Reseptor()
        self.__reseptor_imaj=ReseptorImaj()

        self.__saha.add_widget(self.__labirent_imaj)
        self.__saha.add_widget(self.__goz_imaj)
        self.__saha.add_widget(self.__reseptor_imaj)

        Clock.schedule_once(lambda dt: self.guncelle_olculer(self.__saha), 0) #pencere açılması tamamlandığında, boyutların güncellenmesi için
    
    def baslat(self):
        self.__baslangic_islemleri()

        self.__reseptor_guncellendi=False
        self.__oyun_bitti=False
        self.__goz_hucre=self.__labirent.baslangic_hucre
        self.__goz_imaj.bekle()

        self.__yarisma_saat=Clock.schedule_once(self.geri_sayim,AnimasyonSabit.GERI_SAYIM_GECIKME)


    def geri_sayim(self,dt):
        self.__yarisma_saat=Clock.schedule_once(self.yaris_tik_tak,AnimasyonSabit.ANIMASYON_GECIKME)

    def yaris_tik_tak(self,dt):   
        if self.__goz_imaj.aksiyon!=GozAksiyon.BEKLE:
            self.__yarisma_saat=Clock.schedule_once(self.yaris_tik_tak,AnimasyonSabit.ANIMASYON_GECIKME)
            return
        
        if self.__goz_hucre==self.__labirent.bitis_hucre:           
            print("bitti")
            return
        
        if not self.__reseptor_guncellendi:
            animasyon_suresi=self.__reseptor_guncelle()
            self.__yarisma_saat=Clock.schedule_once(self.yaris_tik_tak, animasyon_suresi+AnimasyonSabit.EPSILON if animasyon_suresi > 0 else AnimasyonSabit.ANIMASYON_GECIKME)
            return
        
        if self.__goz_imaj.animasyon_tamamlandi:
            self.__goz_imaj.animasyon_basladi_resetle()
            self.__goz_imaj.animasyon_tamamlandi_resetle()
            goz_x, goz_y = self.__labirent_imaj.hucre_x_y(HucreNokta.MERKEZ,self.__goz_hucre,self.__saha)
            self.__goz_imaj.konumla(goz_x, goz_y)

            self.__reseptor_guncellendi = False
                
            goz_hareket = self.__goz.karar_ver(self.__reseptor)
            animasyon_suresi=self.__goz_hareket_uygula(goz_hareket)
            
            self.__yarisma_saat=Clock.schedule_once(self.yaris_tik_tak, animasyon_suresi+AnimasyonSabit.EPSILON)
            return
        
        self.__yarisma_saat=Clock.schedule_once(self.yaris_tik_tak, AnimasyonSabit.ANIMASYON_GECIKME)
        
    def __goz_hareket_uygula(self,hareket):
        match hareket:
            case Hareket.SOLA_DON:
                self.__goz_imaj.sola_don()#.yon=Yon((self.__goz_imaj.yon+1)%len(Yon))
                #print("sola döndü")
            case Hareket.SAGA_DON:
                self.__goz_imaj.saga_don()#.yon=Yon((self.__goz_imaj.yon-1)%len(Yon))
                #print("sağa döndü")
            case Hareket.ILERI:
                hucre_satir_numarasi=self.__goz_hucre.satir_numarasi
                hucre_sutun_numarasi=self.__goz_hucre.sutun_numarasi
                match self.__goz_imaj.yon:
                    case Yon.SAG:
                        hucre_sutun_numarasi+=1
                    case Yon.SOL:
                        hucre_sutun_numarasi-=1
                    case Yon.ALT:
                        hucre_satir_numarasi+=1
                    case Yon.UST:
                        hucre_satir_numarasi-=1
                
                duvar=self.__labirent.duvar(self.__goz_hucre,self.__labirent.hucre(hucre_satir_numarasi,hucre_sutun_numarasi))
                
                if duvar.durum==DuvarDurum.ACIK:   
                    self.__goz_hucre=self.__labirent.hucre(hucre_satir_numarasi,hucre_sutun_numarasi)
                    self.__goz_imaj.git()
                else:
                    print("HÖSTT")
                    #self.__goz_imaj.bekle()
        
        return GozImaj.animasyon_suresi(self.__goz_imaj.aksiyon, self.__goz_imaj.yon)

    def guncelle_olculer(self,*args):
        if self.__labirent is None:
            return
        
        self.__labirent_imaj.guncelle_olculer(self.__saha)
                
        goz_x,goz_y=self.__labirent_imaj.hucre_x_y(HucreNokta.MERKEZ,self.__goz_hucre,self.__saha)
        self.__goz_imaj.guncelle_olculer(goz_x,goz_y,self.__labirent_imaj.guncel_hucre_boyut,self.__labirent_imaj.guncel_kenarlik_tam)

        self.__reseptor_imaj.guncelle_olculer(self.__labirent_imaj.guncel_hucre_boyut)

    def __reseptor_guncelle(self):
        yon_fark = self.__goz_imaj.yon - Yon.baslangic()
        reseptor_gercek_konum=ReseptorKonum((self.__reseptor.konum_indis+yon_fark)%len(ReseptorKonum))
        reseptor_x,reseptor_y=self.__labirent_imaj.hucre_x_y(HucreNokta(reseptor_gercek_konum),self.__goz_hucre,self.__saha)

        komsu_hucreler = self.__labirent.komsu_hucreler(self.__goz_hucre)
        hedef_hucre = komsu_hucreler.get(Yon(reseptor_gercek_konum))
        
        duvar_durum = DuvarDurum.KAPALI
        if hedef_hucre:
            duvar_durum = self.__labirent.duvar(self.__goz_hucre, hedef_hucre).durum
        self.__reseptor.deger_guncelle(self.__reseptor.konum_indis, duvar_durum)

        if duvar_durum==DuvarDurum.ACIK:
            if not self.__reseptor_imaj.animasyon_basladi:
                self.__reseptor_imaj.animasyon_tamamlandi_resetle()
                self.__reseptor_imaj.konumla(reseptor_x,reseptor_y)
            
                self.__reseptor_imaj.duvar_acik()

                return ReseptorImaj.animasyon_suresi()
 
            if self.__reseptor_imaj.animasyon_tamamlandi:
                self.__reseptor_imaj.animasyon_basladi_resetle()
                self.__reseptor.konum_indis_guncelle()

                if self.__reseptor.konum_indis == 0:
                    self.__reseptor_guncellendi = True
        else:
            self.__reseptor.konum_indis_guncelle()

            if self.__reseptor.konum_indis == 0:
                self.__reseptor_guncellendi = True

        return 0