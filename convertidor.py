import base64

ruta_imagen = "logo_consultora.jpg" # Asegúrate de que el nombre sea exacto

with open(ruta_imagen, "rb") as image_file:
    cadena_base64 = base64.b64encode(image_file.read()).decode('utf-8')
    print("COPIA LA SIGUIENTE LINEA:")
    print(cadena_base64)