import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.ntheory import isprime

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

def conditions(witness) -> list[bool]:
    try:
        G, p, P = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: p is a prime number
    try:
        h2 = isprime(p)
    except Exception:
        h2 = False
        
    # H_3: P is a Sylow p-subgroup of G
    try:
        if not isinstance(P, PermutationGroup):
            h3 = False
        elif not isinstance(p, (int, sympy.Integer)):
            h3 = False
        elif p < 2:
            h3 = False
        else:
            is_sub = True
            for gen in P.generators:
                if not G.contains(gen):
                    is_sub = False
                    break
            if not is_sub:
                h3 = False
            else:
                order_G = G.order()
                order_P = P.order()
                k = 0
                temp = order_G
                while temp % p == 0:
                    k += 1
                    temp //= p
                h3 = (order_P == p**k)
    except Exception:
        h3 = False
        
    # neg_Q: The normalizer of N_G(P) in G is not equal to N_G(P)
    try:
        def get_normalizer_group(Grp, Sub):
            norm_elements = []
            sub_gens = Sub.generators
            for g in Grp.generate():
                is_norm = True
                g_inv = ~g
                for h in sub_gens:
                    conj = g * h * g_inv
                    if not Sub.contains(conj):
                        is_norm = False
                        break
                if is_norm:
                    norm_elements.append(g)
            return PermutationGroup(*norm_elements)
            
        N1 = get_normalizer_group(G, P)
        N2 = get_normalizer_group(G, N1)
        neg_q = (N1.order() != N2.order())
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: The normalizer of N_G(P) in G is not equal to N_G(P)"
]

N_HYP = 3
NEG_Q_INDEX = 3