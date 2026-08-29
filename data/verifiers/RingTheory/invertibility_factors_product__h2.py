import sympy
from sympy import ZZ, QQ, Rational, Integer
from sympy.abc import x, y, z

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary with keys 'R', 'I', and 'J', where:
      - 'R' is a SymPy domain (e.g., ZZ) representing the commutative ring.
      - 'I' is a list of generators for I (as elements of the fraction field).
      - 'J' is a list of generators for J.
    """
    try:
        R = witness['R']
        I = witness['I']
        J = witness['J']
    except Exception:
        return [False, False, False, False]
    
    # H_1: R is a commutative ring
    try:
        # We assume R is a commutative ring if it's a SymPy domain with the is_PID attribute.
        h1 = hasattr(R, 'is_PID')
    except Exception:
        h1 = False

    # H_2: J is an ideal of R
    try:
        # J is an ideal if all its generators are in R.
        h2 = all(j in R for j in J)
    except Exception:
        h2 = False

    # H_3: The product ideal IJ is an invertible ideal
    try:
        # The generators of the product module IJ
        IJ_gens = [i * j for i in I for j in J]
        # IJ is an ideal of R if all its generators are in R
        ij_is_ideal = all(val in R for val in IJ_gens)
        
        # For simplicity, we restrict invertibility checks to Principal Ideal Domains (PIDs).
        # In a PID, an ideal is invertible if and only if it is non-zero.
        if getattr(R, 'is_PID', False):
            h3 = ij_is_ideal and any(val != 0 for val in IJ_gens)
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: Conclusion fails (It is not the case that both I and J are invertible ideals)
    try:
        i_is_ideal = all(val in R for val in I)
        j_is_ideal = all(val in R for val in J)
        
        if getattr(R, 'is_PID', False):
            i_is_invertible = i_is_ideal and any(val != 0 for val in I)
            j_is_invertible = j_is_ideal and any(val != 0 for val in J)
        else:
            i_is_invertible = False
            j_is_invertible = False
            
        q = i_is_invertible and j_is_invertible
        neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: J is an ideal of R",
    "H_3: The product ideal IJ is an invertible ideal",
    "¬Q: It is not the case that both I and J are invertible ideals"
]

N_HYP = 3
NEG_Q_INDEX = 3