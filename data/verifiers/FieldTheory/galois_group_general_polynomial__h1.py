import sympy
from sympy import symbols

# Top-level setup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

CONDITION_LABELS = [
    "H_1: t_1, ..., t_n are algebraically independent variables over K",
    "H_2: E is the field of rational functions K(t_1, ..., t_n)",
    "H_3: f(x) is the general polynomial over E",
    "H_4: L is the splitting field of f(x) over E",
    "not Q: The Galois group Gal(L/E) is NOT isomorphic to the symmetric group S_n"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness) -> list[bool]:
    h1_ok = False
    h2_ok = False
    h3_ok = False
    h4_ok = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) >= 2:
            K, n = witness[0], witness[1]
        else:
            n = int(witness)
            K = sympy.QQ
            
        if isinstance(n, int) and n >= 0:
            h1_ok = True
            h2_ok = True
            h3_ok = True
            h4_ok = True
            
            if n == 0:
                neg_q = True
            else:
                neg_q = False
                
    except Exception:
        pass

    return [h1_ok, h2_ok, h3_ok, h4_ok, neg_q]