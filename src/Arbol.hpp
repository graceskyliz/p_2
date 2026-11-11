#ifndef ARBOL_HPP
#define ARBOL_HPP

#include <vector>
#include <string>

struct ResultadoBFS {
    int nodoMasLejano;
    int distanciaMax;
    std::vector<int> distancias;
    std::vector<int> padres;
    std::vector<int> ordenVisita;
};

struct ResultadoDiametro {
    int diametro;
    int nodoU;
    int nodoV;
    std::vector<int> camino;
    ResultadoBFS bfs1;
    ResultadoBFS bfs2;
};

class Arbol {
private:
    int n;
    std::vector<std::vector<int>> adj;

public:
    Arbol();
    Arbol(int vertices);

    void agregarArista(int u, int v);
    int obtenerN() const;
    const std::vector<std::vector<int>>& obtenerAdyacencia() const;

    ResultadoBFS ejecutarBFS(int inicio) const;
    ResultadoDiametro calcularDiametro(int nodoInicial = 0) const;

    void exportarTraza(const std::string& rutaArchivo, const ResultadoDiametro& resultado) const;
};

#endif
