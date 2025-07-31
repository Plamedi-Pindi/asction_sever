#!/bin/sh

# echo "PORT = $PORT"
# exec python -m rasa_sdk.endpoint --port $PORT

echo "🔧 Porta definida pelo Railway: $PORT"

# Se a porta estiver vazia, falha imediatamente
if [ -z "$PORT" ]; then
  echo "❌ ERRO: variável de ambiente PORT não está definida!"
  exit 1
fi


# Inicia o servidor
exec python -m rasa_sdk.endpoint --port "$PORT"
