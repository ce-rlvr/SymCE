import sympy
from sympy import QQ, ZZ, symbols
import math
import itertools
import functools

# Top-level setup for Field Theory
x, y, z = symbols('x y z')

def conditions(witness) -> list[bool]:
    """
    witness: dict, tuple, or object representing the properties of the field extensions.
    Expected properties:
      - M_K_finite: bool (True if M/K is a finite extension)
      - M_K_s: int (The separable degree of M/K)
      - M_L_s: int (The separable degree of M/L)
      - L_K_s: int (The separable degree of L/K)
    """
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('M_K_finite', False))
            mk_s = int(witness['M_K_s'])
            ml_s = int(witness['M_L_s'])
            lk_s = int(witness['L_K_s'])
        elif isinstance(witness, (list, tuple)) and len(witness) >= 4:
            h1 = bool(witness[0])
            mk_s = int(witness[1])
            ml_s = int(witness[2])
            lk_s = int(witness[3])
        elif hasattr(witness, 'M_K_finite'):
            h1 = bool(getattr(witness, 'M_K_finite'))
            mk_s = int(getattr(witness, 'M_K_s'))
            ml_s = int(getattr(witness, 'M_L_s'))
            lk_s = int(getattr(witness, 'L_K_s'))
        else:
            return [False, False]
            
        neg_q = (mk_s != ml_s * lk_s)
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: The field extension M/K is finite",
    "¬Q: separable degree of M/K is not the product of M/L and L/K"
]

N_HYP = 1
NEG_Q_INDEX = 1