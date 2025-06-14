# meu_projeto_completo/app/app.py

import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
# Chave secreta para usar 'flash messages' (mensagens de feedback para o usuário)
app.secret_key = os.urandom(24)

# --- CONFIGURAÇÃO DO BANCO DE DADOS ---
def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    db_url = os.environ.get("DATABASE_URL")
    conn = psycopg2.connect(db_url)
    return conn

def init_db():
    """Inicializa as tabelas do banco de dados se não existirem."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Tabela de Livros
    cur.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            title VARCHAR(150) NOT NULL,
            author VARCHAR(100) NOT NULL,
            total_copies INTEGER NOT NULL,
            available_copies INTEGER NOT NULL
        );
    ''')
    
    # Tabela de Empréstimos
    cur.execute('''
        CREATE TABLE IF NOT EXISTS loans (
            id SERIAL PRIMARY KEY,
            book_id INTEGER NOT NULL,
            borrower_name VARCHAR(100) NOT NULL,
            checkout_date DATE NOT NULL DEFAULT CURRENT_DATE,
            FOREIGN KEY (book_id) REFERENCES books (id) ON DELETE CASCADE
        );
    ''')
    
    conn.commit()
    cur.close()
    conn.close()

# --- ROTAS DA APLICAÇÃO ---

@app.route('/')
def index():
    """Página principal que lista livros e empréstimos."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Busca todos os livros
    cur.execute('SELECT * FROM books ORDER BY title;')
    books = cur.fetchall()
    
    # Busca todos os empréstimos ativos com o nome do livro (usando JOIN)
    cur.execute('''
        SELECT loans.id, books.title, loans.borrower_name, loans.checkout_date 
        FROM loans 
        JOIN books ON loans.book_id = books.id
        ORDER BY loans.checkout_date;
    ''')
    loans = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template('index.html', books=books, loans=loans)

@app.route('/book/add', methods=['POST'])
def add_book():
    """Adiciona um novo livro ao banco de dados."""
    title = request.form['title']
    author = request.form['author']
    copies = int(request.form['copies'])

    if title and author and copies > 0:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO books (title, author, total_copies, available_copies) VALUES (%s, %s, %s, %s)',
            (title, author, copies, copies)
        )
        conn.commit()
        cur.close()
        conn.close()
        flash('Livro adicionado com sucesso!', 'success')
    else:
        flash('Erro ao adicionar livro. Verifique os dados.', 'danger')

    return redirect(url_for('index'))

@app.route('/book/checkout/<int:book_id>', methods=['POST'])
def checkout_book(book_id):
    """Empresta um livro, diminuindo cópias disponíveis e criando um registro de empréstimo."""
    borrower_name = request.form['borrower_name']

    if not borrower_name:
        flash('O nome do leitor é obrigatório.', 'danger')
        return redirect(url_for('index'))

    conn = get_db_connection()
    cur = conn.cursor()

    # Transação: Garante que ambas as operações (update e insert) funcionem ou nenhuma delas.
    try:
        # 1. Verifica se há cópias disponíveis
        cur.execute('SELECT available_copies FROM books WHERE id = %s;', (book_id,))
        book = cur.fetchone()
        if book and book[0] > 0:
            # 2. Diminui o número de cópias disponíveis
            cur.execute('UPDATE books SET available_copies = available_copies - 1 WHERE id = %s;', (book_id,))
            # 3. Adiciona o registro na tabela de empréstimos
            cur.execute('INSERT INTO loans (book_id, borrower_name) VALUES (%s, %s);', (book_id, borrower_name))
            conn.commit()
            flash(f'Livro emprestado para {borrower_name}!', 'success')
        else:
            flash('Nenhuma cópia deste livro está disponível para empréstimo.', 'warning')
    except Exception as e:
        conn.rollback() # Desfaz a transação em caso de erro
        flash(f'Ocorreu um erro: {e}', 'danger')
    finally:
        cur.close()
        conn.close()

    return redirect(url_for('index'))

@app.route('/loan/return/<int:loan_id>', methods=['POST'])
def return_book(loan_id):
    """Devolve um livro, aumentando cópias disponíveis e removendo o registro de empréstimo."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # 1. Pega o book_id antes de deletar o empréstimo
        cur.execute('SELECT book_id FROM loans WHERE id = %s;', (loan_id,))
        loan = cur.fetchone()
        if loan:
            book_id = loan[0]
            # 2. Aumenta o número de cópias disponíveis
            cur.execute('UPDATE books SET available_copies = available_copies + 1 WHERE id = %s;', (book_id,))
            # 3. Remove o registro da tabela de empréstimos
            cur.execute('DELETE FROM loans WHERE id = %s;', (loan_id,))
            conn.commit()
            flash('Livro devolvido com sucesso!', 'success')
        else:
            flash('Empréstimo não encontrado.', 'danger')
    except Exception as e:
        conn.rollback()
        flash(f'Ocorreu um erro: {e}', 'danger')
    finally:
        cur.close()
        conn.close()
        
    return redirect(url_for('index'))

@app.route('/book/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    """Exclui um livro do banco de dados."""
    conn = get_db_connection()
    cur = conn.cursor()
    # Verifica se o livro tem empréstimos ativos
    cur.execute('SELECT COUNT(*) FROM loans WHERE book_id = %s;', (book_id,))
    loan_count = cur.fetchone()[0]

    if loan_count > 0:
        flash('Não é possível excluir um livro com empréstimos ativos.', 'danger')
    else:
        cur.execute('DELETE FROM books WHERE id = %s;', (book_id,))
        conn.commit()
        flash('Livro excluído com sucesso.', 'success')
    
    cur.close()
    conn.close()
    return redirect(url_for('index'))

# Garante que o banco de dados seja inicializado quando a aplicação começar
with app.app_context():
    init_db()

# Esta parte não é usada pelo Gunicorn, mas é útil para testes locais
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)