import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
V4 = Z2 * Z2

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_free_abelian_of_rank(G, r):
    try:
        is_ab = getattr(G, 'is_abelian', False)
        if not is_ab:
            return False
        if hasattr(G, 'order'):
            # A finite group is free abelian iff it is the trivial group (rank 0)
            if G.order() == 1 and r == 0:
                return True
            return False
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    try:
        A, B, m, n = witness
        m = int(m)
        n = int(n)
    except Exception:
        return [False, False]
    
    # H_1: A is a free abelian group of finite rank m
    try:
        h1 = is_free_abelian_of_rank(A, m)
    except Exception:
        h1 = False
        
    # neg_Q: A \times B is NOT a free abelian group of rank m + n
    try:
        if hasattr(A, '__mul__'):
            AxB = A * B
            is_free_ab = is_free_abelian_of_rank(AxB, m + n)
            neg_q = not is_free_ab
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a free abelian group of finite rank m",
    "¬Q: A \\times B is not a free abelian group of rank m + n"
]

N_HYP = 1
NEG_Q_INDEX = 1