from base_classes.base_class import HastaneYonetimi

class Hasta(HastaneYonetimi):
    
    def __init__(self, ad, soyad, sifre, tc, tibbi_gecmis):
        super().__init__(ad, soyad, sifre)
        self.__tc = tc
        self.__tibbi_gecmis = tibbi_gecmis
    
    def get_tc(self):
        return self.__tc

    def set_tc(self, deger):
        if len(deger) == 11 and deger.isdigit():
            self.__tc = deger
        else:
            raise ValueError("TC 11 haneli bir sayı olmalıdır.")

    def get_tibbi_gecmis(self):
        return self.__tibbi_gecmis

    def set_tibbi_gecmis(self, deger):
        if isinstance(deger, str):
            self.__tibbi_gecmis = deger
        else:
            raise ValueError("Tıbbi geçmiş bir metin olmalıdır.")
             
    @classmethod
    def hasta_id_atamasi(cls,dosya_yolu):
        hastalar = cls.dosya_oku(dosya_yolu)
        if not hastalar:
            return 1
        mevcut_idler = [int(hasta[0]) for hasta in hastalar]
        return max(mevcut_idler) + 1
    
    def giris(self, sifre, kimlik_no):
        return self.kimlik_dogrula(sifre, kimlik_no, self.hastalar_dosya)

    def randevu_al(self):
        print("Randevu Oluşturma")
        doktorlar = self.dosya_oku(self.doktorlar_dosya)
        branslar = sorted(set([doktor[2] for doktor in doktorlar]))
        print("\nBranşlar Listesi:")
        if not branslar:
            print("Kayıtlı Doktor Bulunamadı")
            return
        else:
            
            for idx, brans in enumerate(branslar, 1):
                print(f"{idx}. {brans}")

        secim_brans = int(input("Bir branş seçin: "))
        if secim_brans < 1 or secim_brans > len(branslar):
            print("Geçersiz branş seçimi.")
            return

        secilen_brans = branslar[secim_brans - 1]
        print(f"{secilen_brans} branşındaki doktorlar:")

        doktorlar_secilen = [doktor for doktor in doktorlar if doktor[2] == secilen_brans]
        for idx, doktor in enumerate(doktorlar_secilen, 1):
            print(f"{idx}. {doktor[1]} - Çalışma Saatleri: {doktor[3]}")

 
        secim_doktor = int(input("Bir doktor seçin: "))
        if secim_doktor < 1 or secim_doktor > len(doktorlar_secilen):
            print("Geçersiz doktor seçimi.")
            return

        secilen_doktor = doktorlar_secilen[secim_doktor - 1]
        calisma_saatleri = secilen_doktor[3].split('-')
        baslangic_saat = int(calisma_saatleri[0].split(':')[0])
        bitis_saat = int(calisma_saatleri[1].split(':')[0])

        # uygun saatleri bulma
        uygun_saatler = self.uygun_saatleri_bul(secilen_doktor[0], baslangic_saat, bitis_saat)
        if not uygun_saatler:
            print("Bu doktor için uygun saat bulunmamaktadır.")
            return

        print("Randevu alabileceğiniz saatler:")
        for idx, saat in enumerate(uygun_saatler, 1):
            print(f"{idx}. {saat}")

        secim_saat = int(input("Bir saat seçin: "))
        if secim_saat < 1 or secim_saat > len(uygun_saatler):
            print("Geçersiz saat seçimi.")
            return

        secilen_saat = uygun_saatler[secim_saat - 1]
        tarih = input("Randevu tarihi girin (YYYY-AA-GG): ")

        # aynı güne randevu kontrolü
        randevular = self.dosya_oku(self.randevular_dosya)
        for randevu in randevular:
            if randevu[1] == self.get_tc() and randevu[4] == tarih:
                print("Hata: Aynı güne birden fazla randevu alamazsınız.")
                return
        
        # hastanın daha önce randevu alıp almadığını kontrol
        mevcut_hasta_id = None
        for randevu in randevular:
            if randevu[1] == self.get_tc():
                mevcut_hasta_id = randevu[0]
                break

        # eğer ilk randevusu ise ona bir id atıyoruz
        if mevcut_hasta_id is None:
            mevcut_hasta_id = str(Hasta.hasta_id_atamasi(self.randevular_dosya))

        # randevu oluşturma
        randevu = [mevcut_hasta_id, self.get_tc(), secilen_doktor[0], secilen_brans, tarih, secilen_saat, "Beklemede"]
        randevular.append(randevu)

        # randevuyu dosyaya kaydet
        self.dosya_veri_ekle(self.randevular_dosya, randevu)

        print("Randevunuz başarıyla oluşturuldu.")

    def uygun_saatleri_bul(self, doktor_id, baslangic_saat, bitis_saat):
        dolu_saatler = []
        for randevu in self.dosya_oku(self.randevular_dosya):
            if randevu[2] == doktor_id and randevu[6] in ["Beklemede", "Aktif"]:
                dolu_saatler.append(randevu[5])

        uygun_saatler = []
        for saat in range(baslangic_saat, bitis_saat):
            saat_str = f"{saat:02}:00"
            if saat_str not in dolu_saatler:
                uygun_saatler.append(saat_str)

        return uygun_saatler
       
    def dosya_guncelle(self, randevular, secilen_randevu):

        with open(self.randevular_dosya, "w", encoding="utf-8") as file:
            for randevu in randevular:
                if randevu == secilen_randevu:
                    file.write(",".join(secilen_randevu) + "\n")
                else:
                    file.write(",".join(randevu) + "\n")
            
    def hasta_ekle(self, ad, soyad, tc, sifre, tibbi_gecmis):
            hastalar = self.dosya_oku(self.hastalar_dosya)

            for hasta in hastalar:
                if hasta[2] == str(tc):
                    return False
                
            veri = [ad, soyad, str(tc), str(sifre), tibbi_gecmis]
            HastaneYonetimi.dosya_veri_ekle(self.hastalar_dosya, veri)
            return True
   
    def randevu_iptal(self):    
        randevular = self.dosya_oku(self.randevular_dosya)

        uygun_randevular = [r for r in randevular if r[1] == self.get_tc() and r[6] in ["Beklemede", "Aktif"]]

        if not uygun_randevular:
            print("İptal edilebilecek randevu bulunamadı.")
            return

        print("İptal edilebilecek randevularınız:")
        for idx, randevu in enumerate(uygun_randevular, 1):
            print(f"{idx}. Tarih: {randevu[4]}, Branş: {randevu[3]}, Saat: {randevu[5]}, Durum: {randevu[6]}")

        try:
            # kuıllanıcıdan iptal etmek istediği randevuyu seçmesini iste
            secim = int(input("İptal etmek istediğiniz randevuyu seçiniz: "))
            if secim < 1 or secim > len(uygun_randevular):
                print("Geçersiz seçim.")
                return

           
            secilen_randevu = uygun_randevular[secim - 1]

            # randevunun durumunu iptal yap
            secilen_randevu[6] = "İptal"
            print("Randevu iptal edildi.")

            self.dosya_guncelle(randevular, secilen_randevu)

        except ValueError:
            print("Lütfen geçerli bir sayı girin.")

    def randevu_goruntule(self):
        randevular = self.dosya_oku(self.randevular_dosya)
        doktorlar = self.dosya_oku(self.doktorlar_dosya)
        
        # hastanin tcsine gore randevular
        hasta_randevulari = [
        randevu for randevu in randevular 
        if randevu[1] == self.get_tc() and randevu[6] in ["Beklemede", "Aktif"]
        ]

        if not hasta_randevulari:
            print("Kayıtlı bir randevunuz bulunmamaktadır.")
            return
        
        print("Randevularınız:")
        for randevu in hasta_randevulari:
            doktor_id = randevu[2]
            doktor = None  
            for d in doktorlar:
                if d[0] == doktor_id:
                    doktor = d
                    break 
            doktor_adi = doktor[1]
            doktor_brans = doktor[2]
            tarih = randevu[4]
            saat = randevu[5]
            durum = randevu[6]
            print(f"Doktor: {doktor_adi} (Branş: {doktor_brans}), Tarih: {tarih}, Saat: {saat}, Durum: {durum}")

    def randevu_gecmisi_goruntule(self):
        randevular = self.dosya_oku(self.randevular_dosya)
        doktorlar = self.dosya_oku(self.doktorlar_dosya)
        
        # Hastanın TC'sine göre randevuları al
        hasta_randevulari = [randevu for randevu in randevular if randevu[1] == self.get_tc() and (randevu[6] == "Tamamlanmış" or randevu[6] == "İptal")]

        if not hasta_randevulari:
            print("Tamamlanmış randevunuz bulunmamaktadır.")
            return
        
        print("Geçmiş Randevularınız:")
        for randevu in hasta_randevulari:
            doktor_id = randevu[2]
            doktor = None
            for d in doktorlar:
                if d[0] == doktor_id:
                    doktor = d
                    break
            doktor_adi = doktor[1]
            doktor_brans = doktor[2]
            tarih = randevu[4]
            saat = randevu[5]
            durum = randevu[6]
            print(f"Doktor: {doktor_adi} (Branş: {doktor_brans}), Tarih: {tarih}, Saat: {saat}, Durum: {durum}")

    def tibbi_gecmis_goruntule(self):
        hastalar = self.dosya_oku(self.hastalar_dosya)

        hasta_tc = self.get_tc()
        tibbigecmis = None

        for hasta in hastalar:
            if hasta[2] == hasta_tc: 
                tibbigecmis = hasta[4]  # Tıbbi geçmişi al
                break

        if tibbigecmis:
            print(f"Tıbbi Geçmişiniz: {tibbigecmis}")
        else:
            print("Bu TC numarasına ait tıbbi geçmiş bulunamadı.")

    @staticmethod
    def bilgi_getirici(searchtc,searchsifre):
            
        dosya_yolu = r"txtler/hastalar.txt"
        
        with open(dosya_yolu,"r",encoding="utf-8") as f:
            satirlarimiz=f.readlines()
            
        guncellenen_documan_verisi=[]
        sozluk1=[]
        try:
            for satirim in satirlarimiz:
                satir_parçaları=satirim.split(",")
                sorgu_tc = satir_parçaları[2].strip()
                sorgu_sifre = satir_parçaları[3].strip()
                
                if sorgu_tc==searchtc and sorgu_sifre==searchsifre:
                    ad_bilgisi= satir_parçaları[0].strip()
                    soyad_bilgisi= satir_parçaları[1].strip()
                    
                    guncellenen_documan_verisi.append(satirim)
                    sozluk1.append((ad_bilgisi,soyad_bilgisi))
                else:
                    guncellenen_documan_verisi.append(satirim)
            
            with open(dosya_yolu, "w", encoding="utf-8") as f:
                f.write("".join(guncellenen_documan_verisi))
            
            return sozluk1[0][0],sozluk1[0][1]
        except:
            print(f"Bilgiler Alinamadi!")