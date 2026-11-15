#include "../src/Arbol.hpp"
#include <iostream>
#include <cassert>
using namespace std;

void testUnSoloNodo() {
    Arbol a(1);
    ResultadoDiametro res = a.calcularDiametro(0);
    assert(res.diametro == 0);
    assert(res.camino.size() == 1);
    assert(res.camino[0] == 0);
    cout << "[PASS] Test Un Solo Nodo" << endl;
}

void testDosNodos() {
    Arbol a(2);
    a.agregarArista(0, 1);
    ResultadoDiametro res = a.calcularDiametro(0);
    assert(res.diametro == 1);
    assert(res.camino.size() == 2);
    cout << "[PASS] Test Dos Nodos" << endl;
}

void testGrafoEstrella() {
    Arbol a(6);
    for (int i = 1; i <= 5; ++i) {
        a.agregarArista(0, i);
    }
    ResultadoDiametro res = a.calcularDiametro(0);
    assert(res.diametro == 2);
    assert(res.camino.size() == 3);
    cout << "[PASS] Test Grafo Estrella" << endl;
}

void testGrafoLinea() {
    Arbol a(5);
    for (int i = 0; i < 4; ++i) {
        a.agregarArista(i, i + 1);
    }
    ResultadoDiametro res = a.calcularDiametro(2);
    assert(res.diametro == 4);
    assert(res.camino.size() == 5);
    cout << "[PASS] Test Grafo Linea" << endl;
}

void testArbolBinarioCompleto() {
    Arbol a(7);
    a.agregarArista(0, 1);
    a.agregarArista(0, 2);
    a.agregarArista(1, 3);
    a.agregarArista(1, 4);
    a.agregarArista(2, 5);
    a.agregarArista(2, 6);
    ResultadoDiametro res = a.calcularDiametro(0);
    assert(res.diametro == 4);
    assert(res.camino.size() == 5);
    cout << "[PASS] Test Arbol Binario Completo" << endl;
}

void testArbolAsimetrico() {
    Arbol a(9);
    a.agregarArista(0, 1);
    a.agregarArista(0, 2);
    a.agregarArista(1, 3);
    a.agregarArista(1, 4);
    a.agregarArista(2, 5);
    a.agregarArista(2, 6);
    a.agregarArista(4, 7);
    a.agregarArista(7, 8);
    ResultadoDiametro res = a.calcularDiametro(0);
    assert(res.diametro == 6);
    assert(res.camino.size() == 7);
    cout << "[PASS] Test Arbol Asimetrico" << endl;
}

void testCargarDesdeArchivo() {
    Arbol a = Arbol::cargarDesdeArchivo("data/arbol_general.txt");
    assert(a.obtenerN() == 9);
    ResultadoDiametro res = a.calcularDiametro(0);
    assert(res.diametro == 6);

    Arbol b = Arbol::cargarDesdeArchivo("data/caso_estrella.txt");
    assert(b.obtenerN() == 6);
    ResultadoDiametro resB = b.calcularDiametro(1);
    assert(resB.diametro == 2);

    cout << "[PASS] Test Carga Desde Archivo" << endl;
}

int main() {
    cout << "--- Ejecutando Pruebas Unitarias del Arbol ---" << endl;
    testUnSoloNodo();
    testDosNodos();
    testGrafoEstrella();
    testGrafoLinea();
    testArbolBinarioCompleto();
    testArbolAsimetrico();
    testCargarDesdeArchivo();
    cout << "--- Todas las pruebas pasaron con exito! ---" << endl;
    return 0;
}
