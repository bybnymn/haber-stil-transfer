#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dinamik Stil Analiz Sistemi
Database'deki tüm haberleri (50 orijinal + kullanıcı eklenen) analiz eder
"""

import os
import re
import json
from collections import Counter, defaultdict
from typing import List, Dict, Tuple
from database import NewsDatabase

class DynamicStyleAnalyzer:
    def __init__(self):
        self.db = NewsDatabase()
        self.all_samples = []
        self.style_patterns = {}
        
    def load_all_samples_from_db(self):
        """Database ve dosyalardan tüm örnekleri yükle"""
        print("📁 Tüm örnekler yükleniyor (dosya + database)...")
        
        self.all_samples = self.db.get_all_samples(include_original=True)
        
        print(f"📊 Toplam {len(self.all_samples)} örnek yüklendi")
        return len(self.all_samples)
    
    def analyze_all_patterns(self):
        """Tüm stil kalıplarını analiz et"""
        if not self.all_samples:
            self.load_all_samples_from_db()
        
        print(f"\n🔍 {len(self.all_samples)} örnek analiz ediliyor...")
        
        # Başlık analizi
        titles = self.extract_titles()
        title_patterns = self.analyze_title_patterns(titles)
        
        # Cümle analizi
        sentences = self.extract_sentences()
        sentence_patterns = self.analyze_sentence_patterns(sentences)
        
        # Kelime analizi
        all_words = self.extract_words()
        word_patterns = self.analyze_word_patterns(all_words)
        
        # İfade analizi
        phrase_patterns = self.analyze_phrase_patterns(all_words)
        
        # Stil kuralları
        style_rules = self.extract_dynamic_style_rules(
            title_patterns, sentence_patterns, phrase_patterns
        )
        
        self.style_patterns = {
            'sample_count': len(self.all_samples),
            'original_count': sum(1 for s in self.all_samples if s['type'] == 'file'),
            'user_added_count': sum(1 for s in self.all_samples if s['type'] == 'database'),
            'title_patterns': title_patterns,
            'sentence_patterns': sentence_patterns,
            'phrase_patterns': phrase_patterns,
            'word_patterns': word_patterns,
            'style_rules': style_rules,
            'analysis_date': '2025-11-01'
        }
        
        return self.style_patterns
    
    def extract_titles(self) -> List[str]:
        """Başlıkları çıkar"""
        titles = []
        for sample in self.all_samples:
            if sample.get('title') and len(sample['title']) > 5:
                titles.append(sample['title'])
            
            # İçerikten de potansiyel başlıkları çıkar
            content = sample['content']
            lines = content.split('\n')
            for line in lines[:3]:  # İlk 3 satır
                line = line.strip()
                if (line and len(line) < 100 and 
                    not line.startswith(('Bu', 'Bir', 'Söz konusu'))):
                    titles.append(line)
        
        return titles
    
    def extract_sentences(self) -> List[str]:
        """Cümleleri çıkar"""
        sentences = []
        for sample in self.all_samples:
            content = sample['content']
            # Cümleleri ayır
            sent_list = re.split(r'[.!?]+', content)
            for sentence in sent_list:
                sentence = sentence.strip()
                if sentence and len(sentence) > 10:
                    sentences.append(sentence)
        
        return sentences
    
    def extract_words(self) -> List[str]:
        """Kelimeleri çıkar"""
        all_words = []
        for sample in self.all_samples:
            content = sample['content']
            words = re.findall(r'\b\w+\b', content.lower())
            all_words.extend(words)
        
        return all_words
    
    def analyze_title_patterns(self, titles: List[str]) -> Dict:
        """Başlık kalıplarını analiz et"""
        patterns = defaultdict(int)
        
        for title in titles:
            # Yer ismi kalıpları
            if any(place in title for place in ["'da", "'de", "'dan", "'den"]):
                patterns["yer_adı + olay"] += 1
            
            # Zaman kalıpları
            if any(word in title.lower() for word in ['yarıştı', 'düzenlendi', 'gerçekleşti']):
                patterns["olay + geçmiş_zaman"] += 1
            
            if any(word in title.lower() for word in ['açacak', 'başlayacak', 'yapılacak']):
                patterns["olay + gelecek_zaman"] += 1
            
            # Kurum kalıpları
            if any(word in title for word in ['Belediye', 'Üniversite', 'Emniyet']):
                patterns["kurum + olay"] += 1
        
        return dict(patterns)
    
    def analyze_sentence_patterns(self, sentences: List[str]) -> Dict:
        """Cümle kalıplarını analiz et"""
        sentence_starts = Counter()
        sentence_endings = Counter()
        
        for sentence in sentences:
            words = sentence.split()
            if len(words) >= 2:
                # İlk 2 kelime (başlangıç)
                start = ' '.join(words[:2])
                sentence_starts[start] += 1
            
            if words:
                # Son kelime (bitiş)
                sentence_endings[words[-1]] += 1
        
        return {
            'starts': dict(sentence_starts.most_common(25)),
            'endings': dict(sentence_endings.most_common(25))
        }
    
    def analyze_phrase_patterns(self, words: List[str]) -> Dict:
        """İfade kalıplarını analiz et"""
        # 2'li kombinasyonlar
        bigrams = Counter()
        for i in range(len(words) - 1):
            bigram = f"{words[i]} {words[i+1]}"
            bigrams[bigram] += 1
        
        # 3'lü kombinasyonlar
        trigrams = Counter()
        for i in range(len(words) - 2):
            trigram = f"{words[i]} {words[i+1]} {words[i+2]}"
            trigrams[trigram] += 1
        
        return {
            'bigrams': dict(bigrams.most_common(40)),
            'trigrams': dict(trigrams.most_common(30))
        }
    
    def analyze_word_patterns(self, words: List[str]) -> Dict:
        """Kelime kalıplarını analiz et"""
        word_freq = Counter(words)
        
        return {
            'most_common': dict(word_freq.most_common(100)),
            'total_words': len(words),
            'unique_words': len(word_freq)
        }
    
    def extract_dynamic_style_rules(self, title_patterns, sentence_patterns, phrase_patterns) -> Dict:
        """Dinamik stil kurallarını çıkar"""
        return {
            'title_formats': list(title_patterns.keys()),
            'sentence_starters': list(sentence_patterns['starts'].keys())[:15],
            'sentence_enders': list(sentence_patterns['endings'].keys())[:15],
            'common_phrases': list(phrase_patterns['trigrams'].keys())[:20],
            'connector_words': [
                phrase for phrase in phrase_patterns['bigrams'].keys()
                if any(word in phrase for word in ['ile', 'için', 'göre', 'olan', 've'])
            ][:15]
        }
    
    def save_analysis_to_db(self):
        """Analiz sonucunu database'e kaydet"""
        if self.style_patterns:
            self.db.save_analysis_result(self.style_patterns)
            print("💾 Analiz database'e kaydedildi")
    
    def run_full_dynamic_analysis(self):
        """Tam dinamik analizi çalıştır"""
        print("🚀 Dinamik Stil Analizi Başlatılıyor...\n")
        
        # Tüm samples yükle
        sample_count = self.load_all_samples_from_db()
        if sample_count == 0:
            print("❌ Hiç örnek bulunamadı!")
            return None
        
        # Analizi çalıştır
        result = self.analyze_all_patterns()
        
        # Database'e kaydet
        self.save_analysis_to_db()
        
        # JSON dosyasına da kaydet
        with open('dynamic_style_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"\n🎉 Dinamik Analiz Tamamlandı!")
        print(f"📊 Analiz Edilen Örnekler:")
        print(f"   - Orijinal: {result['original_count']}")
        print(f"   - Kullanıcı Eklenen: {result['user_added_count']}")
        print(f"   - Toplam: {result['sample_count']}")
        print(f"📁 Sonuç: dynamic_style_analysis.json")
        
        return result

# Test için
if __name__ == "__main__":
    analyzer = DynamicStyleAnalyzer()
    result = analyzer.run_full_dynamic_analysis()
    
    if result:
        print(f"\n✨ {result['sample_count']} örnekten stil kuralları çıkarıldı!")
        print(f"🎯 En yaygın cümle başlangıçları: {list(result['sentence_patterns']['starts'].keys())[:5]}")