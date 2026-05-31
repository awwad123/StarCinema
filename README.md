# 🎬 StarCinema — Bilet Satış Sistemi

BSM218/BSM303 Veritabanı Yönetim Sistemleri — Final Ek Ödevi

## Kurulum Adımları

### 1. MySQL — Veritabanı Oluşturma
MySQL Workbench veya komut satırında `BSM218_Odev3_SQL.sql` dosyasını çalıştırın.

### 2. Python Gereksinimler
```bash
pip install flask flask-cors mysql-connector-python
```

### 3. Veritabanı Bağlantısı
`app.py` dosyasında şu bölümü kendi bilgilerinize göre düzenleyin:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'SIZIN_SIFRENIZ',  # <-- buraya MySQL şifrenizi yazın
    'database': 'star_cinema'
}
```

### 4. Uygulamayı Başlatma
```bash
cd sinema_app
python app.py
```

### 5. Tarayıcıdan Açma
```
http://localhost:5000
```

## Mimari (N-Katmanlı)

```
Presentation Layer  →  templates/index.html (HTML + JavaScript)
Business Layer      →  app.py (Flask rotaları — iş kuralları)
Data Access Layer   →  app.py (Tüm DB işlemleri Stored Procedure ile)
Database            →  MySQL — star_cinema
```

## Özellikler
- ✅ Müşteri CRUD (Ekle / Güncelle / Sil / Listele / Ara)
- ✅ Film CRUD
- ✅ Salon CRUD
- ✅ Seans CRUD + Dolu Koltuk Sayısı (fn_DoluKoltukSayisi)
- ✅ Bilet Satışı + Koltuk/Kapasite Trigger Kontrolü
- ✅ Dashboard (İstatistikler + Son Satışlar)
- ✅ Tüm DB işlemleri SADECE Stored Procedure ile yapılmaktadır
- ✅ Hiçbir katmanda doğrudan SQL (SELECT/INSERT/UPDATE/DELETE) kullanılmamıştır
