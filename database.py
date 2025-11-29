#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dinamik Haber Database Sistemi
Kullanıcıların eklediği haberleri saklar ve stil öğrenmesini günceller
"""

import sqlite3
import os
import json
from datetime import datetime
from typing import List, Dict, Tuple

class NewsDatabase:
    def __init__(self, db_path: str = "news_samples.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Database ve tabloları oluştur"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Haber örnekleri tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS news_samples (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                source TEXT DEFAULT 'user_added',
                added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                word_count INTEGER,
                char_count INTEGER
            )
        ''')
        
        # Stil istatistikleri tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS style_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_samples INTEGER,
                last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                analysis_data TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"✅ Database hazır: {self.db_path}")
    
    def add_news_sample(self, title: str, content: str, source: str = "user_added") -> int:
        """Yeni haber örneği ekle"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        word_count = len(content.split())
        char_count = len(content)
        
        cursor.execute('''
            INSERT INTO news_samples (title, content, source, word_count, char_count)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, content, source, word_count, char_count))
        
        news_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"✅ Yeni haber eklendi: ID {news_id}")
        return news_id
    
    def get_all_samples(self, include_original: bool = True) -> List[Dict]:
        """Tüm haber örneklerini getir"""
        samples = []
        
        # Kullanıcı eklenen haberler
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, content, source, added_date, word_count, char_count
            FROM news_samples 
            WHERE is_active = 1
            ORDER BY added_date DESC
        ''')
        
        for row in cursor.fetchall():
            samples.append({
                'id': row[0],
                'title': row[1],
                'content': row[2],
                'source': row[3],
                'added_date': row[4],
                'word_count': row[5],
                'char_count': row[6],
                'type': 'database'
            })
        
        conn.close()
        
        # Orijinal 50 örnek
        if include_original:
            samples_dir = os.path.join(os.path.dirname(__file__), 'samples')
            if os.path.exists(samples_dir):
                for i in range(1, 51):
                    file_path = os.path.join(samples_dir, f"sample{i}.txt")
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read().strip()
                            if content:
                                samples.append({
                                    'id': f"original_{i}",
                                    'title': f"Örnek {i}",
                                    'content': content,
                                    'source': 'original',
                                    'added_date': '2025-10-31',
                                    'word_count': len(content.split()),
                                    'char_count': len(content),
                                    'type': 'file'
                                })
                    except:
                        continue
        
        print(f"📊 Toplam {len(samples)} örnek bulundu")
        return samples
    
    def get_sample_count(self) -> Tuple[int, int]:
        """Örnek sayılarını getir (orijinal, kullanıcı_eklenen)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM news_samples WHERE is_active = 1')
        user_count = cursor.fetchone()[0]
        
        conn.close()
        
        # Orijinal dosya sayısı
        original_count = 0
        samples_dir = os.path.join(os.path.dirname(__file__), 'samples')
        if os.path.exists(samples_dir):
            for i in range(1, 51):
                file_path = os.path.join(samples_dir, f"sample{i}.txt")
                if os.path.exists(file_path):
                    original_count += 1
        
        return original_count, user_count
    
    def save_analysis_result(self, analysis_data: Dict):
        """Analiz sonucunu kaydet"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        original_count, user_count = self.get_sample_count()
        total_samples = original_count + user_count
        
        cursor.execute('''
            INSERT INTO style_stats (total_samples, analysis_data)
            VALUES (?, ?)
        ''', (total_samples, json.dumps(analysis_data, ensure_ascii=False)))
        
        conn.commit()
        conn.close()
        
        print(f"💾 Analiz sonucu kaydedildi: {total_samples} örnek")
    
    def get_latest_analysis(self) -> Dict:
        """En son analiz sonucunu getir"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT analysis_data FROM style_stats 
            ORDER BY last_update DESC LIMIT 1
        ''')
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return json.loads(result[0])
        return None
    
    def delete_sample(self, sample_id: int) -> bool:
        """Haber örneğini sil (soft delete)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE news_samples SET is_active = 0 
            WHERE id = ?
        ''', (sample_id,))
        
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return affected > 0
    
    def get_sample_stats(self) -> Dict:
        """Database istatistikleri"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Toplam istatistikler
        cursor.execute('''
            SELECT 
                COUNT(*) as total,
                SUM(word_count) as total_words,
                SUM(char_count) as total_chars,
                AVG(word_count) as avg_words,
                MIN(added_date) as first_added,
                MAX(added_date) as last_added
            FROM news_samples 
            WHERE is_active = 1
        ''')
        
        stats = cursor.fetchone()
        conn.close()
        
        original_count, user_count = self.get_sample_count()
        
        return {
            'original_samples': original_count,
            'user_added_samples': user_count,
            'total_samples': original_count + user_count,
            'total_database_samples': stats[0] if stats[0] else 0,
            'total_words': stats[1] if stats[1] else 0,
            'total_chars': stats[2] if stats[2] else 0,
            'avg_words': round(stats[3]) if stats[3] else 0,
            'first_added': stats[4],
            'last_added': stats[5]
        }

# Test için
if __name__ == "__main__":
    db = NewsDatabase()
    
    # Test haberi ekle
    test_title = "Test Haberi"
    test_content = "Bu bir test haberidir. Kütahya'da yeni bir etkinlik gerçekleşti."
    
    news_id = db.add_news_sample(test_title, test_content)
    
    # İstatistikleri göster
    stats = db.get_sample_stats()
    print("📊 Database İstatistikleri:")
    for key, value in stats.items():
        print(f"   {key}: {value}")