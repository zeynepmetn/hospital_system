from base_classes.base_class import HastaneYonetimi
from os import system
class Personel(HastaneYonetimi):
    counter = 0
    def __init__(self, ad, soyad, sifre, gorev):
        super().__init__(ad, soyad, sifre)
        self.__gorev = gorev
        Personel.counter += 1
    
    def get_gorev(self):
        return self.__gorev
    
    def set_gorev(self, deger):
        self.__gorev = deger

    def giris(self, sifre, kimlik_no):
        return self.kimlik_dogrula(sifre, kimlik_no, self.personel_dosya)

    @classmethod
    def personel_counter(cls):
        return cls.counter
    
    def beklemedeki_randevulari_goruntule(self):
        print("Bekleyen Randevular:\n")
        
        icerik=self.dosya_oku(self.randevular_dosya)

        bekleyen_randevular = [satir for satir in icerik if satir[-1].strip() == "Beklemede"]

        if not bekleyen_randevular:
            print("Beklemede olan randevu yok.")
            return

        # Bekleyen randevuları listeleme
        for i, randevu in enumerate(bekleyen_randevular):
            print(f"{i + 1}. HASTA-ID:{randevu[0]} Hasta-TC:{randevu[1]} Doktor-ID:{randevu[2]} Bölüm:{randevu[3]} Tarih-Saat:{randevu[4]} | {randevu[5]}")

        # İşlem seçimi
        secim = input("\nBir işlem seçin (onaylamak için 'O', iptal etmek için 'I' tuşlayın): ").upper()

        if secim == "O":
            secim_id = int(input("Onaylamak için randevu numarasını girin: "))
            if 1 <= secim_id <= len(bekleyen_randevular):
                self.dosya_guncelle(bekleyen_randevular[secim_id - 1])
            else:
                print("Geçersiz seçim.")
        elif secim == "I":
            secim_id = int(input("İptal etmek için randevu numarasını girin: "))
            if 1 <= secim_id <= len(bekleyen_randevular):
                self.randevu_iptal_et(bekleyen_randevular[secim_id - 1])
            else:
                print("Geçersiz seçim.")
        else:
            print("Geçersiz işlem.")
    
    def doktor_ekle(self):    

        try:
            satirlar= self.dosya_oku(self.personel_dosya)

            mevcut_idler = set()
            for satir in satirlar:              
                if len(satir) > 2: 
                    mevcut_idler.add(satir[2])
        except FileNotFoundError:
            mevcut_idler = set()


        while True:
            doktor_id = input("Doktor ID: ").strip()
            if doktor_id in mevcut_idler:
                print("HATA: Bu ID zaten kayıtlı. Lütfen başka bir ID giriniz.")
            else:
                break

        unvanlar = [
            "Pratisyen Hekim",
            "Uzm. Dr",
            "Op. Dr",
            "Doç. Dr",
            "Prof. Dr",
            "Dr. Öğr Üyesi",
            "Başasistan",
            "Asistan Doktor",
            "Başhekim",
            "Konsültan Hekim"
        ]

        for i, unvanım in enumerate(unvanlar):
            print(f"{i+1}--{unvanım}")
        unvan_isim = int(input("Unvan Sec: ").strip())
        bas_unvan = unvanlar[unvan_isim-1]
        doktor_isim = input("Doktor İsmi Soyismi(isim-soyisim): ").strip().split("-")
        kayıt_mahlas = f"{bas_unvan}.{"-".join(doktor_isim)}"

        bolumlerimiz = [
            "Acil Tıp",
            "Anesteziyoloji ve Reanimasyon",
            "Beyin ve Sinir Cerrahisi",
            "Çocuk Cerrahisi",
            "Çocuk Sağlığı ve Hastalıkları",
            "Dermatoloji",
            "Enfeksiyon Hastalıkları",
            "Fiziksel Tıp ve Rehabilitasyon",
            "Genel Cerrahi",
            "Göğüs Cerrahisi",
            "Göğüs Hastalıkları",
            "Göz Hastalıkları",
            "İç Hastalıkları (Dahiliye)",
            "Kadın Hastalıkları ve Doğum",
            "Kardiyoloji",
            "Kulak Burun Boğaz Hastalıkları (KBB)",
            "Nöroloji",
            "Ortopedi ve Travmatoloji",
            "Plastik Rekonstrüktif ve Estetik Cerrahi",
            "Psikiyatri",
            "Radyoloji",
            "Üroloji",
            "Hematoloji",
            "Endokrinoloji",
            "Onkoloji",
            "Nefroloji",
            "Gastroenteroloji",
            "Romatoloji",
            "Patoloji",
            "Yoğun Bakım",
            "Tıbbi Genetik",
            "Tıbbi Mikrobiyoloji",
            "Tıbbi Biyokimya"
        ]

        for i, bolumumuz in enumerate(bolumlerimiz):
            print(f"{i+1}--{bolumumuz}")
        
        bolum_sec = int(input("Bölüm: ").strip())
        bolum = bolumlerimiz[bolum_sec-1]
        calisma_saatleri = input("Çalışma Saatleri (örn. 09:00-17:00): ").strip()
        sifre = input("Doktor Şifresi: ").strip()

        doktor_bilgisi = [doktor_id, kayıt_mahlas,bolum,calisma_saatleri]
        self.dosya_veri_ekle(self.doktorlar_dosya, doktor_bilgisi)

        personel_bilgisi = [doktor_isim[0],doktor_isim[1],doktor_id,sifre,"Doktor"]
        self.dosya_veri_ekle(self.personel_dosya ,personel_bilgisi)
        
        print(f"Doktor {kayıt_mahlas} başarıyla eklendi!")


    def randevu_islemleri(self, randevu):
        print(f"Seçilen randevu: {randevu[0]} - {randevu[1]} - {randevu[2]}")
        islem = input("Randevuyu onaylamak için 'O', iptal etmek için 'I' tuşlayın: ").upper()

        if islem == "O":
            self.dosya_guncelle(randevu)
        elif islem == "I":
            self.randevu_iptal_et(randevu)
        else:
            print("Geçersiz işlem.")
    
    def dosya_guncelle(self, randevu):
            # Dosyadaki randevuyu "Onaylandı" olarak güncelle
        yeni_randevular = []
        randevular = self.dosya_oku(self.randevular_dosya)
        
        for satir in randevular:
            
            if satir[0] == randevu[0] and satir[1] == randevu[1] and satir[2] == randevu[2] and satir[3]==randevu[3] and satir[4]==randevu[4] and satir[5]==randevu[5] and satir[-1].strip() == "Beklemede":
                # Satırdaki durum bilgisini "Aktif" olarak değiştir
                satir[-1] = "Aktif"
                yeni_randevular.append(",".join(satir) + "\n")
            else:
                yeni_randevular.append(",".join(satir) + "\n")

        with open(self.randevular_dosya, "w", encoding="utf-8") as dosya:
            dosya.writelines(yeni_randevular)

        print(f"HASTA-ID:{randevu[0]} Hasta-TC:{randevu[1]} Doktor-ID:{randevu[2]} Bölüm:{randevu[3]} Tarih-Saat:{randevu[4]} | {randevu[5]} AKTİFLESTİRİLDİ")
    
    def randevu_iptal_et(self, randevu):
         # Dosyadan randevuyu sil
        yeni_randevular = []
        with open(self.randevular_dosya, "r", encoding="utf-8") as dosya:
            icerik = dosya.readlines()
        
        for satir in icerik:
            satir_listesi = satir.strip().split(",")
            if satir_listesi[0] == randevu[0] and satir_listesi[1] == randevu[1] and satir_listesi[2] == randevu[2] and satir_listesi[3]==randevu[3] and satir_listesi[4]==randevu[4] and satir_listesi[5]==randevu[5] and satir_listesi[-1].strip() == "Beklemede":
                satir_listesi[-1] = "İptal"
                yeni_randevular.append(",".join(satir_listesi) + "\n")
            else:
                yeni_randevular.append(satir)

        with open(self.randevular_dosya, "w", encoding="utf-8") as dosya:
            dosya.writelines(yeni_randevular)

        print(f"Randevu iptal edildi")

    @staticmethod
    def bilgi_getirici(serachid,searchsifre):
        dosya_yolu = r"txtler/personel.txt"
        with open(dosya_yolu,"r",encoding="utf-8") as f:
            satirlarimiz=f.readlines()
            
        guncellenen_documan_verisi=[]
        sozluk1=[]
        
        try:
            for satirim in satirlarimiz:
                satir_parçaları=satirim.split(",")
                sorgu_tc=satir_parçaları[2].strip()
                sorgu_sifre=satir_parçaları[3].strip()
                
                if sorgu_tc == serachid and sorgu_sifre == searchsifre:
                    ad_bilgisi= satir_parçaları[0].strip()
                    soyad_bilgisi= satir_parçaları[1].strip()
                    sifrem=satir_parçaları[3].strip()
                    gorevm=satir_parçaları[-1].strip()
                    
                    guncellenen_documan_verisi.append(satirim)
                    sozluk1.append((ad_bilgisi,soyad_bilgisi,sifrem,gorevm))
                else:
                    guncellenen_documan_verisi.append(satirim)
            
            with open(dosya_yolu, "w", encoding="utf-8") as f:
                f.write("".join(guncellenen_documan_verisi))
            
            return sozluk1[0][0],sozluk1[0][1],sozluk1[0][2],sozluk1[0][3]
        except:
            print(f"Bilgiler Alinamadi!")