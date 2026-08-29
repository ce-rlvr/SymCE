import sympy
import itertools

# Top-level setup for witness expressions
Reals = sympy.S.Reals
Empty = sympy.S.EmptySet
Interval = sympy.Interval
FiniteSet = sympy.FiniteSet
Union = sympy.Union

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be an iterable or a callable (representing a sequence) 
    of sympy.Set objects.
    """
    # H_1: X is a topological space
    # We verify this by checking that the witness provides a valid sequence of subsets of R.
    try:
        if callable(witness):
            sets = [witness(n) for n in range(1, 20)]
        elif hasattr(witness, '__iter__') and not isinstance(witness, (list, tuple, set)):
            sets = list(itertools.islice(witness, 100))
        else:
            sets = list(witness)
            
        h1_ok = len(sets) > 0 and all(isinstance(s, sympy.Set) for s in sets)
    except Exception:
        h1_ok = False

    def is_connected(s):
        if isinstance(s, sympy.Interval):
            return True
        if isinstance(s, sympy.FiniteSet) and len(s) <= 1:
            return True
        if getattr(s, 'is_EmptySet', False):
            return True
        if s in (sympy.S.Reals, sympy.S.UniversalSet):
            return True
        return False

    # H_2: {A_n} is a sequence of connected subsets of X
    try:
        h2_ok = h1_ok and all(is_connected(s) for s in sets)
    except Exception:
        h2_ok = False

    # ¬Q: The union of A_n is NOT connected
    try:
        if h1_ok:
            union_set = sympy.Union(*sets)
            neg_q_ok = not is_connected(union_set)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: X is a topological space",
    "H_2: {A_n} is a sequence of connected subsets of X",
    "¬Q: The union of A_n is not connected"
]

N_HYP = 2
NEG_Q_INDEX = 2