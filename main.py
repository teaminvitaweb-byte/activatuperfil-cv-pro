import json
import os
import time
import docx
from pypdf import PdfReader
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError
from scripts.generate_docx import render_exact_cv_layout

# Cargar variables de entorno desde .env
load_dotenv()

# Cargar dinámicamente CUALQUIER API Key definida en el .env que empiece por GEMINI_API_KEY
API_KEYS = [
    value for key, value in os.environ.items() 
    if key.startswith("GEMINI_API_KEY") and value.strip()
]

# Eliminar duplicados manteniendo el orden
API_KEYS = list(dict.fromkeys(API_KEYS))

if not API_KEYS:
    raise ValueError("❌ No se encontró ninguna API Key en el archivo .env (asegúrate de definirlas como GEMINI_API_KEY_1, GEMINI_API_KEY_2, etc.)")

print(f"🔑 Se cargaron {len(API_KEYS)} API Key(s) desde el entorno.")

SYSTEM_PROMPT = """
Eres un reclutador ejecutivo y experto en optimización de CVs para filtros ATS y selección de personal.
TU OBJETIVO: Analizar el CV proporcionado y transformarlo según el perfil/área que el usuario solicita.

REGLAS DE ORO STRICTAS (CERO TOLERANCIA A DATOS INVENTADOS):
1. NUNCA inventes, deduzcas ni asumas información que no esté explícitamente en el CV original.
   - NO inventes nombres de empresas, puestos, títulos académicos, fechas, ubicaciones, herramientas, certificados ni métricas ficticias.
   - Si el usuario no proporcionó teléfono, LinkedIn o correo, deja esos campos vacíos.
2. TU TRABAJO ES EXCLUSIVAMENTE REORGANIZAR Y MEJORAR LA REDACCIÓN:
   - Utiliza verbos de acción y vocabulario corporativo de alto impacto.
   - Optimiza la sintaxis para pasar filtros ATS usando palabras clave del puesto objetivo.
   - Traduce funciones pasivas a logros redactados de forma profesional, PERO usando únicamente los hechos descritos por el candidato.
3. Debes responder ESTRICTAMENTE con un objeto JSON válido sin texto adicional ni bloques de Markdown fuera del JSON.

Estructura requerida del JSON:
{
  "diagnostico": {
    "puntos_fuertes": ["..."],
    "mejoras_aplicadas": ["..."]
  },
  "datos_cv": {
    "nombre": "...",
    "titulo": "...",
    "foto_path": "",
    "telefono": "...",
    "email": "...",
    "linkedin": "...",
    "ubicacion": "...",
    "habilidades": ["..."],
    "idiomas": [{"nombre": "...", "nivel": "..."}],
    "educacion": [{"titulo": "...", "institucion": "...", "estado": "...", "detalle": "..."}],
    "perfil": "...",
    "experiencia": [{"cargo": "...", "empresa": "...", "periodo": "...", "responsabilidades": ["..."]}],
    "informacion_adicional": "...",
    "referencias": "..."
  }
}
"""

def cargar_texto_cv(ruta_archivo: str) -> str:
    """Lee el texto del CV desde un archivo (.txt, .docx o .pdf)."""
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"❌ No se encontró el archivo en esta ruta: {ruta_archivo}")

    extension = os.path.splitext(ruta_archivo)[1].lower()

    if extension == ".txt":
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            return f.read()
    elif extension == ".docx":
        doc = docx.Document(ruta_archivo)
        return "\n".join([p.text for p in doc.paragraphs if p.text])
    elif extension == ".pdf":
        reader = PdfReader(ruta_archivo)
        texto = []
        for page in reader.pages:
            t = page.extract_text()
            if t:
                texto.append(t)
        return "\n".join(texto)
    else:
        raise ValueError("❌ Formato no soportado. Usa un archivo .txt, .docx o .pdf")

def solicitar_ia_resistente(prompt_usuario: str, max_intentos_503: int = 6) -> str:
    """Intenta procesar la solicitud alternando entre las API Keys si falla por cuota (429),
    y reintentando pacientemente si el servidor está saturado (503).
    """
    modelo = "gemini-3.8-flash"

    for idx, key in enumerate(API_KEYS, start=1):
        print(f"🔑 Probando con API Key #{idx}...")
        client = genai.Client(api_key=key)

        chat = client.chats.create(
            model=modelo,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.2,
                response_mime_type="application/json"
            )
        )

        for intento in range(1, max_intentos_503 + 1):
            try:
                print(f"🔄 Conectando con {modelo} (Intento {intento}/{max_intentos_503})...")
                response = chat.send_message(prompt_usuario)
                return response.text
            except APIError as e:
                if e.code == 429:
                    print(f"⚠️ La API Key #{idx} agotó su cuota (429). Cambiando a la siguiente clave...")
                    break  # Pasa a la siguiente API Key
                elif e.code == 503:
                    espera = intento * 6
                    print(f"⚠️ Servidor saturado (503). Pausando {espera}s (reintento {intento}/{max_intentos_503})...")
                    time.sleep(espera)
                else:
                    raise e
            except Exception as e:
                if "429" in str(e):
                    print(f"⚠️ Cuota agotada en API Key #{idx}. Cambiando a la siguiente clave...")
                    break
                elif "503" in str(e):
                    espera = intento * 6
                    print(f"⚠️ Servidor ocupado (503). Pausando {espera}s...")
                    time.sleep(espera)
                else:
                    raise e

    raise RuntimeError("❌ No se pudo completar la solicitud. Verifica que tus API Keys tengan cuota y que los servidores de Google estén respondiendo.")

def optimizar_y_generar_cv(texto_cv_original: str, enfilado_a: str, output_docx: str, foto_path: str = ""):
    print("\n⏳ Analizando CV y optimizando redacción con la IA...")

    prompt_usuario = f"""
    CV ORIGINAL DEL CANDIDATO:
    {texto_cv_original}

    OBJETIVO DEL PERFIL / PUESTO DESEADO:
    {enfilado_a}
    """

    respuesta_json_raw = solicitar_ia_resistente(prompt_usuario)
    resultado = json.loads(respuesta_json_raw)

    if foto_path:
        resultado["datos_cv"]["foto_path"] = foto_path

    # Diagnóstico Express
    print("\n" + "="*50)
    print("📊 DIAGNÓSTICO EXPRESS DEL CV")
    print("="*50)
    print("\n✅ Puntos Fuertes Identificados:")
    for pf in resultado["diagnostico"]["puntos_fuertes"]:
        print(f"  • {pf}")

    print("\n✏️ Mejoras Aplicadas:")
    for ma in resultado["diagnostico"]["mejoras_aplicadas"]:
        print(f"  • {ma}")
    print("="*50 + "\n")

    # Guardar copia en JSON
    os.makedirs("output", exist_ok=True)
    with open("output/datos_generados.json", "w", encoding="utf-8") as f:
        json.dump(resultado["datos_cv"], f, ensure_ascii=False, indent=2)

    # Renderizar Word
    render_exact_cv_layout(resultado["datos_cv"], output_docx)
    print(f"🚀 ¡CV generado con éxito en: {os.path.abspath(output_docx)}!")

if __name__ == "__main__":
    print("--- 💼 ACTIVATUPERFIL CV PRO ---")
    
    ruta_cv = input("Escriba la ruta del CV original (.pdf, .docx o .txt): ").strip('"')
    puesto_objetivo = input("Puesto o área objetivo (ej. Soporte Técnico, Administrador): ")
    ruta_foto = input("Ruta de la foto (Opcional, presione Enter para omitir): ").strip('"')

    nombre_salida = "output/cv_optimizado.docx"

    try:
        texto_original = cargar_texto_cv(ruta_cv)
        optimizar_y_generar_cv(
            texto_cv_original=texto_original,
            enfilado_a=puesto_objetivo,
            output_docx=nombre_salida,
            foto_path=ruta_foto
        )
    except Exception as e:
        print(f"\n❌ Error: {e}")