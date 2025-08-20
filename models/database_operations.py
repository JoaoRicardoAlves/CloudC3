"""
Operações de banco de dados sem ORM - Queries SQL manuais
"""
import psycopg2
from config.database import DatabaseConfig
from tabulate import tabulate

class DatabaseOperations:
    def __init__(self):
        self.db_config = DatabaseConfig()
    
    def get_table_counts(self):
        """
        Conta registros em todas as tabelas para o splash screen
        """
        conn = self.db_config.get_connection()
        if not conn:
            return {}
        
        counts = {}
        tables = ['autores', 'livros', 'pedidos', 'itens_pedido']
        
        try:
            cursor = conn.cursor()
            for table in tables:
                query = f"SELECT COUNT(1) as total_{table} FROM {table}"
                cursor.execute(query)
                result = cursor.fetchone()
                counts[table] = result[0] if result else 0
            
            cursor.close()
            conn.close()
            return counts
        except psycopg2.Error as e:
            print(f"Erro ao contar registros: {e}")
            conn.close()
            return {}
    
    # ==================== RELATÓRIOS ====================
    
    def relatorio_vendas_por_genero(self):
        """
        Relatório com GROUP BY - Vendas por gênero
        """
        conn = self.db_config.get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            query = """
                SELECT 
                    l.genero,
                    COUNT(ip.id_item) as total_vendas,
                    SUM(ip.quantidade) as quantidade_vendida,
                    SUM(ip.subtotal) as valor_total_vendas
                FROM livros l
                INNER JOIN itens_pedido ip ON l.id_livro = ip.id_livro
                GROUP BY l.genero
                ORDER BY valor_total_vendas DESC
            """
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return results
        except psycopg2.Error as e:
            print(f"Erro no relatório por gênero: {e}")
            conn.close()
            return []
    
    def relatorio_pedidos_detalhado(self):
        """
        Relatório com JOIN - Pedidos com detalhes dos livros
        """
        conn = self.db_config.get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            query = """
                SELECT 
                    p.id_pedido,
                    p.data_pedido,
                    p.nome_cliente,
                    l.titulo,
                    a.nome_autor,
                    ip.quantidade,
                    ip.preco_unitario,
                    ip.subtotal
                FROM pedidos p
                INNER JOIN itens_pedido ip ON p.id_pedido = ip.id_pedido
                INNER JOIN livros l ON ip.id_livro = l.id_livro
                INNER JOIN autores a ON l.id_autor = a.id_autor
                ORDER BY p.data_pedido DESC, p.id_pedido
            """
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return results
        except psycopg2.Error as e:
            print(f"Erro no relatório detalhado: {e}")
            conn.close()
            return []
    
    # ==================== INSERIR REGISTROS ====================
    
    def inserir_autor(self, nome, nacionalidade, data_nascimento, biografia):
        """
        Insere um novo autor
        """
        conn = self.db_config.get_connection()
        if not conn:
            return False, "Erro de conexão"
        
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO autores (nome_autor, nacionalidade, data_nascimento, biografia)
                VALUES (%s, %s, %s, %s)
                RETURNING id_autor
            """
            cursor.execute(query, (nome, nacionalidade, data_nascimento, biografia))
            autor_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            conn.close()
            return True, f"Autor inserido com sucesso! ID: {autor_id}"
        except psycopg2.Error as e:
            conn.rollback()
            conn.close()
            return False, f"Erro ao inserir autor: {e}"
    
    def inserir_livro(self, titulo, id_autor, genero, ano_publicacao, preco, quantidade_estoque):
        """
        Insere um novo livro
        """
        conn = self.db_config.get_connection()
        if not conn:
            return False, "Erro de conexão"
        
        try:
            cursor = conn.cursor()
            # Verifica se o autor existe
            cursor.execute("SELECT id_autor FROM autores WHERE id_autor = %s", (id_autor,))
            if not cursor.fetchone():
                cursor.close()
                conn.close()
                return False, "Autor não encontrado"
            
            query = """
                INSERT INTO livros (titulo, id_autor, genero, ano_publicacao, preco, quantidade_estoque)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id_livro
            """
            cursor.execute(query, (titulo, id_autor, genero, ano_publicacao, preco, quantidade_estoque))
            livro_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            conn.close()
            return True, f"Livro inserido com sucesso! ID: {livro_id}"
        except psycopg2.Error as e:
            conn.rollback()
            conn.close()
            return False, f"Erro ao inserir livro: {e}"
    
    def inserir_pedido(self, nome_cliente, email_cliente):
        """
        Insere um novo pedido
        """
        conn = self.db_config.get_connection()
        if not conn:
            return False, "Erro de conexão"
        
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO pedidos (nome_cliente, email_cliente, valor_total)
                VALUES (%s, %s, 0.00)
                RETURNING id_pedido
            """
            cursor.execute(query, (nome_cliente, email_cliente))
            pedido_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            conn.close()
            return True, f"Pedido inserido com sucesso! ID: {pedido_id}"
        except psycopg2.Error as e:
            conn.rollback()
            conn.close()
            return False, f"Erro ao inserir pedido: {e}"
    
    # ==================== LISTAR REGISTROS ====================
    
    def listar_autores(self):
        """
        Lista todos os autores
        """
        conn = self.db_config.get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            query = "SELECT id_autor, nome_autor, nacionalidade, data_nascimento FROM autores ORDER BY nome_autor"
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return results
        except psycopg2.Error as e:
            print(f"Erro ao listar autores: {e}")
            conn.close()
            return []
    
    def listar_livros(self):
        """
        Lista todos os livros com nome do autor
        """
        conn = self.db_config.get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            query = """
                SELECT l.id_livro, l.titulo, a.nome_autor, l.genero, l.preco, l.quantidade_estoque
                FROM livros l
                INNER JOIN autores a ON l.id_autor = a.id_autor
                ORDER BY l.titulo
            """
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return results
        except psycopg2.Error as e:
            print(f"Erro ao listar livros: {e}")
            conn.close()
            return []
    
    def listar_pedidos(self):
        """
        Lista todos os pedidos
        """
        conn = self.db_config.get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            query = "SELECT id_pedido, data_pedido, nome_cliente, email_cliente, valor_total FROM pedidos ORDER BY data_pedido DESC"
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return results
        except psycopg2.Error as e:
            print(f"Erro ao listar pedidos: {e}")
            conn.close()
            return []
    
    # ==================== REMOVER REGISTROS ====================
    
    def remover_autor(self, id_autor):
        """
        Remove um autor (verifica dependências)
        """
        conn = self.db_config.get_connection()
        if not conn:
            return False, "Erro de conexão"
        
        try:
            cursor = conn.cursor()
            
            # Verifica se há livros deste autor
            cursor.execute("SELECT COUNT(*) FROM livros WHERE id_autor = %s", (id_autor,))
            count = cursor.fetchone()[0]
            
            if count > 0:
                cursor.close()
                conn.close()
                return False, f"Não é possível remover. Autor possui {count} livro(s) cadastrado(s)."
            
            # Remove o autor
            cursor.execute("DELETE FROM autores WHERE id_autor = %s", (id_autor,))
            if cursor.rowcount == 0:
                cursor.close()
                conn.close()
                return False, "Autor não encontrado"
            
            conn.commit()
            cursor.close()
            conn.close()
            return True, "Autor removido com sucesso"
        except psycopg2.Error as e:
            conn.rollback()
            conn.close()
            return False, f"Erro ao remover autor: {e}"
    
    def remover_livro(self, id_livro):
        """
        Remove um livro (verifica dependências)
        """
        conn = self.db_config.get_connection()
        if not conn:
            return False, "Erro de conexão"
        
        try:
            cursor = conn.cursor()
            
            # Verifica se há itens de pedido deste livro
            cursor.execute("SELECT COUNT(*) FROM itens_pedido WHERE id_livro = %s", (id_livro,))
            count = cursor.fetchone()[0]
            
            if count > 0:
                cursor.close()
                conn.close()
                return False, f"Não é possível remover. Livro possui {count} item(ns) em pedidos."
            
            # Remove o livro
            cursor.execute("DELETE FROM livros WHERE id_livro = %s", (id_livro,))
            if cursor.rowcount == 0:
                cursor.close()
                conn.close()
                return False, "Livro não encontrado"
            
            conn.commit()
            cursor.close()
            conn.close()
            return True, "Livro removido com sucesso"
        except psycopg2.Error as e:
            conn.rollback()
            conn.close()
            return False, f"Erro ao remover livro: {e}"
    
    def remover_pedido(self, id_pedido):
        """
        Remove um pedido (CASCADE remove itens automaticamente)
        """
        conn = self.db_config.get_connection()
        if not conn:
            return False, "Erro de conexão"
        
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pedidos WHERE id_pedido = %s", (id_pedido,))
            if cursor.rowcount == 0:
                cursor.close()
                conn.close()
                return False, "Pedido não encontrado"
            
            conn.commit()
            cursor.close()
            conn.close()
            return True, "Pedido removido com sucesso"
        except psycopg2.Error as e:
            conn.rollback()
            conn.close()
            return False, f"Erro ao remover pedido: {e}"
    
    # ==================== ATUALIZAR REGISTROS ====================
    
    def atualizar_autor(self, id_autor, nome, nacionalidade, data_nascimento, biografia):
        """
        Atualiza um autor
        """
        conn = self.db_config.get_connection()
        if not conn:
            return False, "Erro de conexão"
        
        try:
            cursor = conn.cursor()
            query = """
                UPDATE autores 
                SET nome_autor = %s, nacionalidade = %s, data_nascimento = %s, biografia = %s
                WHERE id_autor = %s
            """
            cursor.execute(query, (nome, nacionalidade, data_nascimento, biografia, id_autor))
            
            if cursor.rowcount == 0:
                cursor.close()
                conn.close()
                return False, "Autor não encontrado"
            
            conn.commit()
            cursor.close()
            conn.close()
            return True, "Autor atualizado com sucesso"
        except psycopg2.Error as e:
            conn.rollback()
            conn.close()
            return False, f"Erro ao atualizar autor: {e}"
    
    def atualizar_livro(self, id_livro, titulo, id_autor, genero, ano_publicacao, preco, quantidade_estoque):
        """
        Atualiza um livro
        """
        conn = self.db_config.get_connection()
        if not conn:
            return False, "Erro de conexão"
        
        try:
            cursor = conn.cursor()
            
            # Verifica se o autor existe
            cursor.execute("SELECT id_autor FROM autores WHERE id_autor = %s", (id_autor,))
            if not cursor.fetchone():
                cursor.close()
                conn.close()
                return False, "Autor não encontrado"
            
            query = """
                UPDATE livros 
                SET titulo = %s, id_autor = %s, genero = %s, ano_publicacao = %s, preco = %s, quantidade_estoque = %s
                WHERE id_livro = %s
            """
            cursor.execute(query, (titulo, id_autor, genero, ano_publicacao, preco, quantidade_estoque, id_livro))
            
            if cursor.rowcount == 0:
                cursor.close()
                conn.close()
                return False, "Livro não encontrado"
            
            conn.commit()
            cursor.close()
            conn.close()
            return True, "Livro atualizado com sucesso"
        except psycopg2.Error as e:
            conn.rollback()
            conn.close()
            return False, f"Erro ao atualizar livro: {e}"
    
    def atualizar_pedido(self, id_pedido, nome_cliente, email_cliente):
        """
        Atualiza um pedido
        """
        conn = self.db_config.get_connection()
        if not conn:
            return False, "Erro de conexão"
        
        try:
            cursor = conn.cursor()
            query = """
                UPDATE pedidos 
                SET nome_cliente = %s, email_cliente = %s
                WHERE id_pedido = %s
            """
            cursor.execute(query, (nome_cliente, email_cliente, id_pedido))
            
            if cursor.rowcount == 0:
                cursor.close()
                conn.close()
                return False, "Pedido não encontrado"
            
            conn.commit()
            cursor.close()
            conn.close()
            return True, "Pedido atualizado com sucesso"
        except psycopg2.Error as e:
            conn.rollback()
            conn.close()
            return False, f"Erro ao atualizar pedido: {e}"
    
    def obter_autor_por_id(self, id_autor):
        """
        Obtém dados de um autor específico
        """
        conn = self.db_config.get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            query = "SELECT id_autor, nome_autor, nacionalidade, data_nascimento, biografia FROM autores WHERE id_autor = %s"
            cursor.execute(query, (id_autor,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result
        except psycopg2.Error as e:
            print(f"Erro ao obter autor: {e}")
            conn.close()
            return None
    
    def obter_livro_por_id(self, id_livro):
        """
        Obtém dados de um livro específico
        """
        conn = self.db_config.get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            query = """
                SELECT l.id_livro, l.titulo, l.id_autor, a.nome_autor, l.genero, l.ano_publicacao, l.preco, l.quantidade_estoque
                FROM livros l
                INNER JOIN autores a ON l.id_autor = a.id_autor
                WHERE l.id_livro = %s
            """
            cursor.execute(query, (id_livro,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result
        except psycopg2.Error as e:
            print(f"Erro ao obter livro: {e}")
            conn.close()
            return None
    
    def obter_pedido_por_id(self, id_pedido):
        """
        Obtém dados de um pedido específico
        """
        conn = self.db_config.get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            query = "SELECT id_pedido, data_pedido, nome_cliente, email_cliente, valor_total FROM pedidos WHERE id_pedido = %s"
            cursor.execute(query, (id_pedido,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result
        except psycopg2.Error as e:
            print(f"Erro ao obter pedido: {e}")
            conn.close()
            return None