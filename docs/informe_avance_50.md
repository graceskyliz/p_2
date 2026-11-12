# Informe de Avance (50%) - Proyecto 2
## Diámetro de un Árbol
**Curso:** CS2023 - Algoritmos y Estructuras de Datos (2026-2)  
**Profesor:** Luciano A. Romero Calla  
**Fecha:** 11 de noviembre de 2026  

**Integrantes:**
- Integrante 1 (Código)
- Integrante 2 (Código)
- Integrante 3 (Código)

---

## 1. Introducción y Motivación

En teoría de grafos y redes, un árbol es un grafo no dirigido conexo y acíclico. Muchas arquitecturas de comunicación, como los protocolos de árbol de expansión (Spanning Tree Protocol) en redes locales, organizan la interconexión de equipos en forma de árbol para evitar bucles de transmisión.

En este tipo de redes, el **diámetro del árbol** representa la máxima distancia (en número de saltos o aristas) que existe entre dos nodos cualesquiera. Esta métrica es fundamental porque:
- Determina la latencia máxima que puede experimentar un paquete de datos en el peor caso al viajar entre dos extremos de la red.
- Ayuda a identificar el centro del árbol, permitiendo ubicar servidores o enrutadores en posiciones óptimas para minimizar retardos promedio.
- Permite caracterizar la dispersión y la topología de la estructura.

---

## 2. Definición del Problema y Algoritmo

### 2.1 Definición Matemática
Dado un árbol $T = (V, E)$ no ponderado con $|V| = n$ vértices y $|E| = n - 1$ aristas, definimos la distancia $d(u, v)$ como el número de aristas en el único camino simple que une a $u$ con $v$. El diámetro $D$ de $T$ se define como:

$$D = \max_{u, v \in V} d(u, v)$$

### 2.2 Algoritmo de dos recorridos BFS
Una búsqueda ingenua que calcule caminos mínimos entre todos los pares tomaría $O(V^2)$ con BFS repetidos o $O(V^3)$ con Floyd-Warshall. Para árboles no ponderados, existe un algoritmo lineal $O(V)$ basado en dos recorridos BFS:

1. **Primer BFS:** Partiendo de un nodo arbitrario $s$ (por ejemplo, el nodo 0), se calcula la distancia hacia todos los demás nodos y se elige el nodo $u$ que tenga la mayor distancia registrada.
2. **Segundo BFS:** Partiendo de $u$, se ejecuta un nuevo BFS para calcular las distancias hacia el resto del árbol y se elige el nodo $v$ con la mayor distancia registrada.
3. **Reconstrucción:** La distancia $d(u, v)$ es el diámetro del árbol. El camino diametral se obtiene recorriendo hacia atrás los punteros del arreglo `padres` desde $v$ hasta llegar a $u$.

### 2.3 Justificación de Corrección
La validez del algoritmo se sustenta en la siguiente propiedad geométrica de los árboles:

> El nodo $u$ más alejado de cualquier nodo arbitrario $s$ es siempre uno de los extremos de al menos un camino diametral del árbol.

**Demostración breve por contradicción:**  
Supongamos que el diámetro real del árbol une los nodos $A$ y $B$, con longitud $D = d(A, B)$. Sea $s$ un nodo arbitrario y $u$ el nodo más lejano a $s$, de modo que $d(s, u) \ge d(s, x)$ para todo $x \in V$.  
Como $T$ es conexo y acíclico, el camino de $s$ a $u$ debe coincidir o intersectarse en algún punto $w$ con el camino diametral que va de $A$ a $B$. Si $u$ no fuera un extremo diametral, la distancia desde $w$ hasta $u$ sería mayor o igual a la distancia desde $w$ hasta $A$ o hasta $B$, lo que permitiría construir un camino simple entre $u$ y uno de los extremos ($A$ o $B$) con longitud mayor que $d(A, B)$. Esto contradice la hipótesis de que $d(A, B)$ era el camino más largo posible. Por tanto, $u$ debe ser un extremo del diámetro. Luego, el segundo BFS desde $u$ alcanzará necesariamente el otro extremo $v$, encontrando la distancia máxima posible $D$.

### 2.4 Análisis de Complejidad
- **Complejidad Temporal:** En un árbol con $V$ nodos y $E = V - 1$ aristas:
  - Primer BFS: recorre cada vértice y arista una vez $\rightarrow O(V + E) = O(V)$.
  - Segundo BFS: recorre cada vértice y arista una vez $\rightarrow O(V + E) = O(V)$.
  - Reconstrucción del camino: retrocede por el arreglo de padres a lo largo del diámetro $\rightarrow O(D) \le O(V)$.
  - Tiempo total: $O(V)$, estrictamente lineal.
- **Complejidad Espacial:** Se requiere memoria para la lista de adyacencia ($O(V)$), los arreglos de distancias y padres ($O(V)$) y la cola de exploración del BFS ($O(V)$). Espacio total: $O(V)$.

---

## 3. Implementación del Software

Para este proyecto separamos la lógica en dos partes:
1. **Motor en C++ (`src/`):**
   - Clase `Arbol` que administra las aristas mediante listas de adyacencia `std::vector<std::vector<int>>`.
   - Método `ejecutarBFS(inicio)` que llena las distancias, los padres y el orden de visita.
   - Método `calcularDiametro(inicio)` que ejecuta los dos BFS, determina los extremos $u$ y $v$ y reconstruye el vector del camino.
   - Método `exportarTraza(ruta, resultado)` que guarda en formato JSON (`output/traza.json`) los datos del árbol, las dos etapas del algoritmo y el camino final.
2. **Generador de Animación en Python (`animacion/`):**
   - Script `animador.py` que lee el archivo JSON generado por C++.
   - Dibuja cada fotograma utilizando la biblioteca `Pillow`, ubicando los nodos y aristas y coloreando el frente de búsqueda en cada paso.
   - Llama a `ffmpeg` para compilar los fotogramas generados en un video final `output/video_diametro.mp4` a 24 cuadros por segundo.

De esta manera, la animación está respaldada directamente por los resultados calculados por nuestra implementación en C++, sin simular pasos manualmente.

---

## 4. Pruebas Unitarias y Casos de Borde

En `tests/test_arbol.cpp` se implementaron pruebas con aserciones para verificar el funcionamiento del algoritmo sobre diversas topologías:

| Caso de prueba | Descripción | Nodos | Diámetro esperado | Resultado |
| :--- | :--- | :---: | :---: | :---: |
| Un solo nodo | Caso base mínimo | 1 | 0 | Correcto |
| Dos nodos | Árbol con una sola arista | 2 | 1 | Correcto |
| Estrella | Un nodo central conectado a 5 hojas | 6 | 2 | Correcto |
| Línea | Cadena simple de nodos consecutivos | 5 | 4 | Correcto |
| Binario completo | Árbol binario simétrico de 3 niveles | 7 | 4 | Correcto |
| Asimétrico | Árbol con ramas de distintas profundidades | 9 | 6 | Correcto |

Todas las pruebas se compilan y validan mediante el comando `make test`.

---

## 5. Estado de la Animación en Video

El script de animación genera un video de demostración con las siguientes secciones:
1. Pantalla de presentación con el nombre del curso, tema e integrantes.
2. Definición del diámetro y dibujo del árbol base.
3. Paso 1: Animación de la primera pasada de BFS resaltando los nodos visitados en color azul y sus distancias, hasta ubicar el nodo más alejado $u$.
4. Paso 2: Animación de la segunda pasada de BFS desde $u$ en color violeta, hasta ubicar el extremo opuesto $v$.
5. Paso 3: Resaltado del camino diametral en color amarillo y visualización de la longitud total.
6. Resumen final con el desglose de la complejidad temporal y espacial $O(V)$.

El archivo generado se guarda en `output/video_diametro.mp4`.

---

## 6. Plan de Trabajo Restante (Hacia la Entrega Final)

Para la entrega final del 20 de noviembre de 2026, el trabajo restante se divide en:
1. **Narración y audio:** Grabar la explicación hablada del algoritmo y montarla sobre el video.
2. **Subtítulos:** Incluir subtítulos en la animación para asegurar claridad en la explicación.
3. **Informe final en PDF:** Redactar el documento final de máximo 4 páginas con la descripción completa, capturas de pantalla y enlaces al repositorio de GitHub y al video subido a YouTube.
