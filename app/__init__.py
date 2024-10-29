from flask import Flask
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import os
import json

#defini db como método SqlAlchemy 
db = SQLAlchemy()


#Cria a função para montar a aplicação e a retorna
def create_app():
    app = Flask(__name__, static_folder='static')   
    app.config["SECRET_KEY"] = "sddsfsfdfgg"
    #configuração banco dados SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/quitanda'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
    
    #Inicializa o metódo db para app
    db.init_app(app)
    
    #models
    from .models import Frutas, Categorias
    #Início: importamos e registramos o Blueprint
    from .routes.routes_main import bp
    app.register_blueprint(bp)
    #Fim: importamos e registramos o Blueprint    
    
    
    
    #Retorno da montagem do app
    return app    

    