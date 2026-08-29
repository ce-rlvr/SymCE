import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.named_groups import AbelianGroup
from sympy.ntheory import factorint

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_order(grp):
    ans = grp.order
    if callable(ans):
        return ans()
    return ans

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple of three sympy PermutationGroups: (G, N, P).
    """
    try:
        if not isinstance(witness, tuple) or len(witness) != 3:
            return [False, False, False, False]
        G, N, P = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and getattr(G, 'is_finite', True)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = isinstance(N, PermutationGroup) and N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h2 = False

    # H_3: P is a Sylow p-subgroup of N
    try:
        h3 = False
        if isinstance(P, PermutationGroup) and P.is_subgroup(N):
            order_P = get_order(P)
            order_N = get_order(N)
            if order_P == 1:
                # The trivial group is a Sylow p-subgroup for any prime p not dividing |N|
                h3 = True
            else:
                factors = factorint(order_P)
                if len(factors) == 1:
                    p = list(factors.keys())[0]
                    index = order_N // order_P
                    if index % p != 0:
                        h3 = True
    except Exception:
        h3 = False

    # ¬Q: G is not the product of N and N_G(P)
    try:
        neg_q = False
        if h1 and h2 and h3:
            def normalizes(g, grp):
                for gen in grp.generators:
                    if (g * gen * ~g) not in grp:
                        return False
                return True
            
            # Compute the order of the normalizer of P in G
            norm_G_P_order = sum(1 for g in G.generate() if normalizes(g, P))
            
            # Compute the order of the normalizer of P in N (which is N \cap N_G(P))
            norm_N_P_order = sum(1 for n in N.generate() if normalizes(n, P))
            
            # The size of the set N * N_G(P) is |N| * |N_G(P)| / |N \cap N_G(P)|
            prod_order = (get_order(N) * norm_G_P_order) // norm_N_P_order
            
            # The conclusion fails if the product does not cover all of G
            neg_q = (prod_order != get_order(G))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "H_3: P is a Sylow p-subgroup of N",
    "¬Q: G is not the product of N and N_G(P)"
]

N_HYP = 3
NEG_Q_INDEX = 3