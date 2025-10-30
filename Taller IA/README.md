🔧 Asistente Inteligente para Taller Automotriz

Sistema de identificación y análisis de piezas automotrices con inteligencia artificial integrada (Google Gemini 2.5 Flash).
Desarrollado en Flask (Python) con reconocimiento de texto e imagen.

🚀 Características Principales

🤖 IA Automotriz Avanzada:
Describe cualquier pieza automotriz y explica qué es y para qué sirve, con lenguaje técnico y claro.

📸 Análisis por Imagen:
Permite subir una foto de una pieza; la IA la analiza e identifica su nombre y función.

💡 Interfaz Moderna y Responsiva:
Diseño limpio y accesible desde navegador, ideal para talleres o estudiantes de mecánica automotriz.

🧩 Librerías Usadas y Su Función
Librería	Descripción
flask	Framework web ligero que permite crear la aplicación del servidor y las rutas para manejar peticiones desde el navegador.
google.generativeai	SDK oficial de Google para conectarse con los modelos de IA Gemini (texto e imágenes). Permite enviar prompts y recibir respuestas generadas.
os	Módulo estándar de Python que permite acceder a variables del sistema, como la clave API guardada en .env.
dotenv (python-dotenv)	Carga automáticamente las variables del archivo .env (como la clave GOOGLE_API_KEY) al entorno del programa.
PIL (Pillow)	Librería de procesamiento de imágenes. Se usa para abrir, validar y convertir imágenes antes de enviarlas al modelo de IA.
io	Permite manejar archivos en memoria (por ejemplo, convertir una imagen subida a flujo binario antes de procesarla).
base64	Se usa para codificar la imagen en texto Base64, formato requerido por la API de Gemini para interpretar imágenes.
🛠️ Instalación Paso a Paso
1️⃣ Requisitos Previos

Python 3.8 o superior → Descargar

Visual Studio Code → Descargar

2️⃣ Extensiones Recomendadas para VS Code

Instala estas extensiones desde el Marketplace:

Python (Microsoft)

Pylance

SQLite

Auto Rename Tag

Live Server

3️⃣ Instalación de Dependencias

En la terminal, dentro del proyecto:

pip install flask google-generativeai python-dotenv pillow

4️⃣ Estructura del Proyecto
Taller_IA/
│
├── app.py                 # Aplicación principal Flask (con integración Gemini)
├── .env                   # Clave privada para Gemini API
├── templates/
│   └── index.html         # Interfaz web con formulario e IA
└── static/
    └── style.css          # Estilos CSS del sitio

5️⃣ Configuración del Archivo .env

Crea un archivo llamado .env en la raíz del proyecto y añade tu clave de Google AI Studio:

GOOGLE_API_KEY=tu_clave_aqui


⚠️ Reemplaza tu_clave_aqui por tu clave real desde https://aistudio.google.com

6️⃣ Ejecutar la Aplicación
python app.py


Luego abre en tu navegador:

http://localhost:5000

🎯 Cómo Usar el Sistema

Escribe el nombre de una pieza (por ejemplo: “bujía”, “sensor MAP”, “amortiguador”).

O sube una imagen clara de la pieza.

Presiona “Obtener Descripción”.

La IA analizará el contenido y mostrará:

Pregunta	Respuesta generada por la IA
❓ ¿Qué es?	Describe la pieza.
🎯 ¿Para qué sirve?	Explica su función y aplicación técnica.
💡 Ejemplos de Uso
Entrada	Resultado
“amortiguador”	Componente de suspensión que absorbe impactos y estabiliza el vehículo.
“bomba de agua”	Circula el refrigerante para mantener la temperatura del motor.
“filtro de aire”	Limpia el aire que entra al motor y evita daños internos.
⚙️ Integración con Gemini API

Fragmento del código principal (app.py):

import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = "gemini-2.5-flash"

response = genai.GenerativeModel(model).generate_content([
    "Explica qué es un alternador y para qué sirve en un automóvil."
])

print(response.text)

🧩 Solución de Problemas

❌ “Error 404 model not found”
→ Usa uno de los modelos disponibles, como gemini-2.5-flash o gemini-2.5-pro.

❌ “Quota exceeded”
→ Has superado el límite gratuito. Espera 24 horas antes de volver a usar la API.

❌ “El sistema no reconoce la imagen”
→ Asegúrate de que el archivo sea .jpg, .jpeg o .png y tenga buena calidad visual.

📂 Archivos Clave
Archivo	Descripción
app.py	Lógica principal de Flask e integración con Gemini.
index.html	Interfaz web para subir imágenes y mostrar resultados.
style.css	Diseño visual del sistema.
.env	Almacena tu clave privada de Google AI.