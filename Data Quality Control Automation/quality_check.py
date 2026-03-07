import pandas as pd

# CSV yükleme
df = pd.read_csv("titanic.csv")

print("Dataset Shape:", df.shape)
print("\Columns:", df.columns)
#df.shape → (satır sayısı, sütun sayısı) verir.
#df.columns → sütun isimlerini listeler.

# -------------------------
# 1. Eksik veri analizi
# -------------------------
missing_ratio = df.isna().mean()
#df.isna() → DataFrame’deki her hücreyi kontrol eder: NaN ise True, değilse False döner.
#df.isna().mean() → True=1, False=0 kabul ederek her sütunun eksik veri yüzdesini hesaplar.

missing_report = pd.DataFrame({
    "Column": missing_ratio.index,
    "MissingRatio": missing_ratio.values
})
#missing_ratio.index → sütun isimleri
#missing_ratio.values → NaN oranları

print("\n=== Missing Data Ratio ===")
print(missing_report)


# -------------------------
# 2. Aykırı değer kontrolü (3 Sigma)
# Fare sütunu üzerinden
# -------------------------
col = "fare"

mean = df[col].mean()
std = df[col].std()

upper_limit = mean + 3*std
lower_limit = mean - 3*std

outliers = df[(df[col] > upper_limit) | (df[col] < lower_limit)]
#Koşul: Fare değeri üst sınırdan büyük veya alt sınırdan küçükse
# | → “veya” anlamına gelir
#Sonuç: outliers DataFrame’i sadece aykırı değerleri içerir.

print("\n=== Outliers in Fare Column ===")
print(outliers[[col]])

print("\nTTotal outliers:", len(outliers))
#outliers[[col]] → sadece Fare sütununu gösterir
#len(outliers) → kaç tane aykırı değer olduğunu verir

# -------------------------
# 3. Genel Veri Kalitesi Raporu
# -------------------------

report = pd.DataFrame({
    "Column": df.columns,
    "MissingRatio": df.isna().mean(),
    "DataType": df.dtypes
})

report["Outlier_Count"] = 0
report.loc[report["Column"] == col, "Outlier_Count"] = len(outliers)
