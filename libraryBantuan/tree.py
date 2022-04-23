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
        self.kata = kata
        self.daftar_kata = daftar_kata 
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
        self.daftar_kata_semua = None  

    def kata_berikutnya(self, pola, awal=False):
        if awal:
            self.now = self.root
        if pola in self.now.next_node:
            self.now = self.now.next_node[pola]
        return self.now.kata

    def buat_tree(self, daftar_kata, kata_root=None, pakai_semua_daftar=False):
        """membuat tree

        Args:
            daftar_kata (list): daftar kata
            kata_root (str, optional): kata awal. Defaults to None.
            pakai_semua_daftar (bool, optional): pakai daftar kata semua untuk split. Defaults to False.
        """        
        

        # Bagian yang pertama kali jalan
        self.pakai_semua_daftar = pakai_semua_daftar
        self.daftar_kata_semua  = daftar_kata
        if kata_root == None:
            kata_root = self.cari_kata_terbaik(daftar_kata)
        self.root = self.__buat_tree(kata_root, daftar_kata, 0)
        self.now  = self.root
    
    def __buat_tree(self, kata, daftar_kata, depth): # buat tree rekursif
        node = Node(kata, daftar_kata)
        if (depth==10) or (len(daftar_kata)<=1): # BASE CASE
            return node
        
        for idx, pola in enumerate(self.semua_pola):
            if kata == 'sarit':
                print(f"{idx} dari {len(self.semua_pola)}")
            next_daftar_kata = self.kandidat(kata, pola, daftar_kata)
            if len(next_daftar_kata)==0:        # tidak ada daftar kata dengan pola ini
                continue
            next_kata = self.cari_kata_terbaik(next_daftar_kata)
            node.next_node[pola] = self.__buat_tree(next_kata, next_daftar_kata, depth+1)
        return node
    
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

    def cari_kata_terbaik(self, daftar_kata):
        def P(n):
            return n / len(daftar_kata)
        def impurity(n):
            return ((n-1) / n) if n!=0 else 0

        hasil = ("TIDAK ADA", -10000)
        impurity_awal = impurity(len(daftar_kata))
        # Cari kata terbaik
        loop_daftar_kata = self.daftar_kata_semua if self.pakai_semua_daftar else daftar_kata
        for kata in loop_daftar_kata:
            impurity_akhir = 0
            for pola in self.semua_pola:         # untuk setiap pola hitung kemungkinannya
                n = len(self.kandidat(kata, pola, daftar_kata))
                impurity_akhir += P(n) * impurity(n)
            
            information_gain = impurity_awal - impurity_akhir           
            if information_gain>hasil[1]:
                hasil = (kata, information_gain)
        return hasil[0]

    def buat_dictionary(self, now):
        hasil = {
            'kata'       : now.kata,
            'daftar kata': now.daftar_kata,
            'next'       : {k:self.buat_dictionary(v) for k,v in now.next_node.items()}
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
        kata = object_dict['kata']
        daftar_kata = object_dict['daftar kata']
        next_node = {}
        node = Node(kata, daftar_kata)

        for pola, next_dict in object_dict['next'].items():
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