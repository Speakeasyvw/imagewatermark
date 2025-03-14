# Usa una imagen oficial de Python
FROM python:3.12

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 5000 para Fly.io
EXPOSE 5000

# Comando para ejecutar el servidor
CMD ["gunicorn", "-b", "0.0.0.0:5000", "server:app"]
