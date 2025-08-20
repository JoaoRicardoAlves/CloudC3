"""
Configuração de conexão com o banco de dados PostgreSQL
"""
import psycopg2
from psycopg2 import sql
import os

class DatabaseConfig:
    def __init__(self):
        # Configurações do banco de dados
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = os.getenv('DB_PORT', '5432')
        self.database = os.getenv('DB_NAME', 'mydatabase')
        self.user = os.getenv('DB_USER', 'user')
        self.password = os.getenv('DB_PASSWORD', 'password')
    
    def get_connection(self):
        """
        Estabelece e retorna uma conexão com o banco de dados
        """
        try:
            connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return connection
        except psycopg2.Error as e:
            print(f"Erro ao conectar com o banco de dados: {e}")
            return None
    
    def test_connection(self):
        """
        Testa a conexão com o banco de dados
        """
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT version();")
                version = cursor.fetchone()
                cursor.close()
                conn.close()
                return True, f"Conexão bem-sucedida! PostgreSQL: {version[0]}"
            except psycopg2.Error as e:
                return False, f"Erro na consulta: {e}"
        else:
            return False, "Não foi possível estabelecer conexão"
    
    def execute_script(self, script_path):
        """
        Executa um script SQL
        """
        conn = self.get_connection()
        if not conn:
            return False, "Erro de conexão"
        
        try:
            cursor = conn.cursor()
            with open(script_path, 'r', encoding='utf-8') as file:
                script = file.read()
            
            cursor.execute(script)
            conn.commit()
            cursor.close()
            conn.close()
            return True, "Script executado com sucesso"
        except Exception as e:
            conn.rollback()
            conn.close()
            return False, f"Erro ao executar script: {e}"