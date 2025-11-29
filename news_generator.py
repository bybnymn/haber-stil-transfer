#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Haber Stil Transfer Sistemi - 50 Gerçek Örnekten Öğrenilmiş İnsan Yazımı
50 gerçek haber örneğinden öğrenilen stil ile AI metnini insan yazımına çevirir
"""

import random
import re
import json
import os
from typing import List, Dict, Tuple
from datetime import datetime

class NewsStyleTransfer:
    def __init__(self):
        print("Info: SpaCy paketi bulunamadı, basit metin işleme kullanılacak")
        
        # Dinamik öğrenme için database bağlantısı (ÖNCE)
        try:
            from database import NewsDatabase
            self.db = NewsDatabase()
            self.dynamic_learning_enabled = True
        except Exception as e:
            print(f"⚠️ Database yüklenemedi: {e}")
            self.dynamic_learning_enabled = False
        
        # 50 örnekten öğrenilen gerçek stil verilerini yükle (SONRA)
        self.load_learned_style()
        
        # ============= GENİŞ SİNONİM VERİTABANI - %75+ DEĞİŞİM İÇİN =============
        self.turkish_synonyms = {
            # METİNDEKİ KELİMELER - ÖNCELİKLİ
            'alışılmış': ['bilinen', 'tanıdık', 'olağan', 'normal'],
            'kalabalık': ['yoğunluk', 'izdiham', 'topluluk', 'kitle'],
            'tuhaf': ['farklı', 'ilginç', 'değişik', 'alışılmadık'],
            'hareketlilik': ['canlılık', 'hareketlilik', 'dinamizm', 'faaliyet'],
            'başladı': ['girdi', 'başlangıç yaptı', 'açıldı', 'başlangıcını yaptı'],
            'sabah': ['sabahleyin', 'erken vakitlerde', 'seher'],
            'erken': ['ilk', 'önceki', 'evveli'],
            'saatlerinde': ['vakitlerinde', 'sularında', 'anında'],
            'kentin': ['şehrin', 'ilin', 'bölgenin'],
            'merkez': ['orta', 'ana', 'temel', 'kalp'],
            'çevre': ['etraf', 'civardaki', 'yakın', 'muhit'],
            'bölgelerinde': ['yörelerde', 'kesimlerinde', 'alanlarında'],
            'aynı': ['eşzamanlı', 'birlikte', 'müşterek', 'tek'],
            'anda': ['zamanda', 'sırada', 'vakitte'],
            'yapılan': ['gerçekleştirilen', 'uygulanan', 'yürütülen', 'icra edilen'],
            'altyapı': ['temel', 'zemin', 'alt yapı', 'infrastructure'],
            'düzenlemeler': ['iyileştirmeler', 'yenilikler', 'değişiklikler', 'revizyonlar'],
            'şehir': ['kent', 'il', 'belde', 'yerleşim'],
            'trafik': ['ulaşım', 'araç trafiği', 'yol akışı', 'seyir'],
            'adeta': ['sanki', 'tıpkı', 'âdeta', 'resmen'],
            'ince': ['hassas', 'nazik', 'duyarlı', 'rafine'],
            'çizgide': ['hatta', 'sınırda', 'çizgisinde'],
            'dengede': ['muvazenede', 'balançta', 'denklette'],
            'tuttu': ['korudu', 'sürdürdü', 'devam ettirdi'],
            'kimi': ['bazı', 'birtakım', 'bir kısım', 'çeşitli'],
            'bölgelerde': ['alanlarda', 'yörelerde', 'kesimlerde'],
            'yollar': ['caddeler', 'sokaklar', 'güzergahlar', 'arterler'],
            'daraldı': ['kısıtlandı', 'azaldı', 'küçüldü'],
            'noktalarda': ['yerlerde', 'konumlarda', 'mevkilerde'],
            'makinelerinin': ['araçların', 'ekipmanların', 'cihazların'],
            'sesi': ['gürültüsü', 'çıkardığı ses', 'yankısı'],
            'rüzgâra': ['havaya', 'atmosfere', 'esen yellere'],
            'karıştı': ['katıldı', 'yayıldı', 'dağıldı'],
            'her': ['bütün', 'tüm', 'tamamında'],
            'zamanki': ['zaman olduğu', 'vakitki', 'defaki'],
            'gibi': ['misali', 'benzeri', 'şeklinde', 'tarzında'],
            'kendi': ['öz', 'hususi', 'mahsus'],
            'temposunu': ['ritimini', 'hızını', 'tempusunu'],
            'hiç': ['asla', 'kesinlikle', 'hiçbir şekilde'],
            'düşürmeden': ['azaltmadan', 'yavaşlatmadan', 'eksilmeden'],
            'akmaya': ['sürdürmeye', 'devama', 'gidişata'],
            'devam': ['süreç', 'akış', 'gidiş', 'seyir'],
            'etti': ['yaptı', 'uyguladı', 'gerçekleştirdi'],
            'yetkililer': ['sorumlular', 'ilgililer', 'görevliler', 'otoriteler'],
            'çalışmalar': ['faaliyetler', 'uygulamalar', 'işler', 'projeler'],
            'çalışmaların': ['faaliyetlerin', 'uygulamaların', 'işlerin'],
            'uzun': ['geniş', 'kapsamlı', 'yoğun', 'etraflı'],
            'süredir': ['zamandır', 'müddetçe', 'dönemdir'],
            'beklenen': ['umut edilen', 'umulan', 'tahmin edilen'],
            'iyileştirme': ['geliştirme', 'düzeltme', 'reform', 'tadilat'],
            'planının': ['projenin', 'programın', 'tasarının'],
            'parçası': ['bileşeni', 'kesimi', 'unsuru', 'cüzü'],
            'olduğunu': ['bulunduğunu', 'teşkil ettiğini', 'vuku bulduğunu'],
            'açıkladı': ['bildirdi', 'duyurdu', 'söyledi', 'belirtti'],
            'açıklamada': ['izahatta', 'beyanatta', 'deklarasyonda'],
            'kısa': ['az', 'sınırlı', 'dar', 'muhtasar'],
            'süreli': ['vadeli', 'zamanlı', 'dönemli'],
            'aksaklıklar': ['sorunlar', 'sıkıntılar', 'engeller', 'aksilikler'],
            'olabilir': ['mümkün', 'muhtemel', 'ihtimal dahilinde'],
            'genelinde': ['çapında', 'boyunca', 'kapsamında'],
            'daha': ['fazla', 'ek', 'ilave', 'ziyade'],
            'hızlı': ['süratli', 'çabuk', 'acele', 'ivedi'],
            'güvenli': ['emniyetli', 'sağlam', 'tehlikesiz', 'emin'],
            'ulaşım': ['transport', 'nakliye', 'erişim'],
            'hedefliyoruz': ['amaçlıyoruz', 'planlıyoruz', 'maksatlıyız'],
            'denildi': ['ifade edildi', 'söylendi', 'dile getirildi'],
            'açıklama': ['izahat', 'beyan', 'tespit', 'deklarasyon'],
            'özellikle': ['bilhassa', 'hususiyle', 'mahsus'],
            'işe': ['mesleğe', 'mesaiye', 'vazifeye'],
            'yetişmeye': ['ulaşmaya', 'kavuşmaya', 'varmaya'],
            'çalışan': ['emek veren', 'mesai yapan', 'uğraşan'],
            'yüzlerce': ['çok sayıda', 'bir çok', 'muteaddit'],
            'insan': ['birey', 'şahıs', 'kişi', 'fert'],
            'küçük': ['ufak', 'minik', 'az', 'mütevazı'],
            'teselli': ['avuntu', 'rahatlık', 'teskin'],
            'oldu': ['gerçekleşti', 'meydana geldi', 'yaşandı', 'vuku buldu'],
            'vatandaşların': ['halkın', 'kentlilerin', 'insanların', 'kişilerin'],
            'çok': ['fazla', 'bir hayli', 'epeyce', 'hayli'],
            'dikkatini': ['ilgisini', 'alakasını', 'merakını'],
            'çeken': ['uyandıran', 'gösteren', 'veren'],
            'detay': ['ayrıntı', 'ince nokta', 'tafsilat'],
            'ise': ['de', 'halbuki', 'oysa'],
            'ekiplerin': ['grupların', 'timlerin', 'kadronun'],
            'olağanüstü': ['fevkalade', 'sıradışı', 'istisnai'],
            'hızla': ['süratle', 'çabuk', 'hemen', 'derhal'],
            'çalışması': ['mesaisi', 'emeği', 'uğraşı'],
            'bazı': ['kimi', 'birtakım', 'bir kısım', 'bir takım'],
            'başlayan': ['girişilen', 'açılan', 'başlatılan'],
            'öğlene': ['öğlen vaktine', 'gündüze', 'orta güne'],
            'doğru': ['yana', 'tarafına', 'istikametine'],
            'belirgin': ['açık', 'net', 'belli', 'vazıh'],
            'ilerleme': ['gelişme', 'progres', 'aşama kaydı', 'terakki'],
            'kaydettiği': ['gösterdiği', 'kat ettiği', 'sağladığı'],
            'görüldü': ['izlendi', 'gözlendi', 'fark edildi', 'dikkat çekti'],
            'sosyal': ['toplumsal', 'sosyal', 'içtimai'],
            'medyada': ['mecrada', 'ortamda', 'platformda'],
            'paylaşılan': ['sergilenen', 'sunulan', 'yayınlanan'],
            'görüntülerde': ['sahnelerde', 'fotoğraflarda', 'videoarda'],
            'yoğunluğa': ['kalabalığa', 'yüklenmeye', 'akına'],
            'rağmen': ['karşın', 'karşılık', 'mukabil'],
            'işçilerin': ['çalışanların', 'emekçilerin', 'personelin'],
            'dakik': ['zamanında', 'tam vakitli', 'disiplinli'],
            'ritimle': ['tempoyla', 'hızla', 'düzenle'],
            'çalıştığı': ['mesai yaptığı', 'emek verdiği', 'uğraştığı'],
            'akışının': ['seyrinin', 'hareketinin', 'geçişinin'],
            'kontrollü': ['denetimli', 'yönlendirilmiş', 'dizginli'],
            'şekilde': ['biçimde', 'tarzda', 'suretle'],
            'yönlendirildiği': ['sevk edildiği', 'yönetildiği', 'idare edildiği'],
            'izlendi': ['gözlendi', 'seyreildi', 'takip edildi'],
            'esnaf': ['işletmeciler', 'dükkan sahipleri', 'ticaret erbabı', 'tüccarlar'],
            'tarafında': ['cephesinde', 'kesiminde', 'yönünde'],
            'temkinli': ['dikkatli', 'ihtiyatlı', 'tedbirli'],
            'umut': ['ümit', 'beklenti', 'ümitvar olma'],
            'havası': ['atmosfer', 'hava', 'ortam'],
            'hâkim': ['galip', 'baskın', 'hakim', 'egemen'],
            'dükkan': ['işyeri', 'mağaza', 'dükkan'],
            'sahipleri': ['işletmecileri', 'malikleri', 'patronları'],
            'biraz': ['az', 'bir nebze', 'kısmi'],
            'gürültü': ['ses', 'şamata', 'velvele', 'patırtı'],
            'toz': ['tozlanma', 'kirlilik', 'toz bulutu'],
            'sonunda': ['nihayetinde', 'neticede', 'akabinde'],
            'işler': ['faaliyetler', 'meseleler', 'konular'],
            'kolaylaşacaksa': ['rahatlayacaksa', 'sadeleşecekse', 'basitleşecekse'],
            'razıyız': ['memnunuz', 'kabul ediyoruz', 'onaylıyoruz'],
            'diyerek': ['ifadesiyle', 'sözleriyle', 'şeklinde'],
            'süreci': ['operasyonu', 'safhayı', 'aşamayı'],
            'değerlendiriyor': ['yorumluyor', 'tahlil ediyor', 'analiz ediyor'],
            'bölgedeki': ['mahalledeki', 'havzadaki', 'kesimindeki'],
            'işletmeler': ['firmalar', 'şirketler', 'kuruluşlar', 'teşebbüsler'],
            'gün': ['bugün', 'zaman', 'vakit'],
            'içinde': ['kapsamında', 'esnasında', 'sırasında'],
            'yaşanan': ['görülen', 'ortaya çıkan', 'cereyan eden'],
            'yoğunluk': ['kalabalık', 'doluluk', 'yığılma'],
            'nedeniyle': ['yüzünden', 'sebebiyle', 'dolayısıyla'],
            'müşteri': ['alıcı', 'ziyaretçi', 'misafir', 'müşterek'],
            'akışında': ['geçişinde', 'hareketinde', 'dolanımında'],
            'dalgalanmalar': ['değişimler', 'iniş çıkışlar', 'inişler'],
            'söylüyor': ['belirtiyor', 'ifade ediyor', 'dile getiriyor'],
            'akşam': ['gece', 'sonrasında', 'akşam üzeri'],
            'saatlerine': ['vakitlerine', 'anlarına', 'zamanlarına'],
            'sakinleşirken': ['durulurken', 'yavaşlarken', 'azalırken'],
            'yarın': ['ertesi gün', 'sonraki gün', 'yarınki gün'],
            'etkisini': ['tesirini', 'neticesini', 'sonuçlarını'],
            'net': ['açık', 'belirgin', 'kesin', 'vazıh'],
            'göstereceği': ['sergileyeceği', 'ortaya çıkaracağı', 'belli edeceği'],
            'belirtiliyor': ['söyleniyor', 'ifade ediliyor', 'kaydediliyor'],
            'hatlarındaki': ['güzergahlarındaki', 'rotalarındaki', 'yollarındaki'],
            'zamandır': ['dönemdir', 'müddettir', 'süredir'],
            'beklediği': ['umduğu', 'beklentisi', 'arzuladığı'],
            'yeniliklerden': ['değişikliklerden', 'reformlardan', 'iyileştirmelerden'],
            'biri': ['tanesi', 'adedi', 'tanesinden'],
            'olarak': ['şeklinde', 'suretiyle', 'niteliğinde'],
            'görülüyor': ['algılanıyor', 'değerlendiriliyor', 'kabul görüyor'],
            # YENİ EKLEMELER - Doğalgaz haberi için
            'doğalgaz': ['doğal gaz', 'gaz'],
            'çalışmalarında': ['işlemlerinde', 'faaliyetlerinde', 'operasyonlarında'],
            'sona': ['nihayete', 'tamamına', 'bitişe'],
            'gelindi': ['ulaşıldı', 'varıldı', 'erişildi'],
            'devam': ['süreç', 'akış', 'gidiş', 'seyir', 'devam'],
            'eden': ['süren', 'giden', 'oluşan'],
            'altyapı': ['temel', 'zemin', 'alt yapı', 'infrastructure'],
            'hatlarına': ['borularına', 'şebekesine', 'güzergahlarına'],
            'akışı': ['sevkiyatı', 'dağıtımı', 'iletimi'],
            'sağlandı': ['temin edildi', 'verildi', 'gerçekleşti'],
            'konuya': ['meseleye', 'hususaya', 'mevzuya'],
            'ilişkin': ['dair', 'ait', 'yönelik'],
            'belediye': ['şehir', 'belediye', 'kent yönetimi'],
            'başkanı': ['başkanı', 'reisi', 'lideri'],
            'günü': ['günü', 'tarihi', 'vakti'],
            'itibarıyla': ['itibaren', 'başlayarak', 'ile'],
            'hatlara': ['şebekelere', 'borolara', 'güzergahlara'],
            'verildiğini': ['aktarıldığını', 'sağlandığını', 'başlatıldığını'],
            'belirterek': ['söyleyerek', 'ifade ederek', 'bildirerek'],
            'bilgilendirdi': ['haber verdi', 'duyurdu', 'anlattı'],
            'kullanımına': ['tüketimine', 'istifadesine', 'kullanılmasına'],
            'geçiş': ['dönüşüm', 'transfer', 'değişim'],
            'sürecinde': ['aşamasında', 'safhasında', 'evresinde'],
            'abonelerin': ['müşterilerin', 'kullanıcıların', 'tüketicilerin'],
            'yapması': ['gerçekleştirmesi', 'tamamlaması', 'icra etmesi'],
            'gereken': ['lazım olan', 'zorunlu', 'gerekli'],
            'işlemleri': ['süreçleri', 'adımları', 'prosedürleri'],
            'şekilde': ['biçimde', 'tarzda', 'suretle'],
            'sıraladı': ['listeledi', 'saydı', 'belirtti'],
            'projelerin': ['planların', 'tasarıların', 'programların'],
            'onaylanması': ['tasdiki', 'kabulü', 'onanması'],
            'sayaç': ['metre', 'ölçer', 'saat'],
            'ücretlerinin': ['bedellerinin', 'fiyatlarının', 'masraflarının'],
            'ödenmesi': ['ödenmesi', 'tediyesi', 'verilmesi'],
            'sayaçların': ['metrelerin', 'ölçerlerin', 'saatlerin'],
            'temin': ['sağlama', 'edinme', 'bulma'],
            'edilerek': ['sağlanarak', 'yapılarak', 'gerçekleştirilerek'],
            'takılması': ['montajı', 'yerleştirilmesi', 'kurulması'],
            'açılım': ['başlatma', 'aktivasyon', 'devreye alma'],
            'işlemlerinin': ['süreçlerinin', 'adımlarının', 'prosedürlerinin'],
            'tamamlanması': ['bitirilmesi', 'sonlandırılması', 'nihayete erdirilmesi'],
            'söz': ['bahis', 'sözkonusu', 'anılan'],
            'konusu': ['edilen', 'bahsi geçen', 'anılan'],
            'evlere': ['konutlara', 'hanelere', 'meskenlere'],
            'tesisatı': ['sistemini', 'altyapısını', 'kurulumunu'],
            'döşeyen': ['kuran', 'monte eden', 'yapan'],
            'firmalar': ['şirketler', 'kuruluşlar', 'işletmeler'],
            'tarafından': ['vasıtasıyla', 'eliyle', 'aracılığıyla'],
            'yürütüleceğini': ['yapılacağını', 'icra edileceğini', 'sürdürüleceğini'],
            'vurguladı': ['belirtti', 'vurguladı', 'altını çizdi'],
            'belirtilen': ['söylenen', 'anlatılan', 'bildirilen'],
            'tamamlayan': ['bitiren', 'sonlandıran', 'nihayete erdiren'],
            'kullanmaya': ['tüketmeye', 'istifade etmeye', 'kullanılmasına'],
            'başladığı': ['geçtiği', 'giriştiği', 'başlangıcını yaptığı'],
            'ifade': ['beyan', 'izahat', 'söz'],
            'edildi': ['yapıldı', 'söylendi', 'bildirildi'],
            'bilgilendirme': ['enformasyon', 'haberdar etme', 'duyuru'],
            'mesajını': ['bildirisini', 'notunu', 'açıklamasını'],
            'saygılarımla': ['hürmetlerimle', 'saygıyla', 'saygı ile'],
            'notuyla': ['ibaresiyle', 'sözleriyle', 'ifadesiyle'],
            'noktaladı': ['bitirdi', 'sonlandırdı', 'tamamladı'],
        }
        
        # AI'dan insan stiline çevrim kuralları (50 örnekten çıkarılan)
        self.ai_to_human_patterns = [
            # Formal ifadeleri gerçek örneklerdeki gibi yap
            (r'gerçekleştirilmiştir', 'gerçekleşti'),
            (r'düzenlenmiştir', 'düzenlendi'),  
            (r'katılım sağlanmıştır', 'katılım gösterdi'),
            (r'başvuru yapılmıştır', 'başvuru yapıldı'),
            (r'değerlendirilmiştir', 'değerlendirme yapıldı'),
            (r'bildirilmektedir', 'bildirildi'),
            (r'ifade edilmektedir', 'açıklandı'),
            
            # Örneklerde yaygın olan ifadeler
            (r'bu bağlamda', 'bu çerçevede'),
            (r'söz konusu', 'bahsedilen'),
            (r'müteakiben', 'bunun üzerine'),
            (r'neticesinde', 'sonucunda'),
            
            # Gerçek örneklerdeki doğal akış
            (r'yapılan çalışmalar', 'yürütülen çalışmalar'),
            (r'elde edilen veriler', 'ulaşılan sonuçlar'),
            (r'tespit edilmiştir', 'belirlendi'),
        ]
        
    def load_learned_style(self):
        """Dinamik öğrenme sonuçlarını yükle ve sample metinlerini oku - HER SEFERINDE YENİDEN ÖĞREN"""
        try:
            # DİNAMİK ÖĞRENME: Her çalıştırmada yeniden analiz et
            if self.dynamic_learning_enabled:
                print("🧠 Dinamik öğrenme aktif - tüm örnekler analiz ediliyor...")
                self.run_dynamic_learning()
            
            # Önce dinamik analiz sonucunu dene
            dynamic_file = os.path.join(os.path.dirname(__file__), 'dynamic_style_analysis.json')
            if os.path.exists(dynamic_file):
                with open(dynamic_file, 'r', encoding='utf-8') as f:
                    self.learned_style = json.load(f)
                print(f"✅ Dinamik stil yüklendi ({self.learned_style.get('sample_count', '?')} örnek)")
            else:
                # Sonra statik analiz sonucunu dene
                static_file = os.path.join(os.path.dirname(__file__), 'style_analysis.json')
                if os.path.exists(static_file):
                    with open(static_file, 'r', encoding='utf-8') as f:
                        self.learned_style = json.load(f)
                    print(f"✅ Statik stil yüklendi (50 örnek)")
                else:
                    # Hiçbiri yoksa varsayılan
                    self.learned_style = self.get_default_style()
                    print("⚠️ Stil analizi bulunamadı, varsayılan kullanılıyor")
            
            # Sample dosyalarından gerçek cümleleri oku
            self.load_sample_sentences()
            
        except Exception as e:
            self.learned_style = self.get_default_style()
            self.real_sentences = []
            print(f"⚠️ Stil yüklenirken hata: {e}")
    
    def run_dynamic_learning(self):
        """Database'deki TÜM örneklerden yeni stil kalıpları öğren - AKILLI CACHE SİSTEMİ"""
        try:
            from dynamic_analyzer import DynamicStyleAnalyzer
            
            analyzer = DynamicStyleAnalyzer()
            sample_count = analyzer.load_all_samples_from_db()
            
            # Cache kontrolü: Önceki analiz dosyası varsa, örnek sayısını kontrol et
            dynamic_file = os.path.join(os.path.dirname(__file__), 'dynamic_style_analysis.json')
            should_relearn = True
            
            if os.path.exists(dynamic_file):
                try:
                    with open(dynamic_file, 'r', encoding='utf-8') as f:
                        cached_data = json.load(f)
                        cached_count = cached_data.get('sample_count', 0)
                        
                        # Eğer örnek sayısı aynıysa, yeniden öğrenmeye gerek yok
                        if cached_count == sample_count:
                            should_relearn = False
                            print(f"📌 Cache aktif - {sample_count} örnek zaten analiz edilmiş")
                        else:
                            print(f"🔄 Yeni örnekler tespit edildi: {cached_count} → {sample_count}")
                except:
                    pass
            
            if should_relearn and sample_count > 50:  # Yeni örnekler varsa
                print(f"📚 {sample_count} örnek bulundu - yeniden öğreniliyor...")
                analyzer.analyze_all_patterns()
                analyzer.save_analysis_to_db()  # Database'e kaydet
                
                # JSON dosyasına da kaydet
                dynamic_file = os.path.join(os.path.dirname(__file__), 'dynamic_style_analysis.json')
                with open(dynamic_file, 'w', encoding='utf-8') as f:
                    result = {
                        'sample_count': sample_count,
                        'sentence_patterns': analyzer.style_patterns.get('sentence_patterns', {}),
                        'phrase_patterns': analyzer.style_patterns.get('phrase_patterns', {}),
                        'top_words': analyzer.style_patterns.get('top_words', {})
                    }
                    json.dump(result, f, ensure_ascii=False, indent=2)
                
                print("✅ Dinamik öğrenme tamamlandı!")
            elif sample_count <= 50:
                print(f"📊 {sample_count} örnek - statik analiz kullanılıyor")
                
        except Exception as e:
            print(f"⚠️ Dinamik öğrenme hatası: {e}")
    
    def load_sample_sentences(self):
        """Sample dosyalarından ÖĞRENİLEN özellikleri çıkar"""
        samples_dir = os.path.join(os.path.dirname(__file__), 'samples')
        
        # Öğrenilen özellikler
        self.learned_features = {
            'sentence_starters': {},  # Cümle başlangıçları
            'sentence_enders': {},    # Cümle sonları  
            'common_phrases': {},     # Yaygın ifadeler
            'word_replacements': {},  # Kelime değişimleri
            'avg_sentence_length': 0, # Ortalama cümle uzunluğu
            'passive_to_active': {},  # Pasif->Aktif çevrimleri
        }
        
        if not os.path.exists(samples_dir):
            return
        
        all_sentences = []
        all_words = []
        
        # Sample'ları oku ve analiz et
        for filename in os.listdir(samples_dir):
            if filename.endswith('.txt'):
                filepath = os.path.join(samples_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # Cümleleri ayır
                        sentences = [s.strip() for s in content.split('.') if len(s.strip()) > 10]
                        all_sentences.extend(sentences)
                        
                        for sentence in sentences:
                            # Kelimeleri topla
                            words = sentence.split()
                            all_words.extend(words)
                            
                            # Cümle başlangıçlarını öğren (ilk 2-3 kelime)
                            if len(words) >= 2:
                                starter = ' '.join(words[:2])
                                self.learned_features['sentence_starters'][starter] = \
                                    self.learned_features['sentence_starters'].get(starter, 0) + 1
                            
                            # Cümle sonlarını öğren (son kelime)
                            if words:
                                ender = words[-1].lower().strip('.,!?')
                                if len(ender) > 2:
                                    self.learned_features['sentence_enders'][ender] = \
                                        self.learned_features['sentence_enders'].get(ender, 0) + 1
                
                except:
                    continue
        
        # Ortalama cümle uzunluğunu hesapla
        if all_sentences:
            total_words = sum(len(s.split()) for s in all_sentences)
            self.learned_features['avg_sentence_length'] = total_words / len(all_sentences)
        
        # Yaygın ifadeleri bul (2-3 kelimelik)
        for i in range(len(all_words) - 2):
            bigram = f"{all_words[i]} {all_words[i+1]}"
            self.learned_features['common_phrases'][bigram] = \
                self.learned_features['common_phrases'].get(bigram, 0) + 1
        
        # Sample'larda OLMAYAN AI kalıplarını tespit et
        self.detect_ai_patterns_not_in_samples(all_sentences)
        
        print(f"📚 {len(all_sentences)} cümle analiz edildi")
        print(f"📊 Öğrenilen: {len(self.learned_features['sentence_starters'])} başlangıç, "
              f"{len(self.learned_features['sentence_enders'])} son, "
              f"Ort. uzunluk: {int(self.learned_features['avg_sentence_length'])} kelime")
    
    def detect_ai_patterns_not_in_samples(self, sample_sentences):
        """Sample'larda OLMAYAN AI kalıplarını tespit et"""
        
        all_text = ' '.join(sample_sentences).lower()
        
        # AI'ın kullandığı ama sample'larda olmayan kalıplar
        ai_patterns = [
            'yoğun hareketlilik',
            'kısa sürede',
            'bu bağlamda',
            'bu çerçevede',
            'bu kapsamda',
            'etkisi altına',
            'yapılan düzenlemelerin',
            'yapılan çalışmalar',
            'gerçekleştirilen faaliyetler',
            'hem merakını hem de',
            '-mıştır',
            '-miştir',
            '-maktadır',
            '-mektedir',
        ]
        
        # Sample'larda olmayan kalıpları bul
        self.ai_only_patterns = []
        for pattern in ai_patterns:
            if pattern not in all_text:
                self.ai_only_patterns.append(pattern)
        
        print(f"� Sample'larda OLMAYAN {len(self.ai_only_patterns)} AI kalıbı tespit edildi")
    
    def get_default_style(self):
        """Varsayılan stil kalıpları"""
        return {
            "sentence_patterns": {
                "starts": {
                    "Kütahya'da": 4,
                    "Bu çerçevede": 6, 
                    "İl Emniyet": 7,
                    "Kütahya Belediyesi": 3,
                    "Bu arada": 3,
                    "Kazada yaralanan": 4
                },
                "endings": {
                    "etti": 22,
                    "edildi": 19,
                    "geldi": 15,
                    "söyledi": 12,
                    "konuştu": 12,
                    "oldu": 11
                }
            },
            "phrase_patterns": {
                "bigrams": {
                    "polis ekipleri": 18,
                    "112 acil": 18,
                    "acil çağrı": 18,
                    "olay yerine": 18,
                    "kütahya da": 81
                },
                "trigrams": {
                    "112 acil çağrı": 18,
                    "polis ekipleri sevk": 11,
                    "olay yerine sağlık": 14,
                    "acil çağrı merkezi": 14
                }
            },
            "top_words": {
                "kütahya": 155,
                "ve": 139,
                "da": 104,
                "bir": 60,
                "bu": 52,
                "ile": 46,
                "sağlık": 40,
                "için": 36,
                "ekipleri": 35,
                "polis": 25
            }
        }
    
    def aggressive_word_replacement(self, text: str, target_change_rate: float = 0.75) -> str:
        """
        KELİMELERİ MAXIMUM AGRESİF BİÇİMDE DEĞİŞTİR - Hedef: %75+ değişim (AI dedektörünü atlatmak için)
        
        Args:
            text: Değiştirilecek metin
            target_change_rate: Hedef değişim oranı (0.75 = %75)
        
        Returns:
            Kelimeleri değiştirilmiş metin
        """
        words = text.split()
        total_words = len(words)
        changed_count = 0
        result_words = []
        
        # Değiştirilmemesi gereken kelimeler (çok kısa veya özel)
        skip_words = {'da', 've', 'bir', 'bu', 'ile', 'için', 'de', 'mi', 'mı', 'mu', 'mü',
                     'ama', 'hem', 'ya', 'ki', 'ne', 'o', 'şu',
                     'kütahya', 'kütahya\'da', 'kütahya\'nın', 'kütahya\'ya',
                     'var', 'yok', 'iki', 'üç', 'dört', 'beş'}
        
        # İlk geçiş - değiştirilebilecek kelimeleri say
        changeable_count = 0
        for word in words:
            clean_word = re.sub(r'[.,!?;:()\"\'»«""]', '', word).lower()
            if len(clean_word) > 3 and clean_word not in skip_words:
                if clean_word in self.turkish_synonyms:
                    changeable_count += 1
        
        # Değiştirme ihtimalini hesapla - hedef %75'e ulaşmak için
        if changeable_count > 0:
            needed_changes = int(total_words * target_change_rate)
            change_probability = min(1.0, needed_changes / changeable_count * 1.1)  # %10 fazla hedefle
        else:
            change_probability = 0.0
        
        print(f"   ↳ Hedef: {int(total_words * target_change_rate)} kelime (%{target_change_rate*100:.0f})")
        
        # İkinci geçiş - kelimeleri değiştir
        for i, word in enumerate(words):
            # Temiz kelimeyi al (noktalama işaretleri olmadan)
            clean_word = re.sub(r'[.,!?;:()\"\'»«""]', '', word).lower()
            
            # Değiştirilmesi gereken mi kontrol et
            should_try_change = (
                len(clean_word) > 3 and  # En az 4 harfli kelimeler
                clean_word not in skip_words and
                random.random() < change_probability  # Dinamik ihtimal
            )
            
            changed = False
            
            if should_try_change:
                # SİNONİM veritabanından dene
                if clean_word in self.turkish_synonyms:
                    synonyms = self.turkish_synonyms[clean_word]
                    new_word = random.choice(synonyms)
                    
                    # Büyük/küçük harf kontrolü - orijinal kelimenin formatını koru
                    if word and word[0].isupper():
                        new_word = new_word[0].upper() + new_word[1:]
                    
                    # Noktalama işaretlerini koru
                    punctuation = ''
                    if word and word[-1] in '.,!?;:':
                        punctuation = word[-1]
                        new_word += punctuation
                    
                    result_words.append(new_word)
                    changed_count += 1
                    changed = True
            
            if not changed:
                # Değiştirilmedi, orijinali kullan
                result_words.append(word)
        
        change_percentage = (changed_count / total_words * 100) if total_words > 0 else 0
        print(f"   ↳ Gerçekleşen: {changed_count}/{total_words} kelime (%{change_percentage:.1f})")
        
        return ' '.join(result_words)
    
    def restructure_sentences(self, text: str) -> str:
        """
        CÜMLE YAPILARINI MAXIMUM AGRESİF DEĞİŞTİR - AI kalıplarını tamamen kır
        """
        # ÖNCE AGRESİF KELİME/İFADE TEMİZLEME
        text = re.sub(r'\byapılan\s+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\bgerçekleştirilen\s+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\buygulanan\s+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\byürütülen\s+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\bkonuya ilişkin\s+', 'konuda ', text, flags=re.IGNORECASE)
        text = re.sub(r'\bilişkin\s+', 'dair ', text, flags=re.IGNORECASE)
        text = re.sub(r'\bitibarıyla\b', 'itibaren', text, flags=re.IGNORECASE)
        text = re.sub(r'\badeta\s+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\bsanki\s+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\btıpkı\s+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\bsöz konusu\s+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\s+tarafından\s+', ' ', text, flags=re.IGNORECASE)
        
        # Cümleleri ayır
        sentences = re.split(r'([.!?])\s+', text)
        restructured = []
        
        i = 0
        while i < len(sentences):
            sentence = sentences[i].strip()
            
            if not sentence or len(sentence) < 3:
                i += 1
                continue
            
            # Noktalama işaretini ekle
            punctuation = '.'
            if i + 1 < len(sentences) and sentences[i + 1] in '.!?':
                punctuation = sentences[i + 1]
                i += 1
            
            # UZUN CÜMLE BÖL
            words = sentence.split()
            if len(words) > 25:
                parts = sentence.split(',', 1)
                if len(parts) == 2 and len(parts[0].split()) > 8:
                    restructured.append(parts[0].strip() + '.')
                    second = parts[1].strip()
                    if second:
                        second = second[0].upper() + second[1:] if len(second) > 1 else second
                        restructured.append(second + punctuation)
                else:
                    restructured.append(sentence + punctuation)
            else:
                restructured.append(sentence + punctuation)
            
            i += 1
        
        result = ' '.join(restructured)
        result = re.sub(r'\.+', '.', result)
        result = re.sub(r'\s+', ' ', result)
        result = re.sub(r'\s+([.,!?])', r'\1', result)
        
        return result.strip()
    
    def humanize_ai_text(self, ai_text: str) -> str:
        """AI metnini SAMPLE'LARDAN ÖĞRENİLEN ÖZELLİKLERE göre çevir"""
        
        text = ai_text
        
        # ========== ADIM 0: AGRESİF KELİME DEĞİŞTİRME - %70+ DEĞİŞİM İÇİN ==========
        print("🔄 Agresif kelime değiştirme yapılıyor...")
        text = self.aggressive_word_replacement(text)
        
        # ========== ADIM 0.5: CÜMLE YAPISINI DEĞİŞTİR (YENİ!) ==========
        print("🔀 Cümle yapıları yeniden düzenleniyor...")
        text = self.restructure_sentences(text)
        
        # ========== ADIM 1: SAMPLE'LARDA OLMAYAN AI KALIPLARINI SİL ==========
        
        if hasattr(self, 'ai_only_patterns'):
            for pattern in self.ai_only_patterns:
                # Pattern temizleme
                if pattern.startswith('-'):
                    # Ek kalıpları (-mıştır, -maktadır)
                    text = re.sub(pattern.replace('-', r'\w+') + r'\b', 
                                  lambda m: m.group(0)[:-len(pattern)+1] + 'dı' if 'mıştır' in pattern else m.group(0)[:-len(pattern)+1] + 'yor',
                                  text, flags=re.IGNORECASE)
                else:
                    # Normal kalıpları sil
                    text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        # ========== ADIM 2: ÖĞRENİLEN ORTALAMA CÜMLE UZUNLUĞUNA GÖRE AYARLA ==========
        
        if hasattr(self, 'learned_features'):
            target_length = int(self.learned_features.get('avg_sentence_length', 15))
            text = self.adjust_to_learned_length(text, target_length)
        
        # ========== ADIM 3: SAMPLE'LARDA YAYGINN İFADELERİ KULLAN ==========
        
        text = self.use_learned_phrases(text)
        
        # ========== ADIM 4: TEMEL TEMİZLİK ==========
        
        # Standart AI kalıplarını temizle
        replacements = [
            # Ekler
            (r'alınmıştır', 'alındı'),
            (r'yapılmıştır', 'yapıldı'),
            (r'edilmiştir', 'edildi'),
            (r'olmuştur', 'oldu'),
            
            # -maktadır/-mektedir
            (r'yapılmaktadır', 'yapılıyor'),
            (r'edilmektedir', 'ediliyor'),
            (r'olmaktadır', 'oluyor'),
            (r'bulunmaktadır', 'bulunuyor'),
            
            # Gereksiz kelimeler
            (r'yapılan ', ''),
            (r'gerçekleştirilen ', ''),
            (r'yürütülen ', ''),
            
            # Şehir->Kent
            (r'\bşehir\b', 'kent'),
            (r'\bşehirde\b', 'kentte'),
            (r'\bşehrin\b', 'kentin'),
        ]
        
        for pattern, replacement in replacements:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        # ========== ADIM 5: TEMİZLİK ==========
        
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\s*,\s*,', ',', text)
        text = re.sub(r'\s+([.,!?])', r'\1', text)
        text = re.sub(r'([.,!?])([A-ZÇĞİÖŞÜa-zçğıöşü])', r'\1 \2', text)
        
        # ========== ADIM 6: CÜMLE BAŞLANGIŞLARINI DÜZENLE ==========
        
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        fixed = []
        for s in sentences:
            if s:
                s = s[0].upper() + s[1:] if len(s) > 1 else s.upper()
                fixed.append(s)
        
        text = '. '.join(fixed)
        
        if text and not text.endswith('.'):
            text += '.'
        
        return text.strip()
    
    def adjust_to_learned_length(self, text: str, target_length: int) -> str:
        """Cümleleri öğrenilen ortalama uzunluğa göre ayarla"""
        
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        result = []
        
        for sentence in sentences:
            words = sentence.split()
            
            # Çok uzunsa böl
            if len(words) > target_length * 1.5:
                # Virgülden böl
                if ',' in sentence:
                    parts = sentence.split(',', 1)
                    if len(parts[0].split()) > 5:
                        result.append(parts[0].strip())
                        second = parts[1].strip()
                        if second:
                            second = second[0].upper() + second[1:] if len(second) > 1 else second
                            result.append(second)
                    else:
                        result.append(sentence)
                else:
                    result.append(sentence)
            else:
                result.append(sentence)
        
        return '. '.join(result)
    
    def use_learned_phrases(self, text: str) -> str:
        """Sample'larda öğrenilen yaygın ifadeleri tercih et"""
        
        if not hasattr(self, 'learned_features'):
            return text
        
        common_phrases = self.learned_features.get('common_phrases', {})
        
        # En yaygın 20 ifadeyi al
        top_phrases = sorted(common_phrases.items(), key=lambda x: x[1], reverse=True)[:20]
        
        # Bu ifadelerin AI karşılıklarını değiştir
        for phrase, count in top_phrases:
            # Örnek: "olay yerine" yaygınsa, "olaya" yerine "olay yerine" kullan
            if 'olay yerine' in phrase:
                text = re.sub(r'olaya\b', 'olay yerine', text, flags=re.IGNORECASE)
            elif 'sağlık ekipleri' in phrase:
                text = re.sub(r'ambulans\b', 'sağlık ekipleri', text, flags=re.IGNORECASE)
            elif 'polis ekipleri' in phrase:
                text = re.sub(r'polis\b', 'polis ekipleri', text, flags=re.IGNORECASE, count=1)
        
        return text
    
    def strip_ai_language(self, text: str) -> str:
        """AI dilinin TÜM izlerini sil - Sample'larda böyle ifadeler YOK"""
        
        # AI'ın en tipik kalıpları - SAMPLE'LARDA HİÇ GEÇMİYOR
        ai_phrases_to_remove = [
            r'\byoğun hareketlilik\b',
            r'\betkisi altına ald[ıi]\b',
            r'\bkısa sürede\b',
            r'\bbüyük ölçüde\b',
            r'\başta olmak üzere\b',
            r'\bkapsamlı bir şekilde\b',
            r'\bdikkat çekici bir şekilde\b',
            r'\bönemle belirtmek gerekir\b',
            r'\bbu bağlamda\b',
            r'\bbu çerçevede\b',
            r'\bbu kapsamda\b',
            r'\bbu doğrultuda\b',
        ]
        
        for phrase in ai_phrases_to_remove:
            text = re.sub(phrase, '', text, flags=re.IGNORECASE)
        
        # AI cümle yapıları -> Gazetecilik dili
        replacements = [
            # Uzun AI yapıları -> Kısa gazetecilik
            (r'yapılan düzenlemelerin (.+?) için planlandığını belirtirken', r'düzenlemelerin \1 için yapıldığını söyledi'),
            (r'hem (.+?) hem de (.+?) çekti', r'\2 çekti'),
            (r'aynı anda yürütülen çalışmalar', 'çalışmalar'),
            (r'yapılan çalışmalar', 'çalışmalar'),
            (r'gerçekleştirilen faaliyetler', 'faaliyetler'),
            (r'yürütülen projeler', 'projeler'),
            
            # Pasif -> Aktif (Sample'larda aktif cümleler çok)
            (r'ifade edildi', 'açıklandı'),
            (r'belirtildi', 'söylendi'),
            (r'bildirildi', 'açıklandı'),
            (r'vurgulandı', 'belirtildi'),
            (r'açıklandı', 'duyuruldu'),
            
            # Gereksiz sıfatlar
            (r'yoğun ilgi', 'ilgi'),
            (r'büyük ilgi', 'ilgi'),
            (r'yüksek katılım', 'katılım'),
            (r'geniş katılım', 'katılım'),
        ]
        
        for pattern, replacement in replacements:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text
    
    def make_sentences_journalistic(self, text: str) -> str:
        """Cümleleri sample'lardaki gibi KISA, DİREKT, NET yap"""
        
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        result = []
        
        for sentence in sentences:
            # SAMPLE TARZI: Uzun cümleleri böl
            words = sentence.split()
            
            if len(words) > 20:
                # Virgülden böl ve iki cümle yap (sample'larda çok kısa cümleler var)
                parts = sentence.split(',', 1)
                if len(parts) == 2 and len(parts[0].split()) > 5:
                    # İlk kısım yeterince uzunsa onu cümle yap
                    first_part = parts[0].strip()
                    result.append(first_part)
                    
                    # İkinci kısmı temizle ve ayrı cümle yap
                    second = parts[1].strip()
                    if second and len(second) > 10:
                        # İkinci kısmı büyük harfle başlat
                        second = second[0].upper() + second[1:] if len(second) > 1 else second.upper()
                        result.append(second)
                else:
                    result.append(sentence)
            else:
                result.append(sentence)
        
        return '. '.join(result)
    
    def use_real_journalist_words(self, text: str) -> str:
        """Sample'larda GERÇEKTEN kullanılan gazetecilik kelimelerini kullan"""
        
        # SAMPLE'LARDAN ÇIKARILAN GERÇEK GAZETECİ KELİMELER
        journalist_replacements = [
            # Sample'larda sürekli geçen ifadeler
            (r'\bşehir\b', 'kent'),
            (r'\bşehirde\b', 'kentte'),
            (r'\bşehrin\b', 'kentin'),
            
            # Sample'lardaki eylemler
            (r'\bkatıldı\b', 'katılım gösterdi'),
            (r'\bgerçekleşti\b', 'meydana geldi'),
            (r'\bdüzenlendi\b', 'gerçekleşti'),
            (r'\byapıldı\b', 'düzenlendi'),
            
            # Sample'lardaki kişi ifadeleri  
            (r'\byetkililer\b', 'yetkililer'),
            (r'\bvatandaşlar\b', 'vatandaşların'),
            
            # Sample'larda geçen sonuç ifadeleri
            (r'\bbaşarı elde etti\b', 'derece elde etti'),
            (r'\bbaşarılı oldu\b', 'derece aldı'),
            
            # Zaman ifadeleri (sample tarzı)
            (r'\bbugün\b', 'bugün'),
            (r'\bdün\b', 'dün'),
            (r'\byarın\b', 'yarın'),
        ]
        
        for pattern, replacement in journalist_replacements:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text
    
    def remove_non_journalistic(self, text: str) -> str:
        """Sample'larda GEÇMEYENleri çıkar - gerçek gazeteciler böyle yazmaz"""
        
        # Gereksiz kelimeler (sample'larda hiç yok)
        filler_words = [
            r'\baslında\b',
            r'\bgerçekten\b',
            r'\btamamen\b',
            r'\bkesinlikle\b',
            r'\btam olarak\b',
            r'\bgörüldüğü üzere\b',
            r'\bbilindiği gibi\b',
            r'\bmalum olduğu üzere\b',
        ]
        
        for filler in filler_words:
            text = re.sub(filler + r'\s*', '', text, flags=re.IGNORECASE)
        
        # Çift boşlukları temizle
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\s+([.,!?])', r'\1', text)
        
        return text
    
    def final_journalist_touches(self, text: str) -> str:
        """Son rötuşlar - sample'lardaki gibi akıcı yap"""
        
        # Noktalama düzenle
        text = re.sub(r'\.+', '.', text)
        text = re.sub(r'\s*\.\s*', '. ', text)
        
        # Her cümleyi büyük harfle başlat
        sentences = text.split('. ')
        fixed = []
        for s in sentences:
            if s:
                s = s.strip()
                if s:
                    fixed.append(s[0].upper() + s[1:] if len(s) > 1 else s.upper())
        
        text = '. '.join(fixed)
        
        # Son noktayı koy (sample'larda her zaman var)
        if text and not text.endswith('.'):
            text += '.'
        
        return text
    
    def apply_basic_fixes(self, text: str) -> str:
        """Temel AI dil kalıplarını sample stiline çevir - ÇOK AGRESIF"""
        
        # MAXIMUM AGRESIF DEĞİŞİKLİKLER - %70+ kelime değişimi için
        replacements = [
            # AI'ın en tipik yapıları - DAHA FAZLA
            (r'alışılmış bir kalabalıkla değil', 'farklı bir atmosferle'),
            (r'tuhaf bir hareketlilikle', 'yoğun bir tempoyla'),
            (r'başlayan yoğun hareketlilik', 'başlayan etkinlikler'),
            (r'yoğun hareketlilik', 'canlılık'),
            (r'hareketlilik', 'yoğunluk'),
            (r'etkisi altına aldı', 'dikkat çekti'),
            (r'kısa sürede', 'hızla'),
            (r'aynı anda yürütülen', 'farklı noktalarda yapılan'),
            (r'yürütülen çalışmalar', 'çalışmalar'),
            (r'hem merakını hem de dikkatini çekti', 'ilgi çekti'),
            (r'merakını çekti', 'ilgi uyandırdı'),
            (r'dikkatini çekti', 'göze çarptı'),
            (r'dikkat çeken', 'öne çıkan'),
            
            # Yapılan/yapılacak kalıpları - TAMAMEN DEĞİŞTİR
            (r'yapılan düzenlemelerin', 'düzenlemelerin'),
            (r'yapılan çalışmaların', 'çalışmaların'),
            (r'yapılan açıklamalarda', 'açıklamalarda'),
            (r'yapılan toplantıda', 'toplantıda'),
            (r'yapılan törende', 'törende'),
            (r'yapılan yarışmada', 'yarışmada'),
            (r'yapılan etkinlikte', 'etkinlikte'),
            (r'yapılan çalışmalar', 'çalışmalar'),
            (r'yapılan', 'gerçekleştirilen'),
            
            # ZAMAN İFADELERİ - Çeşitlendir
            (r'sabahın erken saatlerinde', 'sabah erken saatlerde'),
            (r'erken saatlerinde', 'sabah saatlerinde'),
            (r'akşam saatlerine doğru', 'akşam sularında'),
            (r'öğlene doğru', 'öğlen saatlerinde'),
            
            # YER İFADELERİ - Değiştir
            (r'kentin hem merkez hem de çevre bölgelerinde', 'kent merkezinde ve çevresinde'),
            (r'şehir genelinde', 'kent genelinde'),
            (r'şehrin', 'kentin'),
            (r'şehri', 'kenti'),
            (r'şehirde', 'kentte'),
            (r'şehre', 'kente'),
            
            # HAREKET VE EYLEM KELİMELERİ - Sinonimle değiştir
            (r'akmaya devam etti', 'sürdü'),
            (r'devam etti', 'sürdü'),
            (r'başladı', 'girdi'),
            (r'gerçekleşti', 'oldu'),
            (r'gerçekleştirildi', 'yapıldı'),
            (r'düzenlendi', 'yapıldı'),
            (r'sağlandı', 'verildi'),
            
            # Genel işleyiş gibi karmaşık ifadeler
            (r'genel işleyişini iyileştirmek', 'iyileştirmek'),
            (r'iyileştirmek için', 'için'),
            (r'planlandığını belirtirken', 'planlandığını söyledi'),
            (r'belirtirken', 'söyledi'),
            (r'ifade edildi', 'açıklandı'),
            (r'vurgulandı', 'söylendi'),
            (r'açıklandı', 'bildirildi'),
            
            # Yoğunluk ifadeleri
            (r'geçici yoğunlukların oluştuğu', 'yoğunluk yaşandığı'),
            (r'oluştuğu', 'yaşandığı'),
            
            # Bağlaçlar ve geçişler
            (r'Bu çerçevede', 'Bu kapsamda'),
            (r'Bu bağlamda', 'Bu arada'),
            (r'Bunun yanı sıra', 'Ayrıca'),
            (r'Diğer taraftan', 'Öte yandan'),
            
            # Koordinasyon ve işbirliği
            (r'koordineli çalıştığı', 'birlikte çalıştığı'),
            (r'koordine edileceği', 'birlikte yapılacağı'),
            (r'işbirliği yapıldı', 'birlikte çalışıldı'),
            
            # Bilgilendirme
            (r'bilgilendirileceği', 'bilgi verileceği'),
            (r'bilgilendirildi', 'bilgi verildi'),
            (r'bilgilendirilecek', 'bilgi verilecek'),
            
            # Takip ve izleme
            (r'yakından takip edenler', 'takip edenler'),
            (r'yakından izleyenler', 'izleyenler'),
            
            # Zaman ifadeleri
            (r'uzun vadede', 'ilerleyen dönemde'),
            (r'kısa vadede', 'yakın zamanda'),
            (r'orta vadede', 'bir süre sonra'),
            
            # Sonuç ifadeleri
            (r'olumlu sonuçlar doğurmasını', 'faydalı olmasını'),
            (r'olumlu sonuçlar', 'faydalar'),
            (r'olumsuz sonuçlar', 'sorunlar'),
            
            # Formal yapılar
            (r'gerçekleştirilmiştir', 'gerçekleşti'),
            (r'gerçekleştirildi', 'gerçekleşti'),
            (r'düzenlenmiştir', 'düzenlendi'),
            (r'sağlanmıştır', 'sağlandı'),
            (r'yapılmıştır', 'yapıldı'),
            (r'edilmiştir', 'edildi'),
            (r'alınmıştır', 'alındı'),
            
            # -maktadır/-mektedir (AI'ın en tipik özelliği!)
            (r'bulunmaktadır', 'bulunuyor'),
            (r'olmaktadır', 'oluyor'),
            (r'yapmaktadır', 'yapıyor'),
            (r'etmektedir', 'ediyor'),
            (r'gelmektedir', 'geliyor'),
            (r'çalışmaktadır', 'çalışıyor'),
            (r'yürütülmektedir', 'yürütülüyor'),
            (r'sürdürülmektedir', 'sürüyor'),
            (r'devam etmektedir', 'devam ediyor'),
        ]
        
        for pattern, replacement in replacements:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text
    
    def replace_with_real_sentences(self, text: str) -> str:
        """Metindeki cümleleri sample'lardaki GERÇEK kelime kalıplarıyla harmanla (anlam korunur)"""
        
        if not hasattr(self, 'real_sentences') or not self.real_sentences['all']:
            return text
        
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        result = []
        
        for i, sentence in enumerate(sentences):
            # Her cümlenin STİLİNİ sample'lardan öğren ama İÇERİĞİNİ koru
            transformed = self.apply_sample_style_to_sentence(sentence)
            result.append(transformed)
        
        return '. '.join(result)
    
    def apply_sample_style_to_sentence(self, sentence: str) -> str:
        """Cümlenin içeriğini koruyarak sample'lardaki STİL KALIPLARINI uygula"""
        
        transformed = sentence
        
        # Sample'lardaki yaygın BAŞLANGIÇ kalıpları
        if any(sentence.startswith(word) for word in ['Kütahya', 'İstanbul', 'Ankara', 'Türkiye']):
            # "Kütahya'da X yapıldı" -> sample tarzında "Kütahya'da X gerçekleşti" gibi
            transformed = re.sub(r"'da (.+) yapıldı", r"'da \1 gerçekleşti", transformed)
            transformed = re.sub(r"'da (.+) düzenlendi", r"'da \1 düzenlenen tören", transformed)
        
        # Sample'lardaki yaygın EYLEM kalıpları
        action_patterns = [
            (r'katılım gösterdi', 'yoğun ilgi gösterdi'),
            (r'katıldı', 'yoğun ilgi gösterdi'),
            (r'yapıldı', 'gerçekleşti'),
            (r'gerçekleştirildi', 'gerçekleşti'),
            (r'düzenlendi', 'düzenlenen tören'),
            (r'açıklandı', 'bilgiler verildi'),
            (r'belirtildi', 'açıkladı'),
            (r'bildirildi', 'bildirdi'),
        ]
        
        for pattern, replacement in action_patterns:
            if random.random() < 0.3:  # %30 ihtimalle uygula
                transformed = re.sub(pattern, replacement, transformed, count=1)
        
        # Sample'lardaki yaygın İFADE kalıpları
        phrase_patterns = [
            (r'çok önemli', 'önemli'),
            (r'oldukça başarılı', 'başarılı'),
            (r'son derece', ''),
            (r'büyük bir', 'bir'),
            (r'yapılan çalışmalar', 'çalışmalar'),
            (r'gerçekleştirilen faaliyetler', 'faaliyetler'),
            (r'yürütülen projeler', 'projeler'),
        ]
        
        for pattern, replacement in phrase_patterns:
            transformed = re.sub(pattern, replacement, transformed)
        
        # Sample'lardaki yaygın BAĞLAÇ kullanımları
        connector_patterns = [
            (r'^Bu çerçevede', 'Bu kapsamda'),
            (r'^Bu bağlamda', 'Bu arada'),
            (r'^Öte yandan', 'Diğer taraftan'),
        ]
        
        for pattern, replacement in connector_patterns:
            if random.random() < 0.5:
                transformed = re.sub(pattern, replacement, transformed)
        
        return transformed
    
    def adapt_sentence_to_context(self, real_sentence: str, original_sentence: str) -> str:
        """Sample'daki gerçek cümleyi orijinal cümlenin bağlamına adapte et"""
        
        # Orijinal cümleden önemli kelimeleri çıkar
        important_words = self.extract_important_words(original_sentence)
        
        # Gerçek cümledeki bazı kelimeleri orijinalden gelen kelimelerle değiştir
        adapted = real_sentence
        
        # Eğer orijinalde yer ismi varsa, sample cümledeki yer ismini değiştir
        place_patterns = [
            (r'Kütahya\'da', important_words.get('place', 'Kütahya') + "'da"),
            (r'Kütahya\'nın', important_words.get('place', 'Kütahya') + "'nın"),
            (r'Kütahya', important_words.get('place', 'Kütahya')),
        ]
        
        for pattern, replacement in place_patterns:
            if important_words.get('place'):
                adapted = re.sub(pattern, replacement, adapted, count=1)
        
        # Orijinaldeki özel isimleri koru
        if important_words.get('organization'):
            # Sample'daki kurumu orijinaldeki kurumla değiştir
            org_patterns = [
                r'Galatasaray[^\s]*',
                r'Milli Eğitim[^\s]*',
                r'İl Emniyet[^\s]*',
                r'\b[A-ZÇĞIÖŞÜ][a-zçğıöşü]+ (Müdürlüğü|Bakanlığı|Derneği|Belediyesi)\b'
            ]
            for pattern in org_patterns:
                adapted = re.sub(pattern, important_words['organization'], adapted, count=1)
        
        # Sayıları orijinalden al
        if important_words.get('numbers'):
            # Sample'daki sayıları orijinal sayılarla değiştir
            numbers_in_adapted = re.findall(r'\d+', adapted)
            orig_numbers = important_words['numbers']
            for i, num in enumerate(numbers_in_adapted):
                if i < len(orig_numbers):
                    adapted = adapted.replace(num, orig_numbers[i], 1)
        
        return adapted
    
    def extract_important_words(self, sentence: str) -> Dict[str, str]:
        """Cümleden önemli kelimeleri çıkar"""
        words = {}
        
        # Yer isimleri (büyük harfle başlayan ve 'da/de/nın/nin' ile biten)
        place_match = re.search(r"([A-ZÇĞİÖŞÜ][a-zçğıöşü]+)'(?:da|de|nın|nin|ya|ye)", sentence)
        if place_match:
            words['place'] = place_match.group(1)
        
        # Kurum/organizasyon isimleri (büyük harfle başlayan 2+ kelime)
        org_match = re.search(r'\b([A-ZÇĞİÖŞÜ][a-zçğıöşü]+(?: [A-ZÇĞİÖŞÜ][a-zçğıöşü]+)+)\b', sentence)
        if org_match:
            words['organization'] = org_match.group(1)
        
        # Sayılar
        numbers = re.findall(r'\d+', sentence)
        if numbers:
            words['numbers'] = numbers
        
        # Olay türü (yarışma, proje, etkinlik, vb)
        event_keywords = ['yarışma', 'proje', 'etkinlik', 'toplantı', 'açılış', 'konferans']
        for keyword in event_keywords:
            if keyword in sentence.lower():
                words['event'] = keyword
                break
        
        return words
    
    def apply_real_patterns(self, text: str) -> str:
        """Sample'lardaki gerçek YAYIN DİLİ kelime kalıplarını kullan"""
        
        # SAMPLE'LARDAN ÇI KARILAN GERÇEK YAYINCI DİLİ KALIPLARI
        real_patterns = [
            # Etkinlik ifadeleri (sample'larda sık geçenler)
            (r'etkinlik yapıldı', 'düzenlenen törende'),
            (r'etkinlik gerçekleşti', 'düzenlenen törende'),
            (r'proje tamamlandı', 'proje derece getirdi'),
            (r'başarı elde edildi', 'derece elde etti'),
            (r'başarılı olundu', 'başarılı oldu'),
            
            # Katılım ifadeleri (sample tarzı)
            (r'katılım sağlandı', 'yoğun ilgi gösterdi'),
            (r'katıldılar', 'yoğun ilgi gösterdi'),
            (r'iştirak etti', 'katıldı'),
            (r'hazır bulundu', 'bir araya geldi'),
            
            # Açıklama ifadeleri (sample'lardaki gibi)
            (r'açıklama yaptı', 'konuştu'),
            (r'açıklamada bulundu', 'bilgiler verdi'),
            (r'bilgi paylaştı', 'açıkladı'),
            (r'demeç verdi', 'konuştu'),
            
            # Yer ifadeleri (sample tarzı)
            (r'olay yerinde', 'olay yerine'),
            (r'merkezde', 'kentte'),
            (r'alanda', 'sahada'),
            (r'bölgede', 'bölgelerde'),
            
            # Sample'larda yaygın olan spesifik ifadeler
            (r'düzenlenen etkinlikte', 'düzenlenen törende'),
            (r'yapılan toplantıda', 'yapılan toplantı'),
            (r'gerçekleştirilen yarışmada', 'yarışmada'),
            (r'açılan sergide', 'sergide'),
            
            # Sample'lardaki doğal sonuçlar
            (r'başarı gösterdi', 'derece elde etti'),
            (r'ödül kazandı', 'derece getirdi'),
            (r'birincilik elde etti', 'derece elde etti'),
            
            # Sample'lardaki kişi ifadeleri
            (r'yetkililer belirtti', 'yetkililer açıkladı'),
            (r'yetkililer söyledi', 'yetkililer bildirdi'),
            (r'yetkililer açıkladı', 'yetkililer konuştu'),
            
            # Sample'lardaki zaman ifadeleri
            (r'geçtiğimiz günlerde', 'dün'),
            (r'yakın zamanda', 'bugün'),
            (r'kısa süre önce', 'dün'),
            (r'önümüzdeki günlerde', 'yarın'),
        ]
        
        applied_count = 0
        for pattern, replacement in real_patterns:
            if pattern in text.lower():
                text = re.sub(pattern, replacement, text, flags=re.IGNORECASE, count=1)
                applied_count += 1
                if applied_count >= 3:  # Maksimum 3 değişim
                    break
        
        return text
    
    def final_touches(self, text: str) -> str:
        """Son rötuşlar ve temizlik"""
        
        # Çift boşlukları temizle
        text = re.sub(r'\s+', ' ', text)
        
        # Nokta-virgül-noktalama düzenlemeleri
        text = re.sub(r'\s+([.,!?])', r'\1', text)
        text = re.sub(r'([.,!?])([A-ZÇĞİÖŞÜ])', r'\1 \2', text)
        
        # İlk harfi büyük yap
        if text:
            text = text[0].upper() + text[1:]
        
        return text
    
    def restructure_sentences(self, text: str) -> str:
        """Cümle yapılarını yeniden düzenle"""
        # Çok uzun cümleleri kısa parçalara böl
        sentences = []
        for sentence in text.split('. '):
            if not sentence.strip():
                continue
                
            words = sentence.split()
            # 30 kelimeden uzunsa böl
            if len(words) > 30:
                # Virgülden veya 'iken', 've' den böl
                parts = re.split(r'(,\s+(?:iken|ancak|fakat))', sentence)
                if len(parts) > 1:
                    # İlk parçayı nokta ile bitir
                    first_part = parts[0].strip()
                    if not first_part.endswith('.'):
                        first_part += '.'
                    sentences.append(first_part)
                    # Kalanı birleştir
                    remaining = ''.join(parts[1:]).strip()
                    if remaining.startswith(','):
                        remaining = remaining[1:].strip().capitalize()
                    sentences.append(remaining)
                else:
                    sentences.append(sentence)
            else:
                sentences.append(sentence)
        
        return '. '.join(sentences)
    
    def remove_filler_words(self, text: str) -> str:
        """Gereksiz dolgu kelimelerini çıkar"""
        fillers = [
            r'\bgerçekten\s+de\b',
            r'\baslında\s+',
            r'\btam olarak\s+',
            r'\ btamamen\s+',
            r'\bkesinlikle\s+',
            r'\bişte\s+',
        ]
        
        for filler in fillers:
            text = re.sub(filler, '', text, flags=re.IGNORECASE)
        
        # Çift boşlukları temizle
        text = re.sub(r'\s+', ' ', text)
        
        return text
    
    def add_natural_flow(self, text: str) -> str:
        """Doğal akış ve geçişler ekle"""
        sentences = [s.strip() for s in text.split('. ') if s.strip()]
        
        if len(sentences) < 2:
            return text
        
        # İkinci cümleye bağlaç ekle (ama kontrollü)
        connectors = ['Öte yandan', 'Ancak', 'Bu durumda', 'Buna göre']
        
        # Rastgele bir cümleye (2. veya 3.) bağlaç ekle
        insert_pos = 1 if len(sentences) > 1 else 0
        
        # Zaten bağlaçla başlamıyorsa ekle
        conn_starts = ['Öte', 'Ancak', 'Bu', 'Ayrıca', 'Bunun', 'Diğer']
        if not any(sentences[insert_pos].startswith(c) for c in conn_starts):
            connector = random.choice(connectors)
            sentences[insert_pos] = f"{connector} {sentences[insert_pos].lower()}"
        
        return '. '.join(sentences)
    
    def vary_vocabulary(self, text: str) -> str:
        """Kelime çeşitliliği sağla - tekrarlanan kelimeleri değiştir"""
        
        # Sık tekrar eden kelimeleri bul ve değiştir
        word_usage = {}
        words = text.split()
        
        # Değiştirilebilir kelime eşleştirmeleri
        synonyms = {
            'yapılan': ['gerçekleştirilen', 'düzenlenen', 'hazırlanan'],
            'yapıldı': ['gerçekleşti', 'oldu', 'tamamlandı'],
            'çalışmalar': ['çalışma', 'faaliyetler', 'hazırlıklar'],
            'açıklamalarda': ['açıklamalara göre', 'belirtilenlere göre'],
            'çekti': ['çekiyor', 'topladı'],
        }
        
        for i, word in enumerate(words):
            clean_word = word.lower().strip('.,!?;:')
            
            if clean_word in word_usage:
                word_usage[clean_word] += 1
                # İkinci kullanımda değiştir
                if word_usage[clean_word] >= 2 and clean_word in synonyms:
                    replacement = synonyms[clean_word][0]
                    # Noktalama işaretlerini koru
                    if word.endswith('.'):
                        words[i] = replacement + '.'
                    elif word.endswith(','):
                        words[i] = replacement + ','
                    else:
                        words[i] = replacement
            else:
                word_usage[clean_word] = 1
        
        return ' '.join(words)
    
    def adjust_sentence_lengths(self, text: str) -> str:
        """Cümle uzunluklarını ayarla - çeşitlilik sağla"""
        sentences = [s.strip() for s in text.split('. ') if s.strip()]
        
        result = []
        for sentence in sentences:
            words = sentence.split()
            
            # 35+ kelimelik cümleleri böl
            if len(words) > 35:
                # Ortadan böl
                mid = len(words) // 2
                # Virgül ara
                comma_pos = -1
                for i in range(mid-5, mid+5):
                    if i < len(words) and words[i].endswith(','):
                        comma_pos = i
                        break
                
                if comma_pos > 0:
                    first_part = ' '.join(words[:comma_pos+1])[:-1] + '.'
                    second_part = ' '.join(words[comma_pos+1:]).capitalize()
                    result.append(first_part)
                    result.append(second_part)
                else:
                    result.append(sentence)
            else:
                result.append(sentence)
        
        return '. '.join(result)
    
    def split_long_sentences(self, text: str) -> str:
        """Çok uzun cümleleri böl"""
        sentences = text.split('. ')
        result = []
        
        for sentence in sentences:
            words = sentence.split()
            if len(words) > 25:  # 25 kelimeden uzunsa böl
                # Virgülden böl
                parts = sentence.split(', ')
                if len(parts) > 2:
                    # İlk kısmı al, nokta koy
                    result.append(parts[0] + '.')
                    # Kalanı birleştir
                    remaining = ', '.join(parts[1:])
                    result.append(remaining)
                else:
                    result.append(sentence)
            else:
                result.append(sentence)
        
        return '. '.join(result)
    
    def make_sentences_active(self, text: str) -> str:
        """Pasif yapıları mümkün olduğunca aktif yap"""
        # Pasif yapılar -> aktif
        active_conversions = [
            (r'tarafından ([^\s]+) edildi', r'tarafından \1 etti'),
            (r'tarafından ([^\s]+) yapıldı', r'tarafından \1 yaptı'),
            (r'katılım sağlandı', 'katıldı'),
            (r'başvuru yapıldı', 'başvurdu'),
            (r'bilgi verildi', 'bilgilendirdi'),
        ]
        
        for pattern, replacement in active_conversions:
            text = re.sub(pattern, replacement, text)
        
        return text
    
    def add_natural_connectors(self, text: str) -> str:
        """Doğal bağlaçlar ve geçişler ekle"""
        sentences = text.split('. ')
        
        connectors = [
            'Ayrıca', 'Bu arada', 'Öte yandan', 'Bunun yanı sıra',
            'Diğer taraftan', 'Böylece', 'Sonuç olarak'
        ]
        
        if len(sentences) > 2:
            # 2. veya 3. cümlenin başına bağlaç ekle
            insert_pos = random.randint(1, min(2, len(sentences)-1))
            connector = random.choice(connectors)
            if sentences[insert_pos] and not sentences[insert_pos].startswith(tuple(connectors)):
                sentences[insert_pos] = f"{connector} {sentences[insert_pos].strip().lower()}"
        
        return '. '.join(sentences)
    
    def reduce_repetitions(self, text: str) -> str:
        """Kelime tekrarlarını azalt"""
        # Aynı kelimeler tekrar ediyorsa eş anlamlılarla değiştir
        synonyms = {
            'gerçekleştirildi': ['düzenlendi', 'yapıldı', 'tamamlandı'],
            'yapıldı': ['gerçekleşti', 'düzenlendi', 'tamamlandı'],
            'önemli': ['dikkat çeken', 'kayda değer', 'öne çıkan'],
            'başarılı': ['verimli', 'etkili', 'olumlu'],
        }
        
        words = text.split()
        word_count = {}
        
        for i, word in enumerate(words):
            word_lower = word.lower().strip('.,!?')
            if word_lower in word_count:
                word_count[word_lower] += 1
                # İkinci kullanımdan sonra eş anlamlı kullan
                if word_count[word_lower] > 1 and word_lower in synonyms:
                    replacement = random.choice(synonyms[word_lower])
                    words[i] = replacement
            else:
                word_count[word_lower] = 1
        
        return ' '.join(words)
    
    def apply_learned_sentence_starters(self, text: str) -> str:
        """Öğrenilen cümle başlangıçlarını uygula"""
        sentences = re.split(r'([.!?]\s*)', text)
        
        starters = list(self.learned_style["sentence_patterns"]["starts"].keys())
        
        for i in range(0, len(sentences), 2):  # Her cümle için
            if sentences[i].strip() and random.random() < 0.3:  # %30 ihtimalle
                # Uygun starter seç
                starter = random.choice(starters[:5])  # En yaygın 5'ini kullan
                
                # Eğer cümle kısa ve uygunsa starter ekle
                if len(sentences[i].split()) < 8:
                    if not sentences[i].strip().startswith(('Kütahya', 'Bu', 'İl')):
                        if starter == "Kütahya'da" and 'Kütahya' not in sentences[i]:
                            sentences[i] = f"{starter} " + sentences[i].strip().lower()
                        elif starter != "Kütahya'da":
                            sentences[i] = f"{starter} " + sentences[i].strip().lower()
        
        return ''.join(sentences)
    
    def inject_common_phrases(self, text: str) -> str:
        """Yaygın ifadeleri metne ekle"""
        common_phrases = list(self.learned_style["phrase_patterns"]["trigrams"].keys())
        
        # Eğer polis/kaza gibi konulardan bahsediyorsa uygun ifadeleri ekle
        if any(word in text.lower() for word in ['polis', 'kaza', 'olay', 'acil']):
            if random.random() < 0.4:  # %40 ihtimalle
                phrase = random.choice([
                    "polis ekipleri sevk edildi",
                    "112 acil çağrı merkezi",
                    "olay yerine sağlık ekipleri"
                ])
                
                # Uygun bir yere ekle
                sentences = text.split('.')
                if len(sentences) > 1:
                    insert_pos = random.randint(1, len(sentences)-1)
                    sentences[insert_pos] = f" {phrase.capitalize()}." + sentences[insert_pos]
                    text = '.'.join(sentences)
        
        return text
    
    def apply_natural_endings(self, text: str) -> str:
        """Doğal cümle sonlarını uygula"""
        endings = list(self.learned_style["sentence_patterns"]["endings"].keys())
        
        # Yapay sonları doğal olanlarla değiştir
        artificial_endings = [
            'yapılmaktadır', 'gerçekleştirilmektedir', 'sağlanmaktadır',
            'yürütülmektedir', 'sürdürülmektedir'
        ]
        
        for artificial in artificial_endings:
            if artificial in text:
                natural = random.choice(endings[:6])  # En yaygın 6 doğal son
                text = text.replace(artificial, natural)
        
        return text
    
    def adjust_word_frequency(self, text: str) -> str:
        """Kelime sıklığına göre ayarla"""
        words = text.split()
        top_words = self.learned_style["top_words"]
        
        # Az kullanılan kelimeleri yaygın olanlarla değiştir (bazen)
        replacements = {
            'işbirliği': 'birlikte',
            'koordinasyon': 'koordineli',
            'implementasyon': 'uygulama',
            'optimizasyon': 'iyileştirme'
        }
        
        for i, word in enumerate(words):
            if word.lower() in replacements and random.random() < 0.6:
                words[i] = replacements[word.lower()]
        
        return ' '.join(words)
    
    def generate_human_like_title(self, content: str) -> str:
        """İçeriğe göre insan benzeri başlık üret"""
        
        # İçerikten anahtar kelimeleri çıkar
        keywords = self.extract_keywords(content)
        
        # Gerçek örneklerdeki başlık kalıplarını kullan
        title_templates = [
            "Kütahya'da {olay} {durum}",
            "{yer}'de {olay} gerçekleşti", 
            "{olay} {sonuç} getirdi",
            "{kurum} {olay} düzenledi",
            "{yer} {olay} ile dikkat çekti"
        ]
        
        # Uygun template seç ve doldur
        template = random.choice(title_templates)
        
        # Template'i doldur
        title = template.format(
            yer=keywords.get('place', 'Kütahya'),
            olay=keywords.get('event', 'etkinlik'),
            durum=keywords.get('status', 'başarıyla gerçekleşti'),
            sonuç=keywords.get('result', 'başarı'),
            kurum=keywords.get('organization', 'Kütahya Belediyesi')
        )
        
        # Başlığı temizle
        title = title.replace('  ', ' ').strip()
        if not title.endswith(('.', '!', '?')):
            title += ""
        
        return title
    
    def extract_keywords(self, content: str) -> Dict[str, str]:
        """İçerikten anahtar kelimeleri çıkar"""
        keywords = {}
        
        # Yer isimleri
        places = ['Kütahya', 'İstanbul', 'Ankara', 'Türkiye']
        for place in places:
            if place in content:
                keywords['place'] = place
                break
        else:
            keywords['place'] = 'Kütahya'  # Varsayılan
        
        # Olay türleri
        events = ['yarışma', 'etkinlik', 'proje', 'toplantı', 'kaza', 'çalışma']
        for event in events:
            if event in content.lower():
                keywords['event'] = event
                break
        else:
            keywords['event'] = 'etkinlik'
        
        # Kurum isimleri
        organizations = ['Belediye', 'Üniversite', 'Emniyet', 'İl Müdürlüğü']
        for org in organizations:
            if org in content:
                keywords['organization'] = f"Kütahya {org}si"
                break
        else:
            keywords['organization'] = 'Kütahya Belediyesi'
        
        # Sonuç durumu
        if any(word in content.lower() for word in ['başarı', 'kazandı', 'derece']):
            keywords['result'] = 'başarı'
            keywords['status'] = 'başarıyla tamamlandı'
        elif any(word in content.lower() for word in ['kaza', 'yaralandı', 'hasar']):
            keywords['result'] = 'kaza'
            keywords['status'] = 'meydana geldi'
        else:
            keywords['result'] = 'sonuç'
            keywords['status'] = 'gerçekleşti'
        
        return keywords
    
    def create_news(self, topic: str) -> Tuple[str, str]:
        """Verilen konuda insan benzeri haber oluştur"""
        
        # Basit haber şablonu (AI benzeri)
        ai_templates = [
            f"""
            {topic} konusunda kapsamlı bir çalışma gerçekleştirilmiştir. 
            Bu bağlamda, ilgili kurumlar tarafından gerekli koordinasyon sağlanmıştır.
            Yapılan değerlendirmeler neticesinde olumlu sonuçlar elde edilmiştir.
            Süreç boyunca tüm paydaşlarla işbirliği yapılmıştır.
            """,
            
            f"""
            {topic} ile ilgili olarak yeni bir proje başlatılmıştır.
            Proje kapsamında çeşitli etkinlikler düzenlenecektir.
            Bu etkinlikler sayesinde önemli kazanımlar elde edilmesi hedeflenmektedir.
            İlgili makamlar konuya gerekli hassasiyeti göstermektedir.
            """,
            
            f"""
            {topic} konusunda önemli bir gelişme yaşanmıştır.
            Gelişme ile birlikte yeni fırsatlar ortaya çıkmıştır.
            Bu fırsatların değerlendirilmesi için gerekli adımlar atılmıştır.
            Süreç hakkında düzenli bilgilendirmeler yapılacaktır.
            """
        ]
        
        # AI benzeri metin seç
        ai_content = random.choice(ai_templates).strip()
        
        # İnsan stiline çevir
        human_content = self.humanize_ai_text(ai_content)
        
        # İnsan benzeri başlık oluştur
        human_title = self.generate_human_like_title(human_content)
        
        return human_title, human_content
    
    def transform_text(self, text: str, generate_title: bool = True) -> Tuple[str, str]:
        """Mevcut metni insan stiline dönüştür"""
        
        # İçeriği dönüştür
        transformed_content = self.humanize_ai_text(text)
        
        # Başlık oluştur
        if generate_title:
            title = self.generate_human_like_title(transformed_content)
        else:
            title = ""
        
        return title, transformed_content

# Geriye uyumluluk için
def create_news_article(topic: str) -> Tuple[str, str]:
    """Eski fonksiyon - geriye uyumluluk için"""
    generator = NewsStyleTransfer()
    return generator.create_news(topic)

def transform_ai_to_human(text: str) -> Tuple[str, str]:
    """AI metnini insan stiline çevir"""
    generator = NewsStyleTransfer()
    return generator.transform_text(text)

# Web uygulaması için uyumlu method
def transform_news_style(self, text: str) -> Tuple[str, str]:
    """Web uygulaması ile uyumlu stil transfer methodu"""
    return self.transform_text(text)

# Method'u NewsStyleTransfer sınıfına ekle
NewsStyleTransfer.transform_news_style = transform_news_style

if __name__ == "__main__":
    # Test için
    generator = NewsStyleTransfer()
    
    test_ai_text = """
    Kütahya'da eğitim konusunda kapsamlı bir proje gerçekleştirilmiştir. 
    Bu bağlamda, öğrenciler tarafından robot tasarımları yapılmıştır.
    Yapılan değerlendirmeler neticesinde başarılı sonuçlar elde edilmiştir.
    """
    
    title, content = generator.transform_text(test_ai_text)
    print("🤖 Orijinal AI Metni:")
    print(test_ai_text)
    print("\n👤 İnsan Stiline Çevrilmiş:")
    print(f"📰 Başlık: {title}")
    print(f"📝 İçerik: {content}")