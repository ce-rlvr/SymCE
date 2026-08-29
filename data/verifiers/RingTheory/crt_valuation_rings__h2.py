import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Given a witness (R, I, J), checks if it is a valid counterexample to the false conjecture:
    "Let R be a valuation ring. Let I and J be comaximal. Either I = R or J = R."
    (The dropped hypothesis is that I and J are ideals; elements can be comaximal but are not the ring itself).
    """
    try:
        R, I, J = witness
    except Exception:
        return [False, False, False]
        
    # H_1: R is a valuation ring
    # We accept fields (which are trivially valuation rings) or custom objects explicitly marked.
    h1 = False
    try:
        if getattr(R, 'is_Field', False):
            h1 = True
        elif hasattr(R, 'is_valuation_ring'):
            h1 = bool(R.is_valuation_ring)
    except Exception:
        pass
        
    # H_2: I and J are comaximal
    h2 = False
    try:
        if hasattr(R, 'are_comaximal'):
            h2 = bool(R.are_comaximal(I, J))
        elif getattr(R, 'is_Field', False):
            # In a field, any non-zero element (or collection containing a non-zero element) generates R.
            # Thus, two elements/ideals are comaximal as long as at least one is non-zero.
            def is_zero(obj):
                try:
                    if isinstance(obj, (list, set, tuple)):
                        return all(e == getattr(R, 'zero', 0) or e == 0 for e in obj)
                    return obj == getattr(R, 'zero', 0) or obj == 0
                except Exception:
                    return False
            
            if not is_zero(I) or not is_zero(J):
                h2 = True
        elif hasattr(R, 'gcd'):
            # Fallback for domains like ZZ (though ZZ is not a valuation ring)
            if R.gcd(I, J) == getattr(R, 'one', 1):
                h2 = True
    except Exception:
        pass
        
    # ¬Q: I != R and J != R
    # The conclusion is "I = R or J = R". We want this to FAIL.
    neg_q = False
    try:
        if I != R and J != R:
            neg_q = True
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a valuation ring",
    "H_2: I and J are comaximal",
    "¬Q: I != R and J != R"
]

N_HYP = 2
NEG_Q_INDEX = 2