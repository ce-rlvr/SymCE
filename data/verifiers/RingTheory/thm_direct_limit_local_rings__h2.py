import sympy
from sympy.abc import x, y, z

class DirectedSystem:
    """
    A mock class to represent a directed system of rings.
    Since SymPy cannot natively compute infinite direct limits of rings,
    this class allows the witness to specify the mathematical properties directly.
    """
    def __init__(self, is_directed_system_of_local_rings=True, limit_is_local_ring=False):
        self.is_directed_system_of_local_rings = is_directed_system_of_local_rings
        self.limit_is_local_ring = limit_is_local_ring

# Top-level setup: named object bindings that the witness expression may reference.
System = DirectedSystem
DirectedSystemOfLocalRings = DirectedSystem

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    """
    # Check Hypothesis 1: (R_i, f_{ij}) is a directed system of local rings
    try:
        h1 = getattr(witness, 'is_directed_system_of_local_rings', 
             getattr(witness, 'is_local_rings', 
             getattr(witness, 'is_directed_system', False)))
        h1_ok = bool(h1)
    except Exception:
        h1_ok = False

    # Check Negated Conclusion: The direct limit of the system is NOT a local ring
    try:
        limit_local = getattr(witness, 'limit_is_local_ring', 
                      getattr(witness, 'limit_is_local', True))
        neg_q_ok = not bool(limit_local)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: (R_i, f_{ij}) is a directed system of local rings",
    "¬Q: The direct limit of the system is not a local ring"
]

N_HYP = 1
NEG_Q_INDEX = 1