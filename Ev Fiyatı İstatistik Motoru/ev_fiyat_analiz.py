import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class EvFiyatAnaliz:
    def __init__(self, dosya_yolu):
        """CSV dosyasını yükleyerek analiz sınıfını başlatır."""
        try:
            self.veri = pd.read_csv(dosya_yolu)
            print("Veri başarıyla yüklendi!")
            print(f"Veri şekli: {self.veri.shape}")
            print("\nİlk 5 satır:")
            print(self.veri.head())
        except FileNotFoundError:
            print("Dosya bulunamadı! Lütfen dosya yolunu kontrol edin.")
            self.veri = None
    
    def istatistik_hesapla(self):
        """Tüm sayısal sütunlar için ortalama, medyan ve standart sapma hesaplar."""
        if self.veri is None:
            print("Veri yüklenmedi!")
            return
        
        sayisal_veri = self.veri.select_dtypes(include=[np.number])
        
        print("\n" + "="*50)
        print("İSTATİSTİKSEL HESAPLAMALAR")
        print("="*50)
        
        for sutun in sayisal_veri.columns:
            ortalama = np.mean(sayisal_veri[sutun])
            medyan = np.median(sayisal_veri[sutun])
            std_sapma = np.std(sayisal_veri[sutun])
            
            print(f"\n{sutun}:")
            print(f"  Ortalama: {ortalama:.2f}")
            print(f"  Medyan: {medyan:.2f}")
            print(f"  Standart Sapma: {std_sapma:.2f}")
    
    def bolge_filtrele(self, bolge_kodu):
        """Belirli bir bölge koduna göre veriyi filtreler ve fiyat ortalamasını hesaplar."""
        if self.veri is None:
            print("Veri yüklenmedi!")
            return
        
        # Bölge kodunu içeren sütunu bulma (farklı isimler olabilir)
        bolge_sutunlari = [col for col in self.veri.columns if 'bolge' in col.lower() or 
                          'region' in col.lower() or 'kod' in col.lower()]
        
        if not bolge_sutunlari:
            print("Bölge bilgisi içeren sütun bulunamadı!")
            return
        
        bolge_sutunu = bolge_sutunlari[0]
        print(f"\nFiltreleme için kullanılan sütun: {bolge_sutunu}")
        
        # NumPy Boolean Masking ile filtreleme
        bolge_maske = self.veri[bolge_sutunu].values == bolge_kodu
        filtrelenmis_veri = self.veri[bolge_maske]
        
        # Fiyat sütununu bulma
        fiyat_sutunlari = [col for col in self.veri.columns if 'fiyat' in col.lower() or 
                          'price' in col.lower()]
        
        if not fiyat_sutunlari:
            print("Fiyat bilgisi içeren sütun bulunamadı!")
            return
        
        fiyat_sutunu = fiyat_sutunlari[0]
        
        if len(filtrelenmis_veri) > 0:
            ortalama_fiyat = np.mean(filtrelenmis_veri[fiyat_sutunu])
            print(f"\nBölge {bolge_kodu} için bulunan ev sayısı: {len(filtrelenmis_veri)}")
            print(f"Bölge {bolge_kodu} ortalama fiyat: {ortalama_fiyat:.2f}")
        else:
            print(f"\nBölge {bolge_kodu} için kayıt bulunamadı!")
        
        return filtrelenmis_veri
    
    def scatter_plot_ciz(self, x_sutun=None, y_sutun=None):
        """İki değişken arasındaki ilişkiyi scatter plot ile gösterir."""
        if self.veri is None:
            print("Veri yüklenmedi!")
            return
        
        # Eğer sütun isimleri belirtilmemişse, otomatik olarak bul
        if x_sutun is None:
            buyukluk_sutunlari = [col for col in self.veri.columns if 'buyukluk' in col.lower() or 
                                 'size' in col.lower() or 'alan' in col.lower() or 
                                 'm2' in col.lower()]
            x_sutun = buyukluk_sutunlari[0] if buyukluk_sutunlari else self.veri.columns[1]
        
        if y_sutun is None:
            fiyat_sutunlari = [col for col in self.veri.columns if 'fiyat' in col.lower() or 
                              'price' in col.lower()]
            y_sutun = fiyat_sutunlari[0] if fiyat_sutunlari else self.veri.columns[0]
        
        plt.figure(figsize=(10, 6))
        plt.scatter(self.veri[x_sutun], self.veri[y_sutun], alpha=0.6, color='blue')
        plt.xlabel(x_sutun)
        plt.ylabel(y_sutun)
        plt.title(f'{x_sutun} ve {y_sutun} Arasındaki İlişki')
        plt.grid(True, alpha=0.3)
        
        # Korelasyon katsayısını hesapla ve göster
        korelasyon = np.corrcoef(self.veri[x_sutun], self.veri[y_sutun])[0, 1]
        plt.text(0.05, 0.95, f'Korelasyon: {korelasyon:.2f}', 
                transform=plt.gca().transAxes, bbox=dict(boxstyle="round", facecolor='wheat'))
        
        plt.tight_layout()
        plt.show()
        
        print(f"\nScatter Plot: {x_sutun} vs {y_sutun}")
        print(f"Korelasyon katsayısı: {korelasyon:.2f}")

def main():
    # Analiz motorunu başlat
    analiz = EvFiyatAnaliz('housing_data.csv')
    
    # Eğer dosya bulunamazsa, örnek veri oluştur
    if analiz.veri is None:
        print("Örnek veri oluşturuluyor...")
        ornek_veri_olustur()
        analiz = EvFiyatAnaliz('housing_data.csv')
    
    # İstatistiksel hesaplamalar
    analiz.istatistik_hesapla()
    
    # Bölgeye göre filtreleme (kullanıcıdan alınabilir)
    bolge_kodu = int(input("\nFiltrelemek istediğiniz bölge kodunu girin: "))
    analiz.bolge_filtrele(bolge_kodu)
    
    # Scatter plot çiz
    print("\nScatter Plot çiziliyor...")
    analiz.scatter_plot_ciz()

def ornek_veri_olustur():
    """Örnek ev fiyat verisi oluşturur."""
    np.random.seed(42)
    
    veri = {
        'fiyat': np.random.normal(500000, 200000, 1000),
        'buyukluk_m2': np.random.normal(120, 40, 1000),
        'bolge_kodu': np.random.choice([1, 2, 3, 4, 5], 1000),
        'oda_sayisi': np.random.randint(1, 6, 1000),
        'bina_yasi': np.random.randint(0, 50, 1000)
    }
    
    # Fiyat ve büyüklük arasında pozitif korelasyon oluştur
    veri['fiyat'] = veri['fiyat'] + veri['buyukluk_m2'] * 1000
    
    df = pd.DataFrame(veri)
    df.to_csv('housing_data.csv', index=False)
    print("Örnek veri 'housing_data.csv' olarak kaydedildi!")

if __name__ == "__main__":
    main()