# Automata is the class that represents an automata.
# It is used to create and manipulate automata.
from automata.node import AutomataState


class Automata:
    """
    Automata class that represents a finite automata.
    """

    def __init__(self,
                 states: list['AutomataState'] = None,
                 alphabet: list[str] = None,
                 transitions: dict[str, dict[str, 'AutomataState']] = None,
                 initial_state: 'AutomataState' = None,
                 final_states: list['AutomataState'] = None):
        """
        Initialize the automata with states, alphabet, transitions, initial state and final states.

        :param states: List of states
        :param alphabet: List of symbols
        :param transitions: Dictionary of transitions
        :param initial_state: Initial state
        :param final_states: List of final states
        """

        states = states or []
        alphabet = alphabet or []
        transitions = transitions or {}
        final_states = final_states or []

        # --- Validaciones (simplificadas para brevedad, las tuyas son más completas) ---
        if states and not all(isinstance(state, AutomataState) for state in states):
            raise ValueError("All states must be instances of AutomataState.")
        if initial_state and initial_state not in states:
            raise ValueError("Initial state must be in the list of states.")
        # ... (más validaciones de tu código original) ...

        # Esta línea es importante: configura state.transitions para cada estado.
        # Para un DFA, esto es dict[symbol, AutomataState_target].
        # Para un NFA, si los AutomataState ya tenían transiciones NFA en _nfa_transitions_store,
        # esta línea NO las afecta, lo cual es bueno.
        for state_obj in states: # Renombrado 'state' a 'state_obj' para claridad
            state_obj.transitions = transitions.get(state_obj.name, {})

        self.epsilon = "ε" # Símbolo Epsilon estándar
        self.states = states
        self.alphabet = alphabet
        # self.transitions almacena la visión general de las transiciones (estilo DFA)
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

    def add_state(self, state: 'AutomataState'):
        if not isinstance(state, AutomataState):
            raise ValueError("State must be an instance of AutomataState.")
        if any(state.name == s.name for s in self.states):
            raise ValueError(f"State '{state.name}' is not unique.")
        self.states.append(state)
        if state.is_accepting and state not in self.final_states: # Evitar duplicados
            self.final_states.append(state)

    def add_transition(self, state_name: str, symbol: str, next_state_name: str):
        """
        Añade una transición. Para NFA, esto debería usar state.add_nfa_transition.
        La actualización de self.transitions aquí es inherentemente DFA.
        Para esta tarea, nos enfocaremos en que los AutomataState tengan la info NFA.
        """
        state = next((s for s in self.states if s.name == state_name), None)
        next_s = next((s for s in self.states if s.name == next_state_name), None)

        if state is None: raise ValueError(f"State '{state_name}' not found.")
        if next_s is None: raise ValueError(f"Next state '{next_state_name}' not found.")
        if symbol != self.epsilon and symbol not in self.alphabet: # Permitir epsilon aunque no esté en el alfabeto principal
            # O añadirlo al alfabeto si es necesario:
            # if symbol not in self.alphabet: self.alphabet.append(symbol)
            raise ValueError(f"Symbol '{symbol}' not in alphabet (and not epsilon).")

        # Para NFA, la información crucial está en el estado mismo
        state.add_nfa_transition(symbol, next_s)

        # Esta parte actualiza self.transitions (la visión del autómata)
        # Si este autómata es un NFA, esta representación es limitada (sobrescribe)
        if state.name not in self.transitions:
            self.transitions[state.name] = {}
        self.transitions[state.name][symbol] = next_s # Estilo DFA: última transición gana

    def add_epsilon_transition(self, state_name: str, next_state_name: str):
        # Epsilon no necesita estar en self.alphabet para esta lógica,
        # pero sí para la conversión a DFA (se excluye explícitamente).
        state = next((s for s in self.states if s.name == state_name), None)
        next_s = next((s for s in self.states if s.name == next_state_name), None)
        if state is None: raise ValueError(f"State '{state_name}' not found.")
        if next_s is None: raise ValueError(f"Next state '{next_state_name}' not found.")

        state.add_nfa_transition(self.epsilon, next_s)
        # Opcionalmente, actualizar self.transitions si se quiere una representación (limitada)
        # if state.name not in self.transitions:
        #     self.transitions[state.name] = {}
        # self.transitions[state.name][self.epsilon] = next_s # Sobrescribe

    def epsilon_closure(self, state_or_states: AutomataState | set[AutomataState]) -> set[AutomataState]:
        """
        Calcula la clausura épsilon para un único estado NFA o un conjunto de estados NFA.
        Se basa en AutomataState.get_nfa_transitions() y el _nfa_transitions_store.
        """
        initial_states_for_closure: set[AutomataState]
        if isinstance(state_or_states, AutomataState):
            # Validar que el estado existe en el autómata
            if state_or_states not in self.states:
                s_obj_by_name = next((s for s in self.states if s.name == state_or_states.name), None)
                if not s_obj_by_name:
                    raise ValueError(f"State {state_or_states.name} not part of this automaton.")
                initial_states_for_closure = {s_obj_by_name}
            else:
                initial_states_for_closure = {state_or_states}
        elif isinstance(state_or_states, set):
            initial_states_for_closure = set()
            for s_in_set in state_or_states:
                if not isinstance(s_in_set, AutomataState):
                    raise ValueError("All elements in states_set must be AutomataState objects.")
                # Validar que los estados del conjunto existen en el autómata
                if s_in_set not in self.states:
                    s_obj_by_name = next((s for s in self.states if s.name == s_in_set.name), None)
                    if not s_obj_by_name:
                        raise ValueError(f"State {s_in_set.name} from set not part of this automaton.")
                    initial_states_for_closure.add(s_obj_by_name)
                else:
                    initial_states_for_closure.add(s_in_set)
        else:
            # Si se pasó un nombre de estado (string) para el caso de un solo estado
            s_obj = next((s for s in self.states if s.name == str(state_or_states)), None)
            if not s_obj:
                raise ValueError(f"State '{state_or_states}' not found or invalid type.")
            initial_states_for_closure = {s_obj}

        closure = set(initial_states_for_closure)  # Incluir los estados iniciales en su clausura
        stack = list(initial_states_for_closure)   # Estados a procesar

        while stack:
            current_s = stack.pop()
            # Usar get_nfa_transitions, que accede a _nfa_transitions_store
            epsilon_next_states = current_s.get_nfa_transitions(self.epsilon)

            for next_s in epsilon_next_states:
                if next_s not in closure:
                    closure.add(next_s)
                    stack.append(next_s)
        return closure

    def to_deterministic(self) -> 'Automata':
        """
        Convierte este autómata (asumido NFA) a un DFA equivalente.
        """
        if self.initial_state is None:
            raise ValueError("El NFA debe tener un estado inicial para la conversión a DFA.")

        # El alfabeto del DFA es el mismo que el del NFA, excluyendo épsilon.
        # Si epsilon no estaba en self.alphabet, no importa.
        dfa_alphabet = [sym for sym in self.alphabet if sym != self.epsilon]

        # dfa_q_map: mapea frozenset de AutomataStates del NFA al nuevo AutomataState del DFA
        dfa_q_map: dict[frozenset[AutomataState], AutomataState] = {}

        # Lista de conjuntos de estados NFA (representando estados DFA) aún no procesados.
        # Usamos una lista como cola (FIFO).
        unprocessed_dfa_q_frozensets: list[frozenset[AutomataState]] = []

        # Componentes del nuevo DFA
        dfa_states_list: list[AutomataState] = []
        dfa_initial_state_obj: AutomataState | None = None
        dfa_final_states_list: list[AutomataState] = []
        # Transiciones para el constructor del Automata DFA:
        # dict[nombre_estado_dfa_str, dict[simbolo_str, objeto_estado_destino_dfa]]
        dfa_transitions_for_constructor: dict[str, dict[str, AutomataState]] = {}

        # 1. Estado inicial del DFA
        # Es la clausura épsilon del estado inicial del NFA.
        nfa_s0_closure = self.epsilon_closure(self.initial_state)
        # Usamos frozenset porque los conjuntos no son hashables para ser claves de diccionario.
        dfa_initial_q_frozenset = frozenset(nfa_s0_closure)

        # Crear el nombre para el estado DFA (basado en los nombres de los estados NFA que contiene)
        # Ordenar para nombres canónicos y consistentes.
        if not dfa_initial_q_frozenset: # Muy improbable si initial_state existe
            dfa_initial_q_name = "{EMPTY_S0_CLOSURE}" # Nombre para un caso anómalo
        else:
            dfa_initial_q_name = "{" + ",".join(sorted(s.name for s in dfa_initial_q_frozenset)) + "}"

        # Un estado DFA es de aceptación si alguno de los estados NFA que contiene es de aceptación.
        is_dfa_s0_accepting = any(s.is_accepting for s in dfa_initial_q_frozenset)

        # Crear el objeto AutomataState para el estado inicial del DFA
        dfa_s0_obj = AutomataState(name=dfa_initial_q_name, is_accepting=is_dfa_s0_accepting)

        dfa_q_map[dfa_initial_q_frozenset] = dfa_s0_obj
        dfa_states_list.append(dfa_s0_obj)
        dfa_initial_state_obj = dfa_s0_obj
        if is_dfa_s0_accepting:
            dfa_final_states_list.append(dfa_s0_obj)

        unprocessed_dfa_q_frozensets.append(dfa_initial_q_frozenset)

        # 2. Procesar iterativamente los estados DFA (conjuntos de estados NFA)
        head = 0 # Usamos la lista `unprocessed_dfa_q_frozensets` como una cola
        while head < len(unprocessed_dfa_q_frozensets):
            current_nfa_states_frozenset = unprocessed_dfa_q_frozensets[head]
            head += 1

            current_dfa_state_obj = dfa_q_map[current_nfa_states_frozenset]
            # Preparar entrada para las transiciones de este estado DFA en el constructor
            dfa_transitions_for_constructor[current_dfa_state_obj.name] = {}

            # Para cada símbolo del alfabeto (excluyendo épsilon)
            for symbol in dfa_alphabet:
                # Calcular move(current_nfa_states_frozenset, symbol)
                # Es el conjunto de estados NFA a los que se puede llegar desde current_nfa_states_frozenset
                # con una transición por 'symbol'.
                move_result_set = set()
                for nfa_s_in_set in current_nfa_states_frozenset:
                    # Usar get_nfa_transitions de AutomataState, que accede a _nfa_transitions_store
                    transitions_on_symbol = nfa_s_in_set.get_nfa_transitions(symbol)
                    move_result_set.update(transitions_on_symbol)

                if not move_result_set: # No hay transiciones para este símbolo desde este conjunto de estados
                    continue

                    # El estado DFA destino es la clausura épsilon del conjunto `move_result_set`
                target_nfa_states_closure = self.epsilon_closure(move_result_set)
                target_nfa_states_frozenset = frozenset(target_nfa_states_closure)

                if not target_nfa_states_frozenset: # Clausura vacía (improbable si move_result no lo era)
                    continue

                # Si este conjunto de estados NFA (target_nfa_states_frozenset) no se ha visto antes,
                # representa un nuevo estado DFA.
                if target_nfa_states_frozenset not in dfa_q_map:
                    new_dfa_q_name = "{" + ",".join(sorted(s.name for s in target_nfa_states_frozenset)) + "}"
                    is_new_dfa_q_accepting = any(s.is_accepting for s in target_nfa_states_frozenset)

                    new_dfa_q_obj = AutomataState(name=new_dfa_q_name, is_accepting=is_new_dfa_q_accepting)

                    dfa_q_map[target_nfa_states_frozenset] = new_dfa_q_obj
                    dfa_states_list.append(new_dfa_q_obj)
                    if is_new_dfa_q_accepting:
                        dfa_final_states_list.append(new_dfa_q_obj)

                    # Añadir a la cola de procesamiento
                    unprocessed_dfa_q_frozensets.append(target_nfa_states_frozenset)

                # Obtener el objeto AutomataState del DFA destino (ya sea nuevo o existente)
                target_dfa_state_obj = dfa_q_map[target_nfa_states_frozenset]

                # Registrar la transición para el constructor del Automata DFA
                dfa_transitions_for_constructor[current_dfa_state_obj.name][symbol] = target_dfa_state_obj

                # Nota: No es necesario llamar a current_dfa_state_obj.add_transition(...) aquí,
                # porque el constructor de Automata (`Automata.__init__`) se encargará de poblar
                # el atributo `transitions` de cada `AutomataState` del DFA usando el
                # diccionario `dfa_transitions_for_constructor`.

        # 3. Construir y retornar el nuevo objeto Automata (que es un DFA)
        dfa = Automata(states=dfa_states_list,
                       alphabet=dfa_alphabet, # Alfabeto original menos épsilon
                       transitions=dfa_transitions_for_constructor,
                       initial_state=dfa_initial_state_obj,
                       final_states=dfa_final_states_list)
        return dfa

    def is_accepting_state(self, state_name: str) -> bool:
        """
        Check if a state is in the final states.

        :param state_name: The name of the state to check
        :return: True if the state is in the final states, False otherwise
        """
        # Check if the state is in the list of states
        state = next((s for s in self.states if s.name == state_name), None)
        if state is None:
            raise ValueError(f"State '{state_name}' is not in the list of states.")
        return state.is_accepting

    def get_transition_idx(self, state_name: str, symbol: str) -> str:
        """
        Get the transition for a given state and symbol.

        :param state_name: The name of the state
        :param symbol: The symbol to get the transition for
        :return: The next state for the given state and symbol
        """
        # Check if the state is in the list of states
        state = next((s for s in self.states if s.name == state_name), None)
        if state is None:
            raise ValueError(f"State '{state_name}' is not in the list of states.")
        # Check if the symbol is in the alphabet
        if symbol not in self.alphabet:
            raise ValueError(f"Symbol '{symbol}' is not in the alphabet.")
        return state.get_next_state(symbol).name

    def set_initial_state(self, state_name: str):
        """
        Set the initial state of the automata.

        :param state_name: The name of the state to set as initial
        """
        # Check if the state is in the list of states
        state = next((s for s in self.states if s.name == state_name), None)
        if state is None:
            raise ValueError(f"State '{state_name}' is not in the list of states.")
        self.initial_state = state


    def __repr__(self):
        """
        Return a string representation of the automata.
        """
        return \
            (f""
             f"Automata(states={self.states}, "
             f"alphabet={self.alphabet}, "
             f"transitions={self.transitions}, "
             f"initial_state={self.initial_state}, "
             f"final_states={self.final_states})"
            )

    def __str__(self):
        """
        Return a string representation of the automata.
        """
        return \
            (f""
             f"Automata(states={self.states}, "
             f"alphabet={self.alphabet}, "
             f"transitions={self.transitions}, "
             f"initial_state={self.initial_state}, "
             f"final_states={self.final_states})"
            )
    def test(self, string: list[str]) -> bool:
        """
        Test if the automata accepts a given string.

        :param string: The string to test
        :return: True if the string is accepted, False otherwise
        """
        current_state = self.initial_state
        for symbol in string:
            current_state = current_state.get_next_state(symbol)
            if current_state is None:
                return False
        return current_state.is_accepting