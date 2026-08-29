import sympy as sp
from sympy.matrices import Matrix, eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for standard algebra objects
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
    "H_1: T is a linear transformation",
    "H_2: P is an isomorphism",
    "H_3: Q is an isomorphism",
    "¬Q: rank(Q ∘ T ∘ P) != rank(T)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        T, P, Q = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: T is a linear transformation
    try:
        h1 = hasattr(T, 'shape') and len(T.shape) == 2 and hasattr(T, 'rank') and callable(T.rank)
    except Exception:
        h1 = False
        
    # H_2: P is an isomorphism U -> V
    try:
        h2 = False
        if hasattr(P, 'shape') and len(P.shape) == 2 and P.shape[0] == P.shape[1] and P.shape[0] == T.shape[1]:
            if hasattr(P, 'det') and callable(P.det):
                h2 = bool(P.det() != 0)
            elif hasattr(P, 'inv') and callable(P.inv):
                try:
                    P.inv()
                    h2 = True
                except Exception:
                    h2 = False
    except Exception:
        h2 = False
        
    # H_3: Q is an isomorphism W -> X
    try:
        h3 = False
        if hasattr(Q, 'shape') and len(Q.shape) == 2 and Q.shape[0] == Q.shape[1] and Q.shape[1] == T.shape[0]:
            if hasattr(Q, 'det') and callable(Q.det):
                h3 = bool(Q.det() != 0)
            elif hasattr(Q, 'inv') and callable(Q.inv):
                try:
                    Q.inv()
                    h3 = True
                except Exception:
                    h3 = False
    except Exception:
        h3 = False
        
    # ¬Q: rank(Q ∘ T ∘ P) != rank(T)
    try:
        comp = Q * T * P
        neg_q = bool(comp.rank() != T.rank())
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]