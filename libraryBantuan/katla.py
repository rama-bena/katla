import numpy as np
import re
import random


class Katla():
    def __init__(self, daftar_kata):
        self.daftar_kata = daftar_kata
        self.huruf_benar = [False, False, False, False, False]
        self.list_pola = []
        T = {'0' : '*', '1' : '?', '2' : '!'}
        for number in range(3**5):
            ternary=np.base_repr(number,base=3)
            pola = f"{ternary:05s}"
            self.list_pola.append(''.join([T[i] for i in pola]))
        
    def kandidat(self, tebakan, pola, daf_kata):
        list_tanda_seru    = [idx for idx,huruf in enumerate(pola) if huruf=='!']
        list_tanda_tanya   = [idx for idx,huruf in enumerate(pola) if huruf=='?']
        list_tanda_bintang = [idx for idx,huruf in enumerate(pola) if huruf=='*']

        # Pola Regex
        pola_regex = ["."]*5
        for pos in list_tanda_seru:                 # huruf di tanda seru benar
            pola_regex[pos] = tebakan[pos] 
            self.huruf_benar[pos] = True   
        for pos in list_tanda_tanya:                # huruf di tanda tanya salah
            pola_regex[pos] = f"[^{tebakan[pos]}]"

        # Cari daftar kata sesuai pola regex
        pola_regex = r"".join(pola_regex)
        daf_kata =  [kata for kata in daf_kata if re.match(pola_regex, kata)]

        # Hilangkan kata yang ada huruf di list_tanda_bintang
        list_huruf_salah = [tebakan[pos] for pos in list_tanda_bintang]
        new_daf_kata = []
        for kata in daf_kata:
            tidak_ada_huruf_salah = True
            kata_tanpa_huruf_benar = [kata[pos] for pos in range(5) if not self.huruf_benar[pos]]
            for huruf_salah in list_huruf_salah:
                if huruf_salah in kata_tanpa_huruf_benar:
                    tidak_ada_huruf_salah = False; break
            if tidak_ada_huruf_salah:
                new_daf_kata.append(''.join(kata))
        daf_kata = new_daf_kata 

        # Cara kata yang ada huruf di tanda tanya
        for pos in list_tanda_tanya:
            huruf = tebakan[pos]
            daf_kata = [kata for kata in daf_kata if huruf in kata]
        
        return daf_kata

    def tebakan_selanjutnya(self, tebakan, pola, tampilkan_detail=False):
        self.daftar_kata = self.kandidat(tebakan, pola, self.daftar_kata)
        if tampilkan_detail:
            print(f"Banyak Kata : {len(self.daftar_kata)}\n{self.daftar_kata}\n\n")
        return self.__cari_kata_selanjutnya()
        
    def __cari_kata_selanjutnya(self):
        kata_terbaik = ("TIDAK ADA KATA", 10**8)
        for kata in self.daftar_kata:
            banyak = 0
            for pola in self.list_pola:
                banyak += len(self.kandidat(kata, pola, self.daftar_kata))
            if banyak < kata_terbaik[1]:
                kata_terbaik = (kata, banyak)
        return kata_terbaik[0]
