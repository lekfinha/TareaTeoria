from algorithms.automata_sufijos import automata_sufijos
from automata.automata import Automata
from automata.node import AutomataState


def dawg(
        automata: 'Automata',
        pattern: str
):
    """
    Constructs the DAWG (Deterministic Acyclic Word Graph) for a given pattern p.
    The DAWG is defined as the DFA resulting from subset construction on the NFA S(p),
    where S(p) recognizes all suffixes of p (including the empty suffix).

    Args:
        :param automata: The automata instance to which the DAWG will be added.
        :param pattern: The pattern p for which the DAWG is constructed.
    Returns:
        An instance of AutomataClass representing the DAWG(p).
    """
    automata = automata_sufijos(automata, pattern)
    # Convert the automata to a deterministic automata
    automata.to_deterministic()
    return automata



