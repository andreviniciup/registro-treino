from app import app, db, Treino, Exercicio
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

def adicionar_treinos():
    with app.app_context():
        try:
            print("Conectando ao banco de dados...")
            
            # Limpa os treinos existentes
            print("Removendo treinos antigos...")
            Exercicio.query.delete()
            Treino.query.delete()
            db.session.commit()
            print("Treinos antigos removidos com sucesso!")

            # Treino A - Peito e Tríceps
            print("Adicionando Treino A...")
            treino_a = Treino(
                nome="Treino A - Peito e Tríceps",
                categoria="Superior",
                status="ativo"
            )
            db.session.add(treino_a)
            db.session.flush()

            exercicios_a = [
                Exercicio(
                    nome="Supino Reto",
                    categoria_muscular="Peito",
                    series_preparacao=2,
                    peso_preparacao=20,
                    series_eficazes=3,
                    repeticoes_eficazes=12,
                    peso_eficazes=30,
                    tempo_descanso=90,
                    instrucoes="Foco em amplitude completa e controle do movimento",
                    treino_id=treino_a.id
                ),
                Exercicio(
                    nome="Supino Inclinado",
                    categoria_muscular="Peito",
                    series_preparacao=2,
                    peso_preparacao=15,
                    series_eficazes=3,
                    repeticoes_eficazes=12,
                    peso_eficazes=25,
                    tempo_descanso=90,
                    instrucoes="Ênfase na parte superior do peito",
                    treino_id=treino_a.id
                ),
                Exercicio(
                    nome="Crossover",
                    categoria_muscular="Peito",
                    series_preparacao=2,
                    peso_preparacao=10,
                    series_eficazes=3,
                    repeticoes_eficazes=15,
                    peso_eficazes=15,
                    tempo_descanso=60,
                    instrucoes="Movimento controlado e constante",
                    treino_id=treino_a.id
                ),
                Exercicio(
                    nome="Tríceps Pulley",
                    categoria_muscular="Tríceps",
                    series_preparacao=2,
                    peso_preparacao=15,
                    series_eficazes=3,
                    repeticoes_eficazes=15,
                    peso_eficazes=20,
                    tempo_descanso=60,
                    instrucoes="Cotovelos fixos, movimento apenas do antebraço",
                    treino_id=treino_a.id
                ),
                Exercicio(
                    nome="Tríceps Francês",
                    categoria_muscular="Tríceps",
                    series_preparacao=2,
                    peso_preparacao=10,
                    series_eficazes=3,
                    repeticoes_eficazes=12,
                    peso_eficazes=15,
                    tempo_descanso=60,
                    instrucoes="Manter os cotovelos próximos à cabeça",
                    treino_id=treino_a.id
                )
            ]
            db.session.add_all(exercicios_a)

            # Treino B - Costas e Bíceps
            print("Adicionando Treino B...")
            treino_b = Treino(
                nome="Treino B - Costas e Bíceps",
                categoria="Superior",
                status="ativo"
            )
            db.session.add(treino_b)
            db.session.flush()

            exercicios_b = [
                Exercicio(
                    nome="Puxada Frontal",
                    categoria_muscular="Costas",
                    series_preparacao=2,
                    peso_preparacao=30,
                    series_eficazes=3,
                    repeticoes_eficazes=12,
                    peso_eficazes=45,
                    tempo_descanso=90,
                    instrucoes="Puxar a barra até o peito, mantendo as costas retas",
                    treino_id=treino_b.id
                ),
                Exercicio(
                    nome="Remada Baixa",
                    categoria_muscular="Costas",
                    series_preparacao=2,
                    peso_preparacao=25,
                    series_eficazes=3,
                    repeticoes_eficazes=12,
                    peso_eficazes=40,
                    tempo_descanso=90,
                    instrucoes="Puxar o peso até a cintura, mantendo as costas retas",
                    treino_id=treino_b.id
                ),
                Exercicio(
                    nome="Rosca Direta",
                    categoria_muscular="Bíceps",
                    series_preparacao=2,
                    peso_preparacao=10,
                    series_eficazes=3,
                    repeticoes_eficazes=12,
                    peso_eficazes=15,
                    tempo_descanso=60,
                    instrucoes="Manter os cotovelos fixos, movimento controlado",
                    treino_id=treino_b.id
                ),
                Exercicio(
                    nome="Rosca Martelo",
                    categoria_muscular="Bíceps",
                    series_preparacao=2,
                    peso_preparacao=8,
                    series_eficazes=3,
                    repeticoes_eficazes=12,
                    peso_eficazes=12,
                    tempo_descanso=60,
                    instrucoes="Manter os pulsos neutros durante todo o movimento",
                    treino_id=treino_b.id
                )
            ]
            db.session.add_all(exercicios_b)

            # Treino C - Pernas
            print("Adicionando Treino C...")
            treino_c = Treino(
                nome="Treino C - Pernas",
                categoria="Inferior",
                status="ativo"
            )
            db.session.add(treino_c)
            db.session.flush()

            exercicios_c = [
                Exercicio(
                    nome="Leg Press",
                    categoria_muscular="Quadríceps",
                    series_preparacao=2,
                    peso_preparacao=40,
                    series_eficazes=3,
                    repeticoes_eficazes=12,
                    peso_eficazes=60,
                    tempo_descanso=120,
                    instrucoes="Ajustar o banco para manter os joelhos alinhados com os pés",
                    treino_id=treino_c.id
                ),
                Exercicio(
                    nome="Cadeira Extensora",
                    categoria_muscular="Quadríceps",
                    series_preparacao=2,
                    peso_preparacao=20,
                    series_eficazes=3,
                    repeticoes_eficazes=15,
                    peso_eficazes=30,
                    tempo_descanso=90,
                    instrucoes="Movimento completo, focando na contração máxima",
                    treino_id=treino_c.id
                ),
                Exercicio(
                    nome="Cadeira Flexora",
                    categoria_muscular="Posterior",
                    series_preparacao=2,
                    peso_preparacao=20,
                    series_eficazes=3,
                    repeticoes_eficazes=15,
                    peso_eficazes=30,
                    tempo_descanso=90,
                    instrucoes="Manter o quadril apoiado no banco",
                    treino_id=treino_c.id
                ),
                Exercicio(
                    nome="Elevação Pélvica",
                    categoria_muscular="Glúteos",
                    series_preparacao=2,
                    peso_preparacao=0,
                    series_eficazes=3,
                    repeticoes_eficazes=15,
                    peso_eficazes=0,
                    tempo_descanso=60,
                    instrucoes="Elevar o quadril até a altura dos ombros",
                    treino_id=treino_c.id
                )
            ]
            db.session.add_all(exercicios_c)

            # Treino D - Ombros e Trapézio
            print("Adicionando Treino D...")
            treino_d = Treino(
                nome="Treino D - Ombros e Trapézio",
                categoria="Superior",
                status="ativo"
            )
            db.session.add(treino_d)
            db.session.flush()

            exercicios_d = [
                Exercicio(
                    nome="Desenvolvimento com Halteres",
                    categoria_muscular="Ombros",
                    series_preparacao=2,
                    peso_preparacao=8,
                    series_eficazes=3,
                    repeticoes_eficazes=12,
                    peso_eficazes=12,
                    tempo_descanso=90,
                    instrucoes="Manter os cotovelos ligeiramente à frente do corpo",
                    treino_id=treino_d.id
                ),
                Exercicio(
                    nome="Elevação Lateral",
                    categoria_muscular="Ombros",
                    series_preparacao=2,
                    peso_preparacao=5,
                    series_eficazes=3,
                    repeticoes_eficazes=15,
                    peso_eficazes=8,
                    tempo_descanso=60,
                    instrucoes="Elevar os braços até a altura dos ombros",
                    treino_id=treino_d.id
                ),
                Exercicio(
                    nome="Encolhimento com Halteres",
                    categoria_muscular="Trapézio",
                    series_preparacao=2,
                    peso_preparacao=12,
                    series_eficazes=3,
                    repeticoes_eficazes=12,
                    peso_eficazes=18,
                    tempo_descanso=60,
                    instrucoes="Elevar os ombros mantendo os braços estendidos",
                    treino_id=treino_d.id
                )
            ]
            db.session.add_all(exercicios_d)

            # Treino E - Abdômen e Core
            print("Adicionando Treino E...")
            treino_e = Treino(
                nome="Treino E - Abdômen e Core",
                categoria="Core",
                status="ativo"
            )
            db.session.add(treino_e)
            db.session.flush()

            exercicios_e = [
                Exercicio(
                    nome="Abdominal Reto",
                    categoria_muscular="Abdômen",
                    series_preparacao=0,
                    peso_preparacao=0,
                    series_eficazes=3,
                    repeticoes_eficazes=20,
                    peso_eficazes=0,
                    tempo_descanso=45,
                    instrucoes="Manter a lombar apoiada no chão",
                    treino_id=treino_e.id
                ),
                Exercicio(
                    nome="Prancha",
                    categoria_muscular="Core",
                    series_preparacao=0,
                    peso_preparacao=0,
                    series_eficazes=3,
                    repeticoes_eficazes=1,
                    peso_eficazes=0,
                    tempo_descanso=60,
                    instrucoes="Manter o corpo alinhado, segurar por 30 segundos",
                    treino_id=treino_e.id
                ),
                Exercicio(
                    nome="Abdominal Oblíquo",
                    categoria_muscular="Abdômen",
                    series_preparacao=0,
                    peso_preparacao=0,
                    series_eficazes=3,
                    repeticoes_eficazes=15,
                    peso_eficazes=0,
                    tempo_descanso=45,
                    instrucoes="Alternar os lados, mantendo o controle",
                    treino_id=treino_e.id
                )
            ]
            db.session.add_all(exercicios_e)

            # Commit das alterações
            db.session.commit()
            print("Treinos adicionados com sucesso!")

        except Exception as e:
            db.session.rollback()
            print(f"Erro ao adicionar treinos: {str(e)}")
            raise

if __name__ == "__main__":
    adicionar_treinos() 