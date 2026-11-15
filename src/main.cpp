#include "Arbol.hpp"
#include <iostream>
using namespace std;

void procesarArbol(const Arbol& arbol, const string& nombre, const string& rutaSalida, int inicio = 0) {
    cout << "\n========================================" << endl;
    cout << "Procesando: " << nombre << endl;
    cout << "Cantidad de vertices: " << arbol.obtenerN() << endl;

    ResultadoDiametro res = arbol.calcularDiametro(inicio);

    cout << "Fase 1 (inicio=" << inicio << "): nodo lejano u=" << res.nodoU 
         << " a distancia " << res.bfs1.distanciaMax << endl;
    cout << "Fase 2 (inicio=" << res.nodoU << "): nodo lejano v=" << res.nodoV 
         << " a distancia " << res.bfs2.distanciaMax << endl;
    cout << "Diametro calculado: " << res.diametro << endl;

    cout << "Camino: ";
    for (size_t i = 0; i < res.camino.size(); ++i) {
        cout << res.camino[i];
        if (i + 1 < res.camino.size()) cout << " -> ";
    }
    cout << endl;

    arbol.exportarTraza(rutaSalida, res);
    cout << "Traza guardada en: " << rutaSalida << endl;
}

int main(int argc, char* argv[]) {
    cout << "Proyecto 2: Diametro de un Arbol" << endl;
    cout << "Algoritmos y Estructuras de Datos" << endl;

    if (argc >= 2) {
        string rutaArchivo = argv[1];
        string rutaSalida = (argc >= 3) ? argv[2] : "output/traza.json";
        Arbol a = Arbol::cargarDesdeArchivo(rutaArchivo);
        if (a.obtenerN() > 0) {
            procesarArbol(a, rutaArchivo, rutaSalida, 0);
        }
        return 0;
    }

    Arbol arbolGeneral = Arbol::cargarDesdeArchivo("data/arbol_general.txt");
    if (arbolGeneral.obtenerN() == 0) {
        arbolGeneral = Arbol(9);
        arbolGeneral.agregarArista(0, 1);
        arbolGeneral.agregarArista(0, 2);
        arbolGeneral.agregarArista(1, 3);
        arbolGeneral.agregarArista(1, 4);
        arbolGeneral.agregarArista(2, 5);
        arbolGeneral.agregarArista(2, 6);
        arbolGeneral.agregarArista(4, 7);
        arbolGeneral.agregarArista(7, 8);
    }
    procesarArbol(arbolGeneral, "Arbol General (9 nodos)", "output/traza.json", 0);

    Arbol arbolEstrella = Arbol::cargarDesdeArchivo("data/caso_estrella.txt");
    if (arbolEstrella.obtenerN() == 0) {
        arbolEstrella = Arbol(6);
        for (int i = 1; i <= 5; ++i) {
            arbolEstrella.agregarArista(0, i);
        }
    }
    procesarArbol(arbolEstrella, "Caso de Borde: Grafo Estrella (6 nodos)", "output/traza_estrella.json", 1);

    return 0;
}
