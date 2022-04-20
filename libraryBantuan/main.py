import numpy as np
import pandas as pd
from gameKatla import GameKatla
import os

if __name__ == "__main__":
    file_path = 'D:\Rama Nitip\python\katla\lima huruf.csv'
    daftar_kata = list(pd.read_csv(file_path, header=None)[0])
    game = GameKatla(daftar_kata)

    respon = 'y'
    while respon == 'y':
        print("PERMAINAN KATLA")
        game.mulai_game()
        respon = input("Ingin bermain lagi?[y/n] : ")
        if respon == 'y':
            os.system('cls')
    print(f"SKOR AKHIR ANDA : {game.skor}")
