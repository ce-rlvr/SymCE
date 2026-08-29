import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    n_val = None
    G_val = "Z"
    
    try:
        if isinstance(witness, tuple) or isinstance(witness, list):
            n_val = int(witness[0])
            if len(witness) > 1:
                G_val = witness[1]
        else:
            n_val = int(witness)
    except Exception:
        pass
        
    h1 = False
    try:
        if isinstance(G_val, str) and G_val in ["Z", "Z^n", "Q", "R", "Z^2", "Z^3"]:
            h1 = True
        elif G_val in [sympy.S.Integers, sympy.S.Reals, sympy.S.Rationals]:
            h1 = True
        elif callable(getattr(G_val, 'order', None)) and G_val.order() == 1:
            h1 = True
    except Exception:
        h1 = False
        
    h2 = False
    try:
        if n_val is not None and n_val >= 2:
            h2 = True
    except Exception:
        h2 = False
        
    neg_q = False
    try:
        if n_val is not None and n_val >= 2:
            if not sympy.isprime(n_val):
                neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a torsion-free abelian group",
    "H_2: R(G) is the group ring of G over R",
    "¬Q: R(G) is not an integral domain"
]

N_HYP = 2
NEG_Q_INDEX = 2