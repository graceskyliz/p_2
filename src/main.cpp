#include "Arbol.hpp"
#include <iostream>

int main() {
    std::cout << "========================================" << std::endl;
    std::cout << "  AED - Proyecto 2: Diametro de un Arbol" << std::endl;
    std::cout << "  Avance 50% - Motor y Algoritmo" << std::endl;
    std::cout << "========================================" << std::endl;

    Arbol arbol(9);
    arbol.agregarArista(0, 1);
    arbol.agregarArista(0, 2);
    arbol.agregarArista(1, 3);
    arbol.agregarArista(1, 4);
    arbol.agregarArista(2, 5);
    arbol.agregarArista(2, 6);
    arbol.agregarArista(4, 7);
    arbol.agregarArista(7, 8);

    std::cout << "Arbol construido con " << arbol.obtenerN() << " nodos." << std::endl;

    ResultadoDiametro resultado = arbol.calcularDiametro(0);

    std::cout << "\n[Fase 1: Primer BFS desde nodo inicial 0]" << std::endl;
    std::cout << "Nodo mas lejano alcanzado (u): " << resultado.nodoU << std::endl;
    std::cout << "Distancia desde el inicio: " << resultado.bfs1.distanciaMax << std::endl;

    std::cout << "\n[Fase 2: Segundo BFS desde el nodo u = " << resultado.nodoU << "]" << std::endl;
    std::cout << "Nodo mas lejano alcanzado (v): " << resultado.nodoV << std::endl;
    std::cout << "Diametro del arbol: " << resultado.diametro << std::endl;

    std::cout << "\n[Camino Diametral]" << std::endl;
    for (size_t i = 0; i < resultado.camino.size(); ++i) {
        std::cout << resultado.camino[i];
        if (i + 1 < resultado.camino.size()) {
            std::cout << " -> ";
        }
    }
    std::cout << std::endl;

    std::string rutaSalida = "output/traza.json";
    arbol.exportarTraza(rutaSalida, resultado);
    std::cout << "\nTraza de ejecucion exportada a: " << rutaSalida << std::endl;

    return 0;
}
