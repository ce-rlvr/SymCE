import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

def conditions(witness) -> list[bool]:
    # The witness is expected to be a tuple (G, N, g)
    if isinstance(witness, dict):
        G = witness.get('G')
        N = witness.get('N')
        g = witness.get('g')
    else:
        try:
            if len(witness) == 3:
                G, N, g = witness
            else:
                return [False, False, False]
        except Exception:
            return [False, False, False]

    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: g \in G is an element of finite order
    try:
        h2_ok = isinstance(g, Permutation) and (g in G) and (g.order() > 0)
    except Exception:
        h2_ok = False

    # ¬Q: The order of the coset gN in the quotient group G/N does not divide the order of g in G
    # (This includes the case where G/N is not a valid quotient group because N is not normal)
    try:
        if isinstance(N, Permutation):
            N = PermutationGroup([N])
        elif isinstance(N, list):
            N = PermutationGroup(N)
            
        if not isinstance(N, PermutationGroup):
            neg_q_ok = False
        else:
            # Check if N is a subgroup of G
            is_subgroup = all(gen in G for gen in N.generators)
            if not is_subgroup:
                # If N is not a subgroup, G/N is not a quotient group
                neg_q_ok = True
            else:
                # Check if N is a normal subgroup of G
                is_normal = True
                for g_gen in G.generators:
                    for n_gen in N.generators:
                        if (g_gen * n_gen * (g_gen**-1)) not in N:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                
                if not is_normal:
                    # If N is not normal, G/N is not a quotient group
                    neg_q_ok = True
                else:
                    # If N is normal, G/N is a valid quotient group.
                    # The order of gN is the smallest k > 0 such that g**k in N.
                    k = 1
                    curr = g
                    max_k = g.order()
                    while curr not in N and k <= max_k:
                        curr = curr * g
                        k += 1
                    
                    if k > max_k:
                        neg_q_ok = True
                    else:
                        neg_q_ok = (g.order() % k != 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: g in G is an element of finite order",
    "¬Q: The order of the coset gN in the quotient group G/N does not divide the order of g in G (or G/N is not a valid quotient group)"
]

N_HYP = 2
NEG_Q_INDEX = 2