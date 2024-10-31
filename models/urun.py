from utils.Helpers import Helpers

class Urun:
    def __init__(self, urun_adi, maliyet, uretim_suresi, stok=0):
        self.urun_adi = urun_adi
        self.maliyet = maliyet
        self.uretim_suresi = uretim_suresi
        self.stok = stok

    @staticmethod
    def menu(db):
        while True:
            print("""
            1. Yeni Ürün Ekle
            2. Ürünleri Görüntüle
            3. Ürün Güncelle
            4. Ürün Sil
            5. Stok Ekle
            6. Geri Dön
            """)
            secim = Helpers.secim_al(range(1, 7))
            if secim == 1:
                Urun.ekle(db)
            elif secim == 2:
                Urun.goruntule(db)
            elif secim == 3:
                Urun.guncelle(db)
            elif secim == 4:
                Urun.sil(db)
            elif secim == 5:
                Urun.stok_ekle(db)
            elif secim == 6:
                break

    @staticmethod
    def ekle(db):
        urun_adi = Helpers.dogrula_string(f"Ürün adı: ")
        maliyet = Helpers.dogrula_pozitif_tamsayi(f"Ürün maliyeti: ")
        db.urun_ekle(urun_adi, maliyet)
        print("Ürün başarıyla eklendi.")

    @staticmethod
    def goruntule(db):
        urunler = db.urunleri_goster()
        if urunler:
            for urun in urunler:
                print(f"""
                ID: {urun[0]}
                Ad: {urun[1]}
                Maliyet: {urun[2]}
                Stok: {urun[3]}
                """)
        else:
            print("Görüntülenecek ürün yok.")
        return urunler

    @staticmethod
    def guncelle(db):
        urunler = Urun.goruntule(db)
        if not urunler:
            Helpers.hata_mesaji("Güncellenecek ürün yok.")
            return

        urun_id = Helpers.dogrula_pozitif_tamsayi(f"Güncellemek istediğiniz ürün ID'si: ")
        urun_adi = Helpers.dogrula_string(f"Yeni ürün adı: ")
        maliyet = Helpers.dogrula_pozitif_tamsayi(f"Yeni maliyet: ")
        db.urun_guncelle(urun_id, urun_adi, maliyet)
        print("Ürün başarıyla güncellendi.")

    @staticmethod
    def sil(db):
        urunler = Urun.goruntule(db)
        if not urunler:
            Helpers.hata_mesaji("Silinecek ürün yok.")
            return

        urun_id = Helpers.dogrula_pozitif_tamsayi(f"Silmek istediğiniz ürün ID'si: ")
        db.urun_sil(urun_id)
        print("Ürün başarıyla silindi.")

    @staticmethod
    def stok_ekle(db):
        urunler = Urun.goruntule(db)
        if not urunler:
            Helpers.hata_mesaji("Stok eklemek için önce ürün ekleyin.")
            return

        urun_id = Helpers.dogrula_pozitif_tamsayi(f"Stok eklemek istediğiniz ürün ID'si: ")
        miktar = Helpers.dogrula_pozitif_tamsayi(f"Eklenecek stok miktarı: ")
        db.stok_artir(urun_id, miktar)
        print("Stok başarıyla eklendi.")

        siparisler = db.beklemedeki_siparisleri_getir(urun_id)
        for siparis in siparisler:
            siparis_id = siparis[0]
            siparis_miktari = db.siparis_miktarini_cek(siparis_id)
            if siparis_miktari <= miktar:
                print(f"Ürün ID {urun_id} stoğu {siparis_miktari} siparişi karşıladı. Sipariş ID {siparis_id} tamamlandı.")
                db.siparis_durum_guncelle(siparis_id, "Tamamlandı")
                miktar -= siparis_miktari
            else:
                db.stok_azalt(urun_id, miktar)
                break