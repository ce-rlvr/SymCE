import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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
trivial = PermutationGroup([Permutation(0)])

def is_subgroup(H, G):
    try:
        for h in H.generators:
            if h not in G:
                return False
        return True
    except Exception:
        return False

def is_normal(H, G):
    try:
        if not is_subgroup(H, G):
            return False
        for g in G.generators:
            for h in H.generators:
                if (g * h * ~g) not in H:
                    return False
                if (~g * h * g) not in H:
                    return False
        return True
    except Exception:
        return False

def check_cyclic(grp):
    try:
        order = grp.order()
        if order == 1:
            return True
        for g in grp.generate():
            if g.order() == order:
                return True
        return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False, False]
        G, N = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False
        
    # H_2: N is a normal cyclic subgroup of G
    try:
        h2_ok = isinstance(N, PermutationGroup) and is_normal(N, G) and check_cyclic(N)
    except Exception:
        h2_ok = False
        
    # ¬Q: The derived subgroup G' is NOT a cyclic group contained in N
    try:
        G_prime = G.derived_subgroup()
        G_prime_cyclic = check_cyclic(G_prime)
        G_prime_in_N = is_subgroup(G_prime, N)
        
        # The conclusion is (G' is cyclic AND G' is contained in N)
        # We want the negation of the conclusion
        neg_q_ok = not (G_prime_cyclic and G_prime_in_N)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal cyclic subgroup of G",
    "¬Q: G' is not a cyclic group contained in N"
]

N_HYP = 2
NEG_Q_INDEX = 2