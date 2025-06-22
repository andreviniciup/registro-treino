from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

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
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    foto_perfil = db.Column(db.String(200))
    bio = db.Column(db.Text)
    treinos = db.relationship('Treino', backref='usuario', lazy=True)
    metas = db.relationship('Meta', backref='usuario', lazy=True)
    desafios_criados = db.relationship('Desafio', backref='criador', lazy=True, foreign_keys='Desafio.criador_id')
    desafios_participando = db.relationship('ParticipanteDesafio', backref='usuario', lazy=True)

class Treino(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    categoria = db.Column(db.String(50))
    status = db.Column(db.String(20), default='ativo')
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
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

class Meta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    tipo = db.Column(db.String(50))  # 'treino', 'peso', 'cardio', etc.
    valor_objetivo = db.Column(db.Float)
    valor_atual = db.Column(db.Float, default=0)
    data_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    data_fim = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='ativa')  # 'ativa', 'concluida', 'cancelada'
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    registros = db.relationship('RegistroMeta', backref='meta', lazy=True)

class RegistroMeta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    valor = db.Column(db.Float)
    observacoes = db.Column(db.Text)
    meta_id = db.Column(db.Integer, db.ForeignKey('meta.id'), nullable=False)

class Desafio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    tipo = db.Column(db.String(50))  # 'treino', 'peso', 'cardio', etc.
    valor_objetivo = db.Column(db.Float)
    data_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    data_fim = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='ativo')  # 'ativo', 'finalizado', 'cancelado'
    criador_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    participantes = db.relationship('ParticipanteDesafio', backref='desafio', lazy=True)

class ParticipanteDesafio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    desafio_id = db.Column(db.Integer, db.ForeignKey('desafio.id'), nullable=False)
    data_entrada = db.Column(db.DateTime, default=datetime.utcnow)
    valor_atual = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='participando')  # 'participando', 'concluido', 'desistiu'

# Criar as tabelas
with app.app_context():
    db.create_all()
    
    # Executar migração se necessário
    try:
        from sqlalchemy import text
        
        # Verificar se a coluna usuario_id existe na tabela treino
        result = db.session.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'treino' AND column_name = 'usuario_id'
        """))
        
        if not result.fetchone():
            print("Executando migração do banco de dados...")
            
            # Adicionar coluna usuario_id
            db.session.execute(text("ALTER TABLE treino ADD COLUMN usuario_id INTEGER"))
            
            # Criar usuário padrão
            db.session.execute(text("""
                INSERT INTO usuario (nome, email, senha_hash, data_cadastro) 
                VALUES ('Usuário Padrão', 'default@example.com', 'default_hash', NOW())
                ON CONFLICT (email) DO NOTHING
            """))
            
            # Pegar ID do usuário padrão
            result = db.session.execute(text("SELECT id FROM usuario WHERE email = 'default@example.com'"))
            user_id = result.fetchone()[0]
            
            # Atualizar treinos existentes
            db.session.execute(text(f"UPDATE treino SET usuario_id = {user_id} WHERE usuario_id IS NULL"))
            
            db.session.commit()
            print("Migração concluída!")
            
    except Exception as e:
        print(f"Erro na migração: {str(e)}")
        db.session.rollback()

# Rotas
@app.route('/')
def home():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.get(session['usuario_id'])
    treinos = Treino.query.filter_by(usuario_id=usuario.id).order_by(Treino.data_criacao.desc()).all()
    metas = Meta.query.filter_by(usuario_id=usuario.id, status='ativa').all()
    desafios = Desafio.query.filter_by(status='ativo').all()
    
    return render_template('home.html', usuario=usuario, treinos=treinos, metas=metas, desafios=desafios)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and check_password_hash(usuario.senha_hash, senha):
            session['usuario_id'] = usuario.id
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Email ou senha incorretos!', 'danger')
    
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        
        if Usuario.query.filter_by(email=email).first():
            flash('Email já cadastrado!', 'danger')
            return redirect(url_for('cadastro'))
        
        senha_hash = generate_password_hash(senha)
        usuario = Usuario(nome=nome, email=email, senha_hash=senha_hash)
        db.session.add(usuario)
        db.session.commit()
        
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('login'))
    
    return render_template('cadastro.html')

@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('login'))

@app.route('/metas')
def metas():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.get(session['usuario_id'])
    metas = Meta.query.filter_by(usuario_id=usuario.id).order_by(Meta.data_inicio.desc()).all()
    return render_template('metas.html', usuario=usuario, metas=metas)

@app.route('/nova_meta', methods=['GET', 'POST'])
def nova_meta():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        tipo = request.form['tipo']
        valor_objetivo = float(request.form['valor_objetivo'])
        data_fim = datetime.strptime(request.form['data_fim'], '%Y-%m-%d')
        
        meta = Meta(
            titulo=titulo,
            descricao=descricao,
            tipo=tipo,
            valor_objetivo=valor_objetivo,
            data_fim=data_fim,
            usuario_id=session['usuario_id']
        )
        db.session.add(meta)
        db.session.commit()
        
        flash('Meta criada com sucesso!', 'success')
        return redirect(url_for('metas'))
    
    return render_template('nova_meta.html')

@app.route('/desafios')
def desafios():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.get(session['usuario_id'])
    desafios = Desafio.query.filter_by(status='ativo').all()
    return render_template('desafios.html', usuario=usuario, desafios=desafios)

@app.route('/novo_desafio', methods=['GET', 'POST'])
def novo_desafio():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        tipo = request.form['tipo']
        valor_objetivo = float(request.form['valor_objetivo'])
        data_fim = datetime.strptime(request.form['data_fim'], '%Y-%m-%d')
        
        desafio = Desafio(
            titulo=titulo,
            descricao=descricao,
            tipo=tipo,
            valor_objetivo=valor_objetivo,
            data_fim=data_fim,
            criador_id=session['usuario_id']
        )
        db.session.add(desafio)
        db.session.commit()
        
        flash('Desafio criado com sucesso!', 'success')
        return redirect(url_for('desafios'))
    
    return render_template('novo_desafio.html')

@app.route('/desafio/<int:desafio_id>/participar', methods=['POST'])
def participar_desafio(desafio_id):
    if 'usuario_id' not in session:
        return jsonify({'success': False, 'error': 'Usuário não logado'})
    
    desafio = Desafio.query.get_or_404(desafio_id)
    
    # Verificar se já está participando
    participante = ParticipanteDesafio.query.filter_by(
        usuario_id=session['usuario_id'],
        desafio_id=desafio_id
    ).first()
    
    if participante:
        return jsonify({'success': False, 'error': 'Já está participando deste desafio'})
    
    participante = ParticipanteDesafio(
        usuario_id=session['usuario_id'],
        desafio_id=desafio_id
    )
    db.session.add(participante)
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/meta/<int:meta_id>/registrar', methods=['POST'])
def registrar_meta(meta_id):
    if 'usuario_id' not in session:
        return jsonify({'success': False, 'error': 'Usuário não logado'})
    
    meta = Meta.query.get_or_404(meta_id)
    valor = float(request.json['valor'])
    observacoes = request.json.get('observacoes', '')
    
    registro = RegistroMeta(
        valor=valor,
        observacoes=observacoes,
        meta_id=meta_id
    )
    db.session.add(registro)
    
    # Atualizar valor atual da meta
    meta.valor_atual += valor
    
    # Verificar se a meta foi concluída
    if meta.valor_atual >= meta.valor_objetivo:
        meta.status = 'concluida'
    
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/treino/<int:treino_id>')
def treino(treino_id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    treino = Treino.query.get_or_404(treino_id)
    if treino.usuario_id != session['usuario_id']:
        flash('Acesso negado!', 'danger')
        return redirect(url_for('home'))
    
    return render_template('treino.html', treino=treino)

@app.route('/exercicio/<int:exercicio_id>')
def exercicio(exercicio_id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    exercicio = Exercicio.query.get_or_404(exercicio_id)
    if exercicio.treino.usuario_id != session['usuario_id']:
        flash('Acesso negado!', 'danger')
        return redirect(url_for('home'))
    
    return render_template('exercicio.html', exercicio=exercicio)

@app.route('/novo_treino', methods=['GET', 'POST'])
def novo_treino():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            # Criar o treino
            nome = request.form['nome']
            categoria = request.form['categoria']
            
            treino = Treino(nome=nome, categoria=categoria, usuario_id=session['usuario_id'])
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
    if 'usuario_id' not in session:
        return jsonify({'success': False, 'error': 'Usuário não logado'})
    
    treino = Treino.query.get_or_404(treino_id)
    if treino.usuario_id != session['usuario_id']:
        return jsonify({'success': False, 'error': 'Acesso negado'})
    
    sessao = SessaoTreino(treino_id=treino_id)
    db.session.add(sessao)
    db.session.commit()
    return jsonify({'success': True, 'sessao_id': sessao.id})

@app.route('/exercicio/<int:exercicio_id>/completar', methods=['POST'])
def completar_exercicio(exercicio_id):
    if 'usuario_id' not in session:
        return jsonify({'success': False, 'error': 'Usuário não logado'})
    
    exercicio = Exercicio.query.get_or_404(exercicio_id)
    if exercicio.treino.usuario_id != session['usuario_id']:
        return jsonify({'success': False, 'error': 'Acesso negado'})
    
    # Aqui você pode adicionar lógica para registrar o progresso do exercício
    return jsonify({'success': True})

@app.route('/treino/<int:treino_id>/finalizar', methods=['POST'])
def finalizar_treino(treino_id):
    if 'usuario_id' not in session:
        return jsonify({'success': False, 'error': 'Usuário não logado'})
    
    treino = Treino.query.get_or_404(treino_id)
    if treino.usuario_id != session['usuario_id']:
        return jsonify({'success': False, 'error': 'Acesso negado'})
    
    treino.status = 'completo'
    db.session.commit()
    return jsonify({'success': True})

@app.route('/exercicio/<int:exercicio_id>/atualizar', methods=['POST'])
def atualizar_exercicio(exercicio_id):
    if 'usuario_id' not in session:
        return jsonify({'success': False, 'error': 'Usuário não logado'})
    
    exercicio = Exercicio.query.get_or_404(exercicio_id)
    if exercicio.treino.usuario_id != session['usuario_id']:
        return jsonify({'success': False, 'error': 'Acesso negado'})
    
    try:
        data = request.get_json()
        
        # Atualizar séries de preparação
        if 'peso_preparacao' in data:
            exercicio.peso_preparacao = float(data['peso_preparacao'])
        if 'series_preparacao' in data:
            exercicio.series_preparacao = int(data['series_preparacao'])
            
        # Atualizar séries eficazes
        if 'peso_eficazes' in data:
            exercicio.peso_eficazes = float(data['peso_eficazes'])
        if 'repeticoes_eficazes' in data:
            exercicio.repeticoes_eficazes = int(data['repeticoes_eficazes'])
            
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port) 