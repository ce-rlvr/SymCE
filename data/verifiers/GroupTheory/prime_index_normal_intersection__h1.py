import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.combinatorics import PermutationGroup
from sympy import isprime

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

def conditions(witness):
    try:
        if len(witness) != 4:
            return [False] * 5
        G, N, p, H = witness
    except Exception:
        return [False] * 5

    # H1: N is a normal subgroup of G
    try:
        h1 = True
        for gen in N.generators:
            if gen not in G:
                h1 = False
                break
        if h1:
            for g in G.generators:
                for n in N.generators:
                    if (g * n * ~g) not in N:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    # H3: index of N in G is p
    try:
        h3 = (G.order() == p * N.order())
    except Exception:
        h3 = False

    # H4: H is a subgroup of G
    try:
        h4 = True
        for gen in H.generators:
            if gen not in G:
                h4 = False
                break
    except Exception:
        h4 = False

    # neg_Q: not (H \subseteq N or index of H cap N in H == p)
    try:
        h_in_n = True
        for gen in H.generators:
            if gen not in N:
                h_in_n = False
                break
        
        index_p = False
        try:
            if hasattr(H, 'intersection'):
                H_cap_N = H.intersection(N)
                index_p = (H.order() == p * H_cap_N.order())
            elif hasattr(H, 'intersect'):
                H_cap_N = H.intersect(N)
                index_p = (H.order() == p * H_cap_N.order())
            else:
                HN = PermutationGroup(list(H.generators) + list(N.generators))
                index_p = (HN.order() == p * N.order())
        except Exception:
            HN = PermutationGroup(list(H.generators) + list(N.generators))
            index_p = (HN.order() == p * N.order())
            
        neg_q = not (h_in_n or index_p)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: p is a prime number",
    "H_3: index of N in G is p",
    "H_4: H is a subgroup of G",
    "¬Q: H is not a subgroup of N and index of H cap N in H is not p"
]

N_HYP = 4
NEG_Q_INDEX = 4