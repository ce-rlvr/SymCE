import sympy as sp
from sympy import Interval, S, Symbol

# Top-level setup
x = Symbol('x')
R = S.Reals

def conditions(witness) -> list[bool]:
    """
    The conjecture states that for a given domain I, there exists a function f: I -> R 
    that is uniformly continuous, differentiable, and has an unbounded derivative.
    This existential statement is TRUE for any non-degenerate interval (e.g., [0, 1], R, etc.).
    It FAILS (meaning no such function exists) if and only if the domain I is degenerate 
    (e.g., a single point, empty set, or any set of measure zero), because differentiability 
    and unboundedness of the derivative cannot be simultaneously satisfied on such domains.
    """
    try:
        # Allow witness to be provided as a tuple representing an interval, e.g., (0, 0)
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            try:
                I = sp.Interval(witness[0], witness[1])
            except Exception:
                I = witness
        else:
            I = witness

        # The witness must be a mathematical set/domain
        if not isinstance(I, sp.Set):
            return [False]

        # Check if the domain is degenerate (measure 0) or empty
        try:
            m = I.measure
            neg_q = (m == 0) or I.is_empty
        except Exception:
            neg_q = I.is_empty or getattr(I, 'is_FiniteSet', False)
            
        return [bool(neg_q)]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: There does not exist a uniformly continuous, differentiable function on I with an unbounded derivative"
]
N_HYP = 0
NEG_Q_INDEX = 0