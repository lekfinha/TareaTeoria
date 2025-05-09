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

    def to_dict(self): # Added method
        return {"len_pattern": self.len_pattern, "time": self.time}

# Or even simpler if only Results objects need custom handling:
def results_serializer(obj):
    if isinstance(obj, Results):
        return obj.to_dict() # or directly return the dict here
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def main():
    alphabet = ["A", "C", "G", "T"]
    n = 2**15 # Reducido para pruebas más rápidas, ajústalo a 2**20 para tu experimento final
    j_values = [6, 7, 8, 9, 10] # Renombrado 'j' a 'j_values' para claridad

    # Inicializamos las listas de resultados
    results_bdm: list[Results] = []
    results_kmp: list[Results] = []
    results_boyer_moore: list[Results] = []

    num_repetitions = 5 # Reducido para pruebas más rápidas, ajústalo a 10

    print(f"Generando texto base de longitud {n}...")
    text = crear_texto(alphabet, n) # Generar el texto una vez si es el mismo para todos los patrones
    print("Texto generado.")

    for i in j_values:
        # Para cada longitud de patrón, repetimos el experimento
        for rep_num in range(num_repetitions):
            current_pattern_len_target = 2**i
            print(f"Iteración para j={i} (longitud de patrón: 2^{i}={current_pattern_len_target}), Repetición: {rep_num + 1}/{num_repetitions}")

            # Obtenemos el patron (podrías querer generar un nuevo texto y patrón cada vez si el experimento lo requiere)
            # Si el texto es el mismo, solo varía el patrón.
            pattern = obtener_patron(text, i) # obtener_patron toma el exponente i

            if not pattern: # Manejar caso de patrón vacío si obtener_patron puede retornarlo
                print(f"Advertencia: Patrón vacío para j={i}. Saltando esta iteración.")
                continue

            actual_len_pattern = len(pattern) # Longitud real del patrón generado

            # Medimos el tiempo de ejecucion del algoritmo BDM
            start_time = time.perf_counter() # CAMBIO AQUÍ
            backwards_dawg_matching(text, pattern)
            end_time = time.perf_counter()   # CAMBIO AQUÍ
            results_bdm.append(Results(actual_len_pattern, end_time - start_time))

            # Haz lo mismo para KMP y Boyer-Moore para consistencia
            start_time = time.perf_counter() # CAMBIO AQUÍ
            kmp_search(text, pattern)
            end_time = time.perf_counter()   # CAMBIO AQUÍ
            results_kmp.append(Results(actual_len_pattern, end_time - start_time))

            start_time = time.perf_counter() # CAMBIO AQUÍ
            boyer_moore(text, pattern)
            end_time = time.perf_counter()   # CAMBIO AQUÍ
            results_boyer_moore.append(Results(actual_len_pattern, end_time - start_time))

    results_to_serialize = [ # Renombrado para evitar confusión con la clase Results
        {
            "alg": "BDM",
            "results": results_bdm, # results_bdm es una lista de objetos Results
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

    # Graficamos los resultados
    for result_group in results_to_serialize:
        alg = result_group["alg"]
        data = result_group["results"] # data es una lista de objetos Results

        # Extraemos los tiempos y las longitudes de los patrones
        # Asegurarse que data no esté vacía
        if data:
            times = [res.time for res in data]
            len_patterns = [res.len_pattern for res in data]
            plot_2d(len_patterns, times, title=f"Algoritmo {alg}", xlabel="Longitud del patrón", ylabel="Tiempo (s)")
        else:
            print(f"No hay datos para graficar para el algoritmo {alg}.")

    # Guardamos los resultados en un archivo json
    output_filename = "results.json"
    try:
        with open(output_filename, "w") as f:
            json.dump(results_to_serialize, f, indent=4, default=results_serializer)
        print(f"\nResultados guardados exitosamente en {output_filename}")
    except Exception as e:
        print(f"\nError al guardar los resultados en JSON: {e}")


# This is the main entry point of the script.
if __name__ == "__main__":
    main()