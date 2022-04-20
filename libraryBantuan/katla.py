import numpy as np
import re
import random
from tqdm import tqdm

class Katla():
    def __init__(self, daftar_kata):
        self.daftar_kata_semua = daftar_kata
        self.daftar_kata = daftar_kata
        
        
    def kandidat(self, tebakan, pola, daf_kata):
        pola_regex = [r"\w"]*5
        huruf_tanda_tanya = [tebakan[i] for i in range(5) if pola[i]=='?']
        huruf_bintang = ''.join([tebakan[i] for i in range(5) if (pola[i]=='*') & (tebakan[i] not in huruf_tanda_tanya)])

        # Membentuk pola regex
        for i, p in enumerate(pola):
            if p == '!':
                pola_regex[i] = tebakan[i]
            elif p == '?':
                pola_regex[i] = f"[^ {tebakan[i]+huruf_bintang}]"
            elif p == '*':
                pola_regex[i] = f"[^ {huruf_bintang}]"
        
        pola_regex = r"".join(pola_regex)
        daf_kata = re.findall(pola_regex, ' '.join(daf_kata))

        # Mengambil kata2 yang ada huruf ?
        list_harus_ada_huruf = [tebakan[i] for i in range(5) if pola[i]=='?']
        new_daf_kata = []
        for kata in daf_kata:
            kata_tanpa_benar = [kata[i] for i in range(5) if pola[i]!='!']
            sudah_benar = True
            for harus_ada_huruf in list_harus_ada_huruf:
                if harus_ada_huruf in kata_tanpa_benar:
                    kata_tanpa_benar.remove(harus_ada_huruf)
                else:
                    sudah_benar=False; break
            if sudah_benar:
                new_daf_kata.append(kata)
        return new_daf_kata
        

    def tebakan_selanjutnya(self, tebakan, pola, tampilkan_detail=False):
        self.daftar_kata = self.kandidat(tebakan, pola, self.daftar_kata)
        if tampilkan_detail:
            print(f"Banyak Kata : {len(self.daftar_kata)}\n{self.daftar_kata}\n\n")
        return self.__cari_kata_selanjutnya()
        
    def __cari_kata_selanjutnya(self):
        # Cari semua kemungkinan pola
        semua_pola = []
        T = {'0' : '*', '1' : '?', '2' : '!'}
        for number in range(3**5):
            ternary=np.base_repr(number,base=3)
            pola = f"{ternary:05s}"
            semua_pola.append(''.join([T[i] for i in pola]))
        
        # Cari kata terbaik
        kata_terbaik = ("TIDAK ADA KATA", 10**8)
        for kata in self.daftar_kata:
            banyak = 0
            for pola in semua_pola:
                banyak += len(self.kandidat(kata, pola, self.daftar_kata))
                if banyak > kata_terbaik[1]:
                    break
            if banyak < kata_terbaik[1]:
                kata_terbaik = (kata, banyak)
        return kata_terbaik[0]
