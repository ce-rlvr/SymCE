import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.abc import x, y, z
from sympy.polys.domains import PolynomialRing

CONDITION_LABELS = [
    "H_1: A is a k-algebra",
    "H_2: A is finite-dimensional as a vector space over k",
    "¬Q: A is not an Artinian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture:
    'Let A be a k-algebra. If A is finite-dimensional as a vector space over k, then A is an Artinian ring.'
    
    The conjecture is false because it drops the hypothesis that k is a field.
    If k is not a field (e.g., k = ZZ), then A can be a finitely generated free module 
    (loosely called 'finite-dimensional vector space' in the false conjecture) over k 
    without being Artinian.
    """
    try:
        # The witness can be a tuple (A, k) or just A (in which case we assume k = A)
        if isinstance(witness, tuple) and len(witness) == 2:
            A, k = witness
        else:
            A = witness
            k = witness

        # H_1: A is a k-algebra
        h1 = False
        if hasattr(A, 'is_Ring') and A.is_Ring and hasattr(k, 'is_Ring') and k.is_Ring:
            if A == k:
                h1 = True
            elif hasattr(A, 'domain') and A.domain == k:
                h1 = True
            elif hasattr(A, 'ext') and A.ext is not None:
                h1 = True

        # H_2: A is finite-dimensional as a vector space (or free module) over k
        h2 = False
        if h1:
            if A == k:
                h2 = True
            elif hasattr(A, 'ext') and A.ext is not None:
                h2 = True
            elif isinstance(A, PolynomialRing):
                h2 = False

        # ¬Q: A is not an Artinian ring
        neg_q = False
        if A == sympy.ZZ:
            neg_q = True
        elif isinstance(A, PolynomialRing):
            neg_q = True
        elif hasattr(A, 'is_Field') and A.is_Field:
            neg_q = False

        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]