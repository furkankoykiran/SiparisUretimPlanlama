class Helpers:
    @staticmethod
    def secim_al(gecerli_secimler):
        while True:
            try:
                secim = int(input("Seçiminizi yapın: "))
                if secim in gecerli_secimler:
                    return secim
                else:
                    print("Geçersiz seçim, lütfen tekrar deneyin.")
            except ValueError:
                print("Geçersiz giriş, lütfen bir sayı girin.")

    @staticmethod
    def dogrula_pozitif_tamsayi(input_str):
        while True:
            try:
                deger = int(input(input_str))
                if deger > 0:
                    return deger
                else:
                    print("Lütfen pozitif bir sayı girin.")
            except ValueError:
                print("Geçersiz giriş. Lütfen bir tamsayı girin.")

    @staticmethod
    def dogrula_string(input_str):
        while True:
            try:
                deger = input(input_str)
                if deger:
                    return deger
                else:
                    print("Bu alan boş bırakılamaz.")
            except ValueError:
                print("Geçersiz giriş. Lütfen bir metin girin.")

    @staticmethod
    def hata_mesaji(mesaj):
        print(f"Hata: {mesaj}")
