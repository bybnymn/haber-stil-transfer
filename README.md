# 🚀 Haber Stil Transfer Pro# 🚀 Haber Yeniden Yazıcı



AI tarafından yazılmış Türkçe haber metinlerini insan tarafından yazılmış gibi dönüştüren profesyonel web uygulaması.Python tabanlı, Windows'ta çalışan bir haber metni düzenleme programı. Bu program yapay zeka değil, öğrenilmiş bir "stil profiline" göre AI yazımı haberleri daha okunabilir ve insansı bir habercilik diline dönüştürür.



## ✨ Özellikler## 📋 Özellikler



- **Dinamik Öğrenme**: 50+ örnek haberden otomatik öğrenme- **Stil Öğrenme**: Sample haber dosyalarından yazı stilini analiz eder

- **Kelime Değişimi**: %70+ kelime değişim oranı- **Akıllı Düzenleme**: Cümle uzunluklarını ayarlar, bağlaç ekler

- **Stil Transfer**: AI kalıplarını kırarak doğal metin üretimi- **Başlık Üretimi**: Otomatik başlık ve spot paragraf oluşturur

- **Web Arayüzü**: Kullanıcı dostu modern web interface- **GUI Arayüz**: Kullanıcı dostu PySide6 arayüzü

- **REST API**: Programatik erişim için API endpoint'leri- **Türkçe Destek**: Türkçe NLP modeli ile gelişmiş analiz

- **Cache Sistemi**: Performans optimizasyonu

## 🛠️ Kurulum

## 🛠️ Teknolojiler

### Gereksinimler

- Python 3.9+- Python 3.10+

- Flask (Web Framework)- Windows 10/11 (macOS ve Linux'ta da çalışır)

- SQLite (Database)- macOS'ta: Xcode Command Line Tools (`xcode-select --install`)

- Gunicorn (Production Server)

### Adım 1: Otomatik Kurulum (Önerilen)

## 📦 Kurulum```bash

python3 setup.py

### Yerel Geliştirme```



```bash### Adım 2: Manuel Kurulum

# Repoyu klonla```bash

git clone <repo-url># Kütüphaneleri kur

cd haber-yazici-projepip3 install -r requirements.txt



# Virtual environment oluştur# Türkçe NLP modelini indir

python3 -m venv .venvpython3 -m spacy download tr_core_news_md

source .venv/bin/activate  # Windows: .venv\Scripts\activate```



# Bağımlılıkları yükle### macOS Kurulum Sorunu Çözümü

pip install -r requirements.txtEğer `xcode-select` hatası alıyorsanız:

```bash

# Sunucuyu başlatxcode-select --install

python app_web.py```

```

## 🎯 Kullanım

Tarayıcıda http://localhost:5001 adresine git.

### Komut Satırı Kullanımı

### Production Deployment

#### 1. Stil Öğrenme

#### Heroku```bash

# samples/ klasörüne en az 5 haber .txt dosyası koyun

```bashpython style_train.py

# Heroku CLI ile login ol```

heroku login

#### 2. Haber Yeniden Yazma  

# Yeni uygulama oluştur```bash

heroku create haber-stil-transfer# input.txt dosyasına yeniden yazılacak haberi koyun

python rewrite_news.py

# Deploy et# Sonuç output.txt dosyasında oluşur

git push heroku main```



# Tarayıcıda aç### GUI Kullanımı

heroku open```bash

```python app.py

```

#### Render / Railway / Fly.io

GUI'da şu işlemleri yapabilirsiniz:

1. GitHub'a projeyi push et- 📁 **Samples Klasörü Seç**: Stil öğrenmek için haber dosyalarını seçin

2. Platform dashboard'undan "New Web Service" seç- 🧠 **Stil Öğret**: Seçilen dosyalardan stil profili oluşturun  

3. GitHub repo'sunu bağla- 📄 **Dosyadan Yükle**: Düzenlenecek haberi yükleyin

4. Deploy et (Procfile otomatik algılanır)- 🔄 **Metni Düzenle**: Haberi öğrenilen stile göre yeniden yazın

- 💾 **Çıktıyı Kaydet**: Sonucu dosyaya kaydedin

## 🎯 API Kullanımı

## 📁 Proje Yapısı

### Metin Dönüştür

```

```bashhaber-yazici-proje/

curl -X POST http://localhost:5001/transform \├── style_train.py      # Stil öğrenme modülü

  -H "Content-Type: application/json" \├── rewrite_news.py     # Haber yeniden yazma modülü  

  -d '{"text": "Haber metni buraya..."}'├── app.py              # GUI uygulaması

```├── requirements.txt    # Python bağımlılıkları

├── samples/            # Örnek haber dosyaları (boş)

### Örnek Ekle├── input.txt          # Test giriş dosyası

├── style.json         # Öğrenilmiş stil profili (oluşur)

```bash└── output.txt         # Çıkış dosyası (oluşur)

curl -X POST http://localhost:5001/add-sample \```

  -H "Content-Type: application/json" \

  -d '{"text": "Örnek haber metni..."}'## 🧠 Nasıl Çalışır?

```

### 1. Stil Öğrenme (`style_train.py`)

### İstatistikler- Sample dosyalarındaki haberleri analiz eder

- Ortalama cümle/paragraf uzunluğu hesaplar

```bash- Sık kullanılan bağlaçları tespit eder  

curl http://localhost:5001/get-stats- Kaçınılması gereken dolgu kelimeleri bulur

```- Cümle başlangıç kalıplarını öğrenir

- Okunabilirlik ve kelime karmaşıklığını ölçer

### Manuel Öğrenme- Sonuçları `style.json` dosyasına kaydeder



```bash### 2. Metin Düzenleme (`rewrite_news.py`)

curl -X POST http://localhost:5001/force-learn- Gereksiz dolgu kelimeleri kaldırır ("aslında", "yani", "şey")

```- Uzun cümleleri böler, kısa cümleleri birleştirir

- Uygun bağlaç ve geçiş ifadeleri ekler

## 📊 Performans- Otomatik başlık ve spot paragraf oluşturur

- Paragraflara organize eder

- **Kelime Değişim Oranı**: %70-75- Sonucu `output.txt` dosyasına kaydeder

- **İşleme Hızı**: ~2-3 saniye/metin

- **Otomatik Öğrenme**: Her 10 yeni örnekte## 📊 Örnek Çalışma Akışı

- **Cache Hit Rate**: %90+

1. **Hazırlık**: `samples/` klasörüne 10-20 kaliteli haber .txt dosyası koyun

## 🔧 Yapılandırma2. **Öğrenme**: `python style_train.py` → `style.json` oluşur

3. **Test**: `input.txt` dosyasına AI yazımı bir haber koyun  

Ortam değişkenleri:4. **Düzenleme**: `python rewrite_news.py` → `output.txt` oluşur

5. **Sonuç**: Düzenlenmiş, daha okunabilir haber metni

- `PORT`: Sunucu portu (varsayılan: 5001)

- `FLASK_ENV`: production/development## 🎨 GUI Ekran Görüntüleri



## 🔒 GüvenlikGUI uygulaması şu bölümlerden oluşur:

- **Sol Panel**: Kontrol butonları ve durum bilgileri

- CORS koruması aktif- **Sağ Panel**: Giriş ve çıkış metin alanları  

- Input sanitization- **Tab'lar**: Giriş ve çıkış metinleri arasında geçiş

- Rate limiting önerilir (production'da nginx/cloudflare)- **İlerleme Çubuğu**: İşlem durumu göstergesi



## 📝 Lisans## 🔧 Teknik Detaylar



MIT License### Kullanılan Kütüphaneler

- **spaCy**: Türkçe doğal dil işleme

## 🤝 Katkıda Bulunma- **Pydantic**: Veri modelleme ve doğrulama

- **TextStat**: Okunabilirlik analizi

Pull request'ler kabul edilir. Büyük değişiklikler için önce issue açın.- **WordFreq**: Kelime sıklığı analizi  

- **PySide6**: Modern GUI framework

## 📧 İletişim

### Desteklenen Analizler

Sorularınız için issue açabilirsiniz.- Cümle segmentasyonu

- Kelime sıklığı analizi
- Noktalama işareti kalıpları
- Morfolojik analiz (POS tagging)
- Okunabilirlik skorları

## 🐛 Sorun Giderme

### Sık Karşılaşılan Hatalar

**"Türkçe spaCy modeli bulunamadı"**
```bash
python -m spacy download tr_core_news_md
```

**"style.json bulunamadı"**  
Önce `python style_train.py` komutunu çalıştırın.

**"Sample dosyası bulunamadı"**
`samples/` klasörüne .txt formatında haber dosyaları ekleyin.

**GUI açılmıyor**
```bash
pip install --upgrade pyside6
```

## 📝 Lisans

Bu proje MIT lisansı altında yayınlanmıştır.

## 🤝 Katkıda Bulunma

1. Projeyi fork edin
2. Feature branch oluşturun (`git checkout -b feature/yeni-özellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik eklendi'`)
4. Branch'i push edin (`git push origin feature/yeni-özellik`)
5. Pull Request oluşturun

## 📞 İletişim

- **Proje**: Haber Yeniden Yazıcı v1.0
- **Teknoloji**: Python 3.10+, spaCy, PySide6
- **Platform**: Windows, macOS, Linux

---

🚀 **İpucu**: En iyi sonuçlar için samples/ klasörüne kaliteli, düzgün yazılmış haber metinleri ekleyin!