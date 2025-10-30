from flask import Flask, render_template, request, jsonify
import sqlite3, os, base64, re
from dotenv import load_dotenv
import google.generativeai as genai
from groq import Groq
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# 🔹 Base de datos
def crear_base_datos():
    conn = sqlite3.connect('piezas.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS piezas
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nombre TEXT NOT NULL,
                  descripcion TEXT,
                  categoria TEXT,
                  vehiculos_compatibles TEXT,
                  ubicacion_taller TEXT)''')
    piezas_ejemplo = [
        ('Bujía', 'Produce chispa para encender el combustible', 'Motor', 'Toyota Corolla 2010-2015', 'Estante A1'),
        ('Filtro de Aceite', 'Filtra impurezas del aceite del motor', 'Filtros', 'Todos los modelos', 'Estante B2'),
        ('Disco de Freno', 'Disco metálico para frenar las ruedas', 'Frenos', 'Nissan Sentra 2015', 'Estante C3')
    ]
    c.executemany('INSERT OR IGNORE INTO piezas (nombre, descripcion, categoria, vehiculos_compatibles, ubicacion_taller) VALUES (?,?,?,?,?)', piezas_ejemplo)
    conn.commit()
    conn.close()


def buscar_en_inventario(descripcion):
    conn = sqlite3.connect('piezas.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM piezas 
                 WHERE nombre LIKE ? OR descripcion LIKE ? OR categoria LIKE ?''',
              (f'%{descripcion}%', f'%{descripcion}%', f'%{descripcion}%'))
    resultados = c.fetchall()
    conn.close()
    return resultados


# 🔹 Configuración de APIs
dotenv_path = r"E:\licenciatura Magaly\IA y Sistemas Expertos\Taller IA\.env"
load_dotenv(dotenv_path)

groq_api = os.getenv("GROQ_API_KEY")
gemini_api = os.getenv("GEMINI_API_KEY")

if not groq_api:
    raise ValueError("❌ Falta GROQ_API_KEY en el archivo .env")
if not gemini_api:
    raise ValueError("❌ Falta GEMINI_API_KEY en el archivo .env")

client_groq = Groq(api_key=groq_api)
genai.configure(api_key=gemini_api)


# 🔹 IA de texto (Groq)
def generar_descripcion_completa(nombre_pieza):
    """Genera 'qué es' y 'para qué sirve' usando Groq."""
    try:
        prompt = f"""
        Eres un experto en mecánica automotriz.
        Explica de forma técnica pero comprensible (máximo 4 párrafos por sección):
        1. Qué es la pieza automotriz llamada "{nombre_pieza}".
        2. Para qué sirve o cuál es su función principal.
        """

        response = client_groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Eres un mecánico experto en diagnóstico automotriz."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=500
        )

        texto = response.choices[0].message.content.strip()
        partes = re.split(r"(?i)\n\s*(?:2\.|2\)|para qué sirve|función principal)", texto, maxsplit=1)

        que_es = re.sub(r"(?i)^\s*1[\.\)]?\s*", "", partes[0]).strip() if partes else "No se pudo obtener información."
        para_que_sirve = partes[1].strip() if len(partes) > 1 else ""

        # Fallback si no vino "para qué sirve"
        if not para_que_sirve:
            try:
                prompt_fallback = f"Explica para qué sirve la pieza automotriz '{nombre_pieza}' en máximo 3 párrafos."
                resp2 = client_groq.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "Eres un mecánico experto en diagnóstico automotriz."},
                        {"role": "user", "content": prompt_fallback}
                    ],
                    temperature=0.6,
                    max_tokens=300
                )
                para_que_sirve = resp2.choices[0].message.content.strip()
            except Exception as e2:
                para_que_sirve = f"No se pudo obtener información. (Error fallback: {e2})"

        return {
            "pieza": nombre_pieza.title(),
            "que_es": que_es,
            "para_que_sirve": para_que_sirve,
            "encontrado": True
        }

    except Exception as e:
        return {
            "pieza": nombre_pieza.title(),
            "que_es": "No se pudo obtener información.",
            "para_que_sirve": f"Error: {str(e)}",
            "encontrado": False
        }


# 🔹 IA de imágenes (Gemini)
def analizar_imagen_pieza(imagen_base64):
    """Analiza imagen con Gemini Vision."""
    try:
        if imagen_base64.startswith("data:"):
            imagen_base64 = imagen_base64.split(",", 1)[1]

        imagen_bytes = base64.b64decode(imagen_base64)
        img = Image.open(BytesIO(imagen_bytes)).convert("RGB")

        model = genai.GenerativeModel("models/gemini-2.5-flash-image")
        prompt = (
            "Eres un mecánico experto. Analiza la imagen de una pieza automotriz y responde:\n"
            "1. Nombre más probable de la pieza.\n"
            "2. Qué es (máx. 4 párrafos).\n"
            "3. Para qué sirve (máx. 4 párrafos)."
        )

        try:
            response = model.generate_content([prompt, img])
            texto = getattr(response, "text", "").strip()
        except Exception:
            response = model.generate_content([
                prompt,
                {"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(imagen_bytes).decode()}}
            ])
            texto = getattr(response, "text", "").strip()

        partes = re.split(r"(?i)\n\s*(?:2\.|2\)|para qué sirve|función principal)", texto, maxsplit=1)
        que_es = re.sub(r"(?i)^\s*1[\.\)]?\s*", "", partes[0]).strip() if partes else ""
        para_que_sirve = partes[1].strip() if len(partes) > 1 else ""

        nombre_match = re.search(r"(?i)(?:^|\n)\s*(?:1\.|nombre|pieza)\s*[:\-]?\s*(.+)", texto)
        if nombre_match:
            posible_nombre = nombre_match.group(1).split("\n")[0].strip()
        else:
            posible_nombre = " ".join(que_es.split()[:4]).strip() or "Pieza detectada"

        if not para_que_sirve:
            fallback = generar_descripcion_completa(posible_nombre)
            return fallback

        return {"pieza": posible_nombre.title(), "que_es": que_es, "para_que_sirve": para_que_sirve}

    except Exception as e:
        return {"pieza": "Desconocida", "que_es": "No se pudo analizar la imagen.", "para_que_sirve": f"Error: {str(e)}"}


# 🔹 Rutas Flask
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/buscar', methods=['POST'])
def buscar():
    descripcion = request.form['descripcion'].strip()
    if not descripcion:
        return jsonify({'error': 'Por favor, describe la pieza'})
    resultados = buscar_en_inventario(descripcion)
    if not resultados:
        return jsonify({'mensaje': 'No se encontraron piezas que coincidan'})
    resultados_dict = [{'nombre': p[1], 'descripcion': p[2], 'categoria': p[3], 'vehiculos': p[4], 'ubicacion': p[5]} for p in resultados]
    return jsonify(resultados_dict)


@app.route('/descripcion', methods=['POST'])
def descripcion():
    nombre_pieza = request.form.get('nombre_pieza', '').strip()
    imagen_data = request.form.get('imagen', None)
    if imagen_data:
        resultado = analizar_imagen_pieza(imagen_data)
    elif nombre_pieza:
        resultado = generar_descripcion_completa(nombre_pieza)
    else:
        return jsonify({'error': 'Por favor, escribe el nombre o sube una imagen de la pieza'})
    return jsonify(resultado)


@app.route('/agregar_pieza', methods=['POST'])
def agregar_pieza():
    datos = request.form
    if not datos['nombre'] or not datos['ubicacion']:
        return jsonify({'error': 'Nombre y ubicación son obligatorios'})
    conn = sqlite3.connect('piezas.db')
    c = conn.cursor()
    c.execute('''INSERT INTO piezas (nombre, descripcion, categoria, vehiculos_compatibles, ubicacion_taller)
                 VALUES (?, ?, ?, ?, ?)''',
              (datos['nombre'], datos.get('descripcion', ''), datos.get('categoria', 'General'),
               datos.get('vehiculos', 'Varios modelos'), datos['ubicacion']))
    conn.commit()
    conn.close()
    return jsonify({'mensaje': '✅ Pieza agregada correctamente'})


if __name__ == '__main__':
    crear_base_datos()
    app.run(debug=True)
