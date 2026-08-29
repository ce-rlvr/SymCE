import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
x, y, z = sympy.abc.x, sympy.abc.y, sympy.abc.z

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a counterexample to the false conjecture.
    The conjecture claims that for any extension E/F, there exists a finite normal 
    extension K/F containing E such that no proper subfield of K containing E is normal over F.
    This is true for finite extensions (where K is the normal closure), but fails for infinite extensions.
    Thus, the conclusion fails (neg_Q is True) iff the witness represents an infinite extension.
    """
    try:
        def is_finite(w):
            if isinstance(w, (int, float)):
                return True
            if isinstance(w, sympy.Basic):
                if getattr(w, 'is_algebraic', None):
                    return True
                if getattr(w, 'is_transcendental', None):
                    return False
                if getattr(w, 'free_symbols', None):
                    return False
                if getattr(w, 'is_number', None):
                    if getattr(w, 'is_algebraic', None) is False:
                        return False
                    return True
            if isinstance(w, sympy.Poly):
                return True
            if isinstance(w, (list, tuple, set)):
                if len(w) == 0:
                    return True
                return all(is_finite(elem) for elem in w)
            return False
        
        # The conclusion fails if the extension is not finite.
        neg_q = not is_finite(witness)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: There does not exist a finite normal extension K/F containing E such that no proper subfield of K containing E is normal over F"
]

N_HYP = 0
NEG_Q_INDEX = 0