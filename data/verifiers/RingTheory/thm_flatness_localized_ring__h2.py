import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import Rational, Integer

# Top-level setup: named object bindings
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

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: The localized ring S^{-1}R is not a flat R-module"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The dropped hypothesis is that S is a multiplicatively closed subset.
    If S is not multiplicatively closed, the standard construction of S^{-1}R fails to 
    produce a valid module, hence it is not a flat R-module.
    """
    try:
        # Witness can be a tuple (R, S) or just S (with R defaulting to integers)
        if isinstance(witness, tuple) and len(witness) == 2:
            R, S = witness
        else:
            R = sympy.ZZ
            S = witness
    except Exception:
        return [False, False]
        
    # H_1: R is a commutative ring
    try:
        if hasattr(R, 'is_commutative'):
            h1_ok = bool(R.is_commutative)
        else:
            # Fallback if the ring object doesn't explicitly declare commutativity
            h1_ok = True
    except Exception:
        h1_ok = False
        
    # ¬Q: The localized ring S^{-1}R is not a flat R-module
    # This is true if S is not multiplicatively closed, making S^{-1}R ill-defined.
    try:
        S_list = list(S)
        is_closed = True
        for a in S_list:
            for b in S_list:
                prod = a * b
                found = False
                for s in S_list:
                    if prod == s:
                        found = True
                        break
                if not found:
                    is_closed = False
                    break
            if not is_closed:
                break
        neg_q_ok = not is_closed
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]