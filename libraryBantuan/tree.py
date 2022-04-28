# Library Utama
import numpy as np
import random
import re
import pickle

# Library Bantuan
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')
from pprint import pprint

class Node():
    def __init__(self, kata, daftar_kata):
        self.tebakan = kata
        self.kandidat_jawaban = daftar_kata 
        self.next_node = {}

class DecisionTree():
    
    def __init__(self, path_object=None):
        self.semua_pola = self.__cari_semua_kemungkinan_pola()
        self.root = None
        if path_object != None:
            object_dict = self.baca_object(path_object)
            self.root = self.jadikan_object(object_dict)
        self.now = self.root
        self.pakai_semua_daftar = False

    def kata_berikutnya(self, pola, tampilkan_kandidat=False, awal=False):
        if awal:
            self.now = self.root
        if pola in self.now.next_node:
            self.now = self.now.next_node[pola]
            
            if tampilkan_kandidat:
                print(self.now.kandidat_jawaban)
        return self.now.tebakan

    def buat_tree(self, daftar_kata, kata_root=None, pakai_semua_daftar=False):
        """membuat tree

        Args:
            daftar_kata (list): daftar kata
            kata_root (str, optional): kata awal. Defaults to None.
            pakai_semua_daftar (bool, optional): pakai daftar kata semua untuk split. Defaults to False.
        """        
        
        self.pakai_semua_daftar = pakai_semua_daftar
        if kata_root == None:
            kata_root = self.cari_kata_terbaik(daftar_kata, daftar_kata)[0]
        self.root = self.__buat_tree(kata_root, daftar_kata, daftar_kata, 0)
        self.now  = self.root
    
    def __buat_tree(self, kata, daftar_kata_split, kandidat_jawaban, depth): # buat tree rekursif
        node = Node(kata, kandidat_jawaban)
        if (depth==8) or (len(kandidat_jawaban)<=1): # BASE CASE
            return node
        
        for pola in self.semua_pola:
            next_kandidat_jawaban = self.kandidat(kata, pola, kandidat_jawaban)
            if len(next_kandidat_jawaban)==0:        # tidak ada daftar kata dengan pola ini
                continue
            cari_kata_terbaik = self.cari_kata_terbaik(daftar_kata_split, next_kandidat_jawaban)
            next_kata = cari_kata_terbaik[0]
            next_daftar_kata_split = cari_kata_terbaik[1]
            node.next_node[pola] = self.__buat_tree(next_kata, next_daftar_kata_split, next_kandidat_jawaban, depth+1)
        return node
    
    def kandidat(self, tebakan, pola, daf_kata):
        pola_regex = [r"\w"]*5
        huruf_tanda_tanya = [tebakan[i] for i in range(5) if pola[i]=='?']
        huruf_bintang = ''.join([tebakan[i] for i in range(5) if (pola[i]=='*') and (tebakan[i] not in huruf_tanda_tanya)])

        # Membentuk pola regex
        for i, p in enumerate(pola):
            if p == '!':
                pola_regex[i] = tebakan[i]
            elif p == '?' or (p=='*' and tebakan[i] in huruf_tanda_tanya):
                pola_regex[i] = f"[^ {tebakan[i]+huruf_bintang}]"
            elif p == '*':
                pola_regex[i] = f"[^ {huruf_bintang}]"
        
        pola_regex = r"".join(pola_regex)
        daf_kata = re.findall(pola_regex, ' '.join(daf_kata))

        # Mengambil kata2 yang ada huruf ?
        new_daf_kata = []
        for kata in daf_kata:
            kata_tanpa_benar = [kata[i] for i in range(5) if pola[i]!='!']
            sudah_benar = True
            for harus_ada_huruf in huruf_tanda_tanya:
                if harus_ada_huruf in kata_tanpa_benar:
                    kata_tanpa_benar.remove(harus_ada_huruf)
                else:
                    sudah_benar=False; break
            if sudah_benar:
                new_daf_kata.append(kata)
        return new_daf_kata

    def cari_kata_terbaik(self, daftar_kata_split, daftar_kata):
        def P(n):
            return n / len(daftar_kata)
        def impurity(n):
            return ((n-1) / n) if n!=0 else 0

        if len(daftar_kata)==1:
            return (daftar_kata[0], daftar_kata)

        hasil = ("TIDAK ADA", -10000)
        new_daftar_kata_split = []
        impurity_awal = impurity(len(daftar_kata))
        my_set = set(''.join(daftar_kata))
        

        # Cari kata terbaik
        for kata in daftar_kata_split:
            impurity_akhir = 0
            if len(my_set.intersection(set(kata)))==0: # kalau tidak ada satupun huruf yg sama dengn daftar kandidat
                continue
            
            daftar_pola = {}
            for kandidat_jawaban in daftar_kata: # Cari segala kemungkinan pola
                pola = self.getPola(kata, kandidat_jawaban)
                daftar_pola[pola] = daftar_pola[pola]+1 if (pola in daftar_pola) else 1

            for pola, n in daftar_pola.items(): # Hitung nilai impurity akhir
                if pola == "!!!!!":
                    impurity_akhir -= 0.1
                else:
                    impurity_akhir += P(n)*impurity(n)

            information_gain = impurity_awal - impurity_akhir           
            if information_gain>hasil[1]:    # Ganti kata terbaik jika information gain lebih besar
                hasil = (kata, information_gain)
            new_daftar_kata_split.append(kata)
        return hasil[0], new_daftar_kata_split

    def getPola(self, tebakan, jawaban):
        list_jawaban = []
        respon_pola = ['*']*5
        for i in range(5):
            if jawaban[i] == tebakan[i]:
                respon_pola[i] = '!'
            else:
                list_jawaban.append(jawaban[i])
        
        # yellow check / ada tapi salah tempat
        for i in range(5):
            if respon_pola[i] == '!':
                continue
            if tebakan[i] in list_jawaban:
                respon_pola[i] = '?'
                list_jawaban.remove(tebakan[i])
        return ''.join(respon_pola)

    def buat_dictionary(self, now):
        hasil = {
            'kata tebakan'     : now.tebakan,
            'kandidat jawaban' : now.kandidat_jawaban,
            'next pola'        : {k:self.buat_dictionary(v) for k,v in now.next_node.items()}
        }

        return hasil

    def simpan_object(self, path):      # Fungsi buat menyimpan 
        with open(path, 'wb') as file:
            object_dict = self.buat_dictionary(self.root)
            pickle.dump(object_dict, file)

    def baca_object(self, path):
        with open(path, 'rb') as file:
            object_dict = pickle.load(file)
            return object_dict

    def jadikan_object(self, object_dict):
        tebakan = object_dict['kata tebakan']
        kandidat_jawaban = object_dict['kandidat jawaban']
        next_node = {}
        node = Node(tebakan, kandidat_jawaban)

        for pola, next_dict in object_dict['next pola'].items():
            next_node[pola] = self.jadikan_object(next_dict)
        node.next_node = next_node
        return node


    def __cari_semua_kemungkinan_pola(self):
        T = {'0' : '*', '1' : '?', '2' : '!'}
        list_pola = []
        for number in range(3**5):             # total kemungkinan pola : 3 pangkat 5
            ternary=np.base_repr(number,base=3)
            pola = str(ternary).zfill(5)       # kasi angka 0 di depan biar sampai 5 digit
            list_pola.append(''.join([T[i] for i in pola]))
        return list_pola