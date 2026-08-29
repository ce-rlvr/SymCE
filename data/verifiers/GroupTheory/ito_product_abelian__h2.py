import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def conditions(witness) -> list[bool]:
    # witness is expected to be a tuple (G, A, B)
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, A, B = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a group, and A, B are subgroups of G
    try:
        if isinstance(A, list):
            A = PermutationGroup(A)
        if isinstance(B, list):
            B = PermutationGroup(B)
            
        h1 = isinstance(G, PermutationGroup) and isinstance(A, PermutationGroup) and isinstance(B, PermutationGroup)
        if h1:
            for gen in A.generators:
                if gen not in G:
                    h1 = False
                    break
            for gen in B.generators:
                if gen not in G:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H_2: G = AB
    try:
        h2 = False
        if h1:
            a_order = A.order() if callable(getattr(A, 'order', None)) else A.order
            b_order = B.order() if callable(getattr(B, 'order', None)) else B.order
            g_order = G.order() if callable(getattr(G, 'order', None)) else G.order
            
            if a_order <= 5000 and b_order <= 5000:
                if hasattr(A, 'generate'):
                    set_A = list(A.generate())
                else:
                    set_A = list(A.elements)
                    
                if hasattr(B, 'generate'):
                    set_B = list(B.generate())
                else:
                    set_B = list(B.elements)
                    
                intersection_size = sum(1 for a in set_A if a in B)
                if g_order == (len(set_A) * len(set_B)) // intersection_size:
                    h2 = True
    except Exception:
        h2 = False

    # neg_Q: G is not metabelian or not solvable
    try:
        neg_q = False
        if h1:
            C = G.derived_subgroup()
            is_metabelian = C.is_abelian() if callable(getattr(C, 'is_abelian', None)) else C.is_abelian
            is_solvable = G.is_solvable() if callable(getattr(G, 'is_solvable', None)) else G.is_solvable
            neg_q = not (is_metabelian and is_solvable)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group, and A, B are subgroups of G",
    "H_2: G = AB",
    "¬Q: G is not metabelian or not solvable"
]

N_HYP = 2
NEG_Q_INDEX = 2