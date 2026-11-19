import os
import sys
import json
import math
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

def dibujar_arbol(draw, data, posiciones, colores_nodos, aristas_activas, subtitulo, distancias_mostradas, fase_texto, titulo_graf="CS2023 - Diametro de un Arbol"):
    draw.rectangle([(0, 0), (1280, 720)], fill=(20, 24, 33))

    f_titulo = obtener_fuente(28)
    f_sub = obtener_fuente(20)
    f_nodo = obtener_fuente(20)
    f_dist = obtener_fuente(14)
    f_fase = obtener_fuente(18)

    draw.text((40, 25), titulo_graf, font=f_titulo, fill=(240, 246, 252))
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

def animar_escenario_arbol(data, posiciones, titulo_escena, carpeta_salida, frame_inicial):
    fotograma = frame_inicial
    n = data["n"]

    colores = {i: ((45, 55, 72), (160, 174, 192)) for i in range(n)}
    aristas_activas = set()
    distancias = {}

    for _ in range(35):
        img = Image.new("RGB", (1280, 720))
        draw = ImageDraw.Draw(img)
        dibujar_arbol(draw, data, posiciones, colores, aristas_activas,
                      "Propiedad: Desde cualquier nodo inicial s, el nodo mas lejano u es un extremo del diametro.",
                      distancias, f"{titulo_escena} - Estructura Inicial", titulo_escena)
        img.save(os.path.join(carpeta_salida, f"frame_{fotograma:04d}.png"))
        fotograma += 1

    bfs1 = data["bfs1"]
    inicio_bfs1 = bfs1["inicio"]
    orden1 = bfs1["orden_visita"]
    dists1 = bfs1["distancias"]

    for idx, u in enumerate(orden1):
        colores[u] = ((30, 144, 255), (255, 255, 255))
        distancias[u] = dists1[u]
        num_frames = 12 if idx > 0 else 20
        for _ in range(num_frames):
            img = Image.new("RGB", (1280, 720))
            draw = ImageDraw.Draw(img)
            sub = f"BFS 1: Visitando nodo {u} | Distancia acumulada desde origen = {dists1[u]}"
            dibujar_arbol(draw, data, posiciones, colores, aristas_activas, sub, distancias,
                          f"{titulo_escena} - Paso 1: BFS desde nodo {inicio_bfs1}", titulo_escena)
            img.save(os.path.join(carpeta_salida, f"frame_{fotograma:04d}.png"))
            fotograma += 1

    nodo_u = data["nodo_u"]
    colores[nodo_u] = ((245, 158, 11), (255, 255, 255))
    for _ in range(35):
        img = Image.new("RGB", (1280, 720))
        draw = ImageDraw.Draw(img)
        sub = f"Extremo encontrado: u = {nodo_u} (distancia maxima = {bfs1['distancia_max']})"
        dibujar_arbol(draw, data, posiciones, colores, aristas_activas, sub, distancias,
                      f"{titulo_escena} - Fin Paso 1: Primer extremo", titulo_escena)
        img.save(os.path.join(carpeta_salida, f"frame_{fotograma:04d}.png"))
        fotograma += 1

    colores = {i: ((45, 55, 72), (160, 174, 192)) for i in range(n)}
    colores[nodo_u] = ((245, 158, 11), (255, 255, 255))
    distancias = {nodo_u: 0}

    bfs2 = data["bfs2"]
    orden2 = bfs2["orden_visita"]
    dists2 = bfs2["distancias"]

    for idx, u in enumerate(orden2):
        if u != nodo_u:
            colores[u] = ((168, 85, 247), (255, 255, 255))
        distancias[u] = dists2[u]
        num_frames = 12 if idx > 0 else 20
        for _ in range(num_frames):
            img = Image.new("RGB", (1280, 720))
            draw = ImageDraw.Draw(img)
            sub = f"BFS 2: Visitando nodo {u} | Distancia desde extremo u({nodo_u}) = {dists2[u]}"
            dibujar_arbol(draw, data, posiciones, colores, aristas_activas, sub, distancias,
                          f"{titulo_escena} - Paso 2: BFS desde extremo u = {nodo_u}", titulo_escena)
            img.save(os.path.join(carpeta_salida, f"frame_{fotograma:04d}.png"))
            fotograma += 1

    nodo_v = data["nodo_v"]
    colores[nodo_v] = ((239, 68, 68), (255, 255, 255))
    for _ in range(35):
        img = Image.new("RGB", (1280, 720))
        draw = ImageDraw.Draw(img)
        sub = f"Extremo opuesto encontrado: v = {nodo_v} (distancia maxima = {bfs2['distancia_max']})"
        dibujar_arbol(draw, data, posiciones, colores, aristas_activas, sub, distancias,
                      f"{titulo_escena} - Fin Paso 2: Segundo extremo", titulo_escena)
        img.save(os.path.join(carpeta_salida, f"frame_{fotograma:04d}.png"))
        fotograma += 1

    camino = data["camino"]
    colores = {i: ((45, 55, 72), (160, 174, 192)) for i in range(n)}
    for nodo_c in camino:
        colores[nodo_c] = ((16, 185, 129), (255, 255, 255))
    colores[nodo_u] = ((245, 158, 11), (255, 255, 255))
    colores[nodo_v] = ((239, 68, 68), (255, 255, 255))

    for k in range(len(camino) - 1):
        aristas_activas.add((camino[k], camino[k + 1]))

    camino_str = " -> ".join(map(str, camino))
    for _ in range(60):
        img = Image.new("RGB", (1280, 720))
        draw = ImageDraw.Draw(img)
        sub = f"Camino: {camino_str} | Diametro = {data['diametro']} aristas"
        dibujar_arbol(draw, data, posiciones, colores, aristas_activas, sub, distancias,
                      f"{titulo_escena} - Paso 3: Camino Diametral", titulo_escena)
        img.save(os.path.join(carpeta_salida, f"frame_{fotograma:04d}.png"))
        fotograma += 1

    return fotograma

def generar_fotogramas(data_general, data_estrella, carpeta_salida):
    if os.path.exists(carpeta_salida):
        shutil.rmtree(carpeta_salida)
    os.makedirs(carpeta_salida, exist_ok=True)

    fotograma = 0
    f_intro_t = obtener_fuente(42)
    f_intro_s = obtener_fuente(24)
    f_intro_b = obtener_fuente(20)

    for _ in range(55):
        img = Image.new("RGB", (1280, 720), color=(15, 20, 28))
        draw = ImageDraw.Draw(img)
        draw.text((150, 140), "Algoritmos y Estructuras de Datos", font=f_intro_s, fill=(88, 166, 255))
        draw.text((150, 190), "Diametro de un Arbol", font=f_intro_t, fill=(255, 255, 255))
        draw.text((150, 260), "Algoritmo de los dos BFS en tiempo lineal O(V)", font=f_intro_s, fill=(234, 179, 8))
        draw.line([(150, 310), (1130, 310)], fill=(55, 65, 81), width=2)
        
        draw.text((150, 340), "Integrante:", font=f_intro_s, fill=(255, 255, 255))
        draw.text((180, 385), "- Gracia Luz Mendoza Palacios", font=f_intro_b, fill=(201, 209, 217))
        
        draw.text((150, 470), "Profesor: Luciano A. Romero Calla", font=f_intro_b, fill=(156, 163, 175))
        draw.text((150, 510), "Semestre 2026-2", font=f_intro_b, fill=(110, 118, 129))
        img.save(os.path.join(carpeta_salida, f"frame_{fotograma:04d}.png"))
        fotograma += 1

    posiciones_general = {
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

    fotograma = animar_escenario_arbol(data_general, posiciones_general,
                                       "Instancia Ilustrativa: Arbol General",
                                       carpeta_salida, fotograma)

    if data_estrella:
        posiciones_estrella = {0: (640, 360)}
        radio_estrella = 180
        for i in range(1, 6):
            angulo = -math.pi / 2 + (i - 1) * (2 * math.pi / 5)
            posiciones_estrella[i] = (
                int(640 + radio_estrella * math.cos(angulo)),
                int(360 + radio_estrella * math.sin(angulo))
            )

        for _ in range(40):
            img = Image.new("RGB", (1280, 720), color=(15, 20, 28))
            draw = ImageDraw.Draw(img)
            draw.text((150, 240), "Demostracion de Caso de Borde", font=f_intro_t, fill=(255, 255, 255))
            draw.line([(150, 310), (1130, 310)], fill=(55, 65, 81), width=2)
            draw.text((150, 340), "Grafo Estrella (Star Graph) con N = 6 nodos", font=f_intro_s, fill=(88, 166, 255))
            draw.text((150, 390), "Todas las hojas estan a distancia 1 del centro (nodo 0).", font=f_intro_b, fill=(201, 209, 217))
            draw.text((150, 430), "El diametro siempre es 2, conectando cualesquiera dos hojas.", font=f_intro_b, fill=(234, 179, 8))
            img.save(os.path.join(carpeta_salida, f"frame_{fotograma:04d}.png"))
            fotograma += 1

        fotograma = animar_escenario_arbol(data_estrella, posiciones_estrella,
                                           "Caso de Borde: Grafo Estrella",
                                           carpeta_salida, fotograma)

    for _ in range(55):
        img = Image.new("RGB", (1280, 720), color=(15, 20, 28))
        draw = ImageDraw.Draw(img)
        draw.text((150, 130), "Analisis de Complejidad Temporal y Espacial", font=f_intro_t, fill=(255, 255, 255))
        draw.line([(150, 195), (1130, 195)], fill=(55, 65, 81), width=2)
        
        draw.text((150, 230), "1. Primer BFS (desde nodo arbitrario s):", font=f_intro_s, fill=(88, 166, 255))
        draw.text((200, 275), "O(V + E) = O(N + N - 1) = O(N)", font=f_intro_b, fill=(201, 209, 217))

        draw.text((150, 335), "2. Segundo BFS (desde extremo u):", font=f_intro_s, fill=(168, 85, 247))
        draw.text((200, 380), "O(V + E) = O(N + N - 1) = O(N)", font=f_intro_b, fill=(201, 209, 217))

        draw.text((150, 440), "3. Reconstruccion del camino:", font=f_intro_s, fill=(16, 185, 129))
        draw.text((200, 485), "O(D) <= O(N), donde D es el diametro", font=f_intro_b, fill=(201, 209, 217))

        draw.text((150, 550), "Tiempo total: O(N) lineal  |  Memoria auxiliar: O(N)", font=f_intro_s, fill=(234, 179, 8))
        img.save(os.path.join(carpeta_salida, f"frame_{fotograma:04d}.png"))
        fotograma += 1

    for _ in range(45):
        img = Image.new("RGB", (1280, 720), color=(15, 20, 28))
        draw = ImageDraw.Draw(img)
        draw.text((450, 220), "Creditos del Proyecto", font=f_intro_t, fill=(255, 255, 255))
        draw.line([(380, 290), (900, 290)], fill=(55, 65, 81), width=2)
        draw.text((420, 320), "Algoritmos y Estructuras de Datos", font=f_intro_s, fill=(88, 166, 255))
        draw.text((460, 370), "Gracia Luz Mendoza Palacios", font=f_intro_b, fill=(201, 209, 217))
        draw.text((450, 450), "Profesor: Luciano A. Romero Calla", font=f_intro_b, fill=(156, 163, 175))
        draw.text((560, 490), "Semestre 2026-2", font=f_intro_b, fill=(110, 118, 129))
        img.save(os.path.join(carpeta_salida, f"frame_{fotograma:04d}.png"))
        fotograma += 1

    return fotograma

def generar_subtitulos(ruta_srt):
    subtitulos = [
        ("00:00:00,000", "00:00:02,300", "Proyecto 2: Diametro de un Arbol. Integrante: Gracia Luz Mendoza Palacios."),
        ("00:00:02,300", "00:00:04,500", "El diametro es la distancia maxima entre dos nodos cualesquiera en un arbol no ponderado."),
        ("00:00:04,500", "00:00:09,000", "Paso 1: Iniciamos un primer BFS desde el nodo 0 para ubicar el vertice u mas alejado."),
        ("00:00:09,000", "00:00:11,000", "Fin de fase 1: Se identifica el vertice extremo u = 8 a distancia 4."),
        ("00:00:11,000", "00:00:15,500", "Paso 2: Iniciamos un segundo BFS partiendo desde el vertice extremo u = 8."),
        ("00:00:15,500", "00:00:17,500", "Fin de fase 2: Se identifica el vertice opuesto v = 5 a distancia maxima 6."),
        ("00:00:17,500", "00:00:20,500", "Paso 3: Se reconstruye el camino diametral de 6 aristas: 8, 7, 4, 1, 0, 2 y 5."),
        ("00:00:20,500", "00:00:22,500", "Caso de borde: Analizamos un grafo estrella con un nodo central y hojas."),
        ("00:00:22,500", "00:00:26,500", "El algoritmo ejecuta los dos BFS en el grafo estrella encontrando el diametro igual a 2."),
        ("00:00:26,500", "00:00:29,000", "Analisis de complejidad: Dos recorridos BFS lineales toman tiempo O(V + E) = O(N)."),
        ("00:00:29,000", "00:00:31,000", "Creditos finales del proyecto. CS2023 Algoritmos y Estructuras de Datos.")
    ]
    with open(ruta_srt, "w", encoding="utf-8") as f:
        for idx, (inicio, fin, texto) in enumerate(subtitulos, 1):
            f.write(f"{idx}\n{inicio} --> {fin}\n{texto}\n\n")

def main():
    ruta_traza_general = "output/traza.json"
    ruta_traza_estrella = "output/traza_estrella.json"

    if not os.path.exists(ruta_traza_general):
        subprocess.run(["make", "run"])

    with open(ruta_traza_general, "r") as f:
        data_general = json.load(f)

    data_estrella = None
    if os.path.exists(ruta_traza_estrella):
        with open(ruta_traza_estrella, "r") as f:
            data_estrella = json.load(f)

    carpeta_fotogramas = "output/fotogramas"
    fps = 24
    generar_fotogramas(data_general, data_estrella, carpeta_fotogramas)

    video_salida = "output/video_diametro.mp4"

    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", f"{carpeta_fotogramas}/frame_%04d.png",
        "-c:v", "libopenh264",
        "-pix_fmt", "yuv420p",
        video_salida
    ]

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        cmd_fallback = [
            "ffmpeg", "-y",
            "-framerate", str(fps),
            "-i", f"{carpeta_fotogramas}/frame_%04d.png",
            "-c:v", "mpeg4",
            "-pix_fmt", "yuv420p",
            video_salida
        ]
        res = subprocess.run(cmd_fallback, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if res.returncode == 0:
        print(f"Video generado exitosamente: {video_salida}")
        shutil.rmtree(carpeta_fotogramas, ignore_errors=True)
    else:
        print("Error al generar el video con ffmpeg")
        sys.exit(1)

    ruta_srt = "output/subtitulos.srt"
    generar_subtitulos(ruta_srt)
    print(f"Subtitulos sincronizados generados en: {ruta_srt}")

if __name__ == "__main__":
    main()
