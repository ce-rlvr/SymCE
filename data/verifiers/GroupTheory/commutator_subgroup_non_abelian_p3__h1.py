import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: G is a group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: The order of G is p^3
    try:
        n = witness.order() if callable(witness.order) else witness.order
        p = int(round(n**(1/3)))
        h2 = (p**3 == n)
    except Exception:
        h2 = False

    # H_3: G is non-abelian
    try:
        is_ab = witness.is_abelian() if callable(witness.is_abelian) else witness.is_abelian
        h3 = not is_ab
    except Exception:
        h3 = False

    # neg_Q: The commutator subgroup G' has order p and is equal to the center Z(G)
    try:
        n = witness.order() if callable(witness.order) else witness.order
        p = int(round(n**(1/3)))
        
        G_prime = witness.derived_subgroup()
        Z = witness.center()
        
        gp_order = G_prime.order() if callable(G_prime.order) else G_prime.order
        z_order = Z.order() if callable(Z.order) else Z.order
        
        same_order = (gp_order == z_order)
        is_sub = all((g in Z) for g in G_prime.generators)
        
        q_holds = (gp_order == p) and same_order and is_sub
        neg_q = not q_holds
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: The order of G is p^3",
    "H_3: G is non-abelian",
    "¬Q: The commutator subgroup G' does not have order p or is not equal to the center Z(G)"
]

N_HYP = 3
NEG_Q_INDEX = 3