import collections

class AutomataState:
    """
    A class representing a state in an automata.

    Attributes:
        name (str): The name of the state.
        is_accepting (bool): Indicates if the state is an accepting state.
        transitions (dict: str -> AutomataState): A dictionary mapping input symbols to the next state.

    Methods:
        add_transition(symbol: str, state: AutomataState): Adds a transition from this state to another state for a given symbol.
        get_next_state(symbol: str): Returns the next state for a given input symbol.
    """

    def __init__(self, name: str, is_accepting: bool = False, is_error: bool = False):
        self.name = name
        self.is_accepting = is_accepting
        self.is_error = is_error
        self.transitions: dict[str, 'AutomataState'] = {}
        self._nfa_transitions_store: dict[str, set[AutomataState]] = collections.defaultdict(set)

    # getters
    def get_name(self) -> str:
        """Returns the name of the state."""
        return self.name
    def is_accepting_state(self) -> bool:
        """Returns whether the state is an accepting state."""
        return self.is_accepting

    def is_error_state(self) -> bool:
        """Returns whether the state is an error state."""
        return self.is_error

    def add_transition(self, symbol: str, state: 'AutomataState'):
        """Adds a transition from this state to another state for a given symbol."""
        self.transitions[symbol] = state

    def add_nfa_transition(self, symbol: str, next_state: 'AutomataState'):
        """Añade una transición NFA (para construir el NFA inicial)."""
        self._nfa_transitions_store[symbol].add(next_state)

    def get_nfa_transitions(self, symbol: str) -> set['AutomataState']:
        """Obtiene todos los estados destino NFA para un símbolo."""
        return self._nfa_transitions_store.get(symbol, set())

    def get_next_state(self, symbol: str) -> 'AutomataState':
        """Returns the next state for a given input symbol."""
        return self.transitions.get(symbol)

    # Métodos necesarios para usar AutomataState en sets y como claves de diccionario (indirectamente)
    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, AutomataState):
            return self.name == other.name
        return False

    def __lt__(self, other): # Para ordenar nombres de estado consistentemente
        if isinstance(other, AutomataState):
            return self.name < other.name
        return NotImplemented

    def __repr__(self):
        # Representación útil para depuración
        accept_str = "Accepting" if self.is_accepting else "Non-Accepting"
        return f"State({self.name}, {accept_str})"

