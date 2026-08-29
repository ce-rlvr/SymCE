import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, N, x) where:
      - G is a PermutationGroup (representing a group acting on {0, ..., G.degree - 1})
      - N is a PermutationGroup
      - x is an integer
    """
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        G, N, x = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group acting on a set X
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: N is a normal subgroup of G
    try:
        h2_ok = False
        if h1_ok and isinstance(N, PermutationGroup):
            # Check if N is a subgroup of G
            is_subgroup = all(G.contains(gen) for gen in N.generators)
            if is_subgroup:
                # Check normality: g * n * g^-1 in N for all generators g of G and n of N
                is_norm = True
                G_gens = list(G.generators)
                G_gens += [~g for g in G_gens]
                for g in G_gens:
                    g_inv = ~g
                    for n in N.generators:
                        if not N.contains(g * n * g_inv):
                            is_norm = False
                            break
                    if not is_norm:
                        break
                h2_ok = is_norm
    except Exception:
        h2_ok = False

    # H_3: x is an element of X
    try:
        h3_ok = isinstance(x, int) and 0 <= x < G.degree
    except Exception:
        h3_ok = False

    # ¬Q: G != N G_x
    try:
        neg_q_ok = False
        if h1_ok and h2_ok and h3_ok:
            Gx = G.stabilizer(x)
            gens = list(N.generators) + list(Gx.generators)
            if not gens:
                NGx_order = 1
            else:
                NGx = PermutationGroup(gens)
                NGx_order = NGx.order()
            
            # If the order of the subgroup N G_x is not equal to the order of G,
            # then G != N G_x.
            neg_q_ok = NGx_order != G.order()
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: N is a normal subgroup of G",
    "H_3: x is an element of X",
    "¬Q: G != N G_x"
]

N_HYP = 3
NEG_Q_INDEX = 3