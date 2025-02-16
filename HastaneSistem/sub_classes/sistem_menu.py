import time,random
from sub_classes.hasta_class import Hasta
from sub_classes.doktor_class import Doktor
from sub_classes.personel_class import Personel
from os import system

class HastaneSistemi:
    def __init__(self):
        self.hasta = Hasta(None,None,None,None,None)
        self.personel = Personel(None,None,None,None)
        self.doktor = Doktor(None,None,None,None)  # Örnek bir doktor eklemesi
        self.haberler= r"txtler/haberler.txt"
        
    def ana_menu(self):
        while True:
            print("===================================")
            print("       HASTANE YÖNETİM SİSTEMİ     ")
            print("===================================")
            print("      Hoş geldiniz!")
            print("1.   Hasta Giriş Yap")
            print("2.    Hasta Kayıt Ol")
            print("3.  Personel Giriş Yap")
            print("4.  Doktor Giriş Yap")
            print("5.        Çıkış")
            print("6.      Haberler")
            print("===================================")

            secim = input("Lütfen bir seçim yapınız (1, 2, 3, 4, 5, 6): ").strip()

            if secim == "1":
                self.hasta_giris_menu()
            elif secim == "2":
                self.hasta_kayit_menu()
            elif secim == "3":
                self.personel_giris_menu()
            elif secim == "4":
                self.doktor_giris_menu()
            elif secim == "5":
                print("Çıkış yapılıyor. İyi günler!")
                break
            elif secim=="6":
                self.haber_goster()

            else:
                print("Geçersiz seçim. Lütfen tekrar deneyin.")

    def doktor_giris_menu(self):
        print("===================================")
        print("         DOKTOR GİRİŞİ             ")
        print("===================================")
        id= input("Doktor ID: ")        
        sifre = input("Şifre: ")
        system("cls")
        bilgi = Doktor.bilgi_getirici(id,sifre)
        if bilgi is None:
            print("Hatalı ID veya Şifre. Lütfen tekrar deneyin.")
            return  # menuye geri don

        x, y = bilgi
        self.doktor=Doktor(x,y,sifre,id)

        
        if self.doktor.giris(x, y, sifre):
            print("Giriş başarılı. Hoş geldiniz! {0}-{1}".format(x,y))
            while True:
                print("1. Randevuları Görüntüle ve Rapor Yaz")
                print("2. Raporları Görüntüle")
                print("3. Ana Menüye Dön")
                secim = input("Bir işlem seçiniz: ").strip()
                if secim == "1":                   
                    self.doktor.kendi_hastalarini_goruntule(id)       
                elif secim == "2":
                    self.doktor.raporlari_goruntule()  # Yeni fonksiyonu burada çağırıyoruz
                elif secim == "3":
                    break
                else:
                    print("Geçersiz seçim.")

    def hasta_giris_menu(self):
        print("===================================")
        print("         HASTA GİRİŞİ             ")
        print("===================================")
        tc = input("TC Kimlik No: ").strip()
        sifre = input("Şifre: ").strip()
        system("cls")
        bilgi = Hasta.bilgi_getirici(tc, sifre)
        if bilgi is None:
            print("Hatalı TC veya Şifre. Lütfen tekrar deneyin.")
            return  # menuye geri don
        x, y = bilgi
        self.hasta = Hasta(x, y, sifre, tc, None)
        
        if self.hasta.giris(sifre, tc):
            print(f"Giriş başarılı. Hoş geldiniz! {x}-{y}")
            while True:
                print()
                print("1. Randevu Al")
                print("2. Randevu İptal Et")
                print("3. Randevularımı Görüntüle")
                print("4. Randevu Geçmişimi Görüntüle")
                print("5. Tıbbi Geçmişimi Görüntüle")
                print("6. Ana Menüye Dön")
                secim = input("Bir işlem seçiniz: ").strip()
                if secim == "1":
                    self.hasta.randevu_al()
                elif secim == "2":
                    self.hasta.randevu_iptal()
                elif secim=="3":
                    self.hasta.randevu_goruntule()
                elif secim == "4":
                    self.hasta.randevu_gecmisi_goruntule()
                elif secim == "5":
                    self.hasta.tibbi_gecmis_goruntule()
                elif secim == "6":
                    break
                else:
                    print("Geçersiz seçim.")
        else:
            print("Giriş başarısız. Bilgilerinizi kontrol edin.")

    def hasta_kayit_menu(self):
        print("===================================")
        print("         HASTA KAYIT               ")
        print("===================================")
        ad = input("Ad: ").strip()
        soyad = input("Soyad: ").strip()
        tc = input("TC Kimlik No: ").strip()
        sifre = input("Şifre: ").strip()
        tibbi_gecmis = "Bilinmiyor"
        system("cls")
        if tc=="":
            print("TC Girmeniz Zorunludur.")
            return
        self.hasta = Hasta(ad, soyad, tc, sifre, tibbi_gecmis)
        
        if self.hasta.hasta_ekle(ad, soyad, tc, sifre, tibbi_gecmis):
            print("Hasta başarıyla kaydedildi.")
        else:
            print("Hata: Bu TC kimlik numarasıyla kayıtlı bir hasta zaten mevcut.")
            return
    
    def personel_giris_menu(self):
        print("===================================")
        print("         PERSONEL GİRİŞİ          ")
        print("===================================")
        pers_id = input("Personel ID(Kimlik) No: ")
        pers_sifre = input("Şifre: ")
        system("cls")
        bilgi = Personel.bilgi_getirici(pers_id,pers_sifre)
        if bilgi is None:
            print("Hatalı TC veya Şifre. Lütfen tekrar deneyin.")
            return  # menuye geri don

        x,y,z,t = bilgi
        self.personel=Personel(x,y,z,t)

        if self.personel.giris(pers_sifre, pers_id):
            print("Giriş başarılı. Hoş geldiniz! {0}-{1}".format(x,y))
            while True:
                print("1. Beklemede Olan Randevuları Görüntüle")
                print("2. Doktor Kayıt")
                print("3. Ana Menüye Dön")
                secim = input("Bir işlem seçiniz: ").strip()
                if secim == "1":
                    self.personel.beklemedeki_randevulari_goruntule()
                    
                elif secim == "2":
                    self.personel.doktor_ekle()
                elif secim =="3":
                    break
                else:
                    print("\nGeçersiz seçim!\n")
        else:
            print("Giriş başarısız. Bilgilerinizi kontrol edin.")
    
    def haber_goster(self):
        print("===================================")
        print("HABERLER".center(36,"*"))
        print("===================================")
        
        with open(self.haberler, "r", encoding="utf-8") as f:
            icerik = f.read()  

        if icerik:
            haber=icerik.split("---")                     
            secilen = random.choice(haber)  
            haber.remove(secilen)
            print(secilen.strip()+"\n")
            time.sleep(3.0)

            while True:
                print("1-Yeni Haber 2-çıkış")
                sec=input("<<>>")
                if sec=="1":
                    self.haber_goster()
                elif sec=="2":
                    break