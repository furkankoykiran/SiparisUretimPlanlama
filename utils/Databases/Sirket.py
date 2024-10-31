from utils.Database import Database

class SirketDB:
    def __init__(self, database_path):
        self.db = Database(database_path)

    def create_table(self):
        # Tablo oluşturma işlemleri
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS Urunler (
                urun_id INTEGER PRIMARY KEY AUTOINCREMENT,
                urun_adi TEXT,
                maliyet INTEGER,
                stok INTEGER DEFAULT 0
            )
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS Calisanlar (
                calisan_id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT,
                soyisim TEXT,
                maas INTEGER
            )
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS CalisanUrun (
                calisan_id INTEGER,
                urun_id INTEGER,
                FOREIGN KEY (calisan_id) REFERENCES Calisanlar(calisan_id),
                FOREIGN KEY (urun_id) REFERENCES Urunler(urun_id)
            )
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS Siparisler (
                siparis_id INTEGER PRIMARY KEY AUTOINCREMENT,
                urun_id INTEGER REFERENCES Urunler(urun_id),
                miktar INTEGER,
                musteri_adi TEXT,
                oncelik INTEGER CHECK (oncelik IN (1, 2, 3)),
                durum TEXT CHECK (durum IN ('Bekliyor', 'Üretimde', 'Tamamlandı')) DEFAULT 'Bekliyor',
                siparis_tarihi DATETIME DEFAULT (datetime('now', 'localtime')),
                siparis_teslim_tarihi DATETIME DEFAULT NULL,
                siparis_tutari INTEGER
            )
        """)
        print(f"{self.__class__.__name__} tabloları oluşturuldu.")

    # ---------------- URUNLER TABLOSU ----------------

    def urun_ekle(self, urun_adi, maliyet):
        self.db.execute("""
            INSERT INTO Urunler (urun_adi, maliyet)
            VALUES (?, ?)
        """, (urun_adi, maliyet))

    def urunleri_goster(self):
        return self.db.select("SELECT urun_id, urun_adi, maliyet, stok FROM Urunler")
    
    def stok_verisini_getir(self, urun_id):
        return self.db.select("SELECT stok FROM Urunler WHERE urun_id = ?", (urun_id,))[0][0]
    
    def urun_maliyetini_getir(self, urun_id):
        return self.db.select("SELECT maliyet FROM Urunler WHERE urun_id = ?", (urun_id,))[0][0]

    def urun_guncelle(self, urun_id, urun_adi, maliyet):
        self.db.execute("""
            UPDATE Urunler
            SET urun_adi = ?, maliyet = ?
            WHERE urun_id = ?
        """, (urun_adi, maliyet, urun_id))

    def urun_sil(self, urun_id):
        self.db.execute("DELETE FROM Urunler WHERE urun_id = ?", (urun_id,))

    def stok_artir(self, urun_id, miktar):
        self.db.execute("UPDATE Urunler SET stok = stok + ? WHERE urun_id = ?", (miktar, urun_id))

    def stok_azalt(self, urun_id, miktar):
        self.db.execute("UPDATE Urunler SET stok = stok - ? WHERE urun_id = ?", (miktar, urun_id))

    # ---------------- CALISANLAR TABLOSU ----------------

    def calisan_ekle(self, isim, soyisim, maas, urun_id):
        self.db.execute("""
            INSERT INTO Calisanlar (isim, soyisim, maas)
            VALUES (?, ?, ?)
        """, (isim, soyisim, maas))

        calisan_id = self.db.select("SELECT calisan_id FROM Calisanlar ORDER BY calisan_id DESC LIMIT 1")[0][0]
        
        self.calisan_urun_ekle(calisan_id, urun_id)
        
        print("Çalışan başarıyla eklendi.")
        return calisan_id

    def calisanlari_goster(self):
        return self.db.select("""
            SELECT c.calisan_id, c.isim, c.soyisim, c.maas, u.urun_adi
            FROM Calisanlar c
            JOIN CalisanUrun cu ON c.calisan_id = cu.calisan_id
            JOIN Urunler u ON cu.urun_id = u.urun_id
        """)

    def calisan_sil(self, calisan_id):
        self.db.execute("DELETE FROM Calisanlar WHERE calisan_id = ?", (calisan_id,))

    def calisan_urun_ekle(self, calisan_id, urun_id):
        self.db.execute("INSERT INTO CalisanUrun (calisan_id, urun_id) VALUES (?, ?)", (calisan_id, urun_id))

    # ---------------- SIPARISLER TABLOSU ----------------

    def siparis_ekle(self, urun_id, miktar, musteri_adi, oncelik, siparis_tutari):
        self.db.execute("""
            INSERT INTO Siparisler (urun_id, miktar, musteri_adi, oncelik, siparis_tutari)
            VALUES (?, ?, ?, ?, ?)
        """, (urun_id, miktar, musteri_adi, oncelik, siparis_tutari))

        return self.db.select("SELECT siparis_id FROM Siparisler ORDER BY siparis_id DESC LIMIT 1")[0][0]

    def siparisleri_goster(self):
        return self.db.select("SELECT siparis_id, urun_id, miktar, musteri_adi, oncelik, durum, siparis_tarihi, siparis_teslim_tarihi FROM Siparisler WHERE durum = 'Bekliyor'")
    
    def siparis_durum_guncelle(self, siparis_id, durum):
        self.db.execute("UPDATE Siparisler SET durum = ? WHERE siparis_id = ?", (durum, siparis_id))

    def siparis_miktarini_cek(self, siparis_id):
        return self.db.select("SELECT miktar FROM Siparisler WHERE siparis_id = ?", (siparis_id,))[0][0]

    def beklemedeki_siparisleri_getir(self, urun_id):
        return self.db.select("SELECT siparis_id FROM Siparisler WHERE urun_id = ? AND durum IN ('Bekliyor', 'Üretimde') ORDER BY oncelik", (urun_id,))

    def tamamlanmis_siparisleri_getir(self):
        return self.db.select("SELECT siparis_id, urun_id, miktar, siparis_tutari FROM Siparisler WHERE durum = 'Tamamlandı'")