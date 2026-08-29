import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: G is a primitive permutation group acting faithfully on a set X",
    "H_2: N is a regular normal subgroup of G",
    "H_3: x is an element of X",
    "¬Q: The intersection G_x \\cap N is not the trivial subgroup {e}"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        G, N, x = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G is a primitive permutation group acting faithfully on a set X
    try:
        h1 = isinstance(G, PermutationGroup)
        if h1:
            if hasattr(G, 'is_primitive'):
                if callable(G.is_primitive):
                    h1 = bool(G.is_primitive())
                else:
                    h1 = bool(G.is_primitive)
            else:
                h1 = False
    except Exception:
        h1 = False

    # H2: N is a regular normal subgroup of G
    try:
        h2 = False
        if isinstance(N, PermutationGroup):
            # check subgroup
            try:
                if hasattr(N, 'is_subgroup'):
                    is_sub = N.is_subgroup(G)
                else:
                    is_sub = all(G.contains(h) for h in N.generators)
            except Exception:
                is_sub = False
                
            # check normal
            try:
                if hasattr(N, 'is_normal'):
                    is_norm = N.is_normal(G)
                else:
                    is_norm = all(N.contains(g * h * ~g) for g in G.generators for h in N.generators)
            except Exception:
                is_norm = False
                
            # check regular
            try:
                if hasattr(N, 'is_regular'):
                    if callable(N.is_regular):
                        is_reg = N.is_regular()
                    else:
                        is_reg = N.is_regular
                else:
                    if hasattr(N, 'is_transitive'):
                        if callable(N.is_transitive):
                            is_trans = N.is_transitive()
                        else:
                            is_trans = N.is_transitive
                    else:
                        is_trans = False
                    is_reg = is_trans and (N.order() == N.degree)
            except Exception:
                is_reg = False
                
            h2 = bool(is_sub and is_norm and is_reg)
    except Exception:
        h2 = False

    # H3: x is an element of X
    try:
        h3 = isinstance(x, int) and 0 <= x < G.degree
    except Exception:
        h3 = False

    # neg_Q: G_x \cap N is NOT the trivial subgroup {e}
    try:
        # The intersection of G_x and N is exactly the stabilizer of x in N
        N_x = N.stabilizer(x)
        if hasattr(N_x, 'is_trivial'):
            if callable(N_x.is_trivial):
                is_triv = N_x.is_trivial()
            else:
                is_triv = N_x.is_trivial
        else:
            is_triv = (N_x.order() == 1)
        neg_q = not bool(is_triv)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]