import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

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

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False, False]
        p, G = witness
    except Exception:
        return [False, False, False, False]

    # H1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    # H2: G is a group
    try:
        h2 = isinstance(G, PermutationGroup)
    except Exception:
        h2 = False

    # H3: G is non-abelian
    try:
        h3 = not bool(G.is_abelian)
    except Exception:
        h3 = False

    # neg_Q: The commutator subgroup G' has order p and is equal to the center Z(G) (negated)
    try:
        if not h2:
            neg_q = False
        else:
            G_prime = G.derived_subgroup()
            Z_G = G.center()
            
            order_p = (G_prime.order() == p)
            eq_center = G_prime.is_subgroup(Z_G) and Z_G.is_subgroup(G_prime)
            
            neg_q = not (order_p and eq_center)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: G is a group",
    "H_3: G is non-abelian",
    "¬Q: G' does not have order p or G' is not equal to Z(G)"
]

N_HYP = 3
NEG_Q_INDEX = 3