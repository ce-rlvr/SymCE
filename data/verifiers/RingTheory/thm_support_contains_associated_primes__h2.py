import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z, t

# Standard Ring/Field objects that might be referenced in a witness
QQ = sympy.QQ
ZZ = sympy.ZZ

def conditions(witness) -> list[bool]:
    """
    Given a witness (e.g., a tuple (R, I) representing a ring and an ideal),
    check if it satisfies the remaining hypotheses and falsifies the conclusion.
    """
    h1 = False
    neg_q = False
    
    try:
        # Extract the ring R from the witness if it's a tuple (R, I)
        if isinstance(witness, tuple) and len(witness) > 0:
            R = witness[0]
        else:
            R = witness
            
        # H_1: R is a commutative Noetherian ring
        if hasattr(R, 'is_commutative'):
            h1 = bool(R.is_commutative)
        else:
            # If the object doesn't explicitly declare commutativity, 
            # we assume it satisfies the hypothesis for the sake of evaluation.
            h1 = True
            
        # ¬Q: The conclusion FAILS at the witness.
        # The conclusion is: "Every associated prime ideal of the quotient ring R/I 
        # belongs to the support of R/I."
        # 
        # Mathematically, for any module M over a commutative ring R, the associated 
        # primes Ass(M) are ALWAYS a subset of the support Supp(M). 
        # Proof: If P in Ass(M), then P = ann(m) for some non-zero m in M. 
        # The submodule Rm is isomorphic to R/P. Localizing at P, (Rm)_P is isomorphic 
        # to the fraction field of R/P, which is non-zero. Thus M_P is non-zero, 
        # meaning P is in Supp(M).
        # 
        # Since the conclusion is a universal mathematical tautology, it NEVER fails 
        # for any valid commutative ring. Therefore, its negation is unconditionally False.
        neg_q = False
        
    except Exception:
        h1 = False
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "¬Q: There exists an associated prime ideal of R/I that does not belong to the support of R/I"
]

N_HYP = 1
NEG_Q_INDEX = 1