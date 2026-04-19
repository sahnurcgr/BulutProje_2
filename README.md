# İHA Telemetri Verilerinin Gerçek Zamanlı İşlenmesi ve Görselleştirilmesi

Bu proje, bir İnsansız Hava Aracı (İHA) tarafından üretilen telemetri verilerinin (irtifa, hız, konum, batarya durumu vb.) AWS bulut servisleri kullanılarak gerçek zamanlı olarak işlenmesini, depolanmasını ve bir kontrol paneli üzerinden görselleştirilmesini sağlamaktadır.

## Sistem Mimarisi ve Kullanılan Teknolojiler

Proje, tam teşekküllü ve sunucusuz (serverless) bir veri akış mimarisi üzerine kurulmuştur:
* **Veri Üretimi (Python):** İHA sensörlerini simüle eden ve saniyede bir JSON formatında veri üreten yerel script.
* **Veri Akışı (AWS Kinesis Data Streams):** Üretilen yüksek hızlı verilerin buluta aktarıldığı mesaj kuyruğu.
* **Sunucusuz İşlem (AWS Lambda):** Kinesis'ten gelen Base64 şifreli verileri anlık olarak decode eden ve veri tipi dönüşümlerini (Float -> Decimal) yapan olay-güdümlü servis.
* **NoSQL Depolama (AWS DynamoDB):** İşlenen verilerin "drone_id" ve "timestamp" anahtarlarıyla zaman serisi (time-series) formatında kaydedildiği veritabanı.
* **Kullanıcı Arayüzü (Streamlit & Pandas):** Veritabanını anlık okuyarak harita ve grafikleri çizen canlı IoT Kontrol Paneli.

## Proje Dosyaları
* `drone_sim.py`: Sensör verilerini üretip AWS Kinesis'e gönderen simülasyon kodu.
* `dashboard.py`: AWS DynamoDB'den verileri çekerek tarayıcıda canlı grafik ve harita oluşturan Streamlit arayüz kodu.
* `.gitignore`: Gereksiz sistem dosyalarının (venv vb.) GitHub'a yüklenmesini engelleyen dosya.
* `BulutProje2.pdf`: Projenin tüm detaylarını, mimari şemasını ve AWS ayarlarını içeren kapsamlı final raporu.

## Sistemi Yerelde Çalıştırma Adımları

Projeyi kendi bilgisayarınızda test etmek için aşağıdaki adımları izleyebilirsiniz:

**1. Gerekli Kütüphaneleri Kurun:**
```bash
pip install boto3 streamlit pandas
