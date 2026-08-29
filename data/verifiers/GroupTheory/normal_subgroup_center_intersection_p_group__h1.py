import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    Returns a list of booleans: [H_1_ok, H_2_ok, neg_Q_ok]
    """
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) >= 4:
                G, N, p, n = witness[:4]
            else:
                G, N = witness[:2]
                p, n = None, None
        else:
            G = witness.G
            N = witness.N
            p = getattr(witness, 'p', None)
            n = getattr(witness, 'n', None)
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group of order p^n for some integer n >= 1
    try:
        if p is not None and n is not None:
            h1 = bool((G.order() == p**n) and (n >= 1))
        else:
            # If p and n are not explicitly provided, any finite group satisfies this 
            # since we can always choose p = |G| and n = 1.
            h1 = bool(hasattr(G, 'order') and 0 < G.order() < float('inf'))
    except Exception:
        h1 = False

    # H_2: N is a non-trivial normal subgroup of G
    try:
        is_nontrivial = bool(N.order() > 1)
        
        is_subgroup = True
        for n_gen in N.generators:
            if not G.contains(n_gen):
                is_subgroup = False
                break
                
        is_normal = True
        if is_subgroup:
            for g in G.generators:
                for n_gen in N.generators:
                    conj = g * n_gen * (g**-1)
                    if not N.contains(conj):
                        is_normal = False
                        break
                if not is_normal:
                    break
        else:
            is_normal = False
            
        h2 = bool(is_subgroup and is_normal and is_nontrivial)
    except Exception:
        h2 = False

    # neg_Q: The intersection N \cap Z(G) contains ONLY the identity element
    try:
        intersection_size = 0
        for n_elem in N.elements:
            is_in_center = True
            for g in G.generators:
                if n_elem * g != g * n_elem:
                    is_in_center = False
                    break
            if is_in_center:
                intersection_size += 1
                if intersection_size > 1:
                    break
        neg_q = bool(intersection_size == 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group of order p^n for some integer n >= 1",
    "H_2: N is a non-trivial normal subgroup of G",
    "¬Q: The intersection N \\cap Z(G) contains ONLY the identity element"
]

N_HYP = 2
NEG_Q_INDEX = 2