# Dockerfile
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de requerimientos y el código de la aplicación
COPY requirements.txt requirements.txt
COPY app app

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Instalar python-dotenv para cargar variables de entorno
RUN pip install python-dotenv

# Exponer el puerto en el que correrá la aplicación
EXPOSE 8000

# Comando para correr la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]