import sympy
from sympy import ZZ, QQ
from sympy.polys.domains import Domain
from sympy.matrices.normalforms import smith_normal_form

# Top-level setup for potential witness expressions
Z = ZZ
Q = QQ

N_HYP = 1
NEG_Q_INDEX = 1

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: M is not a torsion-free R-module"
]

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If R is an integral domain, then M is a torsion-free R-module."
    
    The witness is expected to be a tuple (R, M), where:
      - R is a SymPy domain (e.g., ZZ, QQ)
      - M is either a list of elements d_i in R (representing the module ⊕ R/(d_i)),
        or a SymPy Matrix (representing a presentation matrix over R).
    """
    try:
        R, M = witness
    except Exception:
        return [False, False]
    
    # H_1: R is an integral domain
    h1 = False
    try:
        # In SymPy, Domain objects (like ZZ, QQ, PolyRing) are integral domains.
        if isinstance(R, Domain):
            h1 = True
    except Exception:
        h1 = False
        
    # ¬Q: M is NOT a torsion-free R-module (i.e., M has torsion)
    neg_q = False
    try:
        if isinstance(M, sympy.Matrix):
            # For a presentation matrix over ZZ, we check the Smith Normal Form.
            if R == ZZ:
                snf = smith_normal_form(M)
                for i in range(min(snf.rows, snf.cols)):
                    val = abs(snf[i, i])
                    # Invariant factors > 1 indicate torsion (Z/dZ where d > 1)
                    if val > 1:
                        neg_q = True
                        break
        else:
            # For a list of elements d_i, the module is ⊕ R/(d_i).
            # It has torsion if any d_i is neither 0 nor a unit.
            if not isinstance(M, (list, tuple)):
                M = [M]
            for d in M:
                try:
                    d_R = R.from_sympy(sympy.sympify(d))
                except Exception:
                    d_R = R(d)
                    
                if d_R != R.zero:
                    is_u = False
                    if R.is_Field:
                        is_u = True
                    elif R == ZZ:
                        is_u = (abs(d_R) == 1)
                    else:
                        try:
                            # Try exact division to check if it's a unit
                            inv = R.exquo(R.one, d_R)
                            is_u = True
                        except Exception:
                            is_u = False
                            
                    if not is_u:
                        neg_q = True
                        break
    except Exception:
        neg_q = False
        
    return [h1, neg_q]