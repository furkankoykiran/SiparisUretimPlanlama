# Nesne Tabanlı Şirket Yönetim Sistemi

Bu proje, Manisa Celal Bayar Üniversitesi, Nesne Tabanlı Programlama dersi kapsamında geliştirilmiştir. Proje, bir şirketin ürün, çalışan ve sipariş yönetimini nesne tabanlı programlama yaklaşımıyla gerçekleştirmektedir.

## Kurulum

1. **Python Yükleyin**: Proje Python 3 ile çalışmaktadır. Python'u indirmek için [Python resmi web sitesini](https://www.python.org/downloads/) ziyaret edebilirsiniz.

2. **Projeyi İndirin**: Bu projeyi yerel makinenize klonlayın veya ZIP olarak indirip açın.

## Çalıştırma

Terminal veya komut satırını açın ve proje dizinine gidin. Aşağıdaki komutu çalıştırarak uygulamayı başlatabilirsiniz:

```bash
python main.py
```

## Proje Yapısı

```
├── main.py
├── models
│   ├── calisan.py
│   ├── siparis.py
│   └── urun.py
├── utils
│   ├── Database.py
│   ├── Helpers.py
│   └── Databases
│       └── Sirket.py
└── db
    └── sirket.db
```

## Özellikler

- **Ürün Yönetimi**: Yeni ürünler ekleyebilir, mevcut ürünleri görüntüleyebilir, güncelleyebilir veya silebilirsiniz.
- **Çalışan Yönetimi**: Çalışan ekleme, görüntüleme ve silme işlemlerini gerçekleştirebilirsiniz.
- **Sipariş Yönetimi**: Sipariş ekleme, görüntüleme, güncelleme ve durum takibi yapabilirsiniz.