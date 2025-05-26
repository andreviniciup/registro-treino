from app import app, db, Treino, Exercicio
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

def adicionar_treinos():
    with app.app_context():
        try:
            # Limpar treinos existentes
            Exercicio.query.delete()
            Treino.query.delete()
            db.session.commit()
            print("Treinos antigos removidos com sucesso!")

            # Treino A - Pernas (ênfase anterior e glúteo)
            treino_a = Treino(
                nome="Treino A - Pernas (ênfase anterior e glúteo)",
                categoria="Pernas",
                status="ativo"
            )
            db.session.add(treino_a)
            db.session.flush()

            exercicios_a = [
                Exercicio(
                    nome="Hack Machine",
                    categoria_muscular="Pernas",
                    instrucoes="2 séries preparatórias\n1 série de trabalho (rest-pause: faz até falhar, 15s de descanso, repete 2x)\nCarga: Progressão semanal, começando com carga que permita 8-10 reps",
                    series_preparacao=2,
                    peso_preparacao=0,
                    series_eficazes=1,
                    repeticoes_eficazes=10,
                    peso_eficazes=0,
                    tempo_descanso=90,
                    treino_id=treino_a.id
                ),
                Exercicio(
                    nome="Leg Press",
                    categoria_muscular="Pernas",
                    instrucoes="1 preparatória\n2 séries de trabalho (última com drop-set: tira 20% do peso e continua até falha)",
                    series_preparacao=1,
                    peso_preparacao=0,
                    series_eficazes=2,
                    repeticoes_eficazes=10,
                    peso_eficazes=0,
                    tempo_descanso=90,
                    treino_id=treino_a.id
                ),
                Exercicio(
                    nome="Cadeira Extensora",
                    categoria_muscular="Pernas",
                    instrucoes="2 séries de trabalho (reps altas: 12-15)\nÚltima série: isometria de 15 segundos na contração máxima após a falha",
                    series_preparacao=0,
                    peso_preparacao=0,
                    series_eficazes=2,
                    repeticoes_eficazes=15,
                    peso_eficazes=0,
                    tempo_descanso=90,
                    treino_id=treino_a.id
                ),
                Exercicio(
                    nome="Cadeira Adutora",
                    categoria_muscular="Pernas",
                    instrucoes="1 série de aquecimento\n2 séries de trabalho (12-15 reps)",
                    series_preparacao=1,
                    peso_preparacao=0,
                    series_eficazes=2,
                    repeticoes_eficazes=15,
                    peso_eficazes=0,
                    tempo_descanso=90,
                    treino_id=treino_a.id
                ),
                Exercicio(
                    nome="Elevação de pernas",
                    categoria_muscular="Abdômen",
                    instrucoes="3 séries até a falha",
                    series_preparacao=0,
                    peso_preparacao=0,
                    series_eficazes=3,
                    repeticoes_eficazes=0,
                    peso_eficazes=0,
                    tempo_descanso=60,
                    treino_id=treino_a.id
                )
            ]

            # Treino B - Peito e Bíceps
            treino_b = Treino(
                nome="Treino B - Peito e Bíceps",
                categoria="Peito",
                status="ativo"
            )
            db.session.add(treino_b)
            db.session.flush()

            exercicios_b = [
                Exercicio(
                    nome="Supino Inclinado",
                    categoria_muscular="Peito",
                    instrucoes="2 séries preparatórias\n2 séries de trabalho (rest-pause)",
                    series_preparacao=2,
                    peso_preparacao=0,
                    series_eficazes=2,
                    repeticoes_eficazes=10,
                    peso_eficazes=0,
                    tempo_descanso=90,
                    treino_id=treino_b.id
                ),
                Exercicio(
                    nome="Crucifixo máquina",
                    categoria_muscular="Peito",
                    instrucoes="1 série preparatória\n2 séries de trabalho (12-15 reps, foco em alongamento)",
                    series_preparacao=1,
                    peso_preparacao=0,
                    series_eficazes=2,
                    repeticoes_eficazes=15,
                    peso_eficazes=0,
                    tempo_descanso=90,
                    treino_id=treino_b.id
                ),
                Exercicio(
                    nome="Paralela na máquina ou Supino Declinado",
                    categoria_muscular="Peito",
                    instrucoes="2 séries de trabalho (8-10 reps)",
                    series_preparacao=0,
                    peso_preparacao=0,
                    series_eficazes=2,
                    repeticoes_eficazes=10,
                    peso_eficazes=0,
                    tempo_descanso=90,
                    treino_id=treino_b.id
                ),
                Exercicio(
                    nome="Rosca Banco Inclinado",
                    categoria_muscular="Bíceps",
                    instrucoes="1 série preparatória\n2 séries de trabalho (10-12 reps, lenta e controlada)",
                    series_preparacao=1,
                    peso_preparacao=0,
                    series_eficazes=2,
                    repeticoes_eficazes=12,
                    peso_eficazes=0,
                    tempo_descanso=90,
                    treino_id=treino_b.id
                ),
                Exercicio(
                    nome="Rosca Scott máquina",
                    categoria_muscular="Bíceps",
                    instrucoes="2 séries de trabalho (12 reps, última com drop-set)",
                    series_preparacao=0,
                    peso_preparacao=0,
                    series_eficazes=2,
                    repeticoes_eficazes=12,
                    peso_eficazes=0,
                    tempo_descanso=90,
                    treino_id=treino_b.id
                )
            ]

            # Treino C - Costas, Ombro, Tríceps
            treino_c = Treino(
                nome="Treino C - Costas, Ombro, Tríceps",
                categoria="Costas",
                status="ativo"
            )
            db.session.add(treino_c)
            db.session.flush()

            exercicios_c = [
                Exercicio(
                    nome="Puxada Supinada",
                    categoria_muscular="Costas",
                    instrucoes="1 série preparatória\n2 séries de trabalho (rest-pause)",
                    series_preparacao=1,
                    peso_preparacao=0,
                    series_eficazes=2,
                    repeticoes_eficazes=10,
                    peso_eficazes=0,
                    tempo_descanso=90,
                    treino_id=treino_c.id
                ),
                Exercicio(
                    nome="Puxada Articulada máquina",
                    categoria_muscular="Costas",
                    instrucoes="2 séries de trabalho (10-12 reps)",
                    series_preparacao=0,
                    peso_preparacao=0,
                    series_eficazes=2,
                    repeticoes_eficazes=12,
                    peso_eficazes=0,
                    tempo_descanso=90,
                    treino_id=treino_c.id
                ),
                Exercicio(
                    nome="Remada Aberta máquina",
                    categoria_muscular="Costas",
                    instrucoes="2 séries de trabalho (12 reps, última com drop-set)",
                    series_preparacao=0,
                    peso_preparacao=0,
                    series_eficazes=2,
                    repeticoes_eficazes=12,
                    peso_eficazes=0,
                    tempo_descanso=90,
                    treino_id=treino_c.id
                ),
                Exercicio(
                    nome="Desenvolvimento Ombro máquina",
                    categoria_muscular="Ombros",
                    instrucoes="1 série preparatória\n2 séries de trabalho (10 reps)",
                    series_preparacao=1,
                    peso_preparacao=0,
                    series_eficazes=2,
                    repeticoes_eficazes=10,
                    peso_eficazes=0,
                    tempo_descanso=90,
                    treino_id=treino_c.id
                ),
                Exercicio(
                    nome="Elevação Lateral",
                    categoria_muscular="Ombros",
                    instrucoes="3 séries (15 reps, últimas 5 reps com técnica de cheating)",
                    series_preparacao=0,
                    peso_preparacao=0,
                    series_eficazes=3,
                    repeticoes_eficazes=15,
                    peso_eficazes=0,
                    tempo_descanso=90,
                    treino_id=treino_c.id
                ),
                Exercicio(
                    nome="Crucifixo Inverso",
                    categoria_muscular="Ombros",
                    instrucoes="1 série preparatória\n1 série de trabalho (máxima falha com isometria final)",
                    series_preparacao=1,
                    peso_preparacao=0,
                    series_eficazes=1,
                    repeticoes_eficazes=12,
                    peso_eficazes=0,
                    tempo_descanso=90,
                    treino_id=treino_c.id
                ),
                Exercicio(
                    nome="Tríceps Francês halter",
                    categoria_muscular="Tríceps",
                    instrucoes="2 séries de trabalho (10 reps)",
                    series_preparacao=0,
                    peso_preparacao=0,
                    series_eficazes=2,
                    repeticoes_eficazes=10,
                    peso_eficazes=0,
                    tempo_descanso=90,
                    treino_id=treino_c.id
                ),
                Exercicio(
                    nome="Testa polia",
                    categoria_muscular="Tríceps",
                    instrucoes="1-2 séries de trabalho (12 reps)",
                    series_preparacao=0,
                    peso_preparacao=0,
                    series_eficazes=2,
                    repeticoes_eficazes=12,
                    peso_eficazes=0,
                    tempo_descanso=90,
                    treino_id=treino_c.id
                ),
                Exercicio(
                    nome="Pulley",
                    categoria_muscular="Tríceps",
                    instrucoes="1 série de trabalho (máxima falha)",
                    series_preparacao=0,
                    peso_preparacao=0,
                    series_eficazes=1,
                    repeticoes_eficazes=12,
                    peso_eficazes=0,
                    tempo_descanso=90,
                    treino_id=treino_c.id
                )
            ]

            # Treino D - Pernas (ênfase posterior e glúteo)
            treino_d = Treino(
                nome="Treino D - Pernas (ênfase posterior e glúteo)",
                categoria="Pernas",
                status="ativo"
            )
            db.session.add(treino_d)
            db.session.flush()

            exercicios_d = [
                Exercicio(
                    nome="Stiff",
                    categoria_muscular="Pernas",
                    instrucoes="2 séries preparatórias\n2 séries de trabalho (10-12 reps, foco no alongamento)",
                    series_preparacao=2,
                    peso_preparacao=0,
                    series_eficazes=2,
                    repeticoes_eficazes=12,
                    peso_eficazes=0,
                    tempo_descanso=90,
                    treino_id=treino_d.id
                ),
                Exercicio(
                    nome="Cadeira Flexora",
                    categoria_muscular="Pernas",
                    instrucoes="2 séries de trabalho (12-15 reps)",
                    series_preparacao=0,
                    peso_preparacao=0,
                    series_eficazes=2,
                    repeticoes_eficazes=15,
                    peso_eficazes=0,
                    tempo_descanso=90,
                    treino_id=treino_d.id
                ),
                Exercicio(
                    nome="Agachamento Smith",
                    categoria_muscular="Pernas",
                    instrucoes="1 série preparatória\n1 série de trabalho (6-8 reps pesada)\n1 série moderada (10 reps)",
                    series_preparacao=1,
                    peso_preparacao=0,
                    series_eficazes=2,
                    repeticoes_eficazes=10,
                    peso_eficazes=0,
                    tempo_descanso=90,
                    treino_id=treino_d.id
                ),
                Exercicio(
                    nome="Cadeira Abdutora",
                    categoria_muscular="Pernas",
                    instrucoes="2 séries de trabalho (15 reps)",
                    series_preparacao=0,
                    peso_preparacao=0,
                    series_eficazes=2,
                    repeticoes_eficazes=15,
                    peso_eficazes=0,
                    tempo_descanso=90,
                    treino_id=treino_d.id
                ),
                Exercicio(
                    nome="Búlgaro",
                    categoria_muscular="Pernas",
                    instrucoes="2 séries de trabalho (10 reps cada perna)",
                    series_preparacao=0,
                    peso_preparacao=0,
                    series_eficazes=2,
                    repeticoes_eficazes=10,
                    peso_eficazes=0,
                    tempo_descanso=90,
                    treino_id=treino_d.id
                )
            ]

            # Treino E - Superiores Completo
            treino_e = Treino(
                nome="Treino E - Superiores Completo",
                categoria="Superiores",
                status="ativo"
            )
            db.session.add(treino_e)
            db.session.flush()

            exercicios_e = [
                Exercicio(
                    nome="Puxada Supinada",
                    categoria_muscular="Costas",
                    instrucoes="2 séries",
                    series_preparacao=0,
                    peso_preparacao=0,
                    series_eficazes=2,
                    repeticoes_eficazes=12,
                    peso_eficazes=0,
                    tempo_descanso=60,
                    treino_id=treino_e.id
                ),
                Exercicio(
                    nome="Supino Inclinado Máquina",
                    categoria_muscular="Peito",
                    instrucoes="2 séries",
                    series_preparacao=0,
                    peso_preparacao=0,
                    series_eficazes=2,
                    repeticoes_eficazes=12,
                    peso_eficazes=0,
                    tempo_descanso=60,
                    treino_id=treino_e.id
                ),
                Exercicio(
                    nome="Rosca Scott máquina",
                    categoria_muscular="Bíceps",
                    instrucoes="2 séries",
                    series_preparacao=0,
                    peso_preparacao=0,
                    series_eficazes=2,
                    repeticoes_eficazes=12,
                    peso_eficazes=0,
                    tempo_descanso=60,
                    treino_id=treino_e.id
                ),
                Exercicio(
                    nome="Desenvolvimento Ombro",
                    categoria_muscular="Ombros",
                    instrucoes="2 séries",
                    series_preparacao=0,
                    peso_preparacao=0,
                    series_eficazes=2,
                    repeticoes_eficazes=12,
                    peso_eficazes=0,
                    tempo_descanso=60,
                    treino_id=treino_e.id
                ),
                Exercicio(
                    nome="Tríceps Pulley",
                    categoria_muscular="Tríceps",
                    instrucoes="2 séries",
                    series_preparacao=0,
                    peso_preparacao=0,
                    series_eficazes=2,
                    repeticoes_eficazes=12,
                    peso_eficazes=0,
                    tempo_descanso=60,
                    treino_id=treino_e.id
                ),
                Exercicio(
                    nome="Crucifixo Máquina",
                    categoria_muscular="Peito",
                    instrucoes="2 séries",
                    series_preparacao=0,
                    peso_preparacao=0,
                    series_eficazes=2,
                    repeticoes_eficazes=12,
                    peso_eficazes=0,
                    tempo_descanso=60,
                    treino_id=treino_e.id
                ),
                Exercicio(
                    nome="Elevação Lateral",
                    categoria_muscular="Ombros",
                    instrucoes="2 séries",
                    series_preparacao=0,
                    peso_preparacao=0,
                    series_eficazes=2,
                    repeticoes_eficazes=12,
                    peso_eficazes=0,
                    tempo_descanso=60,
                    treino_id=treino_e.id
                )
            ]

            # Adicionar todos os exercícios
            for exercicio in exercicios_a + exercicios_b + exercicios_c + exercicios_d + exercicios_e:
                db.session.add(exercicio)

            # Commit das alterações
            db.session.commit()
            print("Treinos adicionados com sucesso!")
            
        except Exception as e:
            print(f"Erro ao adicionar treinos: {str(e)}")
            db.session.rollback()

if __name__ == "__main__":
    # Verifica se está usando PostgreSQL
    if os.getenv('DATABASE_URL', '').startswith('postgresql://'):
        print("Conectando ao banco de dados PostgreSQL...")
    else:
        print("Conectando ao banco de dados SQLite local...")
    
    adicionar_treinos() 