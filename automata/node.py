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

    def __init__(self, name: str, is_accepting: bool = False):
        self.name = name
        self.is_accepting = is_accepting
        self.transitions = {}

    # getters
    def get_name(self) -> str:
        """Returns the name of the state."""
        return self.name
    def is_accepting_state(self) -> bool:
        """Returns whether the state is an accepting state."""
        return self.is_accepting

    def add_transition(self, symbol: str, state: 'AutomataState'):
        """Adds a transition from this state to another state for a given symbol."""
        self.transitions[symbol] = state

    def get_next_state(self, symbol: str) -> 'AutomataState':
        """Returns the next state for a given input symbol."""
        return self.transitions.get(symbol)

    def __hash__(self):
        """Returns the hash of the state."""
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, AutomataState):
            return self.name == other.name
        return False