from flask import Flask, request, jsonify, send_file
import requests
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)

@app.route("/")
def home():
    return "Servidor corriendo en Railway"

def add_watermark(image_url):
    try:
        # Descargar la imagen
        response = requests.get(image_url)
        response.raise_for_status()
        image = Image.open(io.BytesIO(response.content))

        # Crear objeto para dibujar
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        # Posicionar marca de agua en el centro
        text = "KREI"
        text_width, text_height = draw.textsize(text, font=font)
        position = ((image.width - text_width) // 2, (image.height - text_height) // 2)

        # Agregar marca de agua
        draw.text(position, text, fill=(255, 255, 255, 128), font=font)

        # Guardar en memoria
        img_io = io.BytesIO()
        image.save(img_io, format="PNG")
        img_io.seek(0)
        return img_io

    except Exception as e:
        return str(e)

@app.route('/process_image', methods=['POST'])
def process_image():
    data = request.json
    image_url = data.get('image_url')

    if not image_url:
        return jsonify({"error": "No image URL provided"}), 400

    img_io = add_watermark(image_url)
    return send_file(img_io, mimetype='image/png')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
