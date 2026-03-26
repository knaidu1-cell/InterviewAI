#!/bin/bash
echo "Generating .env file for Docker..."
# We explicitly save the variables so Docker can see them
echo "APPLICATION_PORT=${APPLICATION_PORT:-23340}" > .env
echo "CONTAINER_NAME=${CONTAINER_NAME:-interview-ai-app}" >> .env
echo "OLLAMA_BASE_URL=${OLLAMA_BASE_URL:-http://10.230.100.240:17020}" >> .env
echo "OLLAMA_CHAT_MODEL=${OLLAMA_CHAT_MODEL:-llama3.1}" >> .env

echo "✅ .env file created with Port: $APPLICATION_PORT"
cat .env