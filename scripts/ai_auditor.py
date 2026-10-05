import os
import json
import time
from google import genai
from google.genai import types

def auditar_cv_con_ia(texto_cv: str) -> dict:
    """
    Analiza el CV usando gemini-3.8-flash.
    Incluye reintentos para manejar picos de demanda (error 503).
    """
    prompt_path = os.path.join("prompt_templates", "cv_audit_prompt.txt")
    
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_template = f.read()

    # Reemplazo seguro sin interferir con las llaves del JSON
    prompt = prompt_template.replace("{texto_cv}", texto_cv)

    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # Reintentos automáticos para lidiar con el error 503 (servidor saturado)
    max_intentos = 3
    for intento in range(1, max_intentos + 1):
        try:
            print(f"🔄 Conectando con Gemini (gemini-3.8-flash) - Intento {intento}/{max_intentos}...")
            
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.1,
                    tools=[]  # Desactiva AFC para evitar advertencias en consola
                )
            )

            if response and response.text:
                return json.loads(response.text)

        except Exception as e:
            err_msg = str(e)
            if "503" in err_msg or "UNAVAILABLE" in err_msg:
                print(f"⚠️ Servidor ocupado (503). Reintentando en 4 segundos...")
                time.sleep(4)
            else:
                print(f"❌ Error en la llamada a Gemini: {e}")
                break

    return {}