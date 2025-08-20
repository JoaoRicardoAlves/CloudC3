"""
Interface do usuário - Sistema de console amigável
"""
import os
import sys
from datetime import datetime
from tabulate import tabulate
from colorama import init, Fore, Back, Style
from models.database_operations import DatabaseOperations

# Inicializa colorama para cores no terminal
init(autoreset=True)

class Interface:
    def __init__(self):
        self.db_ops = DatabaseOperations()
        self.grupo_membros = [
            "João Ricardo Alves",
            "Keven Leite Silva", 
            "Maria Silva Santos",
            "Pedro Oliveira Costa",
            "Ana Paula Ferreira"
        ]
    
    def limpar_tela(self):
        """Limpa a tela do terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def pausar(self):
        """Pausa a execução até o usuário pressionar Enter"""
        input(f"\n{Fore.YELLOW}Pressione Enter para continuar...{Style.RESET_ALL}")
    
    def splash_screen(self):
        """Tela de inicialização com informações do sistema"""
        self.limpar_tela()
        
        print(f"{Fore.CYAN}{Style.BRIGHT}")
        print("=" * 80)
        print("                    SISTEMA DE GERENCIAMENTO DE BIBLIOTECA")
        print("=" * 80)
        print(f"{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}📚 Desenvolvido por:{Style.RESET_ALL}")
        for i, membro in enumerate(self.grupo_membros, 1):
            print(f"   {i}. {membro}")
        
        print(f"\n{Fore.BLUE}🔧 Tecnologias utilizadas:{Style.RESET_ALL}")
        print("   • Linguagem: Python 3.x")
        print("   • Banco de Dados: PostgreSQL")
        print("   • Interface: Console (sem ORM)")
        
        print(f"\n{Fore.MAGENTA}📊 Status das tabelas no banco de dados:{Style.RESET_ALL}")
        
        counts = self.db_ops.get_table_counts()
        if counts:
            table_data = []
            for table, count in counts.items():
                status = f"{Fore.GREEN}✓" if count > 0 else f"{Fore.RED}✗"
                table_data.append([table.upper(), count, f"{status} {'Populada' if count > 0 else 'Vazia'}{Style.RESET_ALL}"])
            
            print(tabulate(table_data, headers=["TABELA", "REGISTROS", "STATUS"], tablefmt="grid"))
        else:
            print(f"{Fore.RED}❌ Erro ao conectar com o banco de dados{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}{Style.RESET_ALL}")
        self.pausar()
    
    def menu_principal(self):
        """Menu principal do sistema"""
        while True:
            self.limpar_tela()
            print(f"{Fore.CYAN}{Style.BRIGHT}")
            print("=" * 60)
            print("              MENU PRINCIPAL")
            print("=" * 60)
            print(f"{Style.RESET_ALL}")
            
            opcoes = [
                "1. 📊 Relatórios",
                "2. ➕ Inserir Registros", 
                "3. ❌ Remover Registros",
                "4. ✏️  Atualizar Registros",
                "5. 🚪 Sair"
            ]
            
            for opcao in opcoes:
                print(f"   {opcao}")
            
            print(f"\n{Fore.YELLOW}Escolha uma opção (1-5):{Style.RESET_ALL} ", end="")
            
            try:
                escolha = input().strip()
                
                if escolha == "1":
                    self.menu_relatorios()
                elif escolha == "2":
                    self.menu_inserir()
                elif escolha == "3":
                    self.menu_remover()
                elif escolha == "4":
                    self.menu_atualizar()
                elif escolha == "5":
                    self.sair_sistema()
                    break
                else:
                    print(f"{Fore.RED}❌ Opção inválida! Escolha entre 1 e 5.{Style.RESET_ALL}")
                    self.pausar()
            except KeyboardInterrupt:
                self.sair_sistema()
                break
            except Exception as e:
                print(f"{Fore.RED}❌ Erro inesperado: {e}{Style.RESET_ALL}")
                self.pausar()
    
    def menu_relatorios(self):
        """Menu de relatórios"""
        while True:
            self.limpar_tela()
            print(f"{Fore.CYAN}{Style.BRIGHT}")
            print("=" * 60)
            print("                 RELATÓRIOS")
            print("=" * 60)
            print(f"{Style.RESET_ALL}")
            
            opcoes = [
                "1. 📈 Vendas por Gênero (GROUP BY)",
                "2. 📋 Pedidos Detalhados (JOIN)",
                "3. 🔙 Voltar ao Menu Principal"
            ]
            
            for opcao in opcoes:
                print(f"   {opcao}")
            
            print(f"\n{Fore.YELLOW}Escolha uma opção (1-3):{Style.RESET_ALL} ", end="")
            
            try:
                escolha = input().strip()
                
                if escolha == "1":
                    self.relatorio_vendas_genero()
                elif escolha == "2":
                    self.relatorio_pedidos_detalhado()
                elif escolha == "3":
                    break
                else:
                    print(f"{Fore.RED}❌ Opção inválida! Escolha entre 1 e 3.{Style.RESET_ALL}")
                    self.pausar()
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"{Fore.RED}❌ Erro inesperado: {e}{Style.RESET_ALL}")
                self.pausar()
    
    def relatorio_vendas_genero(self):
        """Exibe relatório de vendas por gênero"""
        self.limpar_tela()
        print(f"{Fore.GREEN}{Style.BRIGHT}📈 RELATÓRIO: VENDAS POR GÊNERO{Style.RESET_ALL}")
        print("=" * 80)
        
        dados = self.db_ops.relatorio_vendas_por_genero()
        
        if dados:
            headers = ["Gênero", "Total Vendas", "Qtd. Vendida", "Valor Total (R$)"]
            table_data = []
            
            for row in dados:
                genero, total_vendas, qtd_vendida, valor_total = row
                table_data.append([
                    genero,
                    total_vendas,
                    qtd_vendida,
                    f"R$ {float(valor_total):.2f}"
                ])
            
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
            
            # Totais gerais
            total_geral_vendas = sum(row[1] for row in dados)
            total_geral_qtd = sum(row[2] for row in dados)
            total_geral_valor = sum(float(row[3]) for row in dados)
            
            print(f"\n{Fore.BLUE}{Style.BRIGHT}TOTAIS GERAIS:{Style.RESET_ALL}")
            print(f"Total de Vendas: {total_geral_vendas}")
            print(f"Quantidade Total Vendida: {total_geral_qtd}")
            print(f"Valor Total: R$ {total_geral_valor:.2f}")
        else:
            print(f"{Fore.YELLOW}⚠️  Nenhum dado encontrado para o relatório.{Style.RESET_ALL}")
        
        self.pausar()
    
    def relatorio_pedidos_detalhado(self):
        """Exibe relatório detalhado de pedidos"""
        self.limpar_tela()
        print(f"{Fore.GREEN}{Style.BRIGHT}📋 RELATÓRIO: PEDIDOS DETALHADOS{Style.RESET_ALL}")
        print("=" * 100)
        
        dados = self.db_ops.relatorio_pedidos_detalhado()
        
        if dados:
            headers = ["ID Pedido", "Data", "Cliente", "Livro", "Autor", "Qtd", "Preço Unit.", "Subtotal"]
            table_data = []
            
            for row in dados:
                id_pedido, data_pedido, nome_cliente, titulo, nome_autor, quantidade, preco_unitario, subtotal = row
                table_data.append([
                    id_pedido,
                    data_pedido.strftime('%d/%m/%Y'),
                    nome_cliente,
                    titulo[:30] + "..." if len(titulo) > 30 else titulo,
                    nome_autor,
                    quantidade,
                    f"R$ {float(preco_unitario):.2f}",
                    f"R$ {float(subtotal):.2f}"
                ])
            
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        else:
            print(f"{Fore.YELLOW}⚠️  Nenhum pedido encontrado.{Style.RESET_ALL}")
        
        self.pausar()
    
    def menu_inserir(self):
        """Menu para inserir registros"""
        while True:
            self.limpar_tela()
            print(f"{Fore.CYAN}{Style.BRIGHT}")
            print("=" * 60)
            print("              INSERIR REGISTROS")
            print("=" * 60)
            print(f"{Style.RESET_ALL}")
            
            opcoes = [
                "1. 👤 Inserir Autor",
                "2. 📚 Inserir Livro",
                "3. 🛒 Inserir Pedido",
                "4. 🔙 Voltar ao Menu Principal"
            ]
            
            for opcao in opcoes:
                print(f"   {opcao}")
            
            print(f"\n{Fore.YELLOW}Escolha uma opção (1-4):{Style.RESET_ALL} ", end="")
            
            try:
                escolha = input().strip()
                
                if escolha == "1":
                    self.inserir_autor()
                elif escolha == "2":
                    self.inserir_livro()
                elif escolha == "3":
                    self.inserir_pedido()
                elif escolha == "4":
                    break
                else:
                    print(f"{Fore.RED}❌ Opção inválida! Escolha entre 1 e 4.{Style.RESET_ALL}")
                    self.pausar()
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"{Fore.RED}❌ Erro inesperado: {e}{Style.RESET_ALL}")
                self.pausar()
    
    def inserir_autor(self):
        """Inserir novo autor"""
        while True:
            self.limpar_tela()
            print(f"{Fore.GREEN}{Style.BRIGHT}👤 INSERIR NOVO AUTOR{Style.RESET_ALL}")
            print("=" * 50)
            
            try:
                print(f"{Fore.YELLOW}Nome do Autor:{Style.RESET_ALL} ", end="")
                nome = input().strip()
                if not nome:
                    print(f"{Fore.RED}❌ Nome é obrigatório!{Style.RESET_ALL}")
                    self.pausar()
                    continue
                
                print(f"{Fore.YELLOW}Nacionalidade:{Style.RESET_ALL} ", end="")
                nacionalidade = input().strip()
                
                print(f"{Fore.YELLOW}Data de Nascimento (YYYY-MM-DD) ou Enter para pular:{Style.RESET_ALL} ", end="")
                data_nascimento = input().strip()
                if data_nascimento:
                    try:
                        datetime.strptime(data_nascimento, '%Y-%m-%d')
                    except ValueError:
                        print(f"{Fore.RED}❌ Formato de data inválido! Use YYYY-MM-DD{Style.RESET_ALL}")
                        self.pausar()
                        continue
                else:
                    data_nascimento = None
                
                print(f"{Fore.YELLOW}Biografia:{Style.RESET_ALL} ", end="")
                biografia = input().strip()
                
                sucesso, mensagem = self.db_ops.inserir_autor(nome, nacionalidade, data_nascimento, biografia)
                
                if sucesso:
                    print(f"{Fore.GREEN}✅ {mensagem}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}❌ {mensagem}{Style.RESET_ALL}")
                
                print(f"\n{Fore.YELLOW}Deseja inserir outro autor? (s/N):{Style.RESET_ALL} ", end="")
                continuar = input().strip().lower()
                
                if continuar != 's':
                    break
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"{Fore.RED}❌ Erro inesperado: {e}{Style.RESET_ALL}")
                self.pausar()
    
    def inserir_livro(self):
        """Inserir novo livro"""
        while True:
            self.limpar_tela()
            print(f"{Fore.GREEN}{Style.BRIGHT}📚 INSERIR NOVO LIVRO{Style.RESET_ALL}")
            print("=" * 50)
            
            # Primeiro, mostrar autores disponíveis
            autores = self.db_ops.listar_autores()
            if not autores:
                print(f"{Fore.RED}❌ Nenhum autor cadastrado! Cadastre um autor primeiro.{Style.RESET_ALL}")
                self.pausar()
                break
            
            print(f"{Fore.BLUE}Autores disponíveis:{Style.RESET_ALL}")
            for autor in autores:
                print(f"   ID: {autor[0]} - {autor[1]} ({autor[2]})")
            
            try:
                print(f"\n{Fore.YELLOW}Título do Livro:{Style.RESET_ALL} ", end="")
                titulo = input().strip()
                if not titulo:
                    print(f"{Fore.RED}❌ Título é obrigatório!{Style.RESET_ALL}")
                    self.pausar()
                    continue
                
                print(f"{Fore.YELLOW}ID do Autor:{Style.RESET_ALL} ", end="")
                id_autor = int(input().strip())
                
                print(f"{Fore.YELLOW}Gênero:{Style.RESET_ALL} ", end="")
                genero = input().strip()
                if not genero:
                    print(f"{Fore.RED}❌ Gênero é obrigatório!{Style.RESET_ALL}")
                    self.pausar()
                    continue
                
                print(f"{Fore.YELLOW}Ano de Publicação:{Style.RESET_ALL} ", end="")
                ano_publicacao = input().strip()
                ano_publicacao = int(ano_publicacao) if ano_publicacao else None
                
                print(f"{Fore.YELLOW}Preço (R$):{Style.RESET_ALL} ", end="")
                preco = float(input().strip())
                
                print(f"{Fore.YELLOW}Quantidade em Estoque:{Style.RESET_ALL} ", end="")
                quantidade_estoque = int(input().strip())
                
                sucesso, mensagem = self.db_ops.inserir_livro(titulo, id_autor, genero, ano_publicacao, preco, quantidade_estoque)
                
                if sucesso:
                    print(f"{Fore.GREEN}✅ {mensagem}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}❌ {mensagem}{Style.RESET_ALL}")
                
                print(f"\n{Fore.YELLOW}Deseja inserir outro livro? (s/N):{Style.RESET_ALL} ", end="")
                continuar = input().strip().lower()
                
                if continuar != 's':
                    break
                    
            except ValueError:
                print(f"{Fore.RED}❌ Valor numérico inválido!{Style.RESET_ALL}")
                self.pausar()
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"{Fore.RED}❌ Erro inesperado: {e}{Style.RESET_ALL}")
                self.pausar()
    
    def inserir_pedido(self):
        """Inserir novo pedido"""
        while True:
            self.limpar_tela()
            print(f"{Fore.GREEN}{Style.BRIGHT}🛒 INSERIR NOVO PEDIDO{Style.RESET_ALL}")
            print("=" * 50)
            
            try:
                print(f"{Fore.YELLOW}Nome do Cliente:{Style.RESET_ALL} ", end="")
                nome_cliente = input().strip()
                if not nome_cliente:
                    print(f"{Fore.RED}❌ Nome do cliente é obrigatório!{Style.RESET_ALL}")
                    self.pausar()
                    continue
                
                print(f"{Fore.YELLOW}Email do Cliente:{Style.RESET_ALL} ", end="")
                email_cliente = input().strip()
                
                sucesso, mensagem = self.db_ops.inserir_pedido(nome_cliente, email_cliente)
                
                if sucesso:
                    print(f"{Fore.GREEN}✅ {mensagem}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}❌ {mensagem}{Style.RESET_ALL}")
                
                print(f"\n{Fore.YELLOW}Deseja inserir outro pedido? (s/N):{Style.RESET_ALL} ", end="")
                continuar = input().strip().lower()
                
                if continuar != 's':
                    break
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"{Fore.RED}❌ Erro inesperado: {e}{Style.RESET_ALL}")
                self.pausar()
    
    def menu_remover(self):
        """Menu para remover registros"""
        while True:
            self.limpar_tela()
            print(f"{Fore.CYAN}{Style.BRIGHT}")
            print("=" * 60)
            print("              REMOVER REGISTROS")
            print("=" * 60)
            print(f"{Style.RESET_ALL}")
            
            opcoes = [
                "1. 👤 Remover Autor",
                "2. 📚 Remover Livro",
                "3. 🛒 Remover Pedido",
                "4. 🔙 Voltar ao Menu Principal"
            ]
            
            for opcao in opcoes:
                print(f"   {opcao}")
            
            print(f"\n{Fore.YELLOW}Escolha uma opção (1-4):{Style.RESET_ALL} ", end="")
            
            try:
                escolha = input().strip()
                
                if escolha == "1":
                    self.remover_autor()
                elif escolha == "2":
                    self.remover_livro()
                elif escolha == "3":
                    self.remover_pedido()
                elif escolha == "4":
                    break
                else:
                    print(f"{Fore.RED}❌ Opção inválida! Escolha entre 1 e 4.{Style.RESET_ALL}")
                    self.pausar()
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"{Fore.RED}❌ Erro inesperado: {e}{Style.RESET_ALL}")
                self.pausar()
    
    def remover_autor(self):
        """Remover autor"""
        while True:
            self.limpar_tela()
            print(f"{Fore.RED}{Style.BRIGHT}👤 REMOVER AUTOR{Style.RESET_ALL}")
            print("=" * 50)
            
            autores = self.db_ops.listar_autores()
            if not autores:
                print(f"{Fore.YELLOW}⚠️  Nenhum autor cadastrado.{Style.RESET_ALL}")
                self.pausar()
                break
            
            # Exibir autores
            headers = ["ID", "Nome", "Nacionalidade", "Data Nascimento"]
            table_data = []
            for autor in autores:
                data_nasc = autor[3].strftime('%d/%m/%Y') if autor[3] else "N/A"
                table_data.append([autor[0], autor[1], autor[2] or "N/A", data_nasc])
            
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
            
            try:
                print(f"\n{Fore.YELLOW}Digite o ID do autor a ser removido (0 para cancelar):{Style.RESET_ALL} ", end="")
                id_autor = int(input().strip())
                
                if id_autor == 0:
                    break
                
                # Confirmar remoção
                print(f"{Fore.RED}⚠️  Tem certeza que deseja remover este autor? (s/N):{Style.RESET_ALL} ", end="")
                confirmacao = input().strip().lower()
                
                if confirmacao == 's':
                    sucesso, mensagem = self.db_ops.remover_autor(id_autor)
                    
                    if sucesso:
                        print(f"{Fore.GREEN}✅ {mensagem}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}❌ {mensagem}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}Operação cancelada.{Style.RESET_ALL}")
                
                print(f"\n{Fore.YELLOW}Deseja remover outro autor? (s/N):{Style.RESET_ALL} ", end="")
                continuar = input().strip().lower()
                
                if continuar != 's':
                    break
                    
            except ValueError:
                print(f"{Fore.RED}❌ ID inválido!{Style.RESET_ALL}")
                self.pausar()
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"{Fore.RED}❌ Erro inesperado: {e}{Style.RESET_ALL}")
                self.pausar()
    
    def remover_livro(self):
        """Remover livro"""
        while True:
            self.limpar_tela()
            print(f"{Fore.RED}{Style.BRIGHT}📚 REMOVER LIVRO{Style.RESET_ALL}")
            print("=" * 50)
            
            livros = self.db_ops.listar_livros()
            if not livros:
                print(f"{Fore.YELLOW}⚠️  Nenhum livro cadastrado.{Style.RESET_ALL}")
                self.pausar()
                break
            
            # Exibir livros
            headers = ["ID", "Título", "Autor", "Gênero", "Preço", "Estoque"]
            table_data = []
            for livro in livros:
                table_data.append([
                    livro[0],
                    livro[1][:30] + "..." if len(livro[1]) > 30 else livro[1],
                    livro[2],
                    livro[3],
                    f"R$ {float(livro[4]):.2f}",
                    livro[5]
                ])
            
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
            
            try:
                print(f"\n{Fore.YELLOW}Digite o ID do livro a ser removido (0 para cancelar):{Style.RESET_ALL} ", end="")
                id_livro = int(input().strip())
                
                if id_livro == 0:
                    break
                
                # Confirmar remoção
                print(f"{Fore.RED}⚠️  Tem certeza que deseja remover este livro? (s/N):{Style.RESET_ALL} ", end="")
                confirmacao = input().strip().lower()
                
                if confirmacao == 's':
                    sucesso, mensagem = self.db_ops.remover_livro(id_livro)
                    
                    if sucesso:
                        print(f"{Fore.GREEN}✅ {mensagem}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}❌ {mensagem}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}Operação cancelada.{Style.RESET_ALL}")
                
                print(f"\n{Fore.YELLOW}Deseja remover outro livro? (s/N):{Style.RESET_ALL} ", end="")
                continuar = input().strip().lower()
                
                if continuar != 's':
                    break
                    
            except ValueError:
                print(f"{Fore.RED}❌ ID inválido!{Style.RESET_ALL}")
                self.pausar()
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"{Fore.RED}❌ Erro inesperado: {e}{Style.RESET_ALL}")
                self.pausar()
    
    def remover_pedido(self):
        """Remover pedido"""
        while True:
            self.limpar_tela()
            print(f"{Fore.RED}{Style.BRIGHT}🛒 REMOVER PEDIDO{Style.RESET_ALL}")
            print("=" * 50)
            
            pedidos = self.db_ops.listar_pedidos()
            if not pedidos:
                print(f"{Fore.YELLOW}⚠️  Nenhum pedido cadastrado.{Style.RESET_ALL}")
                self.pausar()
                break
            
            # Exibir pedidos
            headers = ["ID", "Data", "Cliente", "Email", "Valor Total"]
            table_data = []
            for pedido in pedidos:
                table_data.append([
                    pedido[0],
                    pedido[1].strftime('%d/%m/%Y'),
                    pedido[2],
                    pedido[3] or "N/A",
                    f"R$ {float(pedido[4]):.2f}"
                ])
            
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
            
            try:
                print(f"\n{Fore.YELLOW}Digite o ID do pedido a ser removido (0 para cancelar):{Style.RESET_ALL} ", end="")
                id_pedido = int(input().strip())
                
                if id_pedido == 0:
                    break
                
                # Confirmar remoção
                print(f"{Fore.RED}⚠️  Tem certeza que deseja remover este pedido? (s/N):{Style.RESET_ALL} ", end="")
                confirmacao = input().strip().lower()
                
                if confirmacao == 's':
                    sucesso, mensagem = self.db_ops.remover_pedido(id_pedido)
                    
                    if sucesso:
                        print(f"{Fore.GREEN}✅ {mensagem}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}❌ {mensagem}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}Operação cancelada.{Style.RESET_ALL}")
                
                print(f"\n{Fore.YELLOW}Deseja remover outro pedido? (s/N):{Style.RESET_ALL} ", end="")
                continuar = input().strip().lower()
                
                if continuar != 's':
                    break
                    
            except ValueError:
                print(f"{Fore.RED}❌ ID inválido!{Style.RESET_ALL}")
                self.pausar()
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"{Fore.RED}❌ Erro inesperado: {e}{Style.RESET_ALL}")
                self.pausar()
    
    def menu_atualizar(self):
        """Menu para atualizar registros"""
        while True:
            self.limpar_tela()
            print(f"{Fore.CYAN}{Style.BRIGHT}")
            print("=" * 60)
            print("             ATUALIZAR REGISTROS")
            print("=" * 60)
            print(f"{Style.RESET_ALL}")
            
            opcoes = [
                "1. 👤 Atualizar Autor",
                "2. 📚 Atualizar Livro",
                "3. 🛒 Atualizar Pedido",
                "4. 🔙 Voltar ao Menu Principal"
            ]
            
            for opcao in opcoes:
                print(f"   {opcao}")
            
            print(f"\n{Fore.YELLOW}Escolha uma opção (1-4):{Style.RESET_ALL} ", end="")
            
            try:
                escolha = input().strip()
                
                if escolha == "1":
                    self.atualizar_autor()
                elif escolha == "2":
                    self.atualizar_livro()
                elif escolha == "3":
                    self.atualizar_pedido()
                elif escolha == "4":
                    break
                else:
                    print(f"{Fore.RED}❌ Opção inválida! Escolha entre 1 e 4.{Style.RESET_ALL}")
                    self.pausar()
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"{Fore.RED}❌ Erro inesperado: {e}{Style.RESET_ALL}")
                self.pausar()
    
    def atualizar_autor(self):
        """Atualizar autor"""
        while True:
            self.limpar_tela()
            print(f"{Fore.BLUE}{Style.BRIGHT}👤 ATUALIZAR AUTOR{Style.RESET_ALL}")
            print("=" * 50)
            
            autores = self.db_ops.listar_autores()
            if not autores:
                print(f"{Fore.YELLOW}⚠️  Nenhum autor cadastrado.{Style.RESET_ALL}")
                self.pausar()
                break
            
            # Exibir autores
            headers = ["ID", "Nome", "Nacionalidade", "Data Nascimento"]
            table_data = []
            for autor in autores:
                data_nasc = autor[3].strftime('%d/%m/%Y') if autor[3] else "N/A"
                table_data.append([autor[0], autor[1], autor[2] or "N/A", data_nasc])
            
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
            
            try:
                print(f"\n{Fore.YELLOW}Digite o ID do autor a ser atualizado (0 para cancelar):{Style.RESET_ALL} ", end="")
                id_autor = int(input().strip())
                
                if id_autor == 0:
                    break
                
                # Buscar dados atuais do autor
                autor_atual = self.db_ops.obter_autor_por_id(id_autor)
                if not autor_atual:
                    print(f"{Fore.RED}❌ Autor não encontrado!{Style.RESET_ALL}")
                    self.pausar()
                    continue
                
                print(f"\n{Fore.GREEN}Dados atuais do autor:{Style.RESET_ALL}")
                print(f"Nome: {autor_atual[1]}")
                print(f"Nacionalidade: {autor_atual[2] or 'N/A'}")
                print(f"Data Nascimento: {autor_atual[3].strftime('%Y-%m-%d') if autor_atual[3] else 'N/A'}")
                print(f"Biografia: {autor_atual[4] or 'N/A'}")
                
                print(f"\n{Fore.YELLOW}Digite os novos dados (Enter para manter o atual):{Style.RESET_ALL}")
                
                print(f"Nome [{autor_atual[1]}]: ", end="")
                nome = input().strip() or autor_atual[1]
                
                print(f"Nacionalidade [{autor_atual[2] or ''}]: ", end="")
                nacionalidade = input().strip() or autor_atual[2]
                
                data_atual = autor_atual[3].strftime('%Y-%m-%d') if autor_atual[3] else ''
                print(f"Data Nascimento (YYYY-MM-DD) [{data_atual}]: ", end="")
                data_nascimento = input().strip() or data_atual
                
                if data_nascimento:
                    try:
                        datetime.strptime(data_nascimento, '%Y-%m-%d')
                    except ValueError:
                        print(f"{Fore.RED}❌ Formato de data inválido! Use YYYY-MM-DD{Style.RESET_ALL}")
                        self.pausar()
                        continue
                else:
                    data_nascimento = None
                
                print(f"Biografia [{autor_atual[4] or ''}]: ", end="")
                biografia = input().strip() or autor_atual[4]
                
                sucesso, mensagem = self.db_ops.atualizar_autor(id_autor, nome, nacionalidade, data_nascimento, biografia)
                
                if sucesso:
                    print(f"{Fore.GREEN}✅ {mensagem}{Style.RESET_ALL}")
                    
                    # Exibir dados atualizados
                    autor_atualizado = self.db_ops.obter_autor_por_id(id_autor)
                    if autor_atualizado:
                        print(f"\n{Fore.GREEN}Dados atualizados:{Style.RESET_ALL}")
                        print(f"Nome: {autor_atualizado[1]}")
                        print(f"Nacionalidade: {autor_atualizado[2] or 'N/A'}")
                        print(f"Data Nascimento: {autor_atualizado[3].strftime('%d/%m/%Y') if autor_atualizado[3] else 'N/A'}")
                        print(f"Biografia: {autor_atualizado[4] or 'N/A'}")
                else:
                    print(f"{Fore.RED}❌ {mensagem}{Style.RESET_ALL}")
                
                print(f"\n{Fore.YELLOW}Deseja atualizar outro autor? (s/N):{Style.RESET_ALL} ", end="")
                continuar = input().strip().lower()
                
                if continuar != 's':
                    break
                    
            except ValueError:
                print(f"{Fore.RED}❌ ID inválido!{Style.RESET_ALL}")
                self.pausar()
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"{Fore.RED}❌ Erro inesperado: {e}{Style.RESET_ALL}")
                self.pausar()
    
    def atualizar_livro(self):
        """Atualizar livro"""
        while True:
            self.limpar_tela()
            print(f"{Fore.BLUE}{Style.BRIGHT}📚 ATUALIZAR LIVRO{Style.RESET_ALL}")
            print("=" * 50)
            
            livros = self.db_ops.listar_livros()
            if not livros:
                print(f"{Fore.YELLOW}⚠️  Nenhum livro cadastrado.{Style.RESET_ALL}")
                self.pausar()
                break
            
            # Exibir livros
            headers = ["ID", "Título", "Autor", "Gênero", "Preço", "Estoque"]
            table_data = []
            for livro in livros:
                table_data.append([
                    livro[0],
                    livro[1][:30] + "..." if len(livro[1]) > 30 else livro[1],
                    livro[2],
                    livro[3],
                    f"R$ {float(livro[4]):.2f}",
                    livro[5]
                ])
            
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
            
            try:
                print(f"\n{Fore.YELLOW}Digite o ID do livro a ser atualizado (0 para cancelar):{Style.RESET_ALL} ", end="")
                id_livro = int(input().strip())
                
                if id_livro == 0:
                    break
                
                # Buscar dados atuais do livro
                livro_atual = self.db_ops.obter_livro_por_id(id_livro)
                if not livro_atual:
                    print(f"{Fore.RED}❌ Livro não encontrado!{Style.RESET_ALL}")
                    self.pausar()
                    continue
                
                print(f"\n{Fore.GREEN}Dados atuais do livro:{Style.RESET_ALL}")
                print(f"Título: {livro_atual[1]}")
                print(f"Autor: {livro_atual[3]} (ID: {livro_atual[2]})")
                print(f"Gênero: {livro_atual[4]}")
                print(f"Ano: {livro_atual[5] or 'N/A'}")
                print(f"Preço: R$ {float(livro_atual[6]):.2f}")
                print(f"Estoque: {livro_atual[7]}")
                
                # Mostrar autores disponíveis
                autores = self.db_ops.listar_autores()
                print(f"\n{Fore.BLUE}Autores disponíveis:{Style.RESET_ALL}")
                for autor in autores:
                    print(f"   ID: {autor[0]} - {autor[1]}")
                
                print(f"\n{Fore.YELLOW}Digite os novos dados (Enter para manter o atual):{Style.RESET_ALL}")
                
                print(f"Título [{livro_atual[1]}]: ", end="")
                titulo = input().strip() or livro_atual[1]
                
                print(f"ID do Autor [{livro_atual[2]}]: ", end="")
                id_autor_input = input().strip()
                id_autor = int(id_autor_input) if id_autor_input else livro_atual[2]
                
                print(f"Gênero [{livro_atual[4]}]: ", end="")
                genero = input().strip() or livro_atual[4]
                
                print(f"Ano de Publicação [{livro_atual[5] or ''}]: ", end="")
                ano_input = input().strip()
                ano_publicacao = int(ano_input) if ano_input else livro_atual[5]
                
                print(f"Preço (R$) [{float(livro_atual[6]):.2f}]: ", end="")
                preco_input = input().strip()
                preco = float(preco_input) if preco_input else float(livro_atual[6])
                
                print(f"Quantidade em Estoque [{livro_atual[7]}]: ", end="")
                estoque_input = input().strip()
                quantidade_estoque = int(estoque_input) if estoque_input else livro_atual[7]
                
                sucesso, mensagem = self.db_ops.atualizar_livro(id_livro, titulo, id_autor, genero, ano_publicacao, preco, quantidade_estoque)
                
                if sucesso:
                    print(f"{Fore.GREEN}✅ {mensagem}{Style.RESET_ALL}")
                    
                    # Exibir dados atualizados
                    livro_atualizado = self.db_ops.obter_livro_por_id(id_livro)
                    if livro_atualizado:
                        print(f"\n{Fore.GREEN}Dados atualizados:{Style.RESET_ALL}")
                        print(f"Título: {livro_atualizado[1]}")
                        print(f"Autor: {livro_atualizado[3]} (ID: {livro_atualizado[2]})")
                        print(f"Gênero: {livro_atualizado[4]}")
                        print(f"Ano: {livro_atualizado[5] or 'N/A'}")
                        print(f"Preço: R$ {float(livro_atualizado[6]):.2f}")
                        print(f"Estoque: {livro_atualizado[7]}")
                else:
                    print(f"{Fore.RED}❌ {mensagem}{Style.RESET_ALL}")
                
                print(f"\n{Fore.YELLOW}Deseja atualizar outro livro? (s/N):{Style.RESET_ALL} ", end="")
                continuar = input().strip().lower()
                
                if continuar != 's':
                    break
                    
            except ValueError:
                print(f"{Fore.RED}❌ Valor numérico inválido!{Style.RESET_ALL}")
                self.pausar()
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"{Fore.RED}❌ Erro inesperado: {e}{Style.RESET_ALL}")
                self.pausar()
    
    def atualizar_pedido(self):
        """Atualizar pedido"""
        while True:
            self.limpar_tela()
            print(f"{Fore.BLUE}{Style.BRIGHT}🛒 ATUALIZAR PEDIDO{Style.RESET_ALL}")
            print("=" * 50)
            
            pedidos = self.db_ops.listar_pedidos()
            if not pedidos:
                print(f"{Fore.YELLOW}⚠️  Nenhum pedido cadastrado.{Style.RESET_ALL}")
                self.pausar()
                break
            
            # Exibir pedidos
            headers = ["ID", "Data", "Cliente", "Email", "Valor Total"]
            table_data = []
            for pedido in pedidos:
                table_data.append([
                    pedido[0],
                    pedido[1].strftime('%d/%m/%Y'),
                    pedido[2],
                    pedido[3] or "N/A",
                    f"R$ {float(pedido[4]):.2f}"
                ])
            
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
            
            try:
                print(f"\n{Fore.YELLOW}Digite o ID do pedido a ser atualizado (0 para cancelar):{Style.RESET_ALL} ", end="")
                id_pedido = int(input().strip())
                
                if id_pedido == 0:
                    break
                
                # Buscar dados atuais do pedido
                pedido_atual = self.db_ops.obter_pedido_por_id(id_pedido)
                if not pedido_atual:
                    print(f"{Fore.RED}❌ Pedido não encontrado!{Style.RESET_ALL}")
                    self.pausar()
                    continue
                
                print(f"\n{Fore.GREEN}Dados atuais do pedido:{Style.RESET_ALL}")
                print(f"Data: {pedido_atual[1].strftime('%d/%m/%Y')}")
                print(f"Cliente: {pedido_atual[2]}")
                print(f"Email: {pedido_atual[3] or 'N/A'}")
                print(f"Valor Total: R$ {float(pedido_atual[4]):.2f}")
                
                print(f"\n{Fore.YELLOW}Digite os novos dados (Enter para manter o atual):{Style.RESET_ALL}")
                
                print(f"Nome do Cliente [{pedido_atual[2]}]: ", end="")
                nome_cliente = input().strip() or pedido_atual[2]
                
                print(f"Email do Cliente [{pedido_atual[3] or ''}]: ", end="")
                email_cliente = input().strip() or pedido_atual[3]
                
                sucesso, mensagem = self.db_ops.atualizar_pedido(id_pedido, nome_cliente, email_cliente)
                
                if sucesso:
                    print(f"{Fore.GREEN}✅ {mensagem}{Style.RESET_ALL}")
                    
                    # Exibir dados atualizados
                    pedido_atualizado = self.db_ops.obter_pedido_por_id(id_pedido)
                    if pedido_atualizado:
                        print(f"\n{Fore.GREEN}Dados atualizados:{Style.RESET_ALL}")
                        print(f"Data: {pedido_atualizado[1].strftime('%d/%m/%Y')}")
                        print(f"Cliente: {pedido_atualizado[2]}")
                        print(f"Email: {pedido_atualizado[3] or 'N/A'}")
                        print(f"Valor Total: R$ {float(pedido_atualizado[4]):.2f}")
                else:
                    print(f"{Fore.RED}❌ {mensagem}{Style.RESET_ALL}")
                
                print(f"\n{Fore.YELLOW}Deseja atualizar outro pedido? (s/N):{Style.RESET_ALL} ", end="")
                continuar = input().strip().lower()
                
                if continuar != 's':
                    break
                    
            except ValueError:
                print(f"{Fore.RED}❌ ID inválido!{Style.RESET_ALL}")
                self.pausar()
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"{Fore.RED}❌ Erro inesperado: {e}{Style.RESET_ALL}")
                self.pausar()
    
    def sair_sistema(self):
        """Finaliza o sistema"""
        self.limpar_tela()
        print(f"{Fore.CYAN}{Style.BRIGHT}")
        print("=" * 60)
        print("              SISTEMA FINALIZADO")
        print("=" * 60)
        print(f"{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}✅ Obrigado por usar o Sistema de Gerenciamento de Biblioteca!{Style.RESET_ALL}")
        print(f"{Fore.BLUE}📚 Desenvolvido pelos alunos:{Style.RESET_ALL}")
        for membro in self.grupo_membros:
            print(f"   • {membro}")
        
        print(f"\n{Fore.YELLOW}🎓 Projeto acadêmico - Professor Howard Roatti{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}🔧 Tecnologias: Python + PostgreSQL (sem ORM){Style.RESET_ALL}")
        
        sys.exit(0)