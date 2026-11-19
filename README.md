# Proyecto 2: Diámetro de un Árbol
**CS2023 - Algoritmos y Estructuras de Datos (2026-2)**  
**Profesor:** Luciano A. Romero Calla  

---

## Integrante
- Gracia Luz Mendoza Palacios

---

## 1. Descripción del Proyecto

El objetivo de este proyecto es implementar, analizar y demostrar de manera visual y animada el algoritmo para encontrar el **diámetro de un árbol** no ponderado. El diámetro se define como la mayor distancia (en cantidad de aristas) entre dos nodos cualesquiera del árbol.

Para calcularlo en tiempo estrictamente lineal $O(V)$, se emplea el algoritmo de dos recorridos BFS (Búsqueda en Anchura):
1. **Primer BFS:** Parte desde un nodo arbitrario $s$ (por ejemplo, el nodo 0) y encuentra el nodo más distante $u$.
2. **Segundo BFS:** Parte desde $u$ y encuentra el nodo más distante $v$.
3. **Resultado:** La distancia entre $u$ y $v$ es el diámetro del árbol, y el camino se reconstruye retrocediendo por el arreglo de padres desde $v$ hasta $u$.

La lógica algorítmica y la estructura del árbol están implementadas en C++17 (`src/`), la cual exporta los datos de ejecución a formato JSON (`output/`). Un script en Python (`animacion/animador.py`) interpreta la traza y compila un video educativo en MP4 (`output/video_diametro.mp4`) a 24 fps con visualización gráfica paso a paso y subtítulos sincronizados (`output/subtitulos.srt`).

---

## 2. Estructura del Repositorio

```text
proyecto_2/
├── Makefile                  # Automatización de compilación y ejecución
├── .gitignore                # Exclusiones de Git
├── README.md                 # Documentación completa del proyecto
├── data/                     # Grafos de prueba en formato de texto
│   ├── arbol_general.txt     # Árbol ilustrativo (9 nodos)
│   ├── caso_estrella.txt     # Caso de borde: grafo estrella (6 nodos)
│   └── caso_linea.txt        # Caso de borde: grafo línea (5 nodos)
├── src/
│   ├── Arbol.hpp             # Declaración de la clase Arbol y estructuras
│   ├── Arbol.cpp             # Implementación de adyacencia y doble BFS
│   └── main.cpp              # Ejecución de casos y exportación de trazas
├── tests/
│   └── test_arbol.cpp        # 7 pruebas unitarias automatizadas
├── animacion/
│   └── animador.py           # Motor de animación y generación de video MP4
└── output/
    ├── traza.json            # Traza JSON del árbol general
    ├── traza_estrella.json   # Traza JSON del caso de borde estrella
    └── video_diametro.mp4    # Video generado de la animación
```

---

## 3. Requisitos del Sistema

- `g++` con soporte para C++17
- `python3` (versión 3.8 o superior)
- Librería `Pillow` de Python (`pip install Pillow`)
- `ffmpeg` instalado en el sistema

---

## 4. Instrucciones de Uso

### 4.1 Compilar y ejecutar pruebas unitarias
```bash
make test
```
Ejecuta la suite de 7 pruebas unitarias con aserciones que validan:
- Árbol de un solo nodo ($N=1$, diámetro 0).
- Árbol de dos nodos con una arista ($N=2$, diámetro 1).
- Grafo en estrella ($N=6$, diámetro 2).
- Grafo en línea / cadena ($N=5$, diámetro 4).
- Árbol binario simétrico ($N=7$, diámetro 4).
- Árbol asimétrico general ($N=9$, diámetro 6).
- Carga dinámica de grafos desde archivos de texto en `data/`.

### 4.2 Ejecutar el motor C++
```bash
make run
```
Compila y ejecuta `main`, procesando el árbol general (`data/arbol_general.txt`) y el caso de borde estrella (`data/caso_estrella.txt`), generando `output/traza.json` y `output/traza_estrella.json`.

También se puede evaluar cualquier árbol personalizado:
```bash
./main data/caso_linea.txt output/traza_linea.json
```

### 4.3 Generar el video
```bash
make video
```
Ejecuta la lógica en C++ y genera la animación en `output/video_diametro.mp4`. El video incluye:
1. Portada con título, integrante y profesor.
2. Definición formal del diámetro.
3. Demostración animada paso a paso del árbol general (BFS 1, BFS 2 y camino diametral en dorado).
4. Demostración animada del caso de borde (grafo estrella con distribución radial y diámetro 2).
5. Cuadro de análisis de complejidad temporal y espacial $O(V)$.


### 4.4 Limpiar archivos generados
```bash
make clean
```

---

## 5. Complejidad del Algoritmo

- **Complejidad Temporal:** En un árbol con $V$ vértices y $E = V - 1$ aristas, el primer BFS toma $O(V + E) = O(V)$, el segundo BFS toma $O(V + E) = O(V)$ y la reconstrucción toma $O(D) \le O(V)$. El tiempo total es **$O(V)$**, estrictamente lineal.
- **Complejidad Espacial:** Requiere listas de adyacencia ($2V - 2$ enteros), arreglos de distancias ($V$), padres ($V$) y la cola de exploración ($V$). La memoria auxiliar es **$O(V)$**.
