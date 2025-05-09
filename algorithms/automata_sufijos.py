from automata.automata import Automata
from automata.node import AutomataState

def automata_sufijos(pattern: str) -> 'Automata':
    # creamos el automata
    automata = Automata()
    # sea p = p1...pm
    # construimos el estado final q_m+1
    m = len(pattern)
    q_m1 = AutomataState(name=f"q_${m+1}", is_accepting=True)
    # para i \in [m, 1]
    for i in range(m, 0, -1):
        # construimos el estado q_i
        q_i = AutomataState(name=f"q_{i}")
        # agregamos la transicion (q_i, p_i) -> q_i+1
        automata.add_transition(q_i.get_name(), p[i-1], f"q_{i+1}")
    # construimos el estado inicial
    q0 = AutomataState(name="q_0")
    # para i \in [0, m]
    for i in range(m+1):
        # agregamos la transicion (q0, p_i) -> q_i
        automata.add_epsilon_transition(q0.get_name(), f"q_{i}")

    return automata