# Usa uma imagem oficial do Python, versão leve
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências para o container
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do seu projeto para o container
COPY . .

# Comando para rodar a sua aplicação (ajuste 'main.py' para o nome do seu arquivo principal)
CMD ["python", "main.py"]