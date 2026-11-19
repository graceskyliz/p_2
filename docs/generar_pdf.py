import os
import sys
from PIL import Image, ImageDraw, ImageFont

def obtener_fuentes():
    rutas_bold = [
        "/usr/share/fonts/google-droid-sans-fonts/DroidSans-Bold.ttf",
        "/usr/share/fonts/google-carlito-fonts/Carlito-Bold.ttf"
    ]
    rutas_reg = [
        "/usr/share/fonts/google-droid-sans-fonts/DroidSans.ttf",
        "/usr/share/fonts/adwaita-sans-fonts/AdwaitaSans-Regular.ttf"
    ]
    fb = None
    for r in rutas_bold:
        if os.path.exists(r):
            fb = r
            break
    fr = None
    for r in rutas_reg:
        if os.path.exists(r):
            fr = r
            break

    def get_f(bold, size):
        r = fb if bold else fr
        if r:
            try:
                return ImageFont.truetype(r, size)
            except Exception:
                pass
        return ImageFont.load_default()

    return get_f

def envolver_texto(texto, font, max_ancho, draw):
    palabras = texto.split(" ")
    lineas = []
    linea_actual = ""
    for p in palabras:
        prueba = (linea_actual + " " + p).strip()
        bbox = draw.textbbox((0, 0), prueba, font=font)
        ancho = bbox[2] - bbox[0]
        if ancho <= max_ancho:
            linea_actual = prueba
        else:
            if linea_actual:
                lineas.append(linea_actual)
            linea_actual = p
    if linea_actual:
        lineas.append(linea_actual)
    return lineas

def dibujar_encabezado_pagina(draw, num_pag, get_f):
    draw.rectangle([(80, 50), (1160, 52)], fill=(31, 78, 121))
    f_header = get_f(False, 12)
    draw.text((80, 32), "CS2023 - Algoritmos y Estructuras de Datos | Proyecto 2: Diametro de un Arbol", font=f_header, fill=(100, 100, 100))
    f_pie = get_f(False, 12)
    draw.rectangle([(80, 1690), (1160, 1692)], fill=(210, 215, 220))
    draw.text((80, 1700), "Autores: Gracia Luz Mendoza Palacios", font=f_pie, fill=(100, 100, 100))
    draw.text((1080, 1700), f"Pagina {num_pag} de 4", font=f_pie, fill=(100, 100, 100))

def crear_pagina_1(get_f):
    img = Image.new("RGB", (1240, 1754), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    dibujar_encabezado_pagina(draw, 1, get_f)

    draw.rectangle([(80, 75), (1160, 205)], fill=(245, 248, 252), outline=(180, 205, 230), width=1)
    f_tit = get_f(True, 24)
    f_sub = get_f(True, 15)
    f_meta = get_f(False, 13)

    draw.text((105, 90), "Proyecto 2: Calculo y Animacion del Diametro de un Arbol", font=f_tit, fill=(31, 78, 121))
    draw.text((105, 125), "Algoritmo lineal de dos recorridos BFS e implementacion didactica", font=f_sub, fill=(50, 50, 50))
    draw.text((105, 155), "Integrantes: Gracia Luz Mendoza Palacios", font=f_meta, fill=(40, 40, 40))
    draw.text((105, 175), "Profesor: Luciano A. Romero Calla | Periodo Academico: 2026-2", font=f_meta, fill=(90, 90, 90))

    y = 230
    f_sec = get_f(True, 16)
    f_txt = get_f(False, 13)
    f_txt_b = get_f(True, 13)

    draw.text((80, y), "1. Introduccion y Motivacion", font=f_sec, fill=(31, 78, 121))
    y += 28

    parrafos_1 = [
        "En teoria de grafos y diseno de redes de computadoras, un arbol es un grafo no dirigido conexo y sin ciclos. Numerosas arquitecturas reales, tales como los protocolos de arbol de expansion (Spanning Tree Protocol en estandares IEEE 802.1D) en redes de area local (LAN), configuran deliberadamente las conexiones activas en forma de arbol para erradicar tormentas de difusion (broadcast storms) y paquetes en bucle infinito.",
        "Dentro de este modelo, surge una pregunta tecnica fundamental: Cual es el retardo maximo en el peor caso para que un paquete viaje entre dos terminales cualesquiera de la infraestructura? Esta metrica equivale de manera exacta al Diametro de un Arbol: la distancia maxima (medida en cantidad de aristas o saltos) entre cualquier par de nodos.",
        "El calculo eficiente del diametro cumple un papel crucial en:",
        "  - Acotar superiormente la latencia maxima de transporte y convergencia en redes de paquetes.",
        "  - Identificar el centro del arbol (nodo que minimiza la distancia maxima al resto) para ubicar servidores centrales, bases de datos o conmutadores de alta disponibilidad de forma geometricamente optima.",
        "  - Evaluar la robustez y dispersion morfologica de estructuras jerarquicas en sistemas distribuidos."
    ]

    for p in parrafos_1:
        lineas = envolver_texto(p, f_txt, 1080, draw)
        for l in lineas:
            draw.text((80, y), l, font=f_txt, fill=(30, 30, 30))
            y += 20
        y += 8

    y += 10
    draw.text((80, y), "2. Definicion Formal del Problema y ADT Arbol", font=f_sec, fill=(31, 78, 121))
    y += 28

    parrafos_2 = [
        "Sea T = (V, E) un arbol libre no ponderado con |V| = n vertices y |E| = n - 1 aristas. Como T es conexo y aciclico, existe exactamente un camino simple unico entre cada par de vertices u, v pertenecientes a V. Se define la funcion de distancia d(u, v) como el numero de aristas que componen dicho camino simple.",
        "El Diametro del Arbol, denotado por D(T), se formaliza como el maximo de todas las distancias finitas entre pares de nodos:",
        "                                     D(T) = max { d(u, v) : u, v en V }",
        "El Tipo de Dato Abstracto (ADT) Arbol implementado en el lenguaje C++17 soporta las siguientes operaciones fundamentales:",
        "  - Arbol(vertices): Inicializa la estructura asignando n vertices numerados de 0 a n - 1.",
        "  - agregarArista(u, v): Inserta una arista no dirigida bidireccional entre u y v en tiempo O(1).",
        "  - cargarDesdeArchivo(ruta): Lee desde un archivo de texto la dimension n y la lista de aristas.",
        "  - ejecutarBFS(inicio): Realiza un recorrido en anchura devolviendo las distancias y los nodos predecesores.",
        "  - calcularDiametro(inicio): Ejecuta el algoritmo de dos etapas y devuelve el diametro junto con la ruta diametral.",
        "  - exportarTraza(ruta, res): Vuelca en un archivo JSON la secuencia completa de exploracion para su posterior animacion."
    ]

    for p in parrafos_2:
        lineas = envolver_texto(p, f_txt, 1080, draw)
        for l in lineas:
            draw.text((80, y), l, font=f_txt, fill=(30, 30, 30))
            y += 20
        y += 8

    return img

def crear_pagina_2(get_f):
    img = Image.new("RGB", (1240, 1754), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    dibujar_encabezado_pagina(draw, 2, get_f)

    y = 80
    f_sec = get_f(True, 16)
    f_txt = get_f(False, 13)
    f_txt_b = get_f(True, 13)

    draw.text((80, y), "3. Algoritmo de Doble Recorrido BFS", font=f_sec, fill=(31, 78, 121))
    y += 28

    parrafos_3 = [
        "Un enfoque ingenuo (fuerza bruta) ejecutaria busquedas desde cada uno de los vertices del arbol para determinar todas las distancias entre pares, lo cual incurriria en una complejidad cuadratica O(V^2) o cubica O(V^3) si se utilizara Floyd-Warshall. Para arboles no ponderados, existe un algoritmo optimo que calcula el diametro en dos unicos recorridos BFS en tiempo O(V):",
        "Paso 1: Se selecciona un vertice arbitrario inicial s (por ejemplo, el vertice 0). Se ejecuta un primer recorrido BFS calculando el arreglo de distancias desde s hacia todos los demas nodos. Al finalizar, se identifica el vertice u con la mayor distancia registrada: u = argmax { d(s, x) : x en V }.",
        "Paso 2: Se inicia un segundo recorrido BFS tomando a u como vertice origen. Se computan las distancias desde u hacia todo el grafo y se almacena el vector de padres (predecesores). Se determina el nodo v que maximiza la distancia desde u: v = argmax { d(u, x) : x en V }.",
        "Paso 3: El valor d(u, v) representa exactamente el diametro del arbol. La reconstruccion del camino diametral se realiza de manera determinista retrocediendo por el arreglo de predecesores desde v hasta alcanzar u."
    ]

    for p in parrafos_3:
        lineas = envolver_texto(p, f_txt, 1080, draw)
        for l in lineas:
            draw.text((80, y), l, font=f_txt, fill=(30, 30, 30))
            y += 20
        y += 8

    y += 10
    draw.text((80, y), "4. Justificacion Teorica y Demostracion de Correccion", font=f_sec, fill=(31, 78, 121))
    y += 28

    parrafos_4 = [
        "Teorema Fundamental: En cualquier arbol libre no ponderado T, si elegimos un nodo arbitrario s y encontramos el nodo u mas alejado de s, entonces u es necesariamente un vertice extremo de al menos un camino diametral de T.",
        "Demostracion por contradiccion:",
        "Sea A-B un camino diametral de longitud maxima D = d(A, B). Supongamos por el absurdo que u no es un extremo de ningun diametro. Al ser T conexo y libre de ciclos, el camino que une el nodo de partida s con u debe coincidir o intersectarse en algun nodo w con el camino diametral A-B.",
        "Dado que u maximiza la distancia desde s, se cumple d(s, u) >= d(s, A) y d(s, u) >= d(s, B). Restando la distancia comun d(s, w), se deduce de forma directa que d(w, u) >= d(w, A) y d(w, u) >= d(w, B).",
        "Consideremos ahora la ruta simple formada entre u y el extremo mas alejado de w en el diametro (sin perdida de generalidad, B). La longitud de este nuevo camino seria d(u, w) + d(w, B) >= d(A, w) + d(w, B) = d(A, B) = D.",
        "Si la desigualdad fuera estricta, habriamos construido un camino simple de longitud mayor que D, contradiciendo la definicion de que D era el diametro maximo. Si la igualdad se cumple, el camino u-B posee longitud D, lo que convierte a u en un extremo diametral valido. Por lo tanto, u es forzosamente un extremo de un diametro. Finalmente, el segundo BFS desde u explora todo el arbol y encuentra de manera obligatoria el extremo opuesto v con longitud D."
    ]

    for p in parrafos_4:
        lineas = envolver_texto(p, f_txt, 1080, draw)
        for l in lineas:
            draw.text((80, y), l, font=f_txt, fill=(30, 30, 30))
            y += 20
        y += 8

    y += 10
    draw.text((80, y), "5. Analisis de Complejidad Temporal y Espacial", font=f_sec, fill=(31, 78, 121))
    y += 28

    draw.rectangle([(80, y), (1160, y + 175)], fill=(250, 252, 255), outline=(200, 215, 230), width=1)
    y_box = y + 15
    f_code = get_f(True, 12)

    draw.text((105, y_box), "Fase Algoritmica                Complejidad Temporal        Justificacion Operacional", font=f_code, fill=(31, 78, 121))
    y_box += 22
    draw.line([(105, y_box), (1135, y_box)], fill=(200, 215, 230), width=1)
    y_box += 10

    filas_c = [
        ("Primer BFS (desde s)", "O(|V| + |E|) = O(N)", "Visita cada vertice y arista una unica vez (|E| = N - 1)"),
        ("Identificacion extremo u", "O(N)", "Busqueda lineal del maximo valor en el vector de distancias"),
        ("Segundo BFS (desde u)", "O(|V| + |E|) = O(N)", "Explora todas las ramas partiendo desde el extremo hallado"),
        ("Identificacion extremo v", "O(N)", "Busqueda lineal del maximo valor en el segundo vector"),
        ("Reconstruccion camino", "O(D) <= O(N)", "Recorrido inverso mediante punteros del arreglo de padres"),
        ("Complejidad Total Temporal", "O(N)", "Tiempo global lineal estrictamente optimo"),
        ("Complejidad Espacial Auxiliar", "O(N)", "Listas de adyacencia (2N-2), distancias (N), padres (N), cola (N)")
    ]

    for fase, comp, just in filas_c:
        f_b = f_txt_b if "Total" in fase or "Espacial" in fase else f_txt
        draw.text((105, y_box), f"{fase:<30} {comp:<26} {just}", font=f_b, fill=(20, 20, 20))
        y_box += 18

    return img

def crear_pagina_3(get_f):
    img = Image.new("RGB", (1240, 1754), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    dibujar_encabezado_pagina(draw, 3, get_f)

    y = 80
    f_sec = get_f(True, 16)
    f_txt = get_f(False, 13)
    f_txt_b = get_f(True, 13)

    draw.text((80, y), "6. Arquitectura del Software e Implementacion", font=f_sec, fill=(31, 78, 121))
    y += 28

    parrafos_6 = [
        "El proyecto se organiza bajo una separacion funcional en dos capas independientes conectadas mediante un protocolo determinista de exportacion:",
        "1. Motor Algoritmico en C++ (src/): Implementa la estructura Arbol mediante vectores dinamicos de adyacencia std::vector<std::vector<int>>, el algoritmo de doble BFS y la exportacion en JSON de los eventos de visita, distancias acumuladas y el camino diametral final. Cumple con la exigencia academica de que la animacion provenga de una ejecucion algoritmica autentica y no simulada a mano.",
        "2. Generador Grafico y Multimedia en Python (animacion/): Lee las trazas JSON generadas por el ejecutable de C++, calcula las posiciones espaciales de los nodos (disposicion jerarquica para arboles generales y distribucion polar para grafos estrella), renderiza los fotogramas vectoriales en Pillow y ensambla el video final MP4 a 24 fps mediante FFmpeg, produciendo ademas un archivo de subtitulos sincronizados SRT."
    ]

    for p in parrafos_6:
        lineas = envolver_texto(p, f_txt, 1080, draw)
        for l in lineas:
            draw.text((80, y), l, font=f_txt, fill=(30, 30, 30))
            y += 20
        y += 8

    y += 10
    draw.text((80, y), "7. Caso de Borde: Grafo Estrella (Star Graph)", font=f_sec, fill=(31, 78, 121))
    y += 28

    parrafos_7 = [
        "Para validar la generalidad del algoritmo, se analizo y animo de forma explicita el caso de borde del Grafo Estrella con N = 6 nodos. En esta topologia, un unico vertice central (nodo 0) posee grado N - 1 = 5, y todos los vertices restantes son hojas de grado 1 directamente conectadas a el.",
        "Cualidades analiticas del caso estrella:",
        "  - La distancia entre el centro y cualquier hoja es exactamente 1.",
        "  - La distancia entre cualesquiera dos hojas distintas es siempre 1 + 1 = 2.",
        "  - Por lo tanto, para cualquier grafo estrella con N >= 3, el diametro es invariablemente D = 2, sin importar el tamano de N.",
        "  - El algoritmo de doble BFS maneja este caso con precision: si el primer BFS parte de una hoja (nodo 1), el nodo mas distante hallado es otra hoja (nodo 2) a distancia 2; el segundo BFS desde el nodo 2 halla como extremo opuesto cualquier otra hoja a distancia 2, reconstruyendo el camino diametral 2 -> 0 -> 1 sin inconsistencias."
    ]

    for p in parrafos_7:
        lineas = envolver_texto(p, f_txt, 1080, draw)
        for l in lineas:
            draw.text((80, y), l, font=f_txt, fill=(30, 30, 30))
            y += 20
        y += 8

    y += 10
    draw.text((80, y), "8. Matriz de Pruebas Unitarias y Validacion Experimental", font=f_sec, fill=(31, 78, 121))
    y += 28

    draw.rectangle([(80, y), (1160, y + 215)], fill=(255, 255, 255), outline=(200, 215, 230), width=1)
    y_t = y + 12
    draw.rectangle([(81, y + 1), (1159, y + 30)], fill=(240, 245, 250))
    draw.text((95, y_t), "Prueba  Caso Evaluado                  Vertices  Aristas  Diametro Esperado  Diametro Obtenido  Estado", font=get_f(True, 12), fill=(31, 78, 121))
    y_t += 25

    pruebas = [
        ("T1", "Un solo nodo (Caso base trivial)", "1", "0", "0", "0", "PASS"),
        ("T2", "Dos nodos con una arista", "2", "1", "1", "1", "PASS"),
        ("T3", "Grafo estrella (Caso de borde)", "6", "5", "2", "2", "PASS"),
        ("T4", "Grafo linea (Cadena simple)", "5", "4", "4", "4", "PASS"),
        ("T5", "Arbol binario simetrico completo", "7", "6", "4", "4", "PASS"),
        ("T6", "Arbol asimetrico general", "9", "8", "6", "6", "PASS"),
        ("T7", "Carga dinamica desde archivos", "9 y 6", "8 y 5", "6 y 2", "6 y 2", "PASS")
    ]

    for p_id, desc, v, e, de, dob, st in pruebas:
        draw.text((95, y_t), f"{p_id:<7} {desc:<32} {v:<9} {e:<8} {de:<18} {dob:<18} {st}", font=get_f(False, 12), fill=(30, 30, 30))
        y_t += 24

    return img

def crear_pagina_4(get_f):
    img = Image.new("RGB", (1240, 1754), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    dibujar_encabezado_pagina(draw, 4, get_f)

    y = 80
    f_sec = get_f(True, 16)
    f_txt = get_f(False, 13)
    f_txt_b = get_f(True, 13)

    draw.text((80, y), "9. Herramientas Utilizadas y Requisitos del Sistema", font=f_sec, fill=(31, 78, 121))
    y += 28

    parrafos_9 = [
        "El entorno de desarrollo requiere herramientas estandar multiplataforma:",
        "  - Compilador C++: g++ compatible con el estandar C++17 (flags -Wall -Wextra -O2).",
        "  - Lenguaje de Scripting: Python 3.8 o superior.",
        "  - Biblioteca de Renderizado Grafico: Pillow (PIL) version 10+ para dibujo vectorial de fotogramas y generacion de documentos PDF.",
        "  - Codificador Multimedia: FFmpeg con codificador libopenh264 o mpeg4.",
        "  - Pista de Subtitulos: Generacion de archivo SRT sincronizado para acompañar la presentacion."
    ]

    for p in parrafos_9:
        lineas = envolver_texto(p, f_txt, 1080, draw)
        for l in lineas:
            draw.text((80, y), l, font=f_txt, fill=(30, 30, 30))
            y += 20
        y += 8

    y += 10
    draw.text((80, y), "10. Instrucciones para Reproducir el Proyecto", font=f_sec, fill=(31, 78, 121))
    y += 28

    draw.rectangle([(80, y), (1160, y + 175)], fill=(248, 250, 252), outline=(210, 220, 230), width=1)
    y_b = y + 12
    draw.text((95, y_b), "1. Ejecutar la bateria completa de pruebas unitarias", font=get_f(True, 12), fill=(100, 100, 100))
    y_b += 20
    draw.text((95, y_b), "make test", font=get_f(True, 13), fill=(31, 78, 121))
    y_b += 28
    draw.text((95, y_b), "2. Compilar el programa principal en C++ y exportar las trazas", font=get_f(True, 12), fill=(100, 100, 100))
    y_b += 20
    draw.text((95, y_b), "make run", font=get_f(True, 13), fill=(31, 78, 121))
    y_b += 28
    draw.text((95, y_b), "3. Generar la animacion completa en video MP4 y subtitulos", font=get_f(True, 12), fill=(100, 100, 100))
    y_b += 20
    draw.text((95, y_b), "make video", font=get_f(True, 13), fill=(31, 78, 121))
    y += 195

    draw.text((80, y), "11. Contribuciones Individuales de los Integrantes", font=f_sec, fill=(31, 78, 121))
    y += 28

    parrafos_11 = [
        "Gracia Luz Mendoza Palacios (100% de contribucion):",
        "  - Diseno e implementacion en C++ de la clase Arbol con listas de adyacencia dinamicas.",
        "  - Implementacion del algoritmo de doble BFS y algoritmo de reconstruccion del camino diametral.",
        "  - Desarrollo de la suite de pruebas unitarias (tests/test_arbol.cpp) para casos normales y de borde.",
        "  - Redaccion de la fundamentacion matematica, demostracion de correccion y analisis de complejidad del informe.",
        "  - Diseno del motor de renderizado grafico en Python (animacion/animador.py) y disposicion espacial de nodos.",
        "  - Modelado y visualizacion del caso de borde en estrella y diseno de leyendas visuales.",
        "  - Generacion del pipeline de codificacion multimedia en FFmpeg y subtitulos sincronizados SRT.",
        "  - Elaboracion de la documentacion README.md, automatizacion en Makefile y estructura de entrega."
    ]

    for p in parrafos_11:
        lineas = envolver_texto(p, f_txt, 1080, draw)
        for l in lineas:
            draw.text((80, y), l, font=f_txt, fill=(30, 30, 30))
            y += 20
        y += 6

    y += 10
    draw.text((80, y), "12. Conclusiones", font=f_sec, fill=(31, 78, 121))
    y += 28

    conclusiones = [
        "1. El algoritmo de doble BFS demostro una eficiencia optima O(V) tanto en la teoria como en la practica, resolviendo el diametro de arboles en tiempo lineal sin requerir tecnicas complejas de programacion dinamica ni matrices de distancia.",
        "2. La demostracion geometrica por contradiccion confirma que la propiedad de los extremos diametrales es rigurosa y universal para cualquier arbol conexo no dirigido no ponderado.",
        "3. La arquitectura desacoplada C++ -> JSON -> Python permitio respetar de forma estricta el requerimiento academico de que la animacion visual este impulsada por una implementacion real de la estructura de datos."
    ]

    for c in conclusiones:
        lineas = envolver_texto(c, f_txt, 1080, draw)
        for l in lineas:
            draw.text((80, y), l, font=f_txt, fill=(30, 30, 30))
            y += 20
        y += 6

    return img

def main():
    print("Generando informe tecnico final en formato PDF (4 paginas)...")
    get_f = obtener_fuentes()

    p1 = crear_pagina_1(get_f)
    p2 = crear_pagina_2(get_f)
    p3 = crear_pagina_3(get_f)
    p4 = crear_pagina_4(get_f)

    ruta_pdf = "docs/informe_final.pdf"
    p1.save(ruta_pdf, "PDF", resolution=150.0, save_all=True, append_images=[p2, p3, p4])
    print(f"Informe PDF generado exitosamente en: {ruta_pdf}")

if __name__ == "__main__":
    main()
