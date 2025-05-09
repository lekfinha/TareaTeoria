from automata.node import AutomataState

class Automata:
    """
    Clase que representa un autómata finito.
    Maneja tanto autómatas deterministas (AFD) como no deterministas (AFND).
    """

    def __init__(self,
                 states: list[AutomataState] = None,
                 alphabet: list[str] = None,
                 transitions: dict[str, dict[str, list[AutomataState]]] = None,
                 initial_state: AutomataState = None,
                 final_states: list[AutomataState] = None):
        # Inicializar con valores por defecto si son None
        self.states = states or []
        self.alphabet = alphabet or []
        self.transitions = transitions or {}
        self.initial_state = initial_state
        self.final_states = final_states or []
        self.epsilon = "ε"

        # Validaciones
        if self.states:
            if not all(isinstance(s, AutomataState) for s in self.states):
                raise ValueError("Todos los estados deben ser instancias de AutomataState")
            
            state_names = [s.name for s in self.states]
            if len(state_names) != len(set(state_names)):
                raise ValueError("Nombres de estados duplicados")

        if self.final_states:
            invalid = [s for s in self.final_states if s not in self.states]
            if invalid:
                raise ValueError(f"Estados finales no existen en la lista de estados: {[s.name for s in invalid]}")

        if self.initial_state and self.initial_state not in self.states:
            raise ValueError("El estado inicial debe estar en la lista de estados")

    def add_state(self, state: AutomataState):
        """Añade un estado al autómata"""
        if not isinstance(state, AutomataState):
            raise ValueError("Debe ser una instancia de AutomataState")
            
        if state.name in [s.name for s in self.states]:
            raise ValueError(f"Estado duplicado: {state.name}")
            
        self.states.append(state)

    def add_transition(self, from_state: str, symbol: str, to_states: list[str]):
        """Añade una transición entre estados"""
        if symbol not in self.alphabet and symbol != self.epsilon:
            raise ValueError(f"Símbolo '{symbol}' no está en el alfabeto")

        from_state_obj = next((s for s in self.states if s.name == from_state), None)
        if not from_state_obj:
            raise ValueError(f"Estado origen '{from_state}' no existe")

        to_states_objs = []
        for to_state in to_states:
            state = next((s for s in self.states if s.name == to_state), None)
            if not state:
                raise ValueError(f"Estado destino '{to_state}' no existe")
            to_states_objs.append(state)

        if from_state not in self.transitions:
            self.transitions[from_state] = {}
            
        self.transitions[from_state][symbol] = to_states_objs
        from_state_obj.add_transition(symbol, to_states_objs)

    def add_epsilon_transition(self, from_state: str, to_state: str):
        """Añade una transición épsilon"""
        self.add_transition(from_state, self.epsilon, [to_state])

    def to_deterministic(self):
        """Convierte el autómata a determinista usando construcción de subconjuntos"""
        # Implementación completa del algoritmo de subconjuntos
        new_states = []
        new_transitions = {}
        state_queue = []

        # Estado inicial: ε-closure del estado inicial original
        initial_closure = self._epsilon_closure([self.initial_state])
        new_initial = AutomataState(
            name=str(sorted([s.name for s in initial_closure])),
            is_accepting=any(s in self.final_states for s in initial_closure)
        )
        new_states.append(new_initial)
        state_queue.append(initial_closure)

        # Procesar todos los estados nuevos
        while state_queue:
            current_set = state_queue.pop(0)
            current_state_name = new_states[len(new_states) - len(state_queue) - 1].name

            for symbol in self.alphabet:
                next_states = []
                for state in current_set:
                    next_states.extend(state.get_next_states(symbol) or [])
                
                if not next_states:
                    continue
                
                closure = self._epsilon_closure(next_states)
                closure_name = str(sorted(list({s.name for s in closure})))

                existing = next((s for s in new_states if s.name == closure_name), None)
                if not existing:
                    new_state = AutomataState(
                        name=closure_name,
                        is_accepting=any(s in self.final_states for s in closure)
                    )
                    new_states.append(new_state)
                    state_queue.append(closure)
                    existing = new_state

                if current_state_name not in new_transitions:
                    new_transitions[current_state_name] = {}
                new_transitions[current_state_name][symbol] = [existing.name]

        # Actualizar propiedades del autómata
        self.states = new_states
        self.transitions = new_transitions
        self.initial_state = new_initial
        self.final_states = [s for s in new_states if s.is_accepting]

    def _epsilon_closure(self, states: list[AutomataState]) -> list[AutomataState]:
        """Calcula la ε-clausura para un conjunto de estados"""
        closure = set(states)
        stack = list(states)
        
        while stack:
            state = stack.pop()
            epsilon_transitions = state.get_next_states(self.epsilon) or []
            for s in epsilon_transitions:
                if s not in closure:
                    closure.add(s)
                    stack.append(s)
        
        return list(closure)

    def __str__(self):
        return (
            f"Automata(\n"
            f"  Estados: {[s.name for s in self.states]}\n"
            f"  Alfabeto: {self.alphabet}\n"
            f"  Estado Inicial: {self.initial_state.name if self.initial_state else None}\n"
            f"  Estados Finales: {[s.name for s in self.final_states]}\n"
            f"  Transiciones: {self.transitions}\n)"
        )