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
            print(f"Banyak Kata : {len(self.daftar_kata)}")
            # print(self.daftar_kata)
        return self.cari_kata_selanjutnya(tampilkan_detail)
        
    def cari_kata_selanjutnya(self, tampilkan_detail):
        def P(n):
            return n / len(self.daftar_kata)
        def impurity(n):
            return ((n-1) / n) if n!=0 else 0

        semua_pola = self.__cari_semua_kemungkinan_pola()
        hasil_semua = []
        impurity_awal = impurity(len(self.daftar_kata))

        # Cari kata terbaik
        for kata in tqdm(self.daftar_kata):
            impurity_akhir = 0

            for pola in semua_pola:         # untuk setiap pola hitung kemungkinannya
                n = len(self.kandidat(kata, pola, self.daftar_kata))
                impurity_akhir += P(n) * impurity(n)
            
            information_gain = impurity_awal - impurity_akhir
            hasil_semua.append((kata, information_gain))

        hasil_semua.sort(key=lambda x: x[1], reverse=True)
        if tampilkan_detail:
            i = 0
            terbaik = hasil_semua[0][1]
            while hasil_semua[i][1]==terbaik:
                print(hasil_semua[i])
                i+=1
                if i >= len(hasil_semua):
                    break

        return hasil_semua[0][0]

    def __cari_semua_kemungkinan_pola(self):
        T = {'0' : '*', '1' : '?', '2' : '!'}
        list_pola = []
        for number in range(1, 3**5):
            ternary=np.base_repr(number,base=3)
            pola = f"{ternary:05s}"
            list_pola.append(''.join([T[i] for i in pola]))
        return list_pola