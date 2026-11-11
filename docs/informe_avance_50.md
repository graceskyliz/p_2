# Informe de Avance (50%) - Proyecto 2
## CS2023 - Algoritmos y Estructuras de Datos (2026-2)
**Docente:** Luciano A. Romero Calla  
**Tema Asignado:** Diámetro de un Árbol  
**Fecha de Presentación de Avances:** 11 de noviembre de 2026  

---

## 1. Motivación y Planteamiento del Problema

En el diseño y análisis de redes de computadoras, sistemas distribuidos e infraestructuras de telecomunicaciones, la topología de interconexión suele organizarse o reducirse a un árbol de expansión (Spanning Tree) para garantizar conectividad sin bucles ni tormentas de difusión (broadcast storms).

En este contexto, surge una métrica crítica de rendimiento: **¿cuál es el retardo máximo en el peor caso para que un paquete viaje entre dos dispositivos cualesquiera de la red?** 

Esta pregunta se modela directamente mediante el **Diámetro de un Árbol**: la distancia máxima (medida en número de saltos o suma de latencias) que separa a cualquier par de vértices en el grafo acíclico. Resolver este problema de forma óptima permite:
- Calcular la latencia acotada superior de la red.
- Encontrar el centro del árbol (nodo que minimiza la distancia máxima a los demás nodos) para ubicar estratégicamente servidores centrales o enrutadores de alta capacidad.
- Evaluar el cuello de botella estructural de la topología.

---

## 2. Fundamento Teórico y Algoritmo

### 2.1 Definición Formal
Sea $T = (V, E)$ un árbol no dirigido, conexo y no ponderado, donde $|E| = |V| - 1$. La distancia $d(u, v)$ entre dos nodos $u, v \in V$ se define como el número de aristas en el único camino simple que los une. El diámetro $D(T)$ se define como:

$$D(T) = \max_{u, v \in V} d(u, v)$$

### 2.2 Algoritmo de Doble BFS
Calcular las distancias entre todos los pares mediante BFS repetido desde cada vértice requeriría $O(V^2)$ operaciones. Sin embargo, en árboles existe una propiedad matemática fundamental:

> **Propiedad:** Si elegimos un vértice arbitrario $s \in V$ y encontramos el vértice $u$ que maximiza $d(s, u)$, entonces $u$ es necesariamente uno de los extremos de al menos un camino diametral en $T$.

A partir de esta propiedad, el algoritmo opera en dos etapas lineales:
1. **Paso 1:** Ejecutar una Búsqueda en Anchura (BFS) desde un vértice inicial cualquiera $s$. Registrar las distancias y seleccionar el vértice $u$ con la máxima distancia calculada.
2. **Paso 2:** Ejecutar un segundo BFS tomando a $u$ como origen. Registrar las distancias y padres de cada nodo. Identificar el vértice $v$ con la máxima distancia desde $u$.
3. **Paso 3:** La distancia $d(u, v)$ es el diámetro del árbol. El camino diametral se reconstruye iterando desde $v$ hacia $u$ mediante el arreglo de predecesores (`padres`).

### 2.3 Análisis de Complejidad
- **Complejidad Temporal:** Cada ejecución de BFS visita cada vértice y cada arista a lo sumo una vez:
  $$T(V) = 2 \times O(|V| + |E|) = 2 \times O(V + V - 1) = O(V)$$
  La reconstrucción del camino toma $O(D) \le O(V)$. Por lo tanto, el tiempo total es estrictamente lineal $O(V)$.
- **Complejidad Espacial:** Se almacena la lista de adyacencia ($O(V)$), los vectores de distancias y predecesores ($O(V)$) y la cola de exploración del BFS ($O(V)$). La memoria auxiliar requerida es $O(V)$.

---

## 3. Arquitectura del Proyecto (Hito del 50%)

El proyecto adopta una arquitectura modular desacoplada, separando la lógica algorítmica de la capa de renderizado visual:

```
+-------------------------------------------------------+
|                    Motor C++ (src/)                   |
| - Clase Arbol con lista de adyacencia                 |
| - Algoritmo de Doble BFS                              |
| - Reconstruccion de camino diametral                  |
| - Exportador estructurado JSON                        |
+---------------------------+---------------------------+
                            |
                            v output/traza.json
+---------------------------+---------------------------+
|               Generador Visual (animacion/)           |
| - Lector de eventos y estados de traza                |
| - Motor de renderizado vectorial de fotogramas        |
| - Pipeline de codificacion con FFmpeg (libopenh264)   |
+---------------------------+---------------------------+
                            |
                            v output/video_diametro.mp4
```

### Justificación de Diseño
- Cumple estrictamente con el requerimiento de que la animación esté impulsada por una implementación real de la estructura en C++.
- La exportación en JSON permite reproducir fielmente la traza sin simulación manual de pasos.
- Código limpio, legible y sin dependencias externas complejas, adecuado para el nivel universitario formativo.

---

## 4. Casos de Borde y Validación Experimental

Se diseñó una suite de pruebas unitarias (`tests/test_arbol.cpp`) que valida automáticamente los siguientes escenarios:

| Caso de Prueba | Topología | Vértices | Diámetro Esperado | Estado |
| :--- | :--- | :---: | :---: | :---: |
| Un solo nodo | $V = \{0\}$ | 1 | 0 | PASS |
| Dos nodos conexos | $0 - 1$ | 2 | 1 | PASS |
| Grafo estrella | Nodo 0 conectado a 5 hojas | 6 | 2 | PASS |
| Grafo línea | Cadena simple $0-1-2-3-4$ | 5 | 4 | PASS |
| Árbol binario simétrico | Árbol binario completo | 7 | 4 | PASS |
| Árbol asimétrico general | Árbol con ramas de diferente longitud | 9 | 6 | PASS |

Todas las pruebas se ejecutan mediante `make test` y superan las aserciones de consistencia de distancias y tamaño de camino.

---

## 5. Prototipo del Video y Estado de la Animación

El prototipo actual (`animacion/animador.py`) implementa la línea base de la animación educativa con estética inspirada en Manim y 3Blue1Brown:
- Fondo oscuro de alto contraste (`#0f141c`).
- Visualización interactiva de nodos no visitados, frente de onda activo y vértices procesados.
- Transición dinámica de distancias paso a paso.
- Resaltado en color ámbar del primer extremo $u$ y en carmesí del segundo extremo $v$.
- Animación del camino diametral final en color dorado brillante con trazo reforzado.
- Diapositivas de introducción y tarjeta final con el análisis de complejidad formal.
- Salida generada: Video MPEG-4 en alta resolución a 24 fps (`output/video_diametro.mp4`).

---

## 6. Plan de Trabajo Restante (Hacia el 100%)

| Actividad | Porcentaje Actual | Meta al 100% (20 de Noviembre) |
| :--- | :---: | :---: |
| Estructura de Datos en C++ | 100% | Optimización de memoria y documentación |
| Algoritmo de Doble BFS | 100% | Variante de árbol con pesos (algoritmo con pesos no negativos) |
| Pruebas Unitarias de Casos de Borde | 100% | Pruebas de estrés con árboles aleatorios de $N=10^5$ |
| Pipeline de Animación Gráfica | 60% | Transiciones suavizadas por interpolación matemática |
| Locución y Audio Explicativo | 0% | Grabación / síntesis de voz sincronizada |
| Informe Final en PDF (4 páginas) | 30% | Informe final consolidado con enlaces a YouTube y GitHub |
| **Total Global del Proyecto** | **50%** | **100%** |
