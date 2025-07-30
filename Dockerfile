FROM rasa/rasa-sdk:3.6.0

USER root

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh
COPY actions.py /app/actions.py

ENTRYPOINT []

CMD ["./start.sh"]
