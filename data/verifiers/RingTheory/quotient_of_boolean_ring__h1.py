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

from sympy import Integer
from sympy.polys.domains import ZZ, QQ
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "¬Q: The quotient ring R/I is not a Boolean ring"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        n = None
        # If witness is an integer n, it represents the ideal nZ in the ring Z.
        if isinstance(witness, (int, Integer)):
            n = int(witness)
        # If witness is a tuple (R, I), check if R is the ring of integers.
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
            if hasattr(R, 'is_IntegerRing') or str(R) == 'ZZ' or R == ZZ:
                n = int(I)
        
        if n is not None:
            h1 = True  # nZ is always an ideal of Z
            if n == 0:
                # Z/0Z is isomorphic to Z, which is not a Boolean ring (e.g., 2^2 != 2)
                neg_q = True
            else:
                n_abs = abs(n)
                is_boolean = True
                # In a Boolean ring, x^2 = x for all x.
                for i in range(n_abs):
                    if (i**2) % n_abs != i:
                        is_boolean = False
                        break
                neg_q = not is_boolean
            return [h1, neg_q]
            
        # Fallback for sympy Ideals in polynomial rings
        if hasattr(witness, 'ring') and hasattr(witness, 'contains'):
            R = witness.ring
            h1 = True  # It is an ideal object
            
            is_boolean = True
            test_elements = []
            if hasattr(R, 'gens'):
                test_elements.extend(R.gens)
            
            # For R/I to be a Boolean ring, y^2 - y must be in I for all y in R.
            for elem in test_elements:
                try:
                    if (elem**2 - elem) not in witness:
                        is_boolean = False
                        break
                except Exception:
                    pass
            
            # Also test the integer 2 mapped into the ring
            try:
                if (R(2)**2 - R(2)) not in witness:
                    is_boolean = False
            except Exception:
                pass
                
            neg_q = not is_boolean
            return [h1, neg_q]
            
    except Exception:
        pass

    return [h1, neg_q]