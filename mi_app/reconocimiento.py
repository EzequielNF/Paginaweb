import os
import sys
import django
import json
import uuid
import numpy as np
import cv2
from PIL import Image
import face_recognition
from threading import Timer

# Inicializar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_app.settings')
django.setup()

from account.models import Persona

# Función para eliminar el JSON después de 5 segundos
def eliminar_json(ruta):
    if os.path.exists(ruta):
        os.remove(ruta)
        print(f"[🧹] Archivo JSON eliminado: {ruta}")

# Función para cargar rostros desde la base de datos
def cargar_rostros_autorizados():
    print("\n🔍 Cargando rostros autorizados desde la base de datos...")
    codificaciones = []
    usuarios = Persona.objects.all()
    rostros = []

    for user in usuarios:
        if not user.foto:
            print(f"[!] Usuario {user.nombre} {user.apellido} no tiene foto asignada")
            continue

        ruta_foto = user.foto.path
        if os.path.exists(ruta_foto):
            try:
                imagen_pil = Image.open(ruta_foto).convert("RGB")
                imagen = np.array(imagen_pil)
                codificacion = face_recognition.face_encodings(imagen)
                if codificacion:
                    codificaciones.append(codificacion[0])
                    rostros.append(user)
                    print(f"[✔] Registrado: {user.nombre} {user.apellido}")
                else:
                    print(f"[✖] No se detectó rostro en {ruta_foto}")
            except Exception as e:
                print(f"[✖] Error procesando {ruta_foto}: {e}")
        else:
            print(f"[!] No se encontró el archivo: {ruta_foto}")

    return codificaciones, rostros

# Función principal de reconocimiento facial
def reconocimiento_en_vivo(codificaciones_autorizadas, usuarios_autorizados):
    print("\n🎥 Iniciando cámara para reconocimiento facial en vivo...")
    cap = cv2.VideoCapture(0)
    acceso_permitido = False

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[!] No se pudo capturar imagen de la cámara")
            break

        frame_pequeño = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_pequeño = cv2.cvtColor(frame_pequeño, cv2.COLOR_BGR2RGB)

        ubicaciones = face_recognition.face_locations(rgb_pequeño)
        codificaciones = face_recognition.face_encodings(rgb_pequeño, ubicaciones)

        for codificacion, ubicacion in zip(codificaciones, ubicaciones):
            coincidencias = face_recognition.compare_faces(codificaciones_autorizadas, codificacion)
            nombre = "Desconocido"

            distancias = face_recognition.face_distance(codificaciones_autorizadas, codificacion)
            if len(distancias) > 0:
                mejor_match = np.argmin(distancias)
                if coincidencias[mejor_match]:
                    usuario = usuarios_autorizados[mejor_match]
                    nombre = f"{usuario.nombre} {usuario.apellido}"

                    y1, x2, y2, x1 = [v * 4 for v in ubicacion]
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, nombre, (x1, y2 + 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    print(f"[✅] Acceso permitido a: {nombre}")
                    acceso_permitido = True

                    # Guardar imagen
                    if not os.path.exists("logs"):
                        os.makedirs("logs")
                    nombre_archivo = f"{uuid.uuid4().hex}.jpg"
                    ruta_archivo = os.path.join("logs", nombre_archivo)
                    cv2.imwrite(ruta_archivo, frame)

                    # Crear JSON
                    json_path = "ultimo_acceso.json"
                    with open(json_path, "w", encoding="utf-8") as f:
                        json.dump({
                            "nombre": usuario.nombre,
                            "apellido": usuario.apellido,
                            "numero_casa": usuario.numero_casa,
                            "tipo": usuario.tipo,
                            "vehiculo": usuario.vehiculo,
                            "patente": usuario.patente if usuario.patente else "",
                            "foto": usuario.foto.url if usuario.foto else "",
                            "imagen_acceso": f"/media/logs/{nombre_archivo}"
                        }, f, ensure_ascii=False, indent=4)

                    # Programar eliminación del JSON
                    Timer(5.0, eliminar_json, args=[json_path]).start()

                    cv2.imshow("Reconocimiento Facial Condominio", frame)
                    cv2.waitKey(2000)
                    break

        cv2.imshow("Reconocimiento Facial Condominio", frame)

        if acceso_permitido:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Saliendo...")
            break

    cap.release()
    cv2.destroyAllWindows()

# Bloque principal
if __name__ == "__main__":
    print("[🚀] Iniciando sistema de reconocimiento facial...")
    codificaciones, usuarios = cargar_rostros_autorizados()
    if codificaciones:
        reconocimiento_en_vivo(codificaciones, usuarios)
    else:
        print("[⚠️] No se encontraron rostros autorizados.")
