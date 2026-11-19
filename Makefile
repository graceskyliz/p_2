CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2

SRC = src/Arbol.cpp
MAIN = src/main.cpp
TEST_SRC = tests/test_arbol.cpp

all: main test_runner

main: $(SRC) $(MAIN)
	$(CXX) $(CXXFLAGS) -o main $(SRC) $(MAIN)

test_runner: $(SRC) $(TEST_SRC)
	$(CXX) $(CXXFLAGS) -o test_runner $(SRC) $(TEST_SRC)

run: main
	./main

test: test_runner
	./test_runner

video: main
	./main
	python3 animacion/animador.py

pdf:
	python3 docs/generar_pdf.py

clean:
	rm -f main test_runner output/traza.json output/traza_estrella.json output/video_diametro.mp4 output/subtitulos.srt output/audio_completo.wav docs/informe_final.pdf
	rm -rf output/fotogramas output/tmp_audio

.PHONY: all run test video pdf clean
