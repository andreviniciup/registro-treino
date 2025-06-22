from app import app, db
from sqlalchemy import text

def migrate_database():
    with app.app_context():
        try:
            # Verificar se a coluna usuario_id existe na tabela treino
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'treino' AND column_name = 'usuario_id'
            """))
            
            if not result.fetchone():
                print("Adicionando coluna usuario_id à tabela treino...")
                db.session.execute(text("ALTER TABLE treino ADD COLUMN usuario_id INTEGER"))
                
                # Criar um usuário padrão para os treinos existentes
                print("Criando usuário padrão...")
                db.session.execute(text("""
                    INSERT INTO usuario (nome, email, senha_hash, data_cadastro) 
                    VALUES ('Usuário Padrão', 'default@example.com', 'default_hash', NOW())
                    ON CONFLICT (email) DO NOTHING
                """))
                
                # Pegar o ID do usuário padrão
                result = db.session.execute(text("SELECT id FROM usuario WHERE email = 'default@example.com'"))
                user_id = result.fetchone()[0]
                
                # Atualizar todos os treinos existentes para usar o usuário padrão
                print("Atualizando treinos existentes...")
                db.session.execute(text(f"UPDATE treino SET usuario_id = {user_id} WHERE usuario_id IS NULL"))
                
                print("Migração concluída com sucesso!")
            else:
                print("Coluna usuario_id já existe na tabela treino.")
            
            # Verificar se a tabela usuario existe
            result = db.session.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_name = 'usuario'
            """))
            
            if not result.fetchone():
                print("Criando tabela usuario...")
                db.create_all()
                print("Tabela usuario criada com sucesso!")
            
            # Verificar se a tabela meta existe
            result = db.session.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_name = 'meta'
            """))
            
            if not result.fetchone():
                print("Criando tabelas de metas e desafios...")
                db.create_all()
                print("Tabelas criadas com sucesso!")
            
            db.session.commit()
            print("Migração finalizada!")
            
        except Exception as e:
            db.session.rollback()
            print(f"Erro durante a migração: {str(e)}")
            raise

if __name__ == '__main__':
    migrate_database() 