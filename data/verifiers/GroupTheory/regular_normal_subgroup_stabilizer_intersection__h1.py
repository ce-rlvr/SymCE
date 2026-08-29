import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import Integer

# Top-level setup for named groups
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

def conditions(witness):
    try:
        if len(witness) == 3:
            G, N, x = witness
        elif len(witness) == 4:
            G, N, x, _ = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: N is a regular normal subgroup of G
    try:
        is_normal = G.is_normal(N)
        
        # A permutation group is regular on its support if it acts transitively on it
        # and its order equals the size of the support.
        def is_regular_on_support(grp):
            if grp.order() == 1:
                return True
            supp = set()
            for g in grp.generators:
                supp.update(g.support())
            if not supp:
                return True
            orbits = grp.orbits()
            supp_orbits = [orb for orb in orbits if len(orb) > 1]
            if len(supp_orbits) != 1:
                return False
            if len(supp_orbits[0]) != len(supp):
                return False
            return grp.order() == len(supp)
            
        # We allow N to be regular in the strict sympy sense (on its degree) 
        # or regular on its support (in case N was defined with the same degree as G).
        is_reg = N.is_regular or is_regular_on_support(N)
        h1 = bool(is_normal and is_reg)
    except Exception:
        h1 = False

    # H2: x is an element of X (the domain of G)
    try:
        h2 = isinstance(x, (int, Integer)) and 0 <= x < G.degree
    except Exception:
        h2 = False

    # H3: G_x is the stabilizer of x in G
    try:
        G_x = G.stabilizer(x)
        if len(witness) == 4:
            provided_Gx = witness[3]
            h3 = bool(provided_Gx.is_subgroup(G_x) and G_x.is_subgroup(provided_Gx))
        else:
            h3 = True
    except Exception:
        h3 = False

    # neg_Q: The intersection G_x \cap N is NOT the trivial subgroup {e}
    try:
        neg_q = False
        if h3:
            # Check if there is any non-identity element in N that is also in G_x.
            # Since N is a subgroup of G, any element of N that fixes x is in G_x.
            for g in N.generate():
                if not g.is_Identity:
                    if g(x) == x:
                        neg_q = True
                        break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: N is a regular normal subgroup of G",
    "H_2: x is an element of X",
    "H_3: G_x is the stabilizer of x in G",
    "¬Q: The intersection G_x \\cap N is not the trivial subgroup {e}"
]

N_HYP = 3
NEG_Q_INDEX = 3