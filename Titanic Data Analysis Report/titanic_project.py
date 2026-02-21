import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = sns.load_dataset("titanic")
data.to_csv("titanic.csv", index=False)
print("titanic.csv dosyası oluşturuldu.")

print('\nVeri Bilgileri:')
print(data.info())
print("\nİstatistiksel Özet:")
print(data.describe())

median_age = data['age'].median()
data['age'] = data['age'].fillna(median_age)
# fillna() : Veri içindeki eksik (NaN) değerleri doldurur.

data["AgeGroup"] = pd.cut(data["age"], bins=[0, 12, 18, 40, 60, 100], 
                        labels=["Child", "Teen", "Adult", "MiddleAge", "Senior"])

survival_age = data.groupby("AgeGroup")["survived"].mean().reset_index()
survival_age.columns = ["Age Group", "Survival Rate"]
print("\nYaş Gruplarına Göre Hayatta Kalma Oranları:")
print(survival_age)

survival_gender_class = data.groupby(['sex', 'pclass'])['survived'].mean().reset_index()
#reset_index() : index’i normale çevirip veriyi tekrar tablo formatına getiren fonksiyon.
survival_gender_class.columns = ['gender', 'pclass', 'Survival Rate']
print('\n Cinsiyet ve Sınıfa göre hayatta kalma oranları:')
print(survival_gender_class)

plt.figure(figsize=(8,6))
sns.countplot(data=data, x='sex', hue='survived')
#hue : grafikte renkle ikinci bir kategori eklemek.
plt.title('Survival by Gender')
plt.xlabel('Gender')
plt.ylabel('Passenger Count')
plt.legend(title='survived', labels=['Not Survived', 'Survived'])
plt.show()

plt.figure(figsize=(8,6))
sns.boxplot(data=data, x="pclass", y="fare")
plt.title("Relationship between Pclass and Mouse")
plt.xlabel("Passenger Class")
plt.ylabel("Fare")
plt.show()
