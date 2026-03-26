FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
COPY .streamlit .streamlit
# Default Env Vars
ENV OLLAMA_BASE_URL=http://10.230.100.240:17020
ENV OLLAMA_CHAT_MODEL=llama3.1
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]