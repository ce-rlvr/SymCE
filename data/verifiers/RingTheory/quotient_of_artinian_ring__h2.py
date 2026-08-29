import sympy
from sympy import *
from sympy.abc import *
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference.
# Since SymPy does not have built-in support for abstract rings and ideals with Artinian properties,
# we provide simple classes that the witness can instantiate.
class Ring:
    def __init__(self, is_left_artinian=True, is_right_artinian=True):
        self.is_left_artinian = is_left_artinian
        self.is_right_artinian = is_right_artinian

class Ideal:
    def __init__(self, is_left_ideal=True, is_right_ideal=True):
        self.is_left_ideal = is_left_ideal
        self.is_right_ideal = is_right_ideal
        
    @property
    def is_two_sided(self):
        return self.is_left_ideal and self.is_right_ideal

def conditions(witness) -> list[bool]:
    h1 = False
    q = True
    
    try:
        # Allow witness to be a dictionary of properties
        if isinstance(witness, dict):
            h1 = bool(witness.get("R_is_left_artinian", False))
            q = bool(witness.get("R_mod_I_is_left_artinian_ring", True))
            return [h1, not q]
            
        R, I = None, None
        # Allow witness to be a tuple (R, I)
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
        # Allow witness to be an object with R and I attributes
        elif hasattr(witness, 'R') and hasattr(witness, 'I'):
            R = witness.R
            I = witness.I
            
        if R is not None and I is not None:
            # Check if R is a left Artinian ring
            if hasattr(R, 'is_left_artinian'):
                h1 = bool(R.is_left_artinian)
            
            # Check if I is a two-sided ideal
            is_two_sided = False
            if hasattr(I, 'is_two_sided'):
                is_two_sided = bool(I.is_two_sided)
            elif hasattr(I, 'is_left_ideal') and hasattr(I, 'is_right_ideal'):
                is_two_sided = bool(I.is_left_ideal and I.is_right_ideal)
                
            # The conclusion is that R/I is a left Artinian ring.
            # If I is not two-sided, R/I is not a ring, so the conclusion fails.
            if not is_two_sided:
                q = False
            else:
                # If I is two-sided, R/I is a ring. A quotient of a left Artinian ring is left Artinian.
                q = h1
    except Exception:
        pass

    return [h1, not q]

CONDITION_LABELS = [
    "H_1: R is a left Artinian ring",
    "¬Q: The quotient ring R/I is not a left Artinian ring"
]

N_HYP = 1
NEG_Q_INDEX = 1