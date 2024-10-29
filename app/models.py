from . import db   

class Frutas(db.Model):
    __tablename__ = 'frutas'
    id = db.Column(db.Integer, primary_key=True)
    nome_fruta = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, unique=True, nullable=False)
    cor = db.Column(db.String(100), nullable=False)
    data_aquisicao = db.Column(db.Date, nullable=True)
    categoria_id = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Integer, nullable=True, default="1")

class Categorias(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)




    