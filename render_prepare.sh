#!/bin/bash
# Render.com Deploy Hazırlık Scripti

echo "🚀 Render.com Deploy Hazırlık"
echo "=============================="
echo ""

# 1. Git kontrolü
if [ -d .git ]; then
    echo "⚠️  Git repository zaten var. Temizleniyor..."
    rm -rf .git
fi

# 2. Git başlat
echo "📦 Git repository başlatılıyor..."
git init
git add .
git commit -m "Production ready - Haber Stil Transfer Pro"

echo ""
echo "✅ Git hazır!"
echo ""
echo "📝 ŞİMDİ YAPMAN GEREKENLER:"
echo ""
echo "1. GitLab'a git: https://gitlab.com"
echo "2. 'New project' → 'Create blank project' seç"
echo "3. Project name: haber-stil-transfer"
echo "4. Visibility: PUBLIC seç"
echo "5. 'Create project' tıkla"
echo ""
echo "6. Aşağıdaki komutu çalıştır (KULLANICI_ADIN yerine GitLab kullanıcı adını yaz):"
echo ""
echo "   git remote add origin https://gitlab.com/KULLANICI_ADIN/haber-stil-transfer.git"
echo "   git push -u origin main"
echo ""
echo "7. Render.com'a git: https://render.com"
echo "8. 'New +' → 'Web Service' seç"
echo "9. GitLab repo'sunu bağla"
echo ""
echo "10. Ayarlar:"
echo "    Build Command: pip install -r requirements.txt"
echo "    Start Command: gunicorn app_web:app"
echo ""
echo "11. Environment Variables:"
echo "    FLASK_ENV=production"
echo "    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")"
echo ""
echo "12. 'Create Web Service' tıkla"
echo ""
echo "🎉 Deploy tamamlanınca URL'ni alacaksın!"
