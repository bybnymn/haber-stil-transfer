# 🚀 Render.com Deployment Rehberi

## Adım Adım Render.com Deploy

### 📋 Ön Hazırlık

Projen zaten hazır! Sadece Git repository'ye push etmen gerekiyor.

---

## 🔷 Seçenek 1: GitLab ile Deploy (Önerilen - Tamamen Ücretsiz)

### 1. GitLab Hesap Aç
- [gitlab.com](https://gitlab.com) adresine git
- "Register" ile ücretsiz hesap aç
- Email doğrula

### 2. Yeni Proje Oluştur
1. GitLab'da "New project" tıkla
2. "Create blank project" seç
3. Ayarlar:
   - **Project name:** `haber-stil-transfer`
   - **Visibility Level:** **Public** seç (önemli!)
   - "Create project" tıkla

### 3. Projeyi GitLab'a Push Et

Terminal'de şu komutları çalıştır:

```bash
cd /Users/fahritas/Desktop/haber-yazici-proje

# Git başlat
git init

# Dosyaları ekle
git add .

# İlk commit
git commit -m "Production ready deployment"

# GitLab'a bağlan (KULLANICI_ADIN yerine kendi kullanıcı adını yaz)
git remote add origin https://gitlab.com/KULLANICI_ADIN/haber-stil-transfer.git

# Branch oluştur ve push et
git branch -M main
git push -u origin main
```

**Not:** GitLab şifre yerine "Personal Access Token" isteyebilir:
- GitLab → Settings → Access Tokens
- Token oluştur (write_repository yetkisi ile)
- Şifreyi kullan

### 4. Render.com'da Deploy Et

1. [render.com](https://render.com) hesap aç (ücretsiz)
2. Dashboard'da "New +" → "Web Service" tıkla
3. "Connect a repository" bölümünde:
   - "GitLab" seç
   - GitLab hesabını bağla
   - `haber-stil-transfer` repo'sunu seç

4. Ayarları yap:
   ```
   Name: haber-stil-transfer
   Region: Frankfurt (Avrupa için en yakın)
   Branch: main
   Runtime: Python 3
   
   Build Command:
   pip install -r requirements.txt
   
   Start Command:
   gunicorn app_web:app
   
   Instance Type: Free
   ```

5. Environment Variables ekle:
   ```
   FLASK_ENV = production
   SECRET_KEY = [aşağıdaki komutu çalıştır]
   ```
   
   Secret key oluştur:
   ```bash
   python3 -c "import secrets; print(secrets.token_hex(32))"
   ```

6. "Create Web Service" tıkla

### 5. Deploy İzle

- Deploy 5-10 dakika sürer
- Logs'tan durumu izleyebilirsin
- Deploy tamamlanınca URL alacaksın: `https://haber-stil-transfer.onrender.com`

---

## 🔷 Seçenek 2: GitHub ile Deploy

GitHub kullanmak istersen:

```bash
cd /Users/fahritas/Desktop/haber-yazici-proje

git init
git add .
git commit -m "Production ready deployment"
git remote add origin https://github.com/KULLANICI_ADIN/haber-stil-transfer.git
git branch -M main
git push -u origin main
```

Sonra Render'da GitHub repo'sunu bağla.

---

## ✅ Deploy Sonrası Test

```bash
# Health check
curl https://haber-stil-transfer.onrender.com/health

# İstatistikler
curl https://haber-stil-transfer.onrender.com/get-stats

# Transform test
curl -X POST https://haber-stil-transfer.onrender.com/transform \
  -H "Content-Type: application/json" \
  -d '{"text":"Kütahya Altıntaş ilçesinde doğalgaz çalışmaları tamamlandı."}'
```

---

## 🔧 Render.com Ayarları

### Environment Variables (Önemli!)

Render Dashboard → Environment sekmesinden ekle:

| Key | Value |
|-----|-------|
| `FLASK_ENV` | `production` |
| `SECRET_KEY` | Random string (yukarıdaki komutla üret) |

### Auto Deploy (Opsiyonel)

Render otomatik olarak her Git push'ta yeniden deploy eder.

---

## 📊 Ücretsiz Plan Limitleri

- ✅ 750 saat/ay çalışma süresi
- ✅ 512 MB RAM
- ✅ Otomatik HTTPS
- ⚠️ 15 dakika inaktiviteden sonra uyku moduna geçer
- ⚠️ İlk istek yavaş olabilir (cold start)

**İpucu:** UptimeRobot ile 5 dakikada bir health check yaptırarak uyku modunu engelleyebilirsin.

---

## 🐛 Sorun Giderme

### Deploy başarısız olursa:

1. **Logs'u kontrol et:**
   - Render Dashboard → Logs sekmesi

2. **requirements.txt kontrol et:**
   ```bash
   cat requirements.txt
   ```
   Çıktı:
   ```
   Flask>=2.3.0
   Flask-CORS>=4.0.0
   gunicorn>=21.2.0
   ```

3. **runtime.txt kontrol et:**
   ```bash
   cat runtime.txt
   ```
   Çıktı:
   ```
   python-3.9.20
   ```

4. **Database dosyası var mı?**
   ```bash
   ls -lh news_samples.db
   ```

---

## 🎯 Hızlı Başlangıç Komutu

Tek komutta her şeyi yap:

```bash
cd /Users/fahritas/Desktop/haber-yazici-proje && \
git init && \
git add . && \
git commit -m "Production ready" && \
echo "Şimdi GitLab'da repo oluştur ve şu komutu çalıştır:" && \
echo "git remote add origin https://gitlab.com/KULLANICI_ADIN/haber-stil-transfer.git" && \
echo "git push -u origin main"
```

---

## 📞 Yardım

Sorun yaşarsan:
1. Logs'u kontrol et
2. Environment variables'ı doğrula
3. Database dosyasının Git'e dahil olduğunu kontrol et

**Başarılar! 🚀**
