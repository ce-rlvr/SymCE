import sympy
from sympy import ZZ, QQ
from sympy.polys.rings import ring

# Top-level setup: named object bindings that the witness expression may reference.
# We provide some standard polynomial rings over QQ.
R_x, x = ring('x', QQ)
R_xy, X, Y = ring('x, y', QQ)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Let I be a two-sided ideal of R. Then R/I is an Artinian ring."
    
    The witness should be a tuple (R, I) where R is a supported ring 
    (e.g., sympy.ZZ, sympy.QQ, or a SymPy PolyRing) and I is a list/tuple/set of generators.
    """
    try:
        R, I = witness
    except Exception:
        return [False, False]

    # H_1: I is a two-sided ideal of R
    try:
        h1 = False
        if isinstance(I, (list, tuple, set)):
            if R == ZZ:
                h1 = all(isinstance(a, (int, sympy.Integer)) for a in I)
            elif R == QQ:
                h1 = all(isinstance(a, (int, sympy.Integer, sympy.Rational, float)) for a in I)
            elif hasattr(R, 'domain') and hasattr(R, 'gens'):
                try:
                    # Check if all generators can be cast to elements of the ring R
                    for a in I:
                        _ = R(a)
                    h1 = True
                except Exception:
                    h1 = False
    except Exception:
        h1 = False

    # neg_Q: R/I is NOT an Artinian ring
    try:
        neg_q = False
        if h1:
            if R == ZZ:
                # ZZ/I is Artinian iff I is not the zero ideal
                is_art = any(a != 0 for a in I)
                neg_q = not is_art
            elif R == QQ:
                # QQ/I is always Artinian (it is either QQ or the zero ring)
                neg_q = False
            elif hasattr(R, 'ideal'):
                # For polynomial rings over a field, R/I is Artinian iff the ideal is zero-dimensional
                if not I or all(R(a) == R.zero for a in I):
                    neg_q = True
                else:
                    idl = R.ideal(*I)
                    neg_q = not idl.is_zero_dimensional
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: I is a two-sided ideal of R",
    "¬Q: R/I is not an Artinian ring"
]

N_HYP = 1
NEG_Q_INDEX = 1