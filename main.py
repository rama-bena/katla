import numpy as np
import pandas as pd
from gameKatla import GameKatla
import os

if __name__ == "__main__":
    daftar_kata = list(pd.read_csv('lima huruf.csv', header=None)[0])
    game = GameKatla(daftar_kata)

    respon = 'y'
    while respon == 'y':
        print("PERMAINAN KATLA")
        game.mulai_game()
        respon = input("Ingin bermain lagi?[y/n]")
        if respon == 'y':
            os.system('cls')
    print(f"SKOR AKHIR ANDA : {game.skor}")
