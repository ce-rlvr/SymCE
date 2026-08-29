import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.ntheory import isprime

# Standard group theory bindings
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4) # V4 is isomorphic to a subgroup of A4, but we provide A4
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

def conditions(witness) -> list[bool]:
    """
    Checks the hypotheses and negated conclusion for the false conjecture related to Burnside's Fusion Theorem.
    Witness is expected to be a tuple: (G, p, P, x, y)
    where G is a PermutationGroup, p is an integer, P is a PermutationGroup (subgroup of G),
    and x, y are Permutations.
    """
    try:
        G, p, P, x, y = witness
    except Exception:
        return [False, False, False, False, False]

    # H1: p is a prime number dividing the order of G
    try:
        h1 = isprime(p) and G.order() % p == 0
    except Exception:
        h1 = False

    # H2: P is a Sylow p-subgroup of G
    try:
        if not P.is_subgroup(G):
            h2 = False
        else:
            order = P.order()
            if order == 1:
                h2 = False
            else:
                # Check if P is a p-group
                temp = order
                while temp % p == 0:
                    temp //= p
                if temp != 1:
                    h2 = False
                else:
                    # Check if P is maximal (Sylow)
                    G_order = G.order()
                    max_p_power = 1
                    temp = G_order
                    while temp % p == 0:
                        max_p_power *= p
                        temp //= p
                    h2 = (order == max_p_power)
    except Exception:
        h2 = False

    # H3: x and y are elements in the center Z(P) of P
    try:
        if not P.contains(x) or not P.contains(y):
            h3 = False
        else:
            h3 = True
            # Check if x and y commute with all generators of P
            for gen in P.generators:
                if x * gen != gen * x:
                    h3 = False
                    break
                if y * gen != gen * y:
                    h3 = False
                    break
    except Exception:
        h3 = False

    # H4: There exists an element g \in G such that g x g^{-1} = y
    try:
        h4 = False
        for g in G.elements:
            if g * x * ~g == y:
                h4 = True
                break
    except Exception:
        h4 = False

    # neg_Q: There does NOT exist an element n \in N_G(P) such that n x n^{-1} = y
    try:
        neg_q = True
        for g in G.elements:
            if g * x * ~g == y:
                # Check if g normalizes P
                normalizes = True
                for gen in P.generators:
                    if not P.contains(g * gen * ~g):
                        normalizes = False
                        break
                if normalizes:
                    neg_q = False
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number dividing the order of G",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: x and y are elements in the center Z(P) of P",
    "H_4: There exists an element g in G such that g x g^{-1} = y",
    "¬Q: There does NOT exist an element n in N_G(P) such that n x n^{-1} = y"
]

N_HYP = 4
NEG_Q_INDEX = 4