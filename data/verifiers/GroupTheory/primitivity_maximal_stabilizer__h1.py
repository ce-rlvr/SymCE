import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be a tuple: (G, X, x)
    where G is a PermutationGroup, X is the domain set, and x is a point in X.
    """
    try:
        G, X, x = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: X contains at least two elements
    try:
        h1 = isinstance(X, (list, set, tuple)) and len(X) >= 2
    except Exception:
        h1 = False

    # H_2: x is an element of X
    try:
        h2 = x in X
    except Exception:
        h2 = False

    # H_3: G_x is the stabilizer subgroup of x in G
    # We verify that G is a valid permutation group acting on X and we can compute the stabilizer.
    try:
        h3 = False
        if isinstance(G, PermutationGroup) and set(X) == set(range(G.degree)):
            _ = G.stabilizer(x)
            h3 = True
    except Exception:
        h3 = False

    # ¬Q: The action of G on X is primitive if and only if G_x is a maximal subgroup of G (must FAIL)
    try:
        neg_q = False
        if h1 and h2 and h3:
            # P: The action of G on X is primitive
            P = G.is_primitive()
            
            # Q: G_x is a maximal subgroup of G
            # By the orbit-stabilizer theorem and properties of primitive actions,
            # G_x is maximal in G iff the action of G on the orbit of x is primitive and |orbit| > 1.
            orb = list(G.orbit(x))
            if len(orb) <= 1:
                Q = False
            else:
                induced_gens = []
                for g in G.generators:
                    perm_array = [orb.index(g(p)) for p in orb]
                    induced_gens.append(Permutation(perm_array))
                G_on_orb = PermutationGroup(induced_gens)
                Q = G_on_orb.is_primitive()
                
            # The conclusion is P == Q. The negated conclusion is P != Q.
            neg_q = (P != Q)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: X contains at least two elements",
    "H_2: x is an element of X",
    "H_3: G_x is the stabilizer subgroup of x in G",
    "¬Q: The action of G on X is primitive if and only if G_x is a maximal subgroup of G (fails)"
]

N_HYP = 3
NEG_Q_INDEX = 3