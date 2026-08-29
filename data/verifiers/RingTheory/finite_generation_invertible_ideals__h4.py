import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

# Top-level setup: named object bindings that the witness expression may reference.
# Since SymPy does not natively support non-finitely generated ideals, we provide 
# formal classes to allow the witness generator to express the counterexample.

class Ring:
    def __init__(self, name="R", commutative=True):
        self.name = name
        self.is_commutative = commutative

    def __eq__(self, other):
        if not isinstance(other, Ring):
            return False
        return self.name == other.name and self.is_commutative == other.is_commutative

class Ideal:
    def __init__(self, ring, finitely_generated=True):
        self.ring = ring
        self.is_ideal = True
        self.is_finitely_generated = finitely_generated

def conditions(witness) -> list[bool]:
    """
    Given a witness object, checks whether it is a valid counterexample.
    Expected witness format: a tuple (R, I, J) or a dict with keys 'R', 'I', 'J'.
    """
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            I = witness.get('I')
            J = witness.get('J')
        elif isinstance(witness, (list, tuple)) and len(witness) == 3:
            R, I, J = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: R is a commutative ring
    try:
        h1 = bool(getattr(R, 'is_commutative', False))
    except Exception:
        h1 = False

    # H_2: I is an ideal of R
    try:
        h2 = bool(getattr(I, 'is_ideal', False) and getattr(I, 'ring', None) == R)
    except Exception:
        h2 = False

    # H_3: J is an ideal of R
    try:
        h3 = bool(getattr(J, 'is_ideal', False) and getattr(J, 'ring', None) == R)
    except Exception:
        h3 = False

    # ¬Q: The ideal I is NOT finitely generated
    try:
        if hasattr(I, 'is_finitely_generated'):
            neg_q = not bool(I.is_finitely_generated)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "H_3: J is an ideal of R",
    "¬Q: I is not finitely generated"
]

N_HYP = 3
NEG_Q_INDEX = 3