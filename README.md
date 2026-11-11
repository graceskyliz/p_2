# CS2023 - Algoritmos y Estructuras de Datos (2026-2)
## Proyecto 2: Animando Estructuras de Datos
### Tema Asignado: Diámetro de un Árbol (Avance al 50%)

---

## 1. Introducción y Descripción del Problema

El **diámetro de un árbol** es la longitud del camino simple más largo entre cualquier par de nodos pertenecientes al árbol. En un árbol no ponderado, esta longitud corresponde al número total de aristas que conectan ambos extremos.

Encontrar el diámetro de manera ingenua mediante la búsqueda de caminos entre todos los pares de nodos tomaría $O(V^2)$ o $O(V^3)$. Sin embargo, aprovechando la propiedad acíclica y conexa de los árboles, es posible calcularlo en tiempo estrictamente lineal $O(V + E) = O(V)$ mediante dos recorridos BFS (o DFS):

1. **Primer BFS:** Se inicia en un nodo arbitrario $s$. Se calcula la distancia a todos los nodos y se identifica el nodo más alejado $u$.
2. **Segundo BFS:** Se inicia en el nodo $u$. Se calcula la distancia hacia todos los nodos y se identifica el nodo más alejado $v$.
3. **Resultado:** La distancia entre $u$ y $v$ es exactamente el diámetro del árbol, y el camino recorrido entre ambos corresponde al camino diametral.

---

## 2. Estado del Proyecto: Hito del 50% (Avance)

Este repositorio corresponde a la entrega intermedia del **50% del proyecto** (fecha de avance: 11 de noviembre de 2026), cumpliendo con los siguientes objetivos:

- [x] Estructura de datos `Arbol` implementada en C++ con lista de adyacencia.
- [x] Algoritmo de doble BFS implementado en C++ para encontrar el diámetro y reconstruir el camino.
- [x] Generación y exportación de trazas de ejecución en formato estructurado JSON (`output/traza.json`).
- [x] Suite de pruebas unitarias (`tests/test_arbol.cpp`) cubriendo casos base y casos de borde.
- [x] Prototipo funcional del generador de animación educativa (`animacion/animador.py`) usando Pillow y FFmpeg.
- [x] Generación del video educativo preliminar en MP4 (`output/video_diametro.mp4`).
- [x] Documentación técnica e informe de avance de 50% (`docs/informe_avance_50.md`).

---

## 3. Estructura del Repositorio

```text
proyecto_2/
├── aed_project_2.md         # Especificaciones oficiales del proyecto
├── Makefile                 # Automatización de compilación y ejecución
├── README.md                # Presentación general y guía de uso
├── .gitignore               # Archivos excluidos del control de versiones
├── docs/
│   └── informe_avance_50.md # Informe técnico del avance del 50%
├── src/
│   ├── Arbol.hpp            # Definición de la clase Arbol y estructuras
│   ├── Arbol.cpp            # Implementación de métodos y algoritmo
│   └── main.cpp             # Demostración y exportación de traza
├── tests/
│   └── test_arbol.cpp       # Pruebas unitarias de casos de borde
├── animacion/
│   └── animador.py          # Script de renderizado y generación de video MP4
└── output/
    ├── traza.json           # Traza generada por el motor C++
    └── video_diametro.mp4   # Video de la animación generada
```

---

## 4. Requisitos del Sistema

Para compilar y ejecutar el proyecto se requieren las siguientes herramientas estándar:

- **Compilador C++:** `g++` con soporte para C++17.
- **Python:** Versión 3.8 o superior.
- **Librería de imágenes:** `Pillow` (`pip install Pillow`).
- **Codificador multimedia:** `ffmpeg` disponible en el `PATH` del sistema.

---

## 5. Instrucciones de Compilación y Ejecución

### 5.1 Compilar y ejecutar el programa principal en C++
```bash
make run
```
Este comando compila el proyecto y ejecuta `main`, el cual calcula el diámetro de un árbol de ejemplo y genera el archivo `output/traza.json`.

### 5.2 Ejecutar la suite de pruebas unitarias
```bash
make test
```
Ejecuta las pruebas automatizadas que verifican la corrección del algoritmo ante casos de borde:
- Árbol de un solo nodo ($N=1$).
- Árbol de dos nodos ($N=2$).
- Grafo estrella.
- Grafo camino / línea.
- Árbol binario completo simétrico.
- Árbol asimétrico arbitrario.

### 5.3 Generar el video educativo completo
```bash
make video
```
Este comando compila la lógica en C++, ejecuta el algoritmo para producir la traza y dispara el generador gráfico en Python para renderizar los fotogramas y ensamblar `output/video_diametro.mp4`.

### 5.4 Limpiar archivos generados
```bash
make clean
```

---

## 6. Próximos Pasos (Hacia el 100% Final)

Para la entrega final del 20 de noviembre de 2026, se desarrollará el 50% restante:
1. Incorporación de locución / narración de voz sintetizada o grabada y sincronización de subtítulos.
2. Animación de variantes adicionales (comparación conceptual con programación dinámica sobre árboles y árboles con pesos en aristas).
3. Afinamiento visual de transiciones fluidas de nodos (estilo Manim a 60 fps).
4. Redacción del informe final en formato PDF (máximo 4 páginas) con el enlace definitivo del video en YouTube/Drive.
