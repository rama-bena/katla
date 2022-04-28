from pprint import pprint
import numpy as np
import pandas as pd
from gameKatla import GameKatla
from tree import DecisionTree
import os

# if __name__ == "__main__":
#     file_path = "D:\\Rama Nitip\\python\\katla\\file text\\lima huruf katla.csv"
#     daftar_kata = list(pd.read_csv(file_path, header=None)[0])
#     game = GameKatla(daftar_kata)

#     respon = 'y'
#     while respon == 'y':
#         print("PERMAINAN KATLA")
#         game.mulai_game()
#         respon = input("Ingin bermain lagi?[y/n] : ")
#         if respon == 'y':
#             os.system('cls')
#     print(f"SKOR AKHIR ANDA : {game.skor}")

PATH_FILE_TEXT = "D:\\Rama Nitip\\python\\katla\\file text\\"
daftar_kata = list(pd.read_csv(PATH_FILE_TEXT + 'lima huruf katla.csv', header=None)[0])
print(f"Banyak Kata : {len(daftar_kata)}")

with open(PATH_FILE_TEXT+"coba.csv") as file:
    df_sample = file.readlines()
df_sample = [kata[:-1] for kata in df_sample]
print(df_sample)

DT = DecisionTree()
DT.buat_tree(df_sample, pakai_semua_daftar=True)

# pprint(DT.buat_dictionary(DT.root))