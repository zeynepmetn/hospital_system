from base_classes.base_class import HastaneYonetimi

import time

class Doktor(HastaneYonetimi):
    def __init__(self, ad, soyad, sifre, doktor_ıd):
        super().__init__(ad, soyad, sifre)
        self.__doktor_ıd = doktor_ıd
    
    def get_doctor_id(self):
        return self.__doktor_ıd

    def giris(self, ad, soyad, sifre):

        veriler = self.dosya_oku(self.personel_dosya)  # Personel dosyasını oku
        for veri in veriler:
            if len(veri) >= 3 and veri[0] == ad and veri[1] == soyad and veri[3] == sifre:  # [2] şifre
                print("Giriş başarılı.")
                return True
        print("Giriş başarısız. Bilgilerinizi kontrol edin.")
        return False

    def dosya_guncelle(self, *args):
        pass

    def kendi_hastalarini_goruntule(self,id):

        try:
            with open(self.randevular_dosya, 'r', encoding='utf-8') as dosya:
                randevular = dosya.readlines()

            doktor_ozel_randevulari = []
            for randevu in randevular:
                # Randevuyu virgülle ayır
                randevu_parcalari = randevu.strip().split(',')
                if len(randevu_parcalari) >= 7 and randevu_parcalari[2] == id and randevu_parcalari[-1]=="Aktif":
                    doktor_ozel_randevulari.append(randevu_parcalari)

            if doktor_ozel_randevulari:
                print("Kendi hastalarınıza ait randevular:")
                for idx, eleman in enumerate(doktor_ozel_randevulari, 1):
                    yazıcı = " | ".join(eleman)
                    print(f"{idx}. {yazıcı}")

                secim_randevu = int(input("Bir randevu seçin: "))
                if secim_randevu < 1 or secim_randevu > len(doktor_ozel_randevulari):
                    print("Geçersiz saat seçimi.")
                    return None

                # Seçilen randevuyu döndür
                ozel_randevum=doktor_ozel_randevulari[secim_randevu - 1]
                print()
                self.rapor_olustur(ozel_randevum)
            else:
                print("Kendi hastalarınıza ait bir randevu bulunamadı.")
                return None
        except FileNotFoundError:
            print("Randevular dosyası bulunamadı.")
        except Exception as e:
            print(f"Randevuları okuma sırasında bir hata oluştu: {e}")
            return None

    def rapor_olustur(self, ozel_randevum):
 
        try:
            # Doktordan gerekli bilgileri al
            hastalik = input("Hastalık tanısını girin: ")
            tahlil_yontemleri = input("Tahlil yöntemlerini girin: ")
            ilac = input("Kullanması gereken ilaçları girin: ")

            # Raporu oluştur
            with open(self.doktorrapor_dosya, 'a', encoding='utf-8') as dosya:
                rapor = (
                    f"Hasta TC: {ozel_randevum[1]}\n"
                    f"Hastalık: {hastalik}\n"
                    f"Tahlil Yöntemleri: {tahlil_yontemleri}\n"
                    f"Kullanması Gereken İlaç: {ilac}\n"
                    f"Doktor ID: {self.__doktor_ıd}\n"
                    "--------------------------------------\n"
                )
                dosya.write(rapor)
                print("Rapor başarıyla oluşturuldu.")
                
            print("Randevu Pasif Hale Getiriliyor...") ; time.sleep(2.0)
            print()
            """
            Seçilen randevuyu pasif hale getir
            """
            try:
                with open(self.randevular_dosya, 'r', encoding='utf-8') as dosya:
                    randevular = dosya.readlines()

                randevular_yenilenen = []
                kontrol_bolum = ozel_randevum[3]
                kontrol_tarih = ozel_randevum[4]

                for satir in randevular:
                    randevu_parcalari = satir.strip().split(',')
                    if (randevu_parcalari[0] == ozel_randevum[0] and 
                        randevu_parcalari[2] == self.__doktor_ıd and 
                        randevu_parcalari[3] == kontrol_bolum and 
                        randevu_parcalari[4] == kontrol_tarih):
                        
                        # Durumu "Aktif"ten "Pasif"e çevir
                        randevu_parcalari[6] = "Pasif"
                        randevular_yenilenen.append(','.join(randevu_parcalari))
                    else:
                        randevular_yenilenen.append(satir.strip())


                # Yeniden güncellenmiş randevuları dosyaya alt alta yaz
                with open(self.randevular_dosya, 'w', encoding='utf-8') as dosya:
                    for randevu in randevular_yenilenen:
                        dosya.write(randevu + '\n')
                
                print()
                print(f"Hasta ID {ozel_randevum[0]} ve Doktor ID {ozel_randevum[2]} için son randevu başarıyla 'Pasif' hale getirildi.")
                tc_m=ozel_randevum[1]
                self.tibbi_gecmis_guncelle(tc_m)
            except FileNotFoundError:
                print("HATA")
            except Exception as e:
                print(f"Oluşan hata:.{e}")

                
        except FileNotFoundError:
            print("Randevular dosyası bulunamadı.")
        except Exception as e:
            print(f"Randevu güncelleme sırasında bir hata oluştu: {e}")

    def tibbi_gecmis_guncelle(hasta_tc, hastalik):
        # Dosyayı okuma
        with open("txtler/hastalar.txt", "r", encoding="utf-8") as f:
            satirlar = f.readlines()
        yeni_veri = []

        for satir in satirlar:
            satirim = satir.strip().split(",")

            # Eğer hasta TC'si eşleşiyorsa, tıbbi geçmişi güncelle
            if satirim[2] == hasta_tc:
                # Eğer geçmiş 'Bilinmiyor' ise, hastalığı ekle
                if satirim[-1] == "Bilinmiyor":
                    satirim[-1] = hastalik
                else:
                    # Eğer geçmiş zaten varsa, hastalığı ekle
                    satirim[-1] += f"|{hastalik}"

            # Güncellenmiş satırı yeni veri listesine ekle
            yeni_veri.append(",".join(satirim))

        # (yeni veriyi dosyaya kaydetme)
        with open("txtler/hastalar.txt", "w", encoding="utf-8") as f:
            for satir in yeni_veri:
                f.write(satir + "\n")


    def raporlari_goruntule(self):
        try:
            # Dosyayı okuma
            with open(self.doktorrapor_dosya, "r", encoding="utf-8") as file:
                satirlar = file.readlines()

            print("===================================")
            print("Hasta TC'ye göre raporları görüntüleme:")
            print("===================================")

            # Hasta ID alınıyor
            hasta_id = input("Hangi hastanın raporunu görmek istiyorsunuz (Hasta TC):").strip()

            # Hasta ID'sine göre raporları filtreleme
            kendi_raporlari = []
            rapor = []
            for satir in satirlar:
                satir = satir.strip()  # Satırdaki boşlukları temizle
                if satir == "--------------------------------------":
                    if any(f"Hasta TC: {hasta_id}" in line for line in rapor):
                        kendi_raporlari.append("\n".join(rapor))
                    rapor = []  # Yeni rapor için temizle
                else:
                    rapor.append(satir)

            # Filtrelenmiş raporları yazdırma
            if not kendi_raporlari:
                print(f"{hasta_id} ID'li hasta için oluşturulmuş bir rapor bulunamadı.")
            else:
                for rapor in kendi_raporlari:
                    print(rapor)
                    print("-" * 40)

        except FileNotFoundError:
            print("Rapor dosyası bulunamadı.")
        except Exception as e:
            print(f"Rapor görüntüleme sırasında bir hata oluştu: {e}")



    @staticmethod
    def bilgi_getirici(aranan_id, aranan_sifre):
        dosya_yolu = r"txtler/personel.txt"
        
        try:
            with open(dosya_yolu, "r", encoding="utf-8") as f:
                satirlarimiz = f.readlines()

            guncellenen_documan_verisi = []
            sozluk = []
            

            for satirim in satirlarimiz:
                satir_parçaları = satirim.split(",") 

                if satir_parçaları[-1].strip() == "Doktor":
                    doktor_id = satir_parçaları[2].strip()  
                    sorgu_sifre = satir_parçaları[3].strip()  

                    if doktor_id == aranan_id and sorgu_sifre == aranan_sifre:
                        ad_bilgisi = satir_parçaları[0].strip()  
                        soyad_bilgisi = satir_parçaları[1].strip()  
                        sozluk.append((ad_bilgisi,soyad_bilgisi)) 
                       
                        guncellenen_documan_verisi.append(satirim)
                
                    else:
                        guncellenen_documan_verisi.append(satirim)
                else:
                        guncellenen_documan_verisi.append(satirim)

            with open(dosya_yolu, "w", encoding="utf-8") as f:
                f.write("".join(guncellenen_documan_verisi))

            #if doktor_bulundu and sozluk:
            
            return sozluk[0][0],sozluk[0][1]
        except:
            print(f"Bilgiler Alinamadi! Hata")
            return False, False