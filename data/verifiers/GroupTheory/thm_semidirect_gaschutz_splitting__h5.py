import sympy
import sympy.ntheory
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools

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

def conditions(witness) -> list[bool]:
    try:
        G, p, N, P = witness
    except Exception:
        return [False, False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = hasattr(G, 'order') and G.order() < float('inf') and hasattr(G, 'generate')
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = sympy.ntheory.isprime(p)
    except Exception:
        h2 = False

    # H_3: N is an abelian normal p-subgroup of G
    try:
        h3 = False
        if h1 and hasattr(N, 'order') and hasattr(N, 'generate'):
            N_elements = set(N.generate())
            G_elements = set(G.generate())
            if N_elements.issubset(G_elements):
                is_abelian = True
                for a in N_elements:
                    for b in N_elements:
                        if a * b != b * a:
                            is_abelian = False
                            break
                    if not is_abelian:
                        break
                if is_abelian:
                    n_order = N.order()
                    if n_order > 0:
                        factors = sympy.ntheory.factorint(n_order)
                        if (n_order == 1) or (len(factors) == 1 and p in factors):
                            is_normal = True
                            for g in G_elements:
                                g_inv = ~g
                                for n in N_elements:
                                    if g * n * g_inv not in N_elements:
                                        is_normal = False
                                        break
                                if not is_normal:
                                    break
                            h3 = is_normal
    except Exception:
        h3 = False

    # H_4: P is a Sylow p-subgroup of G
    try:
        h4 = False
        if h1 and h2 and hasattr(P, 'order') and hasattr(P, 'generate'):
            P_elements = set(P.generate())
            G_elements = set(G.generate())
            if P_elements.issubset(G_elements):
                p_order = P.order()
                g_order = G.order()
                highest_power = 1
                temp = g_order
                while temp % p == 0:
                    highest_power *= p
                    temp //= p
                if p_order == highest_power:
                    h4 = True
    except Exception:
        h4 = False

    # neg_Q: N does not have a complement in G
    try:
        neg_q = False
        if h1 and h3:
            if G.order() % N.order() != 0:
                neg_q = False
            else:
                k = G.order() // N.order()
                if k == 1:
                    neg_q = False
                else:
                    N_set = set(N.generate())
                    candidates = [g for g in G.generate() if g not in N_set and k % g.order() == 0]
                    
                    if len(candidates) < k - 1:
                        neg_q = True
                    else:
                        has_comp = False
                        max_gens = int(math.log2(k))
                        
                        for r in range(1, max_gens + 1):
                            for gens in itertools.combinations(candidates, r):
                                H = PermutationGroup(*gens)
                                if H.order() == k:
                                    H_elements = set(H.generate())
                                    if len(H_elements.intersection(N_set)) == 1:
                                        has_comp = True
                                        break
                            if has_comp:
                                break
                        neg_q = not has_comp
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: N is an abelian normal p-subgroup of G",
    "H_4: P is a Sylow p-subgroup of G",
    "¬Q: N does not have a complement in G"
]

N_HYP = 4
NEG_Q_INDEX = 4