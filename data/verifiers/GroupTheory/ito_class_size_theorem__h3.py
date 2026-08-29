import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))

def get_elements(G):
    try:
        if hasattr(G, 'elements'):
            return list(G.elements)
        elif hasattr(G, 'generate'):
            return list(G.generate())
    except Exception:
        pass
    return []

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False, False]
        G, A = witness
    except Exception:
        return [False, False, False]
        
    # H1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False
        
    # H2: A is an abelian normal subgroup of G
    try:
        if not isinstance(A, PermutationGroup):
            h2_ok = False
        else:
            A_elems = set(get_elements(A))
            G_elems = set(get_elements(G))
            
            is_sub = A_elems.issubset(G_elems)
            is_ab = A.is_abelian
            
            is_norm = True
            if is_sub:
                for g in G_elems:
                    for a in A_elems:
                        if g * a * ~g not in A_elems:
                            is_norm = False
                            break
                    if not is_norm:
                        break
            else:
                is_norm = False
                
            h2_ok = bool(is_sub and is_ab and is_norm)
    except Exception:
        h2_ok = False
        
    # neg_Q: The size of the conjugacy class of x in G does NOT divide the index of A in G for some x
    try:
        A_elems = set(get_elements(A))
        G_elems = set(get_elements(G))
        if len(A_elems) == 0 or not A_elems.issubset(G_elems):
            neg_q = False
        else:
            index = len(G_elems) // len(A_elems)
            neg_q = False
            for x in G_elems:
                conj_class = set()
                for g in G_elems:
                    conj_class.add(g * x * ~g)
                c_size = len(conj_class)
                if index % c_size != 0:
                    neg_q = True
                    break
    except Exception:
        neg_q = False
        
    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: A is an abelian normal subgroup of G",
    "¬Q: There exists x in G whose conjugacy class size does not divide the index of A in G"
]

N_HYP = 2
NEG_Q_INDEX = 2