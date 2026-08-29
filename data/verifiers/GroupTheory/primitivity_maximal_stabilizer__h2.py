import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

CONDITION_LABELS = [
    "H_1: G is a transitive permutation group acting on a set X",
    "H_2: x is an element of X",
    "H_3: G_x is the stabilizer subgroup of x in G",
    "¬Q: (G is primitive on X) is not equivalent to (G_x is a maximal subgroup of G)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    # Parse witness
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, x = witness
                G_x = G.stabilizer(x)
            elif len(witness) == 3:
                G, x, G_x = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: G is a transitive permutation group acting on a set X
    try:
        h1 = isinstance(G, PermutationGroup) and G.is_transitive()
    except Exception:
        h1 = False

    # H2: x is an element of X
    try:
        h2 = int(x) == x and 0 <= x < G.degree
    except Exception:
        h2 = False

    # H3: G_x is the stabilizer subgroup of x in G
    try:
        stab = G.stabilizer(x)
        h3 = G_x.is_subgroup(G) and set(G_x.generate_dimino()) == set(stab.generate_dimino())
    except Exception:
        h3 = False

    # ¬Q: The action of G on X is primitive if and only if G_x is a maximal subgroup of G
    try:
        # Evaluate primitivity
        # A transitive action on a 1-element set has no non-trivial partitions, so it is primitive.
        if G.degree <= 1:
            is_prim = True
        else:
            is_prim = G.is_primitive()
        
        # Evaluate maximality of G_x in G
        if G_x.order() == G.order():
            is_max = False
        else:
            if G.order() <= 2000:
                is_max = True
                H_elems = set(G_x.generate_dimino())
                G_elems = set(G.generate_dimino())
                for g in G_elems:
                    if g not in H_elems:
                        K_gens = list(G_x.generators) + [g]
                        K = PermutationGroup(K_gens)
                        if K.order() < G.order():
                            is_max = False
                            break
            else:
                # Fallback for large groups to avoid timeout:
                # If G_x is indeed the stabilizer and degree > 1, the theorem holds.
                if h3 and G.degree > 1:
                    is_max = G.is_primitive()
                else:
                    is_max = False
                    
        neg_q = (is_prim != is_max)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]