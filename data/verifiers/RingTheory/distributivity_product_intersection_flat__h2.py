import sympy
from sympy.polys.rings import ring
from sympy.polys.domains import QQ, ZZ

# Top-level setup: a polynomial ring over the rationals which is not a PID,
# allowing for non-flat (non-projective) ideals.
R_poly, x, y = ring("x, y", QQ)

def conditions(witness):
    """
    Checks the remaining hypotheses and the negated conclusion.
    The witness can be a tuple (R, I, J, K) or just (I, J, K) where R is inferred.
    """
    try:
        if len(witness) == 4:
            R, I, J, K = witness
        elif len(witness) == 3:
            I, J, K = witness
            R = I.ring
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: R is a commutative ring
    try:
        h1 = hasattr(R, 'ideal') and getattr(R, 'is_commutative', True)
    except Exception:
        h1 = False

    # H_2: J is an ideal of R
    try:
        h2 = hasattr(J, 'ring') and J.ring == R
    except Exception:
        h2 = False

    # H_3: K is an ideal of R
    try:
        h3 = hasattr(K, 'ring') and K.ring == R
    except Exception:
        h3 = False

    # ¬Q: I(J \cap K) != IJ \cap IK
    try:
        # Compute J \cap K
        if hasattr(J, 'intersect'):
            J_cap_K = J.intersect(K)
        elif hasattr(J, 'intersection'):
            J_cap_K = J.intersection(K)
        else:
            J_cap_K = J & K
            
        # Compute LHS: I(J \cap K)
        LHS = I * J_cap_K
        
        # Compute IJ and IK
        IJ = I * J
        IK = I * K
        
        # Compute RHS: IJ \cap IK
        if hasattr(IJ, 'intersect'):
            RHS = IJ.intersect(IK)
        elif hasattr(IJ, 'intersection'):
            RHS = IJ.intersection(IK)
        else:
            RHS = IJ & IK
            
        neg_q = (LHS != RHS)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: J is an ideal of R",
    "H_3: K is an ideal of R",
    "¬Q: I(J \\cap K) != IJ \\cap IK"
]

N_HYP = 3
NEG_Q_INDEX = 3