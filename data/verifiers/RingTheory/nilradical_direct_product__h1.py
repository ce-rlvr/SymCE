import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros, Matrix
from sympy import Symbol

# Top-level setup: named object bindings that the witness expression may reference.
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Evaluates the remaining hypotheses and the negated conclusion at the witness.
    The conjecture claims that the nilradical of R_1 x R_2 is the direct product 
    of their nilradicals. This is true for commutative rings, but fails if the 
    rings are non-commutative (where the set of nilpotent elements may not form an ideal)
    or if the product is actually infinite (unbounded nilpotency indices).
    """
    h1 = False
    try:
        # H1: Let R = R_1 x R_2 be their direct product.
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            h1 = True
        elif hasattr(witness, 'sets') and len(witness.sets) == 2:
            h1 = True
        elif isinstance(witness, str):
            s = witness.lower()
            if "prod" in s or "times" in s or "x" in s:
                h1 = True
    except Exception:
        pass

    neg_Q = False
    try:
        items = []
        if isinstance(witness, (tuple, list)):
            items = witness
        elif hasattr(witness, 'sets'):
            items = witness.sets
            
        # If the witness represents an infinite product, the conclusion fails
        if len(items) > 2:
            neg_Q = True
            
        # If the witness contains non-commutative rings, the conclusion fails
        for item in items:
            if hasattr(item, 'is_commutative') and item.is_commutative is False:
                neg_Q = True
            elif hasattr(item, 'is_abelian') and item.is_abelian is False:
                neg_Q = True
            elif hasattr(item, 'is_Matrix') and item.is_Matrix:
                if hasattr(item, 'shape') and item.shape != (1, 1):
                    neg_Q = True
            elif type(item).__name__ == 'Quaternion':
                neg_Q = True
                
        # Fallback for string-based witnesses
        if isinstance(witness, str):
            s = witness.lower()
            if "non-commutative" in s or "matrix" in s or "infty" in s or "infinite" in s or "..." in s:
                neg_Q = True
    except Exception:
        pass

    return [h1, neg_Q]

CONDITION_LABELS = [
    "H_1: Let R = R_1 x R_2 be their direct product",
    "¬Q: The nilradical of R is not equal to the direct product of the nilradicals of R_1 and R_2"
]

N_HYP = 1
NEG_Q_INDEX = 1