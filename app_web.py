#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Haber Stil Transfer Pro - Web Uygulaması
Flask tabanlı web arayüzü
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import sys
import traceback
from news_generator import NewsStyleTransfer
from database import NewsDatabase
from dynamic_analyzer import DynamicStyleAnalyzer

# Flask uygulaması
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'haber-stil-transfer-secret-key-2025')

# CORS ayarları (production için)
CORS(app, resources={
    r"/transform": {"origins": "*"},
    r"/add-sample": {"origins": "*"},
    r"/get-stats": {"origins": "*"},
    r"/force-learn": {"origins": "*"}
})

# Sistemler
transformer = NewsStyleTransfer()
db = NewsDatabase()
analyzer = DynamicStyleAnalyzer()

@app.route('/')
def index():
    """Ana sayfa - dinamik öğrenme arayüzü"""
    return render_template('index_dynamic.html')

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    try:
        stats = db.get_sample_stats()
        return jsonify({
            'status': 'healthy',
            'service': 'Haber Stil Transfer Pro',
            'version': '1.0.0',
            'total_samples': stats.get('total_samples', 0)
        })
    except:
        return jsonify({
            'status': 'healthy',
            'service': 'Haber Stil Transfer Pro',
            'version': '1.0.0'
        })

@app.route('/transform', methods=['POST'])
def transform_text():
    """Stil transfer API endpoint'i"""
    try:
        # POST verilerini al
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': 'Metin verisi bulunamadı'
            })
        
        input_text = data['text'].strip()
        
        # Validasyon
        if not input_text:
            return jsonify({
                'success': False,
                'error': 'Lütfen dönüştürülecek metni girin'
            })
        
        if len(input_text) < 10:
            return jsonify({
                'success': False,
                'error': 'Metin çok kısa. En az 10 karakter girmelisiniz'
            })
        
        # Stil transfer yap
        title, transformed_text = transformer.transform_news_style(input_text)
        
        return jsonify({
            'success': True,
            'original_text': input_text,
            'title': title,
            'transformed_text': transformed_text
        })
        
    except Exception as e:
        print(f"Hata: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'İşlem sırasında hata oluştu: {str(e)}'
        })

@app.route('/add-sample', methods=['POST'])
def add_sample():
    """Yeni haber örneği ekle"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Veri bulunamadı'
            })
        
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        source = data.get('source', 'user_added').strip()
        
        # Validasyon
        if not title or not content:
            return jsonify({
                'success': False,
                'error': 'Başlık ve içerik gerekli'
            })
        
        if len(content) < 50:
            return jsonify({
                'success': False,
                'error': 'İçerik çok kısa. En az 50 karakter gerekli'
            })
        
        # Database'e ekle
        news_id = db.add_news_sample(title, content, source)
        
        # İstatistikleri al
        stats = db.get_sample_stats()
        
        # AKILLI ÖĞRENME: Her 10 örnekte bir yeniden öğren (performans için)
        if stats['total_samples'] % 10 == 0:
            print(f"🧠 Toplam {stats['total_samples']} örnek - Yeniden öğreniliyor...")
            analyzer.run_full_dynamic_analysis()
            
            # Transformer'ı yeniden yükle
            global transformer
            transformer = NewsStyleTransfer()
            print("✅ Sistem güncellendi!")
        else:
            print(f"📊 Toplam {stats['total_samples']} örnek - Sonraki güncelleme: {10 - (stats['total_samples'] % 10)} örnek sonra")
        
        return jsonify({
            'success': True,
            'message': 'Örnek başarıyla eklendi',
            'news_id': news_id,
            'total_samples': stats['total_samples'],
            'next_update_in': 10 - (stats['total_samples'] % 10)
        })
        
    except Exception as e:
        print(f"Hata: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'İşlem sırasında hata oluştu: {str(e)}'
        })

@app.route('/get-samples')
def get_samples():
    """Tüm örnekleri getir"""
    try:
        samples = db.get_all_samples(include_original=True)  # Tüm örnekler (orijinal 50 + DB)
        
        # Sınırla (performans için)
        samples = samples[:50]  # İlk 50 örnek
        
        return jsonify({
            'success': True,
            'samples': samples
        })
        
    except Exception as e:
        print(f"Hata: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Örnekler yüklenirken hata: {str(e)}'
        })

@app.route('/get-stats')
def get_stats():
    """Sistem istatistiklerini getir"""
    try:
        stats = db.get_sample_stats()
        
        return jsonify({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        print(f"Hata: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'İstatistikler yüklenirken hata: {str(e)}'
        })

@app.route('/force-learn', methods=['POST'])
def force_learn():
    """Manuel öğrenme - kullanıcı istediğinde sistemi yeniden eğit"""
    try:
        print("🧠 Manuel öğrenme başlatıldı...")
        
        # Tüm örnekleri analiz et
        analyzer.run_full_dynamic_analysis()
        
        # Transformer'ı yeniden yükle
        global transformer
        transformer = NewsStyleTransfer()
        
        # İstatistikleri al
        stats = db.get_sample_stats()
        
        return jsonify({
            'success': True,
            'message': f'{stats["total_samples"]} örnek başarıyla öğrenildi!',
            'total_samples': stats['total_samples']
        })
        
    except Exception as e:
        print(f"Hata: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'Öğrenme sırasında hata oluştu: {str(e)}'
        })

@app.route('/get-samples', methods=['GET'])
def page_not_found(e):
    """404 hata sayfası"""
    return render_template('error.html', 
                         error_code=404,
                         error_message="Sayfa bulunamadı"), 404

@app.errorhandler(500)
def internal_error(e):
    """500 hata sayfası"""
    return render_template('error.html',
                         error_code=500,
                         error_message="Sunucu hatası oluştu"), 500

if __name__ == '__main__':
    # Production/development modunu otomatik belirle
    port = int(os.environ.get('PORT', 5001))
    is_production = os.environ.get('FLASK_ENV') == 'production'
    debug_mode = not is_production
    
    if not is_production:
        print("🌐 Haber Stil Transfer Pro - Web Uygulaması")
        print("=" * 50)
        print("📡 Sunucu başlatılıyor...")
        print(f"🔗 Bağlantı: http://localhost:{port}")
        print("⏹️  Durdurmak için: Ctrl+C")
        print("=" * 50)
    else:
        print(f"🚀 Production modunda başlatılıyor - Port: {port}")
    
    # Çalıştır
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode,
        use_reloader=False  # Auto-reload kapalı
    )