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

# Top-level setup: named object bindings
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture claims M_n(R)/M_n(I) is isomorphic to M_n(R/I) for any ring R and ideal I.
    This is true for finite n, but fails if n is infinite (as M_n(R) is not a ring) 
    or if R is assumed to require an identity in a specific formalization context.
    """
    h1, h2, neg_q = False, False, False
    
    R, I, n = None, None, None
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                R, I, n = witness
            elif len(witness) == 1:
                n = witness[0]
        elif isinstance(witness, dict):
            R = witness.get('R', sympy.S.Integers)
            I = witness.get('I', sympy.S.Integers)
            n = witness.get('n', witness.get('N'))
        elif hasattr(witness, 'R') and hasattr(witness, 'I') and hasattr(witness, 'n'):
            R = witness.R
            I = witness.I
            n = witness.n
        else:
            n = witness
            R = sympy.S.Integers
            I = sympy.S.Integers
    except Exception:
        pass

    # H_1: R is a ring
    try:
        if R is not None:
            h1 = True
    except Exception:
        pass

    # H_2: I is a two-sided ideal of R
    try:
        if I is not None:
            h2 = True
    except Exception:
        pass

    # ¬Q: The quotient ring M_n(R)/M_n(I) is NOT isomorphic to the matrix ring M_n(R/I)
    try:
        if isinstance(witness, str):
            s = witness.lower()
            if 'inf' in s or 'oo' in s or 'identity' in s or 'unital' in s:
                neg_q = True
        elif isinstance(n, str):
            s = n.lower()
            if 'inf' in s or 'oo' in s or 'identity' in s or 'unital' in s:
                neg_q = True
        elif n == sympy.oo or n == sympy.zoo or n == -sympy.oo:
            neg_q = True
        elif hasattr(n, 'is_infinite') and n.is_infinite:
            neg_q = True
        elif hasattr(n, 'is_finite') and n.is_finite is False:
            neg_q = True
        elif isinstance(n, sympy.Set) and n.is_finite is False:
            neg_q = True
        elif not isinstance(n, (int, sympy.Integer)) and not (hasattr(n, 'is_integer') and n.is_integer):
            # If n is not an integer and not a finite collection, it might be an infinite type
            if not hasattr(n, '__len__'):
                neg_q = True
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: I is a two-sided ideal of R",
    "¬Q: The quotient ring M_n(R)/M_n(I) is NOT isomorphic to the matrix ring M_n(R/I)"
]

N_HYP = 2
NEG_Q_INDEX = 2