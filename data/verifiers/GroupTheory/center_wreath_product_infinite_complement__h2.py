import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

def construct_wreath_product(A, B):
    B_degree = max(B.degree, 1)
    B_elems = list(B.generate())
    B_order = len(B_elems)
    
    def perm_to_tuple(p, deg):
        return tuple(p(i) for i in range(deg))
        
    elem_to_idx = {perm_to_tuple(elem, B_degree): i for i, elem in enumerate(B_elems)}
    
    A_gens = A.generators
    A_degree = max(A.degree, 1)
    
    W_gens = []
    for i in range(B_order):
        for g in A_gens:
            images = list(range(B_order * A_degree))
            for j in range(A_degree):
                images[i * A_degree + j] = i * A_degree + g(j)
            if images != list(range(B_order * A_degree)):
                W_gens.append(Permutation(images))
                
    for g in B.generators:
        images = list(range(B_order * A_degree))
        for i, b in enumerate(B_elems):
            b_new = b * g
            tup = perm_to_tuple(b_new, B_degree)
            j = elem_to_idx[tup]
            for k in range(A_degree):
                images[i * A_degree + k] = j * A_degree + k
        if images != list(range(B_order * A_degree)):
            W_gens.append(Permutation(images))
            
    if not W_gens:
        W_gens.append(Permutation(0))
        
    return PermutationGroup(W_gens)

def is_in_center(g, G):
    for h in G.generators:
        if g * h != h * g:
            return False
    return True

def get_center_order(G):
    try:
        if hasattr(G, 'center'):
            C = G.center()
            if hasattr(C, 'order'):
                return C.order()
            elif isinstance(C, list):
                if not C:
                    return 1
                return PermutationGroup(*C).order()
    except Exception:
        pass
    
    c_count = 0
    for g in G.generate():
        if is_in_center(g, G):
            c_count += 1
    return c_count

def conditions(witness) -> list[bool]:
    A = None
    B = None
    W = None
    W_provided = False
    
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            B = witness.get('B')
            if 'W' in witness:
                W = witness['W']
                W_provided = True
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                A, B = witness
            elif len(witness) == 3:
                A, B, W = witness
                W_provided = True
    except Exception:
        pass

    # H1: A is a non-trivial group
    try:
        h1 = hasattr(A, 'order') and A.order() > 1
    except Exception:
        h1 = False

    # H2: W is the restricted wreath product of A by B
    try:
        if not W_provided:
            W = construct_wreath_product(A, B)
            h2 = True
        else:
            expected_order = (A.order() ** B.order()) * B.order()
            h2 = (W.order() == expected_order)
    except Exception:
        h2 = False

    # neg_Q: The center of W is NOT the trivial subgroup
    try:
        c_order = get_center_order(W)
        neg_q = (c_order > 1)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is a non-trivial group",
    "H_2: W is the restricted wreath product of A by B",
    "¬Q: The center of W is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2