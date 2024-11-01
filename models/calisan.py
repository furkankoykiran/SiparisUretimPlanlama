from utils.Helpers import Helpers
from models.urun import Urun

class Calisan:
    def __init__(self, isim, soyisim, maas):
        self.isim = isim
        self.soyisim = soyisim
        self.maas = maas

    @staticmethod
    def menu(db):
        while True:
            print("""
            1. Yeni Çalışan Ekle
            2. Çalışanları Görüntüle
            3. Çalışan Sil
            4. Geri Dön
            """)
            secim = Helpers.secim_al(range(1, 5))
            if secim == 1:
                Calisan.ekle(db)
            elif secim == 2:
                Calisan.goruntule(db)
            elif secim == 3:
                Calisan.sil(db)
            elif secim == 4:
                break

    @staticmethod
    def ekle(db):
        isim = Helpers.dogrula_string(f"Çalışan adı: ")
        soyisim = Helpers.dogrula_string(f"Çalışan soyadı: ")
        maas = Helpers.dogrula_pozitif_tamsayi(f"Maaş: ")

        urunler = Urun.goruntule(db)
        if not urunler:
            Helpers.hata_mesaji("Ürün bulunamadı. Önce ürün ekleyin.")
            return
        
        urun_id = Helpers.dogrula_pozitif_tamsayi(f"Çalışanın üreteceği ürün ID'si: ")

        calisan_id = db.calisan_ekle(isim, soyisim, maas, urun_id)
        print("Çalışan ve üretim ilişkisi başarıyla eklendi.")

    @staticmethod
    def goruntule(db):
        calisanlar = db.calisanlari_goster()
        if calisanlar:
            for calisan in calisanlar:
                calisan_id, isim, soyisim, maas, urun_adi = calisan
                print(f"""
                Çalışan ID: {calisan_id}
                İsim: {isim}
                Soyisim: {soyisim}
                Maaş: {maas}
                Ürettiği Ürün: {urun_adi}
                """)
        else:
            print("Görüntülenecek çalışan yok.")
        return calisanlar

    @staticmethod
    def sil(db):
        calisanlar = Calisan.goruntule(db)
        if not calisanlar:
            Helpers.hata_mesaji("Silinecek çalışan yok.")
            return

        calisan_id = Helpers.dogrula_pozitif_tamsayi(f"Silmek istediğiniz çalışan ID'si: ")
        db.calisan_sil(calisan_id)
        print("Çalışan başarıyla silindi.")
