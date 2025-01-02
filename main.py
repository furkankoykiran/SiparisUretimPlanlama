from utils.Databases.Sirket import SirketDB
from models.urun import Urun
from models.siparis import Siparis
from models.calisan import Calisan
from models.raporlar import Raporlar  # Raporlar menüsü için eklendi

def main_menu():
    sirket_db = SirketDB('db/sirket.db')
    sirket_db.create_table()

    while True:
        print("""
        1. Ürün İşlemleri
        2. Çalışan İşlemleri
        3. Sipariş İşlemleri
        4. Raporlar
        5. Çıkış
        """)
        secim = input("Bir seçim yapın: ")

        if secim == '1':
            Urun.menu(sirket_db)
        elif secim == '2':
            Calisan.menu(sirket_db)
        elif secim == '3':
            Siparis.menu(sirket_db)
        elif secim == '4':
            Raporlar.menu(sirket_db)
        elif secim == '5':
            break
        else:
            print("Geçersiz seçim. Tekrar deneyin.")

if __name__ == "__main__":
    main_menu()
