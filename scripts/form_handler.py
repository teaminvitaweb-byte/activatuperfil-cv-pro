import os

def capturar_o_completar_datos(diagnostico_ia=None) -> dict:
    datos = {
        "nombre": "",
        "titulo": "",
        "telefono": "",
        "email": "",
        "ubicacion": "",
        "foto_path": "",
        "perfil": "",
        "experiencia": [],
        "educacion": [],
        "habilidades": []
    }

    # Si hay datos de la IA los precargamos
    if diagnostico_ia and "datos" in diagnostico_ia:
        ia_data = diagnostico_ia["datos"]
        datos.update({k: v for k, v in ia_data.items() if v})

    print("\n--- DATOS PERSONALES Y FOTO ---")
    if not datos["nombre"]:
        datos["nombre"] = input("Nombre completo: ").strip()
    
    foto_input = input("Ruta de fotografía (.jpg / .png) [Presiona Enter para omitir]: ").strip().strip('"')
    if foto_input and os.path.exists(foto_input):
        datos["foto_path"] = foto_input
    else:
        if foto_input:
            print("⚠️ Archivo de imagen no encontrado. Se generará el CV sin foto.")

    if not datos["titulo"]:
        datos["titulo"] = input("Título profesional / Cargo objetivo: ").strip()
    if not datos["telefono"]:
        datos["telefono"] = input("Teléfono de contacto: ").strip()
    if not datos["email"]:
        datos["email"] = input("Correo electrónico: ").strip()
    if not datos["ubicacion"]:
        datos["ubicacion"] = input("Ubicación (Ciudad, País): ").strip()

    if not datos["perfil"]:
        datos["perfil"] = input("\nPerfil profesional / Resumen ejecutivo: ").strip()

    # Si no hay experiencia cargada de IA, pedir al menos una
    if not datos["experiencia"]:
        print("\n--- EXPERIENCIA LABORAL ---")
        while True:
            cargo = input("\nCargo / Puesto: ").strip()
            if not cargo:
                break
            empresa = input("Empresa: ").strip()
            periodo = input("Período (Ej: 2021 - Presente): ").strip()
            resps = []
            print("Ingresa responsabilidades/logros (línea en blanco para terminar):")
            while True:
                resp = input("  • ").strip()
                if not resp:
                    break
                resps.append(resp)
            
            datos["experiencia"].append({
                "cargo": cargo,
                "empresa": empresa,
                "periodo": periodo,
                "responsabilidades": resps
            })

            mas = input("¿Deseas agregar otra experiencia? (s/n): ").strip().lower()
            if mas != 's':
                break

    # Si no hay educación cargada
    if not datos["educacion"]:
        print("\n--- EDUCACIÓN ---")
        while True:
            titulo = input("\nTítulo o Carrera: ").strip()
            if not titulo:
                break
            inst = input("Institución educativa: ").strip()
            estado = input("Estado / Año (Ej: Graduado, En curso): ").strip()
            
            datos["educacion"].append({
                "titulo": titulo,
                "institucion": inst,
                "estado": estado
            })

            mas = input("¿Deseas agregar otra formación académica? (s/n): ").strip().lower()
            if mas != 's':
                break

    # Si no hay habilidades
    if not datos["habilidades"]:
        print("\n--- HABILIDADES ---")
        habs = input("Ingresa tus habilidades separadas por comas: ").strip()
        if habs:
            datos["habilidades"] = [h.strip() for h in habs.split(",") if h.strip()]

    return datos