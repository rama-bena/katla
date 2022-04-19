import random
from katla import Katla

class GameKatla():
    def __init__(self, daftar_kata):
        self.daftar_kata = daftar_kata
        self.skor = 0
        self.__jawaban = ""

    def mulai_game(self):
        self.__jawaban = random.choice(self.daftar_kata)
        total_tebakan = 6
        menang = False

        for idx_tebakan in range(total_tebakan):
            tebakan = input("Tebakan Anda : ")
            respon_pola = self.__evaluasi_tebakan(tebakan)
            print(f"Hasil tebakan Anda : {respon_pola}")

            if respon_pola == "!!!!!":
                menang = True
                break

        print("Permainan selesai!")
        print(f"Kata yang benar : {self.__jawaban}")
        if menang:
            self.skor += 1
            print("SELAMAT ANDA MENANG")
            print(f"Skor Anda : {self.skor}")
        else:
            print("Anda gagal, kesempatan mencoba sudah 6")

    def __evaluasi_tebakan(self, tebakan):
        list_jawaban = []
        respon_pola = ['*']*5
        for i in range(5):
            if self.__jawaban[i] == tebakan[i]:
                respon_pola[i] = '!'
            else:
                list_jawaban.append(self.__jawaban[i])
        
        for i in range(5):
            if respon_pola[i] == '!':
                continue
            if tebakan[i] in list_jawaban:
                respon_pola[i] = '?'
                list_jawaban.remove(tebakan[i])
        return ''.join(respon_pola)