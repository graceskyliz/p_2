#ifndef ARBOL_HPP
#define ARBOL_HPP

#include <vector>
#include <string>
using namespace std;

struct ResultadoBFS {
    int nodoMasLejano;
    int distanciaMax;
    vector<int> distancias;
    vector<int> padres;
    vector<int> ordenVisita;
};

struct ResultadoDiametro {
    int diametro;
    int nodoU;
    int nodoV;
    vector<int> camino;
    ResultadoBFS bfs1;
    ResultadoBFS bfs2;
};

class Arbol {
private:
    int n;
    vector<vector<int>> adj;

public:
    Arbol();
    Arbol(int vertices);

    void agregarArista(int u, int v);
    int obtenerN() const;
    const vector<vector<int>>& obtenerAdyacencia() const;

    ResultadoBFS ejecutarBFS(int inicio) const;
    ResultadoDiametro calcularDiametro(int nodoInicial = 0) const;

    void exportarTraza(const string& rutaArchivo, const ResultadoDiametro& resultado) const;
};

#endif

