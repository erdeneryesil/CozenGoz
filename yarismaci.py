from siniflar import Goz,Reseptor,DuvarDurum

class BenimGozum(Goz):
    def __init__(self,isim):
        super().__init__(isim)
        
    
    def kararVer(self,reseptor):
        """
        Bu fonksiyon her adımda çağrılır.
        """
        #return self.ileriGit
        if reseptor.on==DuvarDurum.ACIK:
            return self.ileriGit
        else:
            pass
            

        if reseptor.sol==DuvarDurum.ACIK:
            return self.solaDon
        else:
            pass

        if reseptor.sag==DuvarDurum.ACIK:
            return self.sagaDon
        else:
            pass

        if reseptor.arka==DuvarDurum.ACIK:
            return self.sagaDon
        else:
            pass




        
        