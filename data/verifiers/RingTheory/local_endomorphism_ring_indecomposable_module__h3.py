import sympy
from sympy import ZZ, QQ

# Top-level setup: named object bindings
Z = sympy.S.Integers
Q = sympy.S.Rationals

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # Handle string witnesses for common counterexamples
        if isinstance(witness, str):
            w = witness.lower()
            if w in ("z", "zz", "integers", "sympy.s.integers", "sympy.zz"):
                return [True, True, True]
            elif w in ("q", "qq", "rationals", "sympy.s.rationals", "sympy.qq"):
                return [True, True, False]

        # Unpack if witness is a tuple (R, M)
        if isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
        else:
            R = witness
            M = witness
            
        # H_1: R is a ring
        if hasattr(R, 'is_ring') and R.is_ring:
            h1 = True
        elif R in (sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes, ZZ, QQ):
            h1 = True
            
        # H_2: M is an indecomposable R-module
        # We evaluate this for M = R or specific known modules
        if M == R:
            # A ring as a module over itself is indecomposable iff it has no non-trivial idempotents.
            # ZZ, QQ, fields, and polynomial rings over integral domains have no non-trivial idempotents.
            if M in (sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes, ZZ, QQ):
                h2 = True
        elif R in (sympy.S.Integers, ZZ) and M in (sympy.S.Rationals, QQ):
            h2 = True
            
        # ¬Q: The endomorphism ring End_R(M) is not a local ring
        # If M = R, End_R(R) is isomorphic to R. We check if R is not a local ring.
        if M == R:
            # Fields are local rings (unique maximal ideal is (0)).
            if M in (sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes, QQ):
                neg_q = False
            # ZZ is not local (maximal ideals are (p) for prime p).
            elif M in (sympy.S.Integers, ZZ):
                neg_q = True
        elif R in (sympy.S.Integers, ZZ) and M in (sympy.S.Rationals, QQ):
            # End_Z(Q) is isomorphic to Q, which is a field, hence local.
            neg_q = False
            
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: M is an indecomposable R-module",
    "¬Q: The endomorphism ring End_R(M) is not a local ring"
]

N_HYP = 2
NEG_Q_INDEX = 2