import os
import sys
import json
import shutil
import subprocess
from PIL import Image, ImageDraw, ImageFont

def obtener_fuente(tamano):
    rutas = [
        "/usr/share/fonts/google-droid-sans-fonts/DroidSans.ttf",
        "/usr/share/fonts/adwaita-sans-fonts/AdwaitaSans-Regular.ttf",
        "/usr/share/fonts/google-carlito-fonts/Carlito-Bold.ttf"
    ]
    for r in rutas:
        if os.path.exists(r):
            try:
                return ImageFont.truetype(r, tamano)
            except Exception:
                pass
    return ImageFont.load_default()

def dibujar_arbol(draw, data, posiciones, colores_nodos, aristas_activas, subtitulo, distancias_mostradas, fase_texto):
    draw.rectangle([(0, 0), (1280, 720)], fill=(20, 24, 33))

    f_titulo = obtener_fuente(28)
    f_sub = obtener_fuente(20)
    f_nodo = obtener_fuente(20)
    f_dist = obtener_fuente(14)
    f_fase = obtener_fuente(18)

    draw.text((40, 25), "CS2023 - Diametro de un Arbol", font=f_titulo, fill=(240, 246, 252))
    draw.text((40, 65), fase_texto, font=f_fase, fill=(88, 166, 255))
    draw.text((40, 95), subtitulo, font=f_sub, fill=(201, 209, 217))

    for u, v in data["aristas"]:
        p1 = posiciones[u]
        p2 = posiciones[v]
        es_activa = (u, v) in aristas_activas or (v, u) in aristas_activas
        if es_activa:
            color_linea = (234, 179, 8)
            grosor = 6
        else:
            color_linea = (75, 85, 99)
            grosor = 3
        draw.line([p1, p2], fill=color_linea, width=grosor)

    radio = 24
    for i in range(data["n"]):
        x, y = posiciones[i]
        c_relleno, c_borde = colores_nodos.get(i, ((45, 55, 72), (160, 174, 192)))
        
        draw.ellipse([(x - radio, y - radio), (x + radio, y + radio)], fill=c_relleno, outline=c_borde, width=3)
        
        texto_nodo = str(i)
        bbox = draw.textbbox((0, 0), texto_nodo, font=f_nodo)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((x - tw / 2, y - th / 2 - 2), texto_nodo, font=f_nodo, fill=(255, 255, 255))

        if i in distancias_mostradas:
            d_val = distancias_mostradas[i]
            d_txt = f"d={d_val}"
            bbox_d = draw.textbbox((0, 0), d_txt, font=f_dist)
            dw = bbox_d[2] - bbox_d[0]
            draw.text((x - dw / 2, y + radio + 5), d_txt, font=f_dist, fill=(229, 231, 235))

    draw.rectangle([(40, 650), (1240, 695)], fill=(30, 36, 48), outline=(55, 65, 81), width=1)
    f_pie = obtener_fuente(16)
    draw.text((60, 663), "Gris: sin visitar | Azul: BFS 1 | Violeta: BFS 2 | Naranja/Rojo: Extremos | Amarillo: Camino", font=f_pie, fill=(156, 163, 175))

def generar_fotogramas(data, carpeta_salida):
    if os.path.exists(carpeta_salida):
        shutil.rmtree(carpeta_salida)
    os.makedirs(carpeta_salida, exist_ok=True)

    posiciones = {
        0: (640, 180),
        1: (440, 290),
        2: (840, 290),
        3: (320, 410),
        4: (540, 410),
        5: (740, 410),
        6: (960, 410),
        7: (540, 520),
        8: (540, 620)
    }

    fotograma = 0

    f_intro_t = obtener_fuente(44)
    f_intro_s = obtener_fuente(26)
    f_intro_b = obtener_fuente(20)

    for _ in range(60):
        img = Image.new("RGB", (1280, 720), color=(15, 20, 28))
        draw = ImageDraw.Draw(img)
        draw.text((200, 200), "CS2023 - Algoritmos y Estructuras de Datos", font=f_intro_s, fill=(88, 166, 255))
        draw.text((200, 260), "Diametro de un Arbol", font=f_intro_t, fill=(255, 255, 255))
        draw.text((200, 350), "Algoritmo de los dos BFS en tiempo O(V + E)", font=f_intro_s, fill=(234, 179, 8))
        draw.text((200, 420), "Proyecto 2 - Integrantes del Grupo", font=f_intro_b, fill=(156, 163, 175))
        draw.line([(200, 325), (1080, 325)], fill=(55, 65, 81), width=2)
        img.save(os.path.join(carpeta_salida, f"frame_{fotograma:04d}.png"))
        fotograma += 1

    colores = {i: ((45, 55, 72), (160, 174, 192)) for i in range(data["n"])}
    aristas_activas = set()
    distancias = {}

    for _ in range(40):
        img = Image.new("RGB", (1280, 720))
        draw = ImageDraw.Draw(img)
        dibujar_arbol(draw, data, posiciones, colores, aristas_activas,
                      "El diametro es la mayor distancia en aristas entre dos nodos cualesquiera.",
                      distancias, "Definicion del problema")
        img.save(os.path.join(carpeta_salida, f"frame_{fotograma:04d}.png"))
        fotograma += 1

    bfs1 = data["bfs1"]
    inicio_bfs1 = bfs1["inicio"]
    orden1 = bfs1["orden_visita"]
    dists1 = bfs1["distancias"]

    for idx, u in enumerate(orden1):
        colores[u] = ((30, 144, 255), (255, 255, 255))
        distancias[u] = dists1[u]
        num_frames = 15 if idx > 0 else 25
        for _ in range(num_frames):
            img = Image.new("RGB", (1280, 720))
            draw = ImageDraw.Draw(img)
            sub = f"Visitando nodo {u} | Distancia calculada = {dists1[u]}"
            dibujar_arbol(draw, data, posiciones, colores, aristas_activas, sub, distancias,
                          f"Paso 1: Primer BFS desde el nodo {inicio_bfs1}")
            img.save(os.path.join(carpeta_salida, f"frame_{fotograma:04d}.png"))
            fotograma += 1

    nodo_u = data["nodo_u"]
    colores[nodo_u] = ((245, 158, 11), (255, 255, 255))
    for _ in range(45):
        img = Image.new("RGB", (1280, 720))
        draw = ImageDraw.Draw(img)
        sub = f"Nodo mas lejano alcanzado: u = {nodo_u} (distancia maxima = {bfs1['distancia_max']})"
        dibujar_arbol(draw, data, posiciones, colores, aristas_activas, sub, distancias,
                      "Fin del Paso 1: Primer extremo encontrado")
        img.save(os.path.join(carpeta_salida, f"frame_{fotograma:04d}.png"))
        fotograma += 1

    colores = {i: ((45, 55, 72), (160, 174, 192)) for i in range(data["n"])}
    colores[nodo_u] = ((245, 158, 11), (255, 255, 255))
    distancias = {nodo_u: 0}

    bfs2 = data["bfs2"]
    orden2 = bfs2["orden_visita"]
    dists2 = bfs2["distancias"]

    for idx, u in enumerate(orden2):
        if u != nodo_u:
            colores[u] = ((168, 85, 247), (255, 255, 255))
        distancias[u] = dists2[u]
        num_frames = 15 if idx > 0 else 25
        for _ in range(num_frames):
            img = Image.new("RGB", (1280, 720))
            draw = ImageDraw.Draw(img)
            sub = f"Visitando nodo {u} | Distancia desde nodo {nodo_u} = {dists2[u]}"
            dibujar_arbol(draw, data, posiciones, colores, aristas_activas, sub, distancias,
                          f"Paso 2: Segundo BFS desde el extremo u = {nodo_u}")
            img.save(os.path.join(carpeta_salida, f"frame_{fotograma:04d}.png"))
            fotograma += 1

    nodo_v = data["nodo_v"]
    colores[nodo_v] = ((239, 68, 68), (255, 255, 255))
    for _ in range(45):
        img = Image.new("RGB", (1280, 720))
        draw = ImageDraw.Draw(img)
        sub = f"Nodo mas lejano alcanzado: v = {nodo_v} (distancia maxima = {bfs2['distancia_max']})"
        dibujar_arbol(draw, data, posiciones, colores, aristas_activas, sub, distancias,
                      "Fin del Paso 2: Segundo extremo encontrado")
        img.save(os.path.join(carpeta_salida, f"frame_{fotograma:04d}.png"))
        fotograma += 1

    camino = data["camino"]
    colores = {i: ((45, 55, 72), (160, 174, 192)) for i in range(data["n"])}
    for nodo_c in camino:
        colores[nodo_c] = ((16, 185, 129), (255, 255, 255))
    colores[nodo_u] = ((245, 158, 11), (255, 255, 255))
    colores[nodo_v] = ((239, 68, 68), (255, 255, 255))

    for k in range(len(camino) - 1):
        aristas_activas.add((camino[k], camino[k + 1]))

    camino_str = " -> ".join(map(str, camino))
    for _ in range(75):
        img = Image.new("RGB", (1280, 720))
        draw = ImageDraw.Draw(img)
        sub = f"Camino: {camino_str} | Diametro = {data['diametro']} aristas"
        dibujar_arbol(draw, data, posiciones, colores, aristas_activas, sub, distancias,
                      f"Paso 3: Camino diametral (Longitud = {data['diametro']})")
        img.save(os.path.join(carpeta_salida, f"frame_{fotograma:04d}.png"))
        fotograma += 1

    for _ in range(60):
        img = Image.new("RGB", (1280, 720), color=(15, 20, 28))
        draw = ImageDraw.Draw(img)
        draw.text((150, 140), "Analisis de Complejidad", font=f_intro_t, fill=(255, 255, 255))
        draw.line([(150, 210), (1130, 210)], fill=(55, 65, 81), width=2)
        
        draw.text((150, 250), "1. Primer BFS desde nodo inicial:", font=f_intro_s, fill=(88, 166, 255))
        draw.text((200, 295), "O(V + E) = O(N + N - 1) = O(N)", font=f_intro_b, fill=(201, 209, 217))

        draw.text((150, 360), "2. Segundo BFS desde nodo u:", font=f_intro_s, fill=(168, 85, 247))
        draw.text((200, 405), "O(V + E) = O(N + N - 1) = O(N)", font=f_intro_b, fill=(201, 209, 217))

        draw.text((150, 470), "3. Reconstruccion del camino:", font=f_intro_s, fill=(16, 185, 129))
        draw.text((200, 515), "O(D) <= O(N), donde D es el diametro", font=f_intro_b, fill=(201, 209, 217))

        draw.text((150, 580), "Tiempo total: O(N) lineal  |  Memoria auxiliar: O(N)", font=f_intro_s, fill=(234, 179, 8))

        img.save(os.path.join(carpeta_salida, f"frame_{fotograma:04d}.png"))
        fotograma += 1

    return fotograma

def main():
    ruta_traza = "output/traza.json"
    if not os.path.exists(ruta_traza):
        print(f"Error: no se encontro {ruta_traza}")
        print("Ejecuta primero: make run")
        sys.exit(1)

    with open(ruta_traza, "r") as f:
        data = json.load(f)

    carpeta_fotogramas = "output/fotogramas"
    total_frames = generar_fotogramas(data, carpeta_fotogramas)

    video_salida = "output/video_diametro.mp4"
    
    cmd = [
        "ffmpeg", "-y",
        "-framerate", "24",
        "-i", f"{carpeta_fotogramas}/frame_%04d.png",
        "-c:v", "libopenh264",
        "-pix_fmt", "yuv420p",
        video_salida
    ]
    
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        cmd_fallback = [
            "ffmpeg", "-y",
            "-framerate", "24",
            "-i", f"{carpeta_fotogramas}/frame_%04d.png",
            "-c:v", "mpeg4",
            "-pix_fmt", "yuv420p",
            video_salida
        ]
        res = subprocess.run(cmd_fallback, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if res.returncode == 0:
        print(f"Video generado en: {video_salida}")
        shutil.rmtree(carpeta_fotogramas)
    else:
        print("Error al generar el video con ffmpeg")
        sys.exit(1)

if __name__ == "__main__":
    main()
