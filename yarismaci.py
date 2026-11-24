from sabitler import DuvarDurum
from goz import Goz

class BenimGozum(Goz):
    def __init__(self,isim):
        super().__init__(isim)
        
    def karar_ver(self,reseptor):
        """
        Bu fonksiyon her adımda çağrılır.
        """
        if reseptor.on==DuvarDurum.ACIK:
            return self.ileri_git
        else:
            pass

        if reseptor.sol==DuvarDurum.ACIK:
            return self.sola_don
        else:
            pass

        if reseptor.sag==DuvarDurum.ACIK:
            return self.saga_don
        else:
            pass

        if reseptor.arka==DuvarDurum.ACIK:
            return self.saga_don
        else:
            pass