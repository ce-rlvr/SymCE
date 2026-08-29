import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.perm_groups import PermutationGroup

# Standard group theory objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def direct_product(G1, G2):
    """Computes the external direct product of two permutation groups."""
    try:
        res = G1 * G2
        if isinstance(res, PermutationGroup):
            return res
    except Exception:
        pass
    
    # Fallback manual construction
    d1 = G1.degree
    d2 = G2.degree
    gens = []
    for g in G1.generators:
        arr = list(g.array_form)
        if len(arr) < d1:
            arr += list(range(len(arr), d1))
        arr += list(range(d1, d1 + d2))
        gens.append(Permutation(arr))
    for g in G2.generators:
        arr = list(g.array_form)
        if len(arr) < d2:
            arr += list(range(len(arr), d2))
        arr_shifted = list(range(d1)) + [x + d1 for x in arr]
        gens.append(Permutation(arr_shifted))
        
    if not gens:
        # Both groups are trivial
        return PermutationGroup([Permutation(max(0, d1 + d2 - 1))])
    return PermutationGroup(gens)

def is_normal(H, G):
    """Checks if H is a normal subgroup of G."""
    try:
        if hasattr(G, 'is_normal'):
            res = G.is_normal(H)
            if res is not None:
                return res
    except Exception:
        pass

    try:
        # Fallback check
        if hasattr(H, 'is_subgroup'):
            if not H.is_subgroup(G):
                return False
        else:
            for h in H.generators:
                if h not in G:
                    return False
        
        # Check normality via conjugation of generators
        for g in G.generators:
            for h in H.generators:
                if (g * h * g**-1) not in H:
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the conjecture.
    Order of return: [H_1, H_2, neg_Q]
    """
    try:
        if isinstance(witness, dict):
            G1 = witness.get('G1')
            G2 = witness.get('G2')
            N1 = witness.get('N1')
            N2 = witness.get('N2')
        else:
            G1, G2, N1, N2 = witness
    except Exception:
        return [False, False, False]

    # H_1: N1 is a normal subgroup of G1
    try:
        h1 = is_normal(N1, G1)
    except Exception:
        h1 = False

    # H_2: N2 is a normal subgroup of G2
    try:
        h2 = is_normal(N2, G2)
    except Exception:
        h2 = False

    # ¬Q: N1 x N2 is NOT a normal subgroup of G1 x G2
    try:
        G1xG2 = direct_product(G1, G2)
        N1xN2 = direct_product(N1, N2)
        neg_q = not is_normal(N1xN2, G1xG2)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: N1 is a normal subgroup of G1",
    "H_2: N2 is a normal subgroup of G2",
    "¬Q: N1 x N2 is not a normal subgroup of G1 x G2"
]

N_HYP = 2
NEG_Q_INDEX = 2