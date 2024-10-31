from utils.Helpers import Helpers
from models.urun import Urun

class Siparis:
    def __init__(self, urun_id, miktar, musteri_adi, oncelik):
        self.urun_id = urun_id
        self.miktar = miktar
        self.musteri_adi = musteri_adi
        self.oncelik = oncelik

    @staticmethod
    def menu(db):
        while True:
            print("""
            1. Yeni Sipariş Ekle
            2. Siparişleri Görüntüle
            3. Sipariş Güncelle
            4. Sipariş Durum Güncelle
            5. Toplam Satış Hesapla
            6. Geri Dön
            """)
            secim = Helpers.secim_al(range(1, 7))
            if secim == 1:
                Siparis.ekle(db)
            elif secim == 2:
                Siparis.goruntule(db)
            elif secim == 3:
                Siparis.guncelle(db)
            elif secim == 4:
                Siparis.durum_guncelle(db)
            elif secim == 5:
                Siparis.satis_hesapla(db)
            elif secim == 6:
                break

    @staticmethod
    def ekle(db):
        Urun.goruntule(db)

        urun_id = Helpers.dogrula_pozitif_tamsayi(f"Ürün ID'si: ")
        miktar = Helpers.dogrula_pozitif_tamsayi(f"Sipariş miktarı: ")
        musteri_adi = Helpers.dogrula_string(f"Müşteri adı: ")

        print("""
        1. Yüksek
        2. Orta
        3. Düşük
        """)
        oncelik = Helpers.secim_al(range(1, 4))

        siparis_tutari = Helpers.dogrula_pozitif_tamsayi(f"Sipariş tutarı: ")
        siparis_id = db.siparis_ekle(urun_id, miktar, musteri_adi, oncelik, siparis_tutari)
        print("Sipariş başarıyla eklendi.")

        stok = db.stok_verisini_getir(urun_id)
        if stok >= miktar:
            db.siparis_durum_guncelle(siparis_id, "Tamamlandı")
            db.stok_azalt(urun_id, miktar)
            print(f"Stokta yeterli miktar olduğundan sipariş tamamlandı.")
        else:
            print(f"Stokta yeterli miktar olmadığından sipariş beklemeye alındı.")

    @staticmethod
    def goruntule(db):
        siparisler = db.siparisleri_goster()
        if siparisler:
            for siparis in siparisler:
                print(f"""
                Sipariş ID: {siparis[0]}
                Durum: {siparis[1]}
                Müşteri: {siparis[2]}
                Ürün: {siparis[3]}
                Miktar: {siparis[4]}
                Teslim Tarihi: {siparis[5]}
                Öncelik: {siparis[6]}
                """)
        else:
            print("Görüntülenecek sipariş yok.")
        return siparisler

    @staticmethod
    def guncelle(db):
        siparisler = Siparis.goruntule(db)
        if not siparisler:
            Helpers.hata_mesaji("Güncellenecek sipariş yok.")
            return

        siparis_id = Helpers.dogrula_pozitif_tamsayi(f"Güncellemek istediğiniz sipariş ID'si: ")
        urun_id = Helpers.dogrula_pozitif_tamsayi(f"Yeni ürün ID'si: ")
        miktar = Helpers.dogrula_pozitif_tamsayi(f"Yeni miktar: ")
        musteri_adi = Helpers.dogrula_string(f"Yeni müşteri adı: ")

        print("""
        1. Yüksek
        2. Orta
        3. Düşük
        """)
        oncelik = Helpers.secim_al(range(1, 4))

        db.siparis_guncelle(siparis_id, urun_id, miktar, musteri_adi, oncelik)
        print("Sipariş başarıyla güncellendi.")

    @staticmethod
    def durum_guncelle(db):
        siparisler = Siparis.goruntule(db)
        if not siparisler:
            Helpers.hata_mesaji("Güncellenecek sipariş yok.")
            return

        siparis_id = Helpers.dogrula_pozitif_tamsayi(f"Durumunu güncellemek istediğiniz sipariş ID'si: ")

        print("""
        1. Bekliyor
        2. Üretimde
        3. Tamamlandı
        """)
        durum = Helpers.secim_al(range(1, 4))
        durum = "Bekliyor" if durum == 1 else "Üretimde" if durum == 2 else "Tamamlandı"

        db.siparis_durum_guncelle(siparis_id, durum)
        print("Sipariş durumu başarıyla güncellendi.")
    
    @staticmethod
    def satis_hesapla(db):
        # Tamamlanmış siparişlerin toplam tutarını hesapla
        siparisler = db.tamamlanmis_siparisleri_getir()
        if not siparisler:
            print("Hesaplanacak sipariş yok.")
            return
        
        toplam_tutar = 0
        for siparis in siparisler:
            siparis_id, urun_id, miktar, siparis_tutar = siparis
            toplam_tutar += siparis_tutar

        print(f"Toplam satış tutarı: {toplam_tutar} TL")