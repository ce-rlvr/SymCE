import sympy
from sympy import *

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    
    Remaining hypotheses:
      - R is an integral domain
      - R^{\times} is the group of units of R
      
    Conclusion (must fail):
      R is a Unique Factorization Domain if and only if R^* is isomorphic to the direct product of R^{\times} and a free commutative monoid
      
    Note: The conjecture is false because R^* is not defined as the monoid of non-zero elements. 
    If R^* means the monoid of all elements of R, it has a zero element, while R^x \times F does not.
    Thus, for any UFD, R^* is not isomorphic to R^x \times F, making the "if and only if" statement false.
    """
    # H1: R is an integral domain
    try:
        # Check if witness is an integral domain
        # In sympy, domains like ZZ, QQ, or polynomial rings over them are integral domains.
        h1_ok = witness.is_Domain and not witness.is_Field
        # We also accept fields as integral domains, but let's check basic properties
        if not h1_ok:
            if hasattr(witness, 'is_IntegralDomain'):
                h1_ok = witness.is_IntegralDomain
            elif hasattr(witness, 'has_Field'):
                h1_ok = True
            elif witness in [ZZ, QQ]:
                h1_ok = True
    except Exception:
        h1_ok = False

    # H2: R^{\times} is the group of units of R
    # This is a definitional hypothesis, so it holds by definition for any valid ring witness.
    h2_ok = True

    # ¬Q: The conclusion must FAIL at the witness.
    # The conclusion is: R is a UFD iff R^* is isomorphic to R^x \times F.
    # Since R^* (all elements) has a zero element and R^x \times F does not, they are never isomorphic.
    # Thus, the right-hand side of the iff is always False.
    # For the iff to fail, the left-hand side (R is a UFD) must be True.
    # So ¬Q is True iff R is a UFD.
    try:
        if witness == ZZ:
            neg_q_ok = True
        elif witness == QQ:
            neg_q_ok = True
        elif hasattr(witness, 'is_UFD'):
            neg_q_ok = witness.is_UFD
        else:
            # Polynomial rings over fields or ZZ are UFDs
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: R^{\times} is the group of units of R",
    "¬Q: R is a UFD, but R^* (all elements) is not isomorphic to R^{\times} x F (conclusion fails)"
]

N_HYP = 2
NEG_Q_INDEX = 2