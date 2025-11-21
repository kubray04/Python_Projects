from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Gorev(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baslik = db.Column(db.String(100), nullable=False)
    aciklama = db.Column(db.Text, nullable=True)
    durum = db.Column(db.Boolean, default=False)
    tarih = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, baslik, aciklama=None):
        self.baslik = baslik
        self.aciklama = aciklama
    
    def __repr__(self):
        return f'<Gorev {self.baslik}>'
    
    def tamamla(self):
        self.durum = True
    
    def beklemeye_al(self):
        self.durum = False
    
    def to_dict(self):
        return {
            'id': self.id,
            'baslik': self.baslik,
            'aciklama': self.aciklama,
            'durum': self.durum,
            'tarih': self.tarih.strftime('%Y-%m-%d %H:%M')
        }