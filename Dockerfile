FROM rasa/rasa-sdk:3.6.0

USER root

WORKDIR /app

# Copia só requirements para instalar dependências primeiro e aproveitar cache
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# COPY start.sh /app/start.sh
# COPY actions.py /app/actions.py
RUN chmod +x /app/start.sh

ENTRYPOINT []

CMD ["./start.sh"]
