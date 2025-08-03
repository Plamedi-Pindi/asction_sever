FROM python:3.10

WORKDIR /app

# Copia os arquivos do projeto
COPY . /app

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# ENV PYTHONPATH "${PYTHONPATH}:/app/actions"

# Expõe a porta usada pelo action server
EXPOSE 5055

# Comando de inicialização
# CMD ["python", "-m", "actions.actions", "--port", "5055"]
CMD ["python", "-m", "rasa_sdk", "--port", "5055"]
