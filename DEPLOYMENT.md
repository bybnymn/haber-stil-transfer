# 🚀 Deployment Guide - Haber Stil Transfer Pro

Bu rehber, uygulamanızı farklı platformlara deploy etmek için adım adım talimatlar içerir.

## 📋 Ön Gereksinimler

- Git kurulu olmalı
- GitHub hesabı (ücretsiz)
- Deployment platformu hesabı (aşağıdakilerden biri)

## 🌐 Platform Seçimi

### 1. Render.com (Önerilen - Ücretsiz)

**장점:**
- ✅ Ücretsiz plan (750 saat/ay)
- ✅ Otomatik HTTPS
- ✅ Kolay kullanım
- ✅ SQLite destekler

**Adımlar:**

1. GitHub'a projeyi push et:
```bash
cd /Users/fahritas/Desktop/haber-yazici-proje
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/KULLANICI_ADIN/haber-stil-transfer.git
git push -u origin main
```

2. [Render.com](https://render.com)'a git
3. "New +" → "Web Service" seç
4. GitHub repo'nu bağla
5. Ayarları yap:
   - **Name**: haber-stil-transfer
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app_web:app`
6. "Create Web Service" tıkla

**Environment Variables (Render dashboard'dan ekle):**
```
FLASK_ENV=production
SECRET_KEY=<güvenli-random-key-buraya>
```

### 2. Railway.app (Hızlı Başlangıç)

**장점:**
- ✅ Çok hızlı deployment
- ✅ $5 ücretsiz kredi
- ✅ Otomatik HTTPS

**Adımlar:**

1. [Railway.app](https://railway.app)'e git
2. "Start a New Project"
3. "Deploy from GitHub repo" seç
4. Repo'nu seç
5. Otomatik deploy başlar

**Environment Variables:**
```
FLASK_ENV=production
PORT=8080
```

### 3. Heroku (Klasik Seçenek)

**장점:**
- ✅ En popüler platform
- ✅ Güçlü ekosistem
- ⚠️ Artık ücretsiz plan yok (7$/ay'dan başlıyor)

**Adımlar:**

```bash
# Heroku CLI kur (macOS)
brew tap heroku/brew && brew install heroku

# Login ol
heroku login

# Yeni uygulama oluştur
heroku create haber-stil-transfer

# Environment değişkenlerini ayarla
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=<güvenli-random-key>

# Deploy et
git push heroku main

# Tarayıcıda aç
heroku open
```

### 4. Fly.io (Global CDN)

**Adımlar:**

```bash
# Fly CLI kur
curl -L https://fly.io/install.sh | sh

# Login ol
flyctl auth login

# Launch et
flyctl launch

# Deploy et
flyctl deploy
```

## 🔒 Güvenlik Ayarları

### Secret Key Oluştur

```python
import secrets
print(secrets.token_hex(32))
```

Bu komutu terminal'de çalıştır ve çıkan değeri `SECRET_KEY` olarak kullan.

## 📊 Production Checklist

- [ ] `FLASK_ENV=production` ayarlandı
- [ ] `SECRET_KEY` güvenli bir değer olarak ayarlandı
- [ ] Database dosyası (`news_samples.db`) projeye dahil
- [ ] Samples klasörü projeye dahil
- [ ] CORS ayarları yapıldı
- [ ] Health check endpoint test edildi
- [ ] Logs kontrol edildi

## 🧪 Deployment Sonrası Test

```bash
# Health check
curl https://your-app.onrender.com/health

# İstatistik
curl https://your-app.onrender.com/get-stats

# Transform test
curl -X POST https://your-app.onrender.com/transform \
  -H "Content-Type: application/json" \
  -d '{"text": "Test haberi..."}'
```

## 🔧 Sorun Giderme

### Uygulama başlamıyor

1. Logs'u kontrol et:
```bash
# Render
Render dashboard → Logs sekmesi

# Railway
railway logs

# Heroku
heroku logs --tail
```

2. Environment değişkenlerini kontrol et
3. Python versiyonunu kontrol et (`runtime.txt`)

### Database hatası

SQLite dosyaları git'e commit edilmiş mi kontrol et:
```bash
git ls-files news_samples.db
git ls-files samples/
```

### CORS hatası

`app_web.py`'de CORS ayarlarını kontrol et.

## 📈 Monitoring

### Uptime Monitoring (Ücretsiz)

1. [UptimeRobot.com](https://uptimerobot.com) hesap aç
2. Yeni monitor ekle
3. URL: `https://your-app.com/health`
4. Check interval: 5 dakika

### Custom Domain (İsteğe Bağlı)

Render/Railway/Heroku'da custom domain bağlama:
1. Platform dashboard'a git
2. "Custom Domain" ayarlarını aç
3. DNS kayıtlarını ekle
4. SSL otomatik aktif olur

## 💡 İpuçları

- Ücretsiz planlarda 15 dakika inaktiviteden sonra uyku moduna geçer
- Health check endpoint'i ile sürekli aktif tutabilirsiniz
- İlk request yavaş olabilir (cold start)
- Production'da debug mode kapalı olmalı

## 📞 Destek

Sorun yaşarsanız:
1. Logs'u kontrol edin
2. Environment değişkenlerini doğrulayın
3. GitHub'da issue açın

---

**Başarılı deploymentlar! 🚀**
