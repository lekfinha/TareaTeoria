import json
import time
from typing import List
from dataclasses import dataclass

from algorithms.backwards_dawg_matching import backwards_dawg_matching
from algorithms.boyer_moore import boyer_moore
from algorithms.knuth_morris_pratt import kmp_search
from data.crear_texto import crear_texto
from data.obtener_patron import obtener_patron
from graphics.plot_2d import plot_2d

@dataclass
class Results:
    len_pattern: int
    time: float

def benchmark_algorithm(algo_name: str, algo_func, text: str, pattern: str) -> Results:
    """Ejecuta y mide el tiempo de un algoritmo de búsqueda"""
    print(f" Ejecutando {algo_name}...", end=' ', flush=True)
    start_time = time.time()
    algo_func(text, pattern)
    elapsed = time.time() - start_time
    print(f"{algo_name}: {elapsed:.4f}s")
    return Results(len(pattern), elapsed)

def main():
    # Configuración reducida para pruebas
    alphabet = ["A", "C", "G", "T"]
    n = 2**10 # Con números más grandes se demora demasiado, falta optimizar bdm
    j_values = [6,7,8,9,10]  # con j = 10 ya no funciona por el limite que tiene n
    
    print(f"\nIniciando experimento con texto de tamaño {n}")
    print(f"Valores de j: {j_values}\n")
    
    results = {
        "BDM": [],
        "KMP": [],
        "BM": []
    }

    for j in j_values:
        pattern_length = 2**j
        print(f"\nProcesando j = {j} (m = {pattern_length})")
        
        for rep in range(10):
            print(f"\nRepetición {rep + 1}/10")
            
            # 1. Generación de datos
            print("Generando texto...", end=' ', flush=True)
            text = crear_texto(alphabet, n)
            print(f"✅ Texto generado (primeros 10 chars: {text[:10]}...)")
            
            # 2. Obtención de patrón
            print("🔄 Obteniendo patrón...", end=' ', flush=True)
            pattern = obtener_patron(text, j)
            if not pattern:
                print("Error: No se pudo obtener patrón")
                continue
            print(f"Patrón obtenido: {pattern[:10]}... (len={len(pattern)})")
            
            # 3. Benchmarking
            results["BDM"].append(benchmark_algorithm("BDM", backwards_dawg_matching, text, pattern))
            results["KMP"].append(benchmark_algorithm("KMP", kmp_search, text, pattern))
            results["BM"].append(benchmark_algorithm("Boyer-Moore", boyer_moore, text, pattern))

    # Resultados y visualización
    print("\nResultados obtenidos:")
    for algo, data in results.items():
        avg_time = sum(r.time for r in data) / len(data) if data else 0
        print(f"{algo}: {len(data)} ejecuciones, tiempo promedio = {avg_time:.6f}s")

    # Guardar resultados
    with open("results.json", "w") as f:
        json.dump({
            "config": {
                "text_length": n,
                "pattern_lengths": [2**j for j in j_values],
                "repetitions": 2
            },
            "results": {
                algo: [{"len": r.len_pattern, "time": r.time} for r in data]
                for algo, data in results.items()
            }
        }, f, indent=2)
    
    print("\nGenerando gráficos...")
    for algo, data in results.items():
        if data:
            plot_2d(
                [r.len_pattern for r in data],
                [r.time for r in data],
                title=f"Tiempos de {algo}",
                xlabel="Longitud de patrón",
                ylabel="Tiempo (s)"
            )

    print("\nTodos los experimentos completados!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nEjecución interrumpida por el usuario")
    except Exception as e:
        print(f"\nError inesperado: {str(e)}")
        raise