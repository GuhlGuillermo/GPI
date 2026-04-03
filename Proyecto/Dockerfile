FROM python:3.12-slim

# Evitar que Python escriba archivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Evitar que Python mande a buffer el output stdout y stderr
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto
COPY . /app/

# Recolectar estáticos (útil para producción de Django)
# RUN python manage.py collectstatic --noinput

# Exponer el puerto de Gunicorn
EXPOSE 8000

# Comando para correr la aplicación mediante Gunicorn en producción
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
