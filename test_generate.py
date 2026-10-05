import os
from scripts.generate_docx import render_exact_cv_layout

# Datos ficticios completos para prueba
datos_cv = {
    "nombre": "Francisco Berríos",
    "titulo": "Especialista en Operaciones & Gestión Estratégica",
    "foto_path": r"C:\Users\DelmyG\Downloads\foto.jpeg",
    "telefono": "+503 7123-4567",
    "email": "francisco.berrios@email.com",
    "linkedin": "https://www.linkedin.com/in/francisco-berr%C3%ADos-24rb2498/",
    "ubicacion": "San Salvador, El Salvador",
    "habilidades": [
        "Gestión de Proyectos",
        "Análisis de Datos",
        "Optimización de Procesos",
        "Liderazgo de Equipos",
        "Estrategia Comercial",
        "Microsoft Office Advanced"
    ],
    "idiomas": [
        {"nombre": "Español", "nivel": "Nativo"},
        {"nombre": "Inglés", "nivel": "Intermedio | Conversación, Lectura y Escritura"}
    ],
    "educacion": [
        {
            "titulo": "Licenciatura en Administración de Empresas",
            "institucion": "Universidad Centroamericana José Simeón Cañas",
            "estado": "Graduado (2020)"
        },
        {
            "titulo": "Bachillerato General",
            "institucion": "Colegio Santa Cruz",
            "estado": "2015",
            "detalle": "Graduado con honores académicos."
        }
    ],
    "perfil": "Profesional enfocado en la optimización de procesos operativos y la mejora continua. Con experiencia en la coordinación de proyectos multidisciplinarios, análisis de datos para la toma de decisiones y gestión de equipos orientados a resultados.",
    "experiencia": [
        {
            "cargo": "Coordinador de Operaciones",
            "empresa": "Logística & Servicios S.A. de C.V.",
            "periodo": "2021 - Presente",
            "responsabilidades": [
                "Supervisión y optimización de las operaciones diarias del área administrativa.",
                "Implementación de nuevos flujos de trabajo reduciendo tiempos de entrega en un 15%.",
                "Elaboración de reportes ejecutivos de rendimiento y control de presupuesto."
            ]
        },
        {
            "cargo": "Analista de Procesos Jr.",
            "empresa": "Soluciones Corporativas",
            "periodo": "2018 - 2021",
            "responsabilidades": [
                "Documentación y estandarización de procedimientos operativos.",
                "Apoyo en el seguimiento de KPI clave del departamento."
            ]
        }
    ],
    "informacion_adicional": "Disponibilidad inmediata.",
    "referencias": "Referencias profesionales disponibles a solicitud."
}

if __name__ == "__main__":
    output_path = "output/cv_francisco_berrios.docx"
    render_exact_cv_layout(datos_cv, output_path)
    print(f"¡Documento generado exitosamente en: {os.path.abspath(output_path)}!")