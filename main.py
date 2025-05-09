# main
import json
import time

from algorithms.backwards_dawg_matching import backwards_dawg_matching
from algorithms.boyer_moore import boyer_moore
from algorithms.knuth_morris_pratt import kmp_search
from data.crear_texto import crear_texto
from data.obtener_patron import obtener_patron
from graphics.plot_2d import plot_2d


# This function generates a random DNA sequence of length n.
class Results:
    def __init__(self, len_pattern: int, time: float):
        self.len_pattern = len_pattern
        self.time = time



def main():
    alphabet = ["A", "C", "G", "T"]
    n = 2**20
    j = [6, 7, 8, 9, 10]
    # Inicializamos las listas de resultados
    results_bdm: list[Results] = []
    results_kmp: list[Results] = []
    results_boyer_moore: list[Results] = []
    # Generamos el texto aleatorio
    for i in j:
        # repetimos el experimento 10 veces
        for _ in range(10):
            print(f"j: {i}")
            text = crear_texto(alphabet, n)
            # Obtenemos el patron
            pattern = obtener_patron(text, i)
            len_pattern = len(pattern)
            # Medimos el tiempo de ejecucion del algoritmo BDM
            start_time = time.time()
            backwards_dawg_matching(text, pattern)
            end_time = time.time()
            results_bdm.append(Results(len_pattern, end_time - start_time))
            # Medimos el tiempo de ejecucion del algoritmo KMP
            start_time = time.time()
            kmp_search(text, pattern)
            end_time = time.time()
            results_kmp.append(Results(len_pattern, end_time - start_time))
            # Medimos el tiempo de ejecucion del algoritmo Boyer-Moore
            start_time = time.time()
            boyer_moore(text, pattern)
            end_time = time.time()
            results_boyer_moore.append(Results(len_pattern, end_time - start_time))

    results = [
        {
            "alg": "BDM",
            "results": results_bdm,
        },
        {
            "alg": "KMP",
            "results": results_kmp,
        },
        {
            "alg": "BM",
            "results": results_boyer_moore,
        }
    ]
    # graficamos los resultados
    for result in results:
        alg = result["alg"]
        data = result["results"]
        # extraemos los tiempos y las longitudes de los patrones
        times = [res.time for res in data]
        len_patterns = [res.len_pattern for res in data]
        # graficamos
        plot_2d(len_patterns, times, title=f"Algoritmo {alg}", xlabel="Longitud del patrón", ylabel="Tiempo (s)")

    # guardamos los resultados en un archivo json
    with open("results.json", "w") as f:
        json.dump(results, f, indent=3)


# This is the main entry point of the script.
if __name__ == "__main__":
    main()