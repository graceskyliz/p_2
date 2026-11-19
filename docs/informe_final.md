# Informe Final de Proyecto: Diámetro de un Árbol
**Curso:** CS2023 - Algoritmos y Estructuras de Datos (2026-2)  
**Profesor:** Luciano A. Romero Calla  
**Fecha de Entrega:** 20 de noviembre de 2026  

**Integrantes:**
- Gracia Luz Mendoza Palacios (100% de contribución)

**Enlaces del Proyecto:**
- Repositorio en GitHub: `https://github.com/graceskyliz/proyecto_2_aed`
- Video Educativo en YouTube: `https://youtu.be/diametro_arbol_aed`

---

## 1. Introducción y Motivación

En teoría de grafos y redes de telecomunicaciones, un árbol es un grafo no dirigido conexo y libre de ciclos. Numerosas infraestructuras de transporte y difusión de información, como los protocolos de árbol de expansión (Spanning Tree Protocol) en redes LAN (estándar IEEE 802.1D), configuran las rutas activas de comunicación en forma de árbol con el fin primordial de eliminar tormentas de difusión (broadcast storms) y evitar que los paquetes circulen de manera indefinida en bucles cerrados.

En estas arquitecturas acíclicas, surge una interrogante técnica de primer orden: **¿cuál es la máxima cantidad de saltos o el retardo en el peor caso para que un paquete viaje entre dos dispositivos cualesquiera de la red?**

Esta métrica equivale exactamente al **Diámetro de un Árbol**, definido como la longitud del camino simple más largo entre cualquier par de nodos de la estructura. El cálculo determinista y eficiente del diámetro permite:
- **Cota superior de latencia:** Establecer el retardo máximo garantizado de extremo a extremo para aplicaciones de tiempo real o protocolos de consenso distribuido.
- **Determinación del centro del árbol:** Identificar el vértice que minimiza la distancia máxima a los demás nodos, permitiendo situar estratégicamente enrutadores troncales o servidores centrales de alta demanda.
- **Caracterización topológica:** Evaluar el grado de ramificación frente a la linealidad de la red.

---

## 2. Definición Formal del Problema y ADT Árbol

### 2.1 Modelo Matemático
Sea $T = (V, E)$ un árbol no dirigido y no ponderado con $|V| = n$ vértices y $|E| = n - 1$ aristas. Por la condición de árbol, para todo par de vértices $u, v \in V$ existe un único camino simple que los conecta. Se define la distancia $d(u, v)$ como el número de aristas que componen dicho camino.

El **diámetro del árbol**, denotado por $D(T)$, se define formalmente como:

$$D(T) = \max_{u, v \in V} d(u, v)$$

### 2.2 Tipo de Dato Abstracto (ADT) Árbol
Para resolver el problema, implementamos en C++17 una estructura de datos `Arbol` basada en listas de adyacencia dinámicas (`std::vector<std::vector<int>>`), con las siguientes operaciones:
- `Arbol(int vertices)`: Constructor que inicializa $n$ vértices con listas de adyacencia vacías.
- `void agregarArista(int u, int v)`: Inserta una arista bidireccional no ponderada entre $u$ y $v$ en tiempo $O(1)$.
- `static Arbol cargarDesdeArchivo(const string& ruta)`: Construye el árbol leyendo un archivo de texto con el formato estándar ($N$ en la primera línea, seguido de las aristas).
- `ResultadoBFS ejecutarBFS(int inicio)`: Realiza un recorrido en anchura devolviendo los arreglos de distancias, predecesores y orden de visita.
- `ResultadoDiametro calcularDiametro(int inicio)`: Ejecuta las dos pasadas del algoritmo, calcula el diámetro y reconstruye el camino diametral.
- `void exportarTraza(const string& ruta, const ResultadoDiametro& res)`: Serializa en formato JSON la secuencia paso a paso para la animación educativa.

---

## 3. Algoritmo de Doble Recorrido BFS

Un método ingenuo que busque los caminos entre todos los pares tomaría $O(V^2)$ con BFS repetidos o $O(V^3)$ con Floyd-Warshall. En árboles no ponderados, es posible resolver el problema en tiempo lineal $O(V)$ mediante dos recorridos BFS:

1. **Paso 1:** Se selecciona un vértice arbitrario inicial $s$ (por defecto el nodo 0). Se ejecuta un primer BFS para computar las distancias desde $s$ a todos los nodos y se identifica el vértice más alejado $u$:
   $$u = \arg\max_{x \in V} d(s, x)$$
2. **Paso 2:** Se inicia un segundo recorrido BFS tomando a $u$ como punto de partida. Se registran las distancias y los nodos padres de cada vértice. Se determina el vértice más alejado $v$:
   $$v = \arg\max_{x \in V} d(u, x)$$
3. **Paso 3:** La distancia $d(u, v)$ es el diámetro del árbol. El camino diametral se reconstruye iterando hacia atrás por el arreglo `padres` desde $v$ hasta alcanzar $u$.

---

## 4. Justificación Teórica y Demostración de Corrección

### 4.1 Teorema Fundamental
> En cualquier árbol no ponderado $T$, el vértice $u$ más alejado de un vértice arbitrario $s$ es siempre uno de los extremos de al menos un camino diametral de $T$.

### 4.2 Demostración por Contradicción
Supongamos que existe un camino diametral $A - B$ de longitud máxima $D = d(A, B)$. Supongamos por el absurdo que el vértice $u$ (el más alejado de $s$) no forma parte de ningún extremo diametral.

Como $T$ es acíclico y conexo, el camino simple entre $s$ y $u$ debe intersectar en algún nodo $w$ al camino diametral $A - B$. Dado que $u$ maximiza la distancia desde $s$, se cumple:
$$d(s, u) \ge d(s, A) \quad \text{y} \quad d(s, u) \ge d(s, B)$$

Restando la distancia común $d(s, w)$:
$$d(w, u) \ge d(w, A) \quad \text{y} \quad d(w, u) \ge d(w, B)$$

Tomemos el extremo diametral más alejado de $w$ (supongamos $B$). El camino compuesto entre $u$ y $B$ tiene longitud:
$$d(u, w) + d(w, B) \ge d(A, w) + d(w, B) = d(A, B) = D$$

Si la desigualdad fuese estricta, tendríamos un camino más largo que $D$, contradiciendo que $D$ es el diámetro máximo. Si es igual, el camino $u - B$ tiene longitud $D$, por lo que $u$ es efectivamente un extremo diametral. Por lo tanto, el primer BFS siempre encuentra un extremo diametral $u$, y el segundo BFS desde $u$ alcanza necesariamente el extremo opuesto $v$ con longitud máxima $D$.

---

## 5. Análisis de Complejidad Temporal y Espacial

| Etapa del Algoritmo | Complejidad Temporal | Justificación |
| :--- | :---: | :--- |
| Primer BFS (desde $s$) | $O(V + E) = O(N)$ | Visita cada vértice y arista una sola vez ($E = N - 1$). |
| Búsqueda de $u$ | $O(N)$ | Búsqueda lineal del valor máximo en el vector de distancias. |
| Segundo BFS (desde $u$) | $O(V + E) = O(N)$ | Explora el árbol completo partiendo del nodo extremo. |
| Búsqueda de $v$ | $O(N)$ | Búsqueda lineal del valor máximo en el segundo vector. |
| Reconstrucción del camino | $O(D) \le O(N)$ | Retroceso por punteros en el vector de predecesores. |
| **Complejidad Temporal Total** | **$O(N)$** | **Tiempo lineal óptimo.** |
| **Complejidad Espacial Auxiliar** | **$O(N)$** | **Listas de adyacencia ($2N-2$), distancias ($N$), padres ($N$) y cola ($N$).** |

---

## 6. Arquitectura del Software e Implementación

El proyecto se estructuró en dos capas conectadas mediante un archivo de traza:
1. **Motor en C++ (`src/`):**
   - Implementa la clase `Arbol` y el algoritmo de dos BFS.
   - Procesa grafos de entrada desde archivos de texto en `data/`.
   - Exporta los estados de ejecución a archivos JSON (`output/traza.json` y `output/traza_estrella.json`).
2. **Generador Visual en Python (`animacion/`):**
   - Script `animador.py` que interpreta la traza JSON.
   - Dibuja cada cuadro vectorial con Pillow, calculando la disposición espacial de los nodos.
   - Genera los subtítulos sincronizados `output/subtitulos.srt`.
   - Ensambla el video en formato MP4 con FFmpeg (`output/video_diametro.mp4`) a 24 fps.

---

## 7. Caso de Borde Relevante: Grafo Estrella

Se analizó y animó de manera dedicada el caso de borde del **Grafo Estrella** ($N = 6$):
- Un único nodo central (nodo 0) con grado $N - 1 = 5$, conectado a 5 hojas de grado 1.
- La distancia entre el centro y cualquier hoja es 1, y entre cualesquiera dos hojas distintas es $1 + 1 = 2$.
- Por lo tanto, para cualquier grafo estrella con $N \ge 3$, el diámetro es invariablemente **$D = 2$**.
- El algoritmo resuelve este caso sin ambigüedades: el primer BFS encuentra una hoja $u$ a distancia 2, y el segundo BFS desde $u$ encuentra otra hoja $v$ a distancia 2, reconstruyendo el camino $2 \rightarrow 0 \rightarrow 1$.

---

## 8. Batería de Pruebas Unitarias

Se desarrollaron 7 pruebas unitarias en `tests/test_arbol.cpp` que validan todas las variantes topológicas:

| ID | Caso de Prueba | Vértices | Aristas | Diámetro Esperado | Diámetro Obtenido | Resultado |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| T1 | Un solo nodo (caso base) | 1 | 0 | 0 | 0 | Correcto |
| T2 | Dos nodos con una arista | 2 | 1 | 1 | 1 | Correcto |
| T3 | Grafo estrella | 6 | 5 | 2 | 2 | Correcto |
| T4 | Grafo línea (cadena simple) | 5 | 4 | 4 | 4 | Correcto |
| T5 | Árbol binario completo | 7 | 6 | 4 | 4 | Correcto |
| T6 | Árbol asimétrico general | 9 | 8 | 6 | 6 | Correcto |
| T7 | Carga desde archivos | 9 y 6 | 8 y 5 | 6 y 2 | 6 y 2 | Correcto |

Todas las pruebas pasan con éxito mediante el comando `make test`.

---

## 9. Instrucciones de Compilación y Reproducción

El proyecto cuenta con un `Makefile` que automatiza todo el proceso:

```bash
# 1. Compilar y ejecutar las pruebas unitarias
make test

# 2. Ejecutar el motor C++ y exportar las trazas JSON
make run

# 3. Generar la animación completa en video MP4 y subtítulos
make video

# 4. Compilar el informe final en formato PDF (4 páginas)
make pdf

# 5. Limpiar ejecutables y archivos temporales
make clean
```

---

## 10. Contribuciones Individuales de los Integrantes

- **Gracia Luz Mendoza Palacios (100%):**
  - Implementación en C++ de la clase `Arbol` y el algoritmo de dos recorridos BFS.
  - Desarrollo de la suite de pruebas unitarias (`tests/test_arbol.cpp`).
  - Redacción de la fundamentación matemática, demostración de corrección y análisis de complejidad.
  - Desarrollo del motor de animación gráfica en Python (`animacion/animador.py`) con Pillow.
  - Generación del video educativo en MP4 y subtítulos sincronizados SRT.
  - Elaboración del script generador del informe en PDF (`docs/generar_pdf.py`) y automatización del `Makefile`.

---

## 11. Conclusiones

1. El algoritmo de doble BFS demostró ser una solución óptima y elegante de tiempo lineal $O(V)$ y memoria auxiliar $O(V)$, superando ampliamente los enfoques tradicionales cuadráticos basados en caminos mínimos entre todos los pares.
2. La demostración por contradicción sustenta formalmente por qué el nodo más alejado de cualquier vértice inicial siempre es un extremo del diámetro, garantizando la exactitud del algoritmo sobre cualquier árbol no ponderado.
3. La arquitectura desacoplada C++ $\rightarrow$ JSON $\rightarrow$ Python aseguró que la animación visual refleje fielmente los cálculos del motor algorítmico programado por el grupo, cumpliendo con la exigencia académica del proyecto.

---

## 12. Referencias Bibliográficas

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to Algorithms* (4th ed.). MIT Press. Capítulo 20: Elementary Graph Algorithms.
- Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley Professional. Sección 4.1: Undirected Graphs.
- Manim Community Developers. (2026). *Manim - Mathematical Animation Engine Documentation*. https://docs.manim.community/

