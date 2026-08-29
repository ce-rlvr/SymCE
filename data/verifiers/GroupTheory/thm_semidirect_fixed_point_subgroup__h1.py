import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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
    h1_ok = False
    try:
        N, H = witness
        iter(N)
        iter(H)
        for n in N:
            for h in H:
                _ = n * h
                _ = h * n
        h1_ok = True
    except Exception:
        h1_ok = False

    neg_q = False
    if h1_ok:
        try:
            for n in N:
                P = True
                for h in H:
                    if not (n * h == h * n):
                        P = False
                        break
                
                Q = True
                for h in H:
                    try:
                        if not (h * n * h**-1 == n):
                            Q = False
                            break
                    except Exception:
                        Q = False
                        break
                
                if P != Q:
                    neg_q = True
                    break
        except Exception:
            neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: C_N(H) is defined as the centralizer of H in N",
    "¬Q: There exists n in N such that n in C_N(H) is not equivalent to hnh^{-1} = n for all h in H"
]

N_HYP = 1
NEG_Q_INDEX = 1