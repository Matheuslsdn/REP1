from flask import Blueprint,jsonify, render_template, request, session, url_for, flash, redirect
from app.models import Frutas, Categorias
from werkzeug.utils import secure_filename
from datetime import datetime
from app import db
import os
import json


frutas = {
    
    1: {"nome_fruta":"Melancia","preco": 29.99,"quantidade":50},
    2: {"nome_fruta":"Pera","preco": 10,"quantidade":50},
    3: {"nome_fruta":"Uva","preco": 50,"quantidade":35},
    4: {"nome_fruta":"Laranja","preco": 35,"quantidade":30}
    
}

bp = Blueprint("main",__name__,template_folder='../templates/main')

@bp.route('/',endpoint='home')
def index():
    frutas = Frutas.query.all()
    return render_template("frutas.html",frutas=frutas)

@bp.route('/frutas/<int:id>', methods=['GET'])
def get_frutas(id):
    fruta = frutas.get(id)
    if fruta:
        return jsonify(fruta)
    return jsonify({"erro":"Frutas não encontrado"}),404

@bp.route('/categorias',endpoint='categorias')
def categorias():
    categorias = Categorias.query.all()
    return render_template("categorias.html", categorias=categorias)

@bp.route('/deletar',methods=['GET'], endpoint='deleta')
def deletarFruta():
    id = request.args.get('id')
    frutas = Frutas.query.get_or_404(id)    
    try:
        db.session.delete(frutas)
        db.session.commit()
        return redirect(url_for('main.home'))
    except Exception as e:
        db.session.rollback()
        return "Deu erro"
    
    
@bp.route('/atualizar/<int:id>',methods=['GET','POST'], endpoint='atualizar')
def atualizarFruta(id):
    categorias = Categorias.query.all()
    fruta = Frutas.query.get_or_404(id) 
    if request.method == 'POST':
         fruta.nome_fruta= request.form['nome_fruta']
         fruta.quantidade= request.form['quantidade']
         fruta.cor= request.form['cor']
         fruta.data_aquisicao= request.form['data_aquisicao']
         fruta.categoria_id= request.form['categoria_id']
         try:
            db.session.commit()
            flash('Fruta atualizado com sucesso!')
            return redirect(url_for('main.home'))
         except Exception as e:
            db.session.rollback()
            flash(f'Ocorreu um erro ao atualizar: {str(e)}')

    return render_template('editar_fruta.html', fruta=fruta, categorias=categorias)

@bp.route('/cadastro',endpoint='cadastro',methods=['GET','POST'])
def cadastro():
        categorias = Categorias.query.all()
        if request.method == 'POST':
            nome_fruta = request.form['nome_fruta']
            quantidade = request.form['quantidade']
            cor = request.form['cor']
            data_aquisicao = datetime.strptime(request.form['data_aquisicao'],'%Y-%m-%d').date()
            categoria_id= request.form['categoria_id']

            # Cria um novo usuário
            novo_fruta = Frutas(nome_fruta=nome_fruta, quantidade=quantidade, cor=cor, data_aquisicao=data_aquisicao, categoria_id=categoria_id)

            try:
                db.session.add(novo_fruta)
                db.session.commit()
                flash('Fruta cadastrada')
                return redirect(url_for('main.home'))
            except Exception as e:
                db.session.rollback()
                print(f'Ocorreu um erro ao cadastrar: {str(e)}') 
                    
        return render_template("cadastro.html",categorias=categorias)

ARQUIVO_FRUTAS = 'frutas.json'

def carregar_frutas():
    if os.path.exists(ARQUIVO_FRUTAS):
        with open(ARQUIVO_FRUTAS, 'r') as arquivo:
            return json.load(arquivo)
    else:
        with open(ARQUIVO_FRUTAS, 'w') as arquivo:
            json.dump({}, arquivo)
        return {}

def salvar_frutas():
    with open(ARQUIVO_FRUTAS, 'w') as arquivo:
        json.dump(frutasQuitanda, arquivo, indent=4)

frutasQuitanda = carregar_frutas()

bp = Blueprint("main", __name__, template_folder='../templates/main')

@bp.route('/api/fruta', endpoint='api', methods=['GET'])
def get_frutas():
    return jsonify(frutasQuitanda), 200

@bp.route('/api/post/fruta', methods=['POST'])
def criar_fruta():
    dados = request.get_json()
    novo_id = str(max([int(i) for i in frutasQuitanda.keys()]) + 1 if frutasQuitanda else 1)
    try:
        data_aquisicao = datetime.strptime(dados.get("data_aquisicao"), "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"erro": "data de aquisição deve estar no formato YYYY-MM-DD"}), 400
    
    frutasQuitanda[novo_id] = {
        "nome_fruta": dados.get("nome_fruta"),
        "quantidade": dados.get("quantidade"),
        "cor": dados.get("cor"),
        "data_aquisicao": data_aquisicao.isoformat(),
        "categoria_id": dados.get("categoria_id"),
        "texto": "foi"
    }

    salvar_frutas()
    return jsonify(frutasQuitanda[novo_id]), 201
        