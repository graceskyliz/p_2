# Proyecto 2: Diámetro de un Árbol
**CS2023 - Algoritmos y Estructuras de Datos (2026-2)**  
**Profesor:** Luciano A. Romero Calla  

---

## Integrantes
- Integrante 1 (Código)
- Integrante 2 (Código)
- Integrante 3 (Código)

---

## 1. Descripción del Proyecto

El objetivo de este proyecto es implementar y explicar de forma visual el algoritmo para encontrar el **diámetro de un árbol** no ponderado. El diámetro se define como la mayor distancia (en cantidad de aristas) entre cualquier par de nodos del árbol.

Para calcularlo de forma eficiente sin recurrir a fuerza bruta ($O(V^2)$), utilizamos el algoritmo de dos recorridos BFS (Búsqueda en Anchura) que opera en tiempo lineal $O(V)$:
1. Se realiza un primer BFS a partir de un nodo inicial cualquiera (nodo 0) para encontrar el nodo más distante $u$.
2. Se realiza un segundo BFS partiendo desde $u$ para encontrar el nodo más distante $v$.
3. La distancia obtenida entre $u$ y $v$ corresponde al diámetro del árbol, y mediante el arreglo de padres se reconstruye el camino completo.

El núcleo algorítmico y la estructura del árbol están programados en C++, la cual exporta los datos de ejecución a un archivo `output/traza.json`. Luego, un script en Python toma dicha traza y genera un video en formato MP4 (`output/video_diametro.mp4`) utilizando Pillow y FFmpeg para mostrar paso a paso la propagación de cada búsqueda.

---

## 2. Estructura del Directorio

```text
proyecto_2/
├── aed_project_2.md          # Pautas del proyecto
├── Makefile                  # Comandos para compilar y ejecutar
├── .gitignore                # Exclusiones de Git
├── README.md                 # Documentación del repositorio
├── docs/
│   └── informe_avance_50.md  # Informe del avance al 50%
├── src/
│   ├── Arbol.hpp             # Declaración de la clase Arbol y estructuras
│   ├── Arbol.cpp             # Implementación de adyacencia y doble BFS
│   └── main.cpp              # Ejecución de ejemplo y exportación de traza
├── tests/
│   └── test_arbol.cpp        # Pruebas unitarias para distintos casos
├── animacion/
│   └── animador.py           # Generación de la animación y compilación a MP4
└── output/
    └── traza.json            # Traza generada por el ejecutable en C++
```

---

## 3. Requisitos del Sistema

- `g++` (con soporte para C++17)
- `python3`
- Librería `Pillow` de Python (`pip install Pillow`)
- `ffmpeg` instalado y accesible en la terminal

---

## 4. Instrucciones de Uso

### Compilar y ejecutar el programa en C++
```bash
make run
```
Compila el código fuente, calcula el diámetro sobre un árbol de prueba de 9 nodos y genera el archivo `output/traza.json`.

### Ejecutar las pruebas unitarias
```bash
make test
```
Ejecuta la batería de pruebas que comprueba el algoritmo ante casos de borde:
- Árbol con un solo nodo ($N=1$).
- Árbol con dos nodos ($N=2$).
- Grafo en estrella.
- Grafo en línea / camino simple.
- Árbol binario simétrico.
- Árbol asimétrico general.

### Generar la animación en video
```bash
make video
```
Compila y corre el ejecutable en C++, y a continuación ejecuta el script de animación para generar `output/video_diametro.mp4`.

### Limpiar archivos generados
```bash
make clean
```

---

## 5. Estado del Avance (Hito del 50%)

A la fecha (11 de noviembre de 2026), se ha completado:
- Implementación de la clase `Arbol` usando listas de adyacencia.
- Algoritmo de dos BFS y reconstrucción del camino diametral en C++.
- Exportación estructurada de los pasos en formato JSON.
- Suite de pruebas unitarias cubriendo casos normales y límites.
- Script de animación funcional que traduce la traza en fotogramas y compila el video en MP4.
- Redacción del informe de avance intermedio.

Trabajo restante para la entrega final (20 de noviembre de 2026):
- Grabación de la narración de voz para el video explicativo.
- Incorporación de subtítulos y ajustes finales de edición.
- Elaboración del informe final en PDF (máximo 4 páginas) con los enlaces de entrega.
