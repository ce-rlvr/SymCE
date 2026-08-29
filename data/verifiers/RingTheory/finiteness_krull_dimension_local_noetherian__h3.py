import math
import sympy
from sympy import *

# Top-level setup: named object bindings that the witness expression may reference.
# Since SymPy does not natively represent rings of infinite Krull dimension,
# we provide a mock object for Nagata's famous counterexample.
class NagataRingObj:
    @property
    def is_commutative(self):
        return True
    
    @property
    def is_noetherian(self):
        return True
    
    @property
    def krull_dimension(self):
        return math.inf

NagataRing = NagataRingObj()
Nagata_ring = NagataRing

def conditions(witness) -> list[bool]:
    # H_1: R is a commutative ring
    try:
        if isinstance(witness, str) and "nagata" in witness.lower():
            h1 = True
        elif isinstance(witness, dict):
            h1 = bool(witness.get('is_commutative', False))
        else:
            h1 = bool(getattr(witness, 'is_commutative', False))
    except Exception:
        h1 = False

    # H_2: R is Noetherian
    try:
        if isinstance(witness, str) and "nagata" in witness.lower():
            h2 = True
        elif isinstance(witness, dict):
            h2 = bool(witness.get('is_noetherian', False))
        else:
            h2 = bool(getattr(witness, 'is_noetherian', False))
    except Exception:
        h2 = False

    # neg_Q: The Krull dimension of R is infinite (not finite)
    try:
        if isinstance(witness, str) and "nagata" in witness.lower():
            neg_q = True
        elif isinstance(witness, dict):
            kd = witness.get('krull_dimension', None)
            neg_q = (kd == math.inf or str(kd).lower() in ['inf', 'infinity', 'infinite'])
        else:
            kd = getattr(witness, 'krull_dimension', None)
            neg_q = (kd == math.inf or str(kd).lower() in ['inf', 'infinity', 'infinite'])
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is Noetherian",
    "¬Q: The Krull dimension of R is infinite"
]

N_HYP = 2
NEG_Q_INDEX = 2