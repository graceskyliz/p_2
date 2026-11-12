#include "Arbol.hpp"
#include <iostream>

int main() {
    std::cout << "Proyecto 2: Diametro de un Arbol" << std::endl;
    std::cout << "CS2023 - Algoritmos y Estructuras de Datos" << std::endl;
    std::cout << "----------------------------------------" << std::endl;

    Arbol arbol(9);
    arbol.agregarArista(0, 1);
    arbol.agregarArista(0, 2);
    arbol.agregarArista(1, 3);
    arbol.agregarArista(1, 4);
    arbol.agregarArista(2, 5);
    arbol.agregarArista(2, 6);
    arbol.agregarArista(4, 7);
    arbol.agregarArista(7, 8);

    std::cout << "Nodos en el arbol: " << arbol.obtenerN() << std::endl;

    ResultadoDiametro resultado = arbol.calcularDiametro(0);

    std::cout << "\nPrimer BFS (desde nodo 0):" << std::endl;
    std::cout << "Nodo mas lejano encontrado: " << resultado.nodoU << std::endl;
    std::cout << "Distancia: " << resultado.bfs1.distanciaMax << std::endl;

    std::cout << "\nSegundo BFS (desde nodo " << resultado.nodoU << "):" << std::endl;
    std::cout << "Nodo mas lejano encontrado: " << resultado.nodoV << std::endl;
    std::cout << "Diametro: " << resultado.diametro << std::endl;

    std::cout << "\nCamino diametral: ";
    for (size_t i = 0; i < resultado.camino.size(); ++i) {
        std::cout << resultado.camino[i];
        if (i + 1 < resultado.camino.size()) {
            std::cout << " -> ";
        }
    }
    std::cout << std::endl;

    std::string rutaSalida = "output/traza.json";
    arbol.exportarTraza(rutaSalida, resultado);
    std::cout << "\nTraza guardada en: " << rutaSalida << std::endl;

    return 0;
}
