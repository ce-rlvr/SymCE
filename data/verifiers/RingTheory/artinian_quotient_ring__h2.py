import sympy
from sympy import QQ, ZZ
from sympy.abc import x, y, z

# Top-level setup
# No specific named objects required for this domain other than standard SymPy domains.

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Let R be an Artinian ring. The quotient ring R/I is an Artinian ring."
    
    The dropped hypothesis is that I must be an ideal of R.
    A valid witness is a tuple (R, I) where R is an Artinian ring and I is a subset/subring 
    that is NOT an ideal, meaning R/I is not a valid quotient ring (and thus not an Artinian ring).
    """
    try:
        if len(witness) != 2:
            return [False, False]
        R, I = witness
    except Exception:
        return [False, False]
    
    # H_1: R is an Artinian ring
    h1 = False
    try:
        if R in [sympy.QQ, sympy.RR, sympy.CC, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes]:
            h1 = True
        elif hasattr(R, 'is_Field') and R.is_Field:
            h1 = True
        elif hasattr(R, 'is_FiniteField') and R.is_FiniteField:
            h1 = True
        elif hasattr(R, 'is_QuotientRing') and R.is_QuotientRing:
            if hasattr(R.base, 'is_PolynomialRing') and R.base.is_PolynomialRing:
                if R.base.domain.is_Field and not R.ideal.is_zero():
                    h1 = True
        elif hasattr(R, 'elements') and isinstance(getattr(R, 'elements'), (list, set, tuple)):
            h1 = True
    except Exception:
        h1 = False

    # ¬Q: The quotient ring R/I is NOT an Artinian ring
    # This is true if I is not an ideal of R, making R/I not a ring.
    neg_q = False
    try:
        is_ideal = False
        if I == R:
            is_ideal = True
        elif I in [sympy.ZZ, sympy.S.Integers]:
            is_ideal = False
        elif type(I).__name__ in ['Ideal', 'PolyIdeal'] or getattr(I, 'is_Ideal', False):
            if getattr(I, 'ring', R) == R:
                is_ideal = True
            else:
                is_ideal = False
        elif hasattr(I, 'is_Ring') and I.is_Ring:
            is_ideal = False
        elif isinstance(I, (list, tuple)):
            # A list/tuple of elements is typically interpreted as a set of generators for an ideal
            is_ideal = True
        elif isinstance(I, set):
            if I == {0} or I == {getattr(R, 'zero', 0)}:
                is_ideal = True
            else:
                is_ideal = False
        elif hasattr(R, 'elements') and hasattr(I, '__iter__'):
            I_set = set(I)
            if not I_set.issubset(set(R.elements)):
                is_ideal = False
            elif hasattr(R, 'add') and hasattr(R, 'mul'):
                is_ideal = True
                # Check closure under addition
                for a in I_set:
                    for b in I_set:
                        if R.add(a, b) not in I_set:
                            is_ideal = False
                # Check closure under multiplication by elements of R
                for a in I_set:
                    for r in R.elements:
                        if R.mul(r, a) not in I_set:
                            is_ideal = False
                        if R.mul(a, r) not in I_set:
                            is_ideal = False
            else:
                is_ideal = False
        else:
            # If we cannot verify it is an ideal, it is treated as not an ideal.
            is_ideal = False
            
        neg_q = not is_ideal
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is an Artinian ring",
    "¬Q: The quotient ring R/I is not an Artinian ring"
]

N_HYP = 1
NEG_Q_INDEX = 1