from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'sua_chave_secreta_aqui')

# Configuração do banco de dados
if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///treinos.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração para PostgreSQL
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgresql://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgresql://', 'postgresql://', 1)

db = SQLAlchemy(app)

# Modelos
class Treino(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    categoria = db.Column(db.String(50))
    status = db.Column(db.String(20), default='ativo')
    exercicios = db.relationship('Exercicio', backref='treino', lazy=True)

class Exercicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    categoria_muscular = db.Column(db.String(50))
    instrucoes = db.Column(db.Text)
    series_preparacao = db.Column(db.Integer)
    peso_preparacao = db.Column(db.Float)
    series_eficazes = db.Column(db.Integer)
    repeticoes_eficazes = db.Column(db.Integer)
    peso_eficazes = db.Column(db.Float)
    tempo_descanso = db.Column(db.Integer)  # em segundos
    treino_id = db.Column(db.Integer, db.ForeignKey('treino.id'), nullable=False)

class SessaoTreino(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_hora = db.Column(db.DateTime, default=datetime.utcnow)
    treino_id = db.Column(db.Integer, db.ForeignKey('treino.id'), nullable=False)
    observacoes = db.Column(db.Text)

# Criar as tabelas
with app.app_context():
    db.create_all()

# Rotas
@app.route('/')
def home():
    treinos = Treino.query.order_by(Treino.data_criacao.desc()).all()
    return render_template('home.html', treinos=treinos)

@app.route('/treino/<int:treino_id>')
def treino(treino_id):
    treino = Treino.query.get_or_404(treino_id)
    return render_template('treino.html', treino=treino)

@app.route('/exercicio/<int:exercicio_id>')
def exercicio(exercicio_id):
    exercicio = Exercicio.query.get_or_404(exercicio_id)
    return render_template('exercicio.html', exercicio=exercicio)

@app.route('/novo_treino', methods=['GET', 'POST'])
def novo_treino():
    if request.method == 'POST':
        try:
            # Criar o treino
            nome = request.form['nome']
            categoria = request.form['categoria']
            
            treino = Treino(nome=nome, categoria=categoria)
            db.session.add(treino)
            db.session.flush()  # Para obter o ID do treino antes do commit
            
            # Processar exercícios
            exercicios_data = request.form.to_dict()
            exercicio_count = 0
            
            while f'exercicios[{exercicio_count}][nome]' in exercicios_data:
                exercicio = Exercicio(
                    nome=exercicios_data[f'exercicios[{exercicio_count}][nome]'],
                    categoria_muscular=exercicios_data[f'exercicios[{exercicio_count}][categoria_muscular]'],
                    instrucoes=exercicios_data[f'exercicios[{exercicio_count}][instrucoes]'],
                    series_preparacao=int(exercicios_data[f'exercicios[{exercicio_count}][series_preparacao]']),
                    peso_preparacao=float(exercicios_data[f'exercicios[{exercicio_count}][peso_preparacao]']),
                    series_eficazes=int(exercicios_data[f'exercicios[{exercicio_count}][series_eficazes]']),
                    repeticoes_eficazes=int(exercicios_data[f'exercicios[{exercicio_count}][repeticoes_eficazes]']),
                    peso_eficazes=float(exercicios_data[f'exercicios[{exercicio_count}][peso_eficazes]']),
                    tempo_descanso=int(exercicios_data[f'exercicios[{exercicio_count}][tempo_descanso]']),
                    treino_id=treino.id
                )
                db.session.add(exercicio)
                exercicio_count += 1
            
            db.session.commit()
            flash('Treino criado com sucesso!', 'success')
            return redirect(url_for('home'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar treino: {str(e)}', 'danger')
            return redirect(url_for('novo_treino'))
    
    return render_template('novo_treino.html')

@app.route('/treino/<int:treino_id>/iniciar', methods=['POST'])
def iniciar_treino(treino_id):
    treino = Treino.query.get_or_404(treino_id)
    sessao = SessaoTreino(treino_id=treino_id)
    db.session.add(sessao)
    db.session.commit()
    return jsonify({'success': True, 'sessao_id': sessao.id})

@app.route('/exercicio/<int:exercicio_id>/completar', methods=['POST'])
def completar_exercicio(exercicio_id):
    exercicio = Exercicio.query.get_or_404(exercicio_id)
    # Aqui você pode adicionar lógica para registrar o progresso do exercício
    return jsonify({'success': True})

@app.route('/treino/<int:treino_id>/finalizar', methods=['POST'])
def finalizar_treino(treino_id):
    treino = Treino.query.get_or_404(treino_id)
    treino.status = 'completo'
    db.session.commit()
    return jsonify({'success': True})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port) 