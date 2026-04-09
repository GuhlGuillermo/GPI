FROM python:3.12-slim

WORKDIR /app

# Primero las dependencias por eficiencia de caché
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos la app Flask
COPY . .

# Aseguramos que los modulos se entiendan internamente para Pytest
ENV PYTHONPATH=/app

EXPOSE 5000

# Iniciamos la demo del factory Flask
CMD ["python", "app.py"]
