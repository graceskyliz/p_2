#include "Arbol.hpp"
#include <queue>
#include <algorithm>
#include <fstream>
#include <iostream>

Arbol::Arbol() : n(0) {}

Arbol::Arbol(int vertices) : n(vertices), adj(vertices) {}

void Arbol::agregarArista(int u, int v) {
    if (u >= 0 && u < n && v >= 0 && v < n) {
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
}

int Arbol::obtenerN() const {
    return n;
}

const std::vector<std::vector<int>>& Arbol::obtenerAdyacencia() const {
    return adj;
}

ResultadoBFS Arbol::ejecutarBFS(int inicio) const {
    ResultadoBFS res;
    if (n == 0 || inicio < 0 || inicio >= n) {
        res.nodoMasLejano = -1;
        res.distanciaMax = -1;
        return res;
    }

    res.distancias.assign(n, -1);
    res.padres.assign(n, -1);
    
    std::queue<int> cola;
    res.distancias[inicio] = 0;
    cola.push(inicio);

    int maxDist = 0;
    int nodoLejano = inicio;

    while (!cola.empty()) {
        int u = cola.front();
        cola.pop();
        res.ordenVisita.push_back(u);

        if (res.distancias[u] > maxDist) {
            maxDist = res.distancias[u];
            nodoLejano = u;
        }

        for (int v : adj[u]) {
            if (res.distancias[v] == -1) {
                res.distancias[v] = res.distancias[u] + 1;
                res.padres[v] = u;
                cola.push(v);
            }
        }
    }

    res.nodoMasLejano = nodoLejano;
    res.distanciaMax = maxDist;
    return res;
}

ResultadoDiametro Arbol::calcularDiametro(int nodoInicial) const {
    ResultadoDiametro resultado;
    if (n == 0) {
        resultado.diametro = 0;
        resultado.nodoU = -1;
        resultado.nodoV = -1;
        return resultado;
    }

    if (n == 1) {
        resultado.diametro = 0;
        resultado.nodoU = 0;
        resultado.nodoV = 0;
        resultado.camino = {0};
        resultado.bfs1 = ejecutarBFS(0);
        resultado.bfs2 = resultado.bfs1;
        return resultado;
    }

    ResultadoBFS r1 = ejecutarBFS(nodoInicial);
    ResultadoBFS r2 = ejecutarBFS(r1.nodoMasLejano);

    resultado.bfs1 = r1;
    resultado.bfs2 = r2;
    resultado.nodoU = r1.nodoMasLejano;
    resultado.nodoV = r2.nodoMasLejano;
    resultado.diametro = r2.distanciaMax;

    std::vector<int> ruta;
    int curr = r2.nodoMasLejano;
    while (curr != -1) {
        ruta.push_back(curr);
        curr = r2.padres[curr];
    }
    std::reverse(ruta.begin(), ruta.end());
    resultado.camino = ruta;

    return resultado;
}

void Arbol::exportarTraza(const std::string& rutaArchivo, const ResultadoDiametro& resultado) const {
    std::ofstream out(rutaArchivo);
    if (!out.is_open()) {
        std::cerr << "Error al abrir archivo para exportar traza: " << rutaArchivo << std::endl;
        return;
    }

    out << "{\n";
    out << "  \"n\": " << n << ",\n";
    
    out << "  \"aristas\": [\n";
    bool primeraArista = true;
    for (int u = 0; u < n; ++u) {
        for (int v : adj[u]) {
            if (u < v) {
                if (!primeraArista) out << ",\n";
                out << "    [" << u << ", " << v << "]";
                primeraArista = false;
            }
        }
    }
    out << "\n  ],\n";

    out << "  \"diametro\": " << resultado.diametro << ",\n";
    out << "  \"nodo_u\": " << resultado.nodoU << ",\n";
    out << "  \"nodo_v\": " << resultado.nodoV << ",\n";

    out << "  \"camino\": [";
    for (size_t i = 0; i < resultado.camino.size(); ++i) {
        out << resultado.camino[i];
        if (i + 1 < resultado.camino.size()) out << ", ";
    }
    out << "],\n";

    out << "  \"bfs1\": {\n";
    out << "    \"inicio\": " << (resultado.bfs1.ordenVisita.empty() ? 0 : resultado.bfs1.ordenVisita[0]) << ",\n";
    out << "    \"nodo_lejano\": " << resultado.bfs1.nodoMasLejano << ",\n";
    out << "    \"distancia_max\": " << resultado.bfs1.distanciaMax << ",\n";
    out << "    \"orden_visita\": [";
    for (size_t i = 0; i < resultado.bfs1.ordenVisita.size(); ++i) {
        out << resultado.bfs1.ordenVisita[i];
        if (i + 1 < resultado.bfs1.ordenVisita.size()) out << ", ";
    }
    out << "],\n";
    out << "    \"distancias\": [";
    for (size_t i = 0; i < resultado.bfs1.distancias.size(); ++i) {
        out << resultado.bfs1.distancias[i];
        if (i + 1 < resultado.bfs1.distancias.size()) out << ", ";
    }
    out << "]\n";
    out << "  },\n";

    out << "  \"bfs2\": {\n";
    out << "    \"inicio\": " << (resultado.bfs2.ordenVisita.empty() ? 0 : resultado.bfs2.ordenVisita[0]) << ",\n";
    out << "    \"nodo_lejano\": " << resultado.bfs2.nodoMasLejano << ",\n";
    out << "    \"distancia_max\": " << resultado.bfs2.distanciaMax << ",\n";
    out << "    \"orden_visita\": [";
    for (size_t i = 0; i < resultado.bfs2.ordenVisita.size(); ++i) {
        out << resultado.bfs2.ordenVisita[i];
        if (i + 1 < resultado.bfs2.ordenVisita.size()) out << ", ";
    }
    out << "],\n";
    out << "    \"distancias\": [";
    for (size_t i = 0; i < resultado.bfs2.distancias.size(); ++i) {
        out << resultado.bfs2.distancias[i];
        if (i + 1 < resultado.bfs2.distancias.size()) out << ", ";
    }
    out << "]\n";
    out << "  }\n";

    out << "}\n";
    out.close();
}
