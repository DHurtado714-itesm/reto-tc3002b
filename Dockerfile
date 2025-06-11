# Usar Python slim para reducir tamaño
FROM python:3.11-slim

# Instalar paquetes del sistema necesarios para scipy y xgboost
RUN apt-get update && apt-get install -y build-essential gcc libglib2.0-0

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements y luego instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código (incluyendo modelo y templates)
COPY . .

# Exponer el puerto por defecto de Uvicorn
EXPOSE 8000

# Comando para lanzar la app con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
