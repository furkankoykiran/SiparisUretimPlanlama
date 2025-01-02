import matplotlib.pyplot as plt
from utils.Helpers import Helpers

class Raporlar:
    @staticmethod
    def menu(db):
        while True:
            print("""
            1. Kâr - Zarar Grafiği
            2. Ürün Sipariş Yoğunluğu Grafiği
            3. Stok Grafiği
            4. Geri
            """)
            secim = Helpers.secim_al(range(1, 5))
            if secim == 1:
                Raporlar.kar_zarar_grafigi(db)
            elif secim == 2:
                Raporlar.urun_siparis_yogunluk_grafigi(db)
            elif secim == 3:
                Raporlar.stok_grafigi(db)
            elif secim == 4:
                break

    @staticmethod
    def kar_zarar_grafigi(db):
        """
        Tamamlanmış siparişlerden elde edilen toplam satış ile maliyeti karşılaştırarak
        basit bir Kâr - Zarar grafiği oluşturur.
        """
        # Artık doğrudan db.select kullanmıyoruz
        siparisler = db.sirket_rapor_tamamlanmis_siparisler()
        if not siparisler:
            print("Tamamlanmış sipariş yok. Kâr - Zarar grafiği gösterilemiyor.")
            return

        total_sales = 0
        total_cost = 0

        for urun_id, miktar, siparis_tutari in siparisler:
            total_sales += siparis_tutari
            maliyet = db.urun_maliyetini_getir(urun_id)  # DB'deki hazır metod
            total_cost += maliyet * miktar

        kar = total_sales - total_cost

        labels = ["Satış", "Maliyet", "Kâr"]
        values = [total_sales, total_cost, kar]
        colors = ["green", "red", "blue"]

        plt.bar(labels, values, color=colors)
        plt.title("Kâr - Zarar Grafiği")
        plt.ylabel("Tutar (TL)")
        plt.show()

    @staticmethod
    def urun_siparis_yogunluk_grafigi(db):
        """
        Ürünlerin kaç sipariş aldığını (adet olarak) bar grafiği şeklinde gösterir.
        """
        siparis_sayilari = db.sirket_rapor_siparis_sayilari()
        if not siparis_sayilari:
            print("Henüz sipariş yok. Ürün sipariş yoğunluğu grafiği gösterilemiyor.")
            return

        urunler = [row[0] for row in siparis_sayilari]
        siparis_sayisi = [row[1] for row in siparis_sayilari]

        plt.bar(urunler, siparis_sayisi, color="orange")
        plt.title("Ürün Sipariş Yoğunluğu Grafiği")
        plt.xlabel("Ürünler")
        plt.ylabel("Sipariş Sayısı")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def stok_grafigi(db):
        """
        Ürünlerin stok miktarlarını bar grafiği şeklinde gösterir.
        """
        stok_verisi = db.sirket_rapor_stok_verisi()
        if not stok_verisi:
            print("Ürün yok. Stok grafiği gösterilemiyor.")
            return

        urunler = [row[0] for row in stok_verisi]
        stoklar = [row[1] for row in stok_verisi]

        plt.bar(urunler, stoklar, color="purple")
        plt.title("Stok Grafiği")
        plt.xlabel("Ürünler")
        plt.ylabel("Stok Miktarı")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
