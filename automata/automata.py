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

        # Check if all states are instances of AutomataState
        if not all(isinstance(state, AutomataState) for state in states):
            raise ValueError("All states must be instances of AutomataState.")

        # Check if all final states are instances of AutomataState
        if not all(isinstance(state, AutomataState) for state in final_states):
            raise ValueError("All final states must be instances of AutomataState.")

        # Check if the initial state is an instance of AutomataState
        if not isinstance(initial_state, AutomataState):
            raise ValueError("Initial state must be an instance of AutomataState.")

        # Check if the initial state is in the list of states
        if initial_state not in states:
            raise ValueError("Initial state must be in the list of states.")

        # Check if all states are unique
        states_names = {}
        for state in states:
            if state.name in states_names:
                raise ValueError(f"State '{state.name}' is not unique.")
            states_names[state.name] = state

        # Check if the final states are in the list of states
        for state in final_states:
            if state not in states:
                raise ValueError(f"Final state '{state.name}' is not in the list of states.")

        # Check if all final states are unique
        final_states_names = {}
        for state in final_states:
            if state.name in final_states_names:
                raise ValueError(f"Final state '{state.name}' is not unique.")
            final_states_names[state.name] = state


        # Check if all transitions are valid
        for state, transition in transitions.items():
            # Check if the name of the state is a string
            if not isinstance(state, str):
                raise ValueError("State names must be strings.")
            # Check if the transition name is in the states
            if not any(state == s.name for s in states):
                raise ValueError(f"State '{state}' is not in the list of states.")
            if not all(isinstance(t, dict) for t in transition.values()):
                raise ValueError("Transitions must be dictionaries.")
            for symbol, next_state in transition.items():
                # Check if the symbol is in the alphabet
                if symbol not in alphabet:
                    raise ValueError(f"Symbol '{symbol}' is not in the alphabet.")
                # Check if the next state is in the states
                if not any(next_state == s.name for s in states):
                    raise ValueError(f"Next state '{next_state}' is not in the list of states.")
                # Check if the symbol is a string
                if not isinstance(symbol, str):
                    raise ValueError("Transition symbols must be strings.")
                # Check if the next state is an instance of AutomataState
                if not isinstance(next_state, AutomataState):
                    raise ValueError("Next state must be an instance of AutomataState.")

        # Put the transitions in the corresponding state object
        for state in states:
            state.transitions = transitions.get(state.name, {})


        # Initialize the automata
        self.epsilon = "ε"
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

    def add_state(self, state: 'AutomataState'):
        """
        Add a state to the automata.

        :param state: The state to add
        """
        if not isinstance(state, AutomataState):
            raise ValueError("State must be an instance of AutomataState.")

        # Check if the state is unique
        if any(state.name == s.name for s in self.states):
            raise ValueError(f"State '{state.name}' is not unique.")

        self.states.append(state)

    def add_transition(self, state_name: str, symbol: str, next_state_name: str):
        """
        Add a transition to the automata.

        :param state_name: The state id to add the transition to
        :param symbol: The symbol of the transition
        :param next_state_name: The next state of the transition
        """
        # Check if the state is in the list of states
        state = next((s for s in self.states if s.name == state_name), None)
        if state is None:
            raise ValueError(f"State '{state_name}' is not in the list of states.")
        # Check if the next state is in the list of states
        next_state = next((s for s in self.states if s.name == next_state_name), None)
        if next_state is None:
            raise ValueError(f"Next state '{next_state_name}' is not in the list of states.")
        # Check if the symbol is in the alphabet
        if symbol not in self.alphabet:
            raise ValueError(f"Symbol '{symbol}' is not in the alphabet.")

        # Agregamos la transicion al estado
        state.add_transition(symbol, next_state)
        # Agregamos la transicion al automata
        # Check if the state is already in the transitions dictionary
        if state.name not in self.transitions:
            # If not, create a new dictionary for the state
            self.transitions[state.name] = {}
        # Check if the symbol is already in the transitions dictionary for the state
        if symbol not in self.transitions[state.name]:
            # If not, create a new dictionary for the symbol
            self.transitions[state.name][symbol] = next_state

    def add_epsilon_transition(self, state_name: str, next_state_name: str):
        """
        Add an epsilon transition to the automata.

        :param state_name: The state id to add the transition to
        :param next_state_name: The next state of the transition
        """
        self.add_transition(state_name, self.epsilon, next_state_name)

    def to_deterministic(self):
        """
        Convert the automata to a deterministic automata.
        """
        # 1. Obtain de actual automata states, alphabet, transitions, initial state and final states
        actual_states = self.states
        actual_alphabet = self.alphabet
        actual_transitions = self.transitions
        actual_initial_state = self.initial_state
        actual_final_states = self.final_states
        # 2. Create the new automata
        new_states = []
        new_transitions = {}
        new_final_states = []
        new_alphabet = actual_alphabet
        new_initial_state = None
        # 3. Reset the states and transitions
        self.states = []
        self.transitions = {}
        # 4. Add the states to the new automata with no transitions
        for state in actual_states:
            new_state = AutomataState(name=state.name, is_accepting=state.is_accepting)
            self.add_state(new_state)
        #
        # 2. Create a new initial state
        new_initial_state = AutomataState(name=self.initial_state.name, is_accepting=self.initial_state.is_accepting)
        new_states.append(new_initial_state)
        # 3. Create a new final state
        for state in self.final_states:
            new_final_state = AutomataState(name=state.name, is_accepting=True)
            new_final_states.append(new_final_state)
            new_states.append(new_final_state)

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