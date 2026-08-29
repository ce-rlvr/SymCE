import sympy
from sympy.ntheory import factorint
import math
import itertools
import functools

class Ring:
    """A simple representation of a commutative ring Z/nZ."""
    def __init__(self, characteristic):
        self.characteristic = characteristic

class AlgebraicClosure:
    """Represents the algebraic closure of a ring."""
    def __init__(self, base_ring):
        self.base_ring = base_ring
        char = getattr(base_ring, 'characteristic', 0)
        if char > 0:
            factors = factorint(char)
            rad = 1
            for p in factors:
                rad *= p
            self.characteristic = rad
        else:
            self.characteristic = 0

    def is_algebraic_closure_of(self, other):
        if hasattr(self.base_ring, 'characteristic') and hasattr(other, 'characteristic'):
            return self.base_ring.characteristic == other.characteristic
        return False

# Standard algebra objects that might be used as witnesses
Z2 = Ring(2)
Z3 = Ring(3)
Z4 = Ring(4)
Z6 = Ring(6)

def conditions(witness) -> list[bool]:
    try:
        # Expecting witness to be a tuple (F, F_bar)
        if isinstance(witness, tuple) and len(witness) == 2:
            F, F_bar = witness
        else:
            # If witness is just F, we can try to deduce F_bar
            F = witness
            if isinstance(F, (int, sympy.Integer)):
                F = Ring(int(F))
            if hasattr(F, 'characteristic'):
                F_bar = AlgebraicClosure(F)
            else:
                return [False, False]

        # Get characteristics
        if isinstance(F, (int, sympy.Integer)):
            char_F = int(F)
        else:
            char_F = getattr(F, 'characteristic', None)
            if char_F is not None:
                char_F = int(char_F)
            
        if isinstance(F_bar, (int, sympy.Integer)):
            char_F_bar = int(F_bar)
        else:
            char_F_bar = getattr(F_bar, 'characteristic', None)
            if char_F_bar is not None:
                char_F_bar = int(char_F_bar)

        if char_F is None or char_F_bar is None:
            return [False, False]

        # Check H1: F_bar is an algebraic closure of F
        h1 = False
        if hasattr(F_bar, 'is_algebraic_closure_of'):
            try:
                h1 = F_bar.is_algebraic_closure_of(F)
            except Exception:
                pass
        if not h1 and hasattr(F, 'algebraic_closure'):
            try:
                h1 = (F.algebraic_closure() == F_bar)
            except Exception:
                pass
                
        # Fallback for H1 based on radical of the characteristic
        if not h1:
            try:
                if char_F > 0:
                    factors = factorint(char_F)
                    rad = 1
                    for p in factors:
                        rad *= p
                    if char_F_bar == rad:
                        h1 = True
                elif char_F == 0 and char_F_bar == 0:
                    h1 = True
            except Exception:
                pass

        # Check neg_Q: characteristics are different
        neg_q = (char_F != char_F_bar)

        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: \\overline{F} is an algebraic closure of F",
    "¬Q: The characteristic of \\overline{F} is not equal to the characteristic of F"
]

N_HYP = 1
NEG_Q_INDEX = 1