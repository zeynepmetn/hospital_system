from abc import ABC, abstractmethod

import time
from os import system
# Base Class ---------------------------------------------------------------------
class HastaneYonetimi(ABC):
    def __init__(self, ad, soyad, sifre):
        self.__ad = ad
        self.__soyad = soyad
        self.__sifre = sifre
        self.hastalar_dosya = r"txtler/hastalar.txt"
        self.randevular_dosya = r"txtler/randevular.txt"
        self.doktorlar_dosya = r"txtler/doktorlar.txt"
        self.personel_dosya = r"txtler/personel.txt"
        self.doktorrapor_dosya = r"txtler/doktorraporu.txt"

    def get_ad(self):
        return self.__ad

    def set_ad(self, deger):
        self.__ad = deger

    def get_soyad(self):
        return self.__soyad

    def set_soyad(self, deger):
        self.__soyad = deger

    def get_sifre(self):
        return self.__sifre

    def set_sifre(self, deger):
        self.__sifre = deger

    @abstractmethod
    def giris(self):
        pass

    @abstractmethod
    def dosya_guncelle(self, *args):
        pass

    @staticmethod
    def dosya_oku(dosya_yolu):
        try:
            with open(dosya_yolu, "r", encoding="utf-8") as file:
                satirlar = file.readlines()
            return [satir.strip().split(",") for satir in satirlar]
        except FileNotFoundError:
            print(f"{dosya_yolu} bulunamadı.")
            return []

    @staticmethod
    def dosya_veri_ekle(dosya_yolu, veri):
        with open(dosya_yolu, "a", encoding="utf-8") as dosya:
            dosya.write(",".join(veri) + "\n")
       
    @staticmethod
    def kimlik_dogrula(sifre, kimlik_no, dosya_yolu):
        veriler = HastaneYonetimi.dosya_oku(dosya_yolu)
        for veri in veriler:
            if veri[3] == sifre and veri[2] == kimlik_no:
                print("Bilgiler Kontrol Ediliyor..."); time.sleep(2.0)
                system("cls")
                return True
        return False
    