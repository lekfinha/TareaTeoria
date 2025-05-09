from automata.automata import Automata
from automata.node import AutomataState

def construir_automata_sufijos(pattern: str) -> Automata:
    # 1. Definir el alfabeto con los símbolos únicos del patrón
    alphabet = list(set(pattern))
    
    # 2. Crear el autómata con el alfabeto correcto
    automata = Automata(alphabet=alphabet)
    m = len(pattern)
    
    # 3. Crear y añadir estados (q0, q1, ..., qm+1)
    for i in range(m + 2):
        state = AutomataState(name=f"q{i}")
        automata.add_state(state)
    
    # 4. Configurar estado inicial (q0)
    automata.initial_state = next(s for s in automata.states if s.name == "q0")
    
    # 5. Marcar estado final (qm+1)
    final_state = next(s for s in automata.states if s.name == f"q{m+1}")
    final_state.is_accepting = True
    automata.final_states.append(final_state)
    
    # 6. Añadir transiciones para el patrón
    for i in range(m):
        automata.add_transition(f"q{i}", pattern[i], [f"q{i+1}"])
    
    # 7. Añadir transiciones épsilon desde q0
    for i in range(m + 1):
        automata.add_epsilon_transition("q0", f"q{i}")
    
    return automata

def dawg(pattern: str) -> Automata:
    afnd = construir_automata_sufijos(pattern)
    afnd.to_deterministic()
    return afnd