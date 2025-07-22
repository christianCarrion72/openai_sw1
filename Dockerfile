# Usar una imagen base ligera de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar solo los archivos de dependencias primero para aprovechar el cache de Docker
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . .

# Exponer el puerto que usa la aplicación
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "main.py"]