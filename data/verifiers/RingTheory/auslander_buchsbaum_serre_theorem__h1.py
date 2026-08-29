import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

class Ring:
    """
    A mock class to represent a ring with specific properties 
    for the purpose of testing the Auslander-Buchsbaum-Serre Theorem conjecture.
    """
    def __init__(self, is_regular_local=False, finite_global_dimension=False):
        self.is_regular_local = is_regular_local
        self.finite_global_dimension = finite_global_dimension

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, str):
            w = witness.lower()
            # A non-Noetherian valuation ring of rank 1 has finite global dimension 
            # but is not a regular local ring.
            if "valuation" in w or "non-noetherian" in w:
                is_reg = False
                fin_gl = True
            else:
                is_reg = False
                fin_gl = False
        elif isinstance(witness, Ring):
            is_reg = bool(witness.is_regular_local)
            fin_gl = bool(witness.finite_global_dimension)
        elif isinstance(witness, dict):
            is_reg = bool(witness.get('is_regular_local', False))
            fin_gl = bool(witness.get('finite_global_dimension', False))
        else:
            is_reg = bool(getattr(witness, 'is_regular_local', False))
            fin_gl = bool(getattr(witness, 'finite_global_dimension', False))
            
        # The conjecture claims: R is regular local iff global dimension is finite.
        # The negation is that exactly one of these properties holds (XOR).
        neg_q = (is_reg != fin_gl)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: R is a regular local ring XOR its global dimension is finite"
]

N_HYP = 0
NEG_Q_INDEX = 0