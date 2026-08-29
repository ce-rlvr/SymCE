import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math

# Top-level setup for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    # Witness can be (G, H) or (G, H, N)
    try:
        if len(witness) == 2:
            G, H = witness
            N_provided = None
        elif len(witness) == 3:
            G, H, N_provided = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        if not isinstance(G, PermutationGroup):
            h1 = False
        else:
            elements = list(G.generate())
            h1 = isinstance(H, (list, set, tuple)) and all(h in elements for h in H)
    except Exception:
        h1 = False

    # H_2: The index of H in G is a finite integer n
    try:
        if h1:
            H_set = set(H)
            if len(H_set) > 0:
                order_G = G.order()
                h2 = (order_G % len(H_set) == 0)
                n = order_G // len(H_set)
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: N is the normal core of H in G
    try:
        if h1 and h2:
            core = set(H)
            for g in elements:
                g_inv = ~g
                gHg = {g * h * g_inv for h in H}
                core = core.intersection(gHg)
            
            if N_provided is not None:
                h3 = (set(N_provided) == core)
                N = set(N_provided)
            else:
                h3 = True
                N = core
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: N is not a normal subgroup of G or the index of N in G does not divide n!
    try:
        if h1 and h2 and h3:
            if len(N) == 0:
                q = False
            else:
                # Check if N is a subgroup (closed under multiplication and inversion)
                is_subgroup = all((a * b) in N for a in N for b in N) and all(~a in N for a in N)
                
                # Check if N is normal in G
                is_normal = True
                for g in elements:
                    for n_elem in N:
                        if (g * n_elem * ~g) not in N:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                
                # Check if the index of N in G divides n!
                order_G = G.order()
                if order_G % len(N) != 0:
                    index_divides = False
                else:
                    index_N = order_G // len(N)
                    index_divides = (math.factorial(n) % index_N == 0)
                
                q = is_subgroup and is_normal and index_divides
            neg_q = not q
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: The index of H in G is a finite integer n",
    "H_3: N is the normal core of H in G",
    "¬Q: N is not a normal subgroup of G or the index of N in G does not divide n!"
]

N_HYP = 3
NEG_Q_INDEX = 3