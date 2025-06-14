# meu_projeto_web/app/Dockerfile

# Use uma imagem base oficial do Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /usr/src/app

# Copia o arquivo de dependências e instala
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código da aplicação para o diretório de trabalho
COPY . .

# Expõe a porta que a aplicação vai rodar dentro do contêiner
EXPOSE 5000

# O comando para iniciar a aplicação será definido no docker-compose.yml