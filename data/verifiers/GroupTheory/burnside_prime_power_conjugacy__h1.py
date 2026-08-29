import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import factorint
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
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
    neg_q_ok = False
    
    try:
        if not (isinstance(witness, tuple) and len(witness) == 2):
            return [False, False]
        
        G, C = witness
        
        C_list = []
        try:
            C_list = list(C)
        except Exception:
            if hasattr(C, 'elements'):
                C_list = list(C.elements)
                
        C_set = set(C_list)
    except Exception:
        return [False, False]

    # H_1: Let C be a conjugacy class of G.
    try:
        if len(C_set) > 0:
            c = next(iter(C_set))
            if c in G:
                # Try using built-in conjugacy_classes()
                if hasattr(G, 'conjugacy_classes'):
                    for cls in G.conjugacy_classes():
                        cls_list = []
                        try:
                            cls_list = list(cls)
                        except Exception:
                            if hasattr(cls, 'elements'):
                                cls_list = list(cls.elements)
                        if C_set == set(cls_list):
                            h1_ok = True
                            break
                
                # Fallback to manual computation if the group is small enough
                if not h1_ok and hasattr(G, 'elements'):
                    try:
                        order = G.order()
                    except Exception:
                        try:
                            order = len(list(G.elements))
                        except Exception:
                            order = float('inf')
                    
                    if order <= 2000:
                        actual_class = set(g * c * ~g for g in G.elements)
                        if C_set == actual_class:
                            h1_ok = True
    except Exception:
        h1_ok = False

    # ¬Q: The size of C IS of the form p^k for some prime p and integer k >= 1.
    try:
        n = len(C_set)
        if n > 1:
            factors = factorint(n)
            if len(factors) == 1:
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: C is a conjugacy class of G",
    "¬Q: The size of C is of the form p^k for some prime p and integer k >= 1"
]

N_HYP = 1
NEG_Q_INDEX = 1