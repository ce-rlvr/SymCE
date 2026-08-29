import math
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]])])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def to_group(obj):
    if isinstance(obj, PermutationGroup):
        return obj
    try:
        return PermutationGroup(obj)
    except Exception:
        return None

def conditions(witness) -> list[bool]:
    try:
        G, N, H1, H2 = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        G = to_group(G)
        N = to_group(N)
        H1 = to_group(H1)
        H2 = to_group(H2)
    except Exception:
        pass

    try:
        h1 = G is not None and N is not None
        if h1:
            for g in N.generators:
                if g not in G:
                    h1 = False
                    break
    except Exception:
        h1 = False

    try:
        if h1:
            order_G = G.order()
            order_N = N.order()
            if order_G % order_N != 0:
                h2 = False
            else:
                index = order_G // order_N
                h2 = math.gcd(order_N, index) == 1
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        h3 = H1 is not None and H2 is not None and G is not None and N is not None
        if h3:
            order_G = G.order()
            order_N = N.order()
            for H in [H1, H2]:
                for g in H.generators:
                    if g not in G:
                        h3 = False
                        break
                if not h3:
                    break
                
                if order_N * H.order() != order_G:
                    h3 = False
                    break
                
                if math.gcd(order_N, H.order()) != 1:
                    if N.order() < H.order():
                        smaller, larger = N, H
                    else:
                        smaller, larger = H, N
                    
                    larger_elems = set(larger.generate())
                    for g in smaller.generate():
                        if g.is_Identity:
                            continue
                        if g in larger_elems:
                            h3 = False
                            break
                if not h3:
                    break
    except Exception:
        h3 = False

    try:
        if H1 is None or H2 is None or G is None:
            neg_q = False
        elif H1.order() != H2.order():
            neg_q = True
        else:
            def get_cycle_structures(H):
                counts = {}
                for h in H.generate():
                    struct = tuple(sorted(h.cycle_structure.items()))
                    counts[struct] = counts.get(struct, 0) + 1
                return counts
            
            if get_cycle_structures(H1) != get_cycle_structures(H2):
                are_conjugate = False
            else:
                h2_elems = set(H2.generate())
                h1_gens = H1.generators
                are_conjugate = False
                for g in G.generate():
                    maps_into = True
                    for h in h1_gens:
                        if (g * h * ~g) not in h2_elems:
                            maps_into = False
                            break
                    if maps_into:
                        are_conjugate = True
                        break
            neg_q = not are_conjugate
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group and N is a subgroup of G",
    "H_2: The order of N and the index of N in G are coprime",
    "H_3: H1 and H2 are complements of N in G",
    "¬Q: H1 and H2 are not conjugate in G"
]

N_HYP = 3
NEG_Q_INDEX = 3