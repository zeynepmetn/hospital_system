#Kutuphaneler
from sub_classes.hasta_class import Hasta
from sub_classes.doktor_class import Doktor
from sub_classes.personel_class import Personel
from sub_classes.sistem_menu import HastaneSistemi

if __name__ == "__main__":
    sistem = HastaneSistemi()
    sistem.ana_menu()

"""
Sisteme Giriş Yaptığınızda önce Personel kısmına gelin
ID:1980 Sifre:16 ile giriş yapın

Doktor kayıt edin

Ana menuye donup ister hasta kayıt açın, ister 
TC: 123456,sife:11 ile giriş yapın.

Randevu alın, görüntüleyin, ya da iptal edin

Randevu aldıktan sonra personel menusune dönün ve 
Beklemede olan randevuları görüntüleyin, seçin ve onaylayın/iptal edin

Onay verdiyseniz Doktor menusune giriş yapın
Doktorid :2, sifre: serce123 hazır doktor ya da kendi kaydettiğiniz doktorun bilgilerini girin
Randevuları Görüntüle ve Rapor Yaz seçerek hasta işlemlerini yapın ve hasta randevusunu pasif yapın.
Raporları Görüntüleye giderek hasta tc ile kayıtlı raporları görüntüleyin.

"""