import sympy
from sympy import S as sympy_S
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # Witness can be a tuple (R_name, S_list) or just S_list (assuming R = ZZ)
        if isinstance(witness, tuple) and len(witness) == 2:
            R_name, S_list = witness
        else:
            R_name = "ZZ"
            S_list = witness
            
        # H1: R is a unique factorization domain
        if str(R_name) in ("ZZ", "Z", "Integers", "QQ", "Q", "Rationals", "ZZ[x]", "Z[x]"):
            h1 = True
        else:
            h1 = False
            
        if not isinstance(S_list, (list, set, tuple)):
            return [False, False, False]
            
        if len(S_list) > 100:
            return [False, False, False]
            
        S_set = set(S_list)
        if not S_set:
            return [h1, False, False]
            
        # Check if elements are valid for multiplication
        for x in S_set:
            try:
                _ = x * x
            except Exception:
                return [False, False, False]
                
        # H2: S is a multiplicatively closed subset of R
        h2 = True
        for a in S_set:
            for b in S_set:
                if (a * b) not in S_set:
                    h2 = False
                    break
            if not h2:
                break
                
        # ¬Q: The localization S^{-1}R is NOT a unique factorization domain
        # S^{-1}R is the zero ring iff 0 in S. The zero ring is not an integral domain, hence not a UFD.
        # If 0 not in S, S^{-1}R is a localization of a UFD at a multiplicative set not containing 0, which is always a UFD.
        neg_q = False
        for x in S_set:
            if x == 0:
                neg_q = True
                break
                
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: The localization S^{-1}R is not a unique factorization domain"
]

N_HYP = 2
NEG_Q_INDEX = 2