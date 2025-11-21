from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Gorev
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gizli_anahtar_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Veritabanını başlat
db.init_app(app)

# Veritabanı tablolarını oluştur
with app.app_context():
    db.create_all()

# Ana sayfa - Tüm görevleri listele
@app.route('/')
def index():
    gorevler = Gorev.query.all()
    return render_template('index.html', gorevler=gorevler)

# Yeni görev ekle
@app.route('/ekle', methods=['POST'])
def gorev_ekle():
    baslik = request.form.get('baslik')
    aciklama = request.form.get('aciklama')
    
    if baslik:
        yeni_gorev = Gorev(baslik=baslik, aciklama=aciklama)
        db.session.add(yeni_gorev)
        db.session.commit()
        flash('Görev başarıyla eklendi!', 'success')
    else:
        flash('Görev başlığı boş olamaz!', 'danger')
    
    return redirect(url_for('index'))

# Görev durumunu güncelle (Tamamlandı/Beklemede)
@app.route('/durum_guncelle/<int:gorev_id>')
def durum_guncelle(gorev_id):
    gorev = Gorev.query.get_or_404(gorev_id)
    gorev.durum = not gorev.durum
    db.session.commit()
    
    durum = "tamamlandı" if gorev.durum else "beklemede"
    flash(f'Görev {durum} olarak işaretlendi!', 'info')
    
    return redirect(url_for('index'))

# Görevi sil
@app.route('/sil/<int:gorev_id>')
def gorev_sil(gorev_id):
    gorev = Gorev.query.get_or_404(gorev_id)
    db.session.delete(gorev)
    db.session.commit()
    flash('Görev başarıyla silindi!', 'warning')
    
    return redirect(url_for('index'))

# Görevi düzenle sayfası
@app.route('/duzenle/<int:gorev_id>', methods=['GET', 'POST'])
def gorev_duzenle(gorev_id):
    gorev = Gorev.query.get_or_404(gorev_id)
    
    if request.method == 'POST':
        gorev.baslik = request.form.get('baslik')
        gorev.aciklama = request.form.get('aciklama')
        db.session.commit()
        flash('Görev başarıyla güncellendi!', 'success')
        return redirect(url_for('index'))
    
    return render_template('guncelle.html', gorev=gorev)

if __name__ == '__main__':
    app.run(debug=True)