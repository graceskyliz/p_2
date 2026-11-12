#include "Arbol.hpp"
#include <iostream>
using namespace std;

int main() {
    cout << "Proyecto 2: Diametro de un Arbol" << endl;
    cout << "CS2023 - Algoritmos y Estructuras de Datos" << endl;
    cout << "----------------------------------------" << endl;

    Arbol arbol(9);
    arbol.agregarArista(0, 1);
    arbol.agregarArista(0, 2);
    arbol.agregarArista(1, 3);
    arbol.agregarArista(1, 4);
    arbol.agregarArista(2, 5);
    arbol.agregarArista(2, 6);
    arbol.agregarArista(4, 7);
    arbol.agregarArista(7, 8);

    cout << "Nodos en el arbol: " << arbol.obtenerN() << endl;

    ResultadoDiametro resultado = arbol.calcularDiametro(0);

    cout << "\nPrimer BFS (desde nodo 0):" << endl;
    cout << "Nodo mas lejano encontrado: " << resultado.nodoU << endl;
    cout << "Distancia: " << resultado.bfs1.distanciaMax << endl;

    cout << "\nSegundo BFS (desde nodo " << resultado.nodoU << "):" << endl;
    cout << "Nodo mas lejano encontrado: " << resultado.nodoV << endl;
    cout << "Diametro: " << resultado.diametro << endl;

    cout << "\nCamino diametral: ";
    for (size_t i = 0; i < resultado.camino.size(); ++i) {
        cout << resultado.camino[i];
        if (i + 1 < resultado.camino.size()) {
            cout << " -> ";
        }
    }
    cout << endl;

    string rutaSalida = "output/traza.json";
    arbol.exportarTraza(rutaSalida, resultado);
    cout << "\nTraza guardada en: " << rutaSalida << endl;

    return 0;
}
