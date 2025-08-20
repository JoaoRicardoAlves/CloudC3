#!/usr/bin/env python3
"""
Sistema de Gerenciamento de Biblioteca
Projeto acadêmico desenvolvido conforme diretrizes do Professor Howard Roatti

Características:
- Linguagem: Python 3.x
- Banco de Dados: PostgreSQL
- Interface: Console amigável
- CONDIÇÃO CRÍTICA: SEM uso de ORM - Apenas queries SQL manuais

Desenvolvido por:
- João Ricardo Alves
- Keven Leite Silva
- Maria Silva Santos
- Pedro Oliveira Costa
- Ana Paula Ferreira
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório raiz ao path para importações
sys.path.append(str(Path(__file__).parent))

from config.database import DatabaseConfig
from views.interface import Interface

def verificar_dependencias():
    """
    Verifica se todas as dependências estão instaladas
    """
    try:
        import psycopg2
        import tabulate
        import colorama
        return True, "Todas as dependências estão instaladas"
    except ImportError as e:
        return False, f"Dependência faltando: {e}. Execute: pip install -r requirements.txt"

def inicializar_banco():
    """
    Inicializa o banco de dados executando o script de schema
    """
    db_config = DatabaseConfig()
    
    # Testa a conexão
    sucesso, mensagem = db_config.test_connection()
    if not sucesso:
        return False, f"Erro de conexão: {mensagem}"
    
    # Executa o script de criação das tabelas
    script_path = Path(__file__).parent / "database" / "schema.sql"
    if script_path.exists():
        sucesso, mensagem = db_config.execute_script(script_path)
        if not sucesso:
            return False, f"Erro ao executar script: {mensagem}"
    else:
        return False, f"Script SQL não encontrado: {script_path}"
    
    return True, "Banco de dados inicializado com sucesso"

def main():
    """
    Função principal do sistema
    """
    print("🔄 Iniciando Sistema de Gerenciamento de Biblioteca...")
    
    # Verifica dependências
    print("📦 Verificando dependências...")
    sucesso, mensagem = verificar_dependencias()
    if not sucesso:
        print(f"❌ {mensagem}")
        sys.exit(1)
    
    # Inicializa banco de dados
    print("🗄️  Inicializando banco de dados...")
    sucesso, mensagem = inicializar_banco()
    if not sucesso:
        print(f"❌ {mensagem}")
        print("\n💡 Dicas para resolver:")
        print("   1. Verifique se o PostgreSQL está rodando")
        print("   2. Confirme as credenciais no docker-compose.yml")
        print("   3. Execute: docker-compose up -d")
        sys.exit(1)
    
    print("✅ Sistema inicializado com sucesso!")
    print("🚀 Carregando interface...")
    
    # Inicia a interface
    try:
        interface = Interface()
        interface.splash_screen()
        interface.menu_principal()
    except KeyboardInterrupt:
        print("\n\n👋 Sistema interrompido pelo usuário. Até logo!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()