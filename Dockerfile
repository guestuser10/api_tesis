# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos requeridos a la imagen
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Clonar el repositorio
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/guestuser10/api_tesis.git .

# Copiar la librería .so a la imagen
COPY libtopsislib.so .

# Exponer el puerto que usará la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
