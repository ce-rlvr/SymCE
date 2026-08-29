import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for standard algebra objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, M) where M is a maximal subgroup of G.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, M = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: M is a maximal subgroup of G
    h1 = False
    try:
        if hasattr(M, 'is_maximal_subgroup'):
            val = M.is_maximal_subgroup(G)
            h1 = val() if callable(val) else val
        elif hasattr(G, 'is_maximal_subgroup'):
            val = G.is_maximal_subgroup(M)
            h1 = val() if callable(val) else val
        elif isinstance(G, PermutationGroup) and isinstance(M, PermutationGroup):
            is_sub = True
            if hasattr(M, 'is_subgroup'):
                is_sub = M.is_subgroup(G)
            else:
                for gen in M.generators:
                    if not G.contains(gen):
                        is_sub = False
                        break
            
            if is_sub and M.order() < G.order():
                is_max = True
                for g in G.elements:
                    if not M.contains(g):
                        # If M is maximal, adding any element not in M must generate G
                        H = PermutationGroup(list(M.generators) + [g])
                        if H.order() != G.order():
                            is_max = False
                            break
                h1 = is_max
    except Exception:
        h1 = False

    # H_2: M is an abelian group
    h2 = False
    try:
        if hasattr(M, 'is_abelian'):
            val = M.is_abelian
            h2 = val() if callable(val) else val
    except Exception:
        h2 = False

    # ¬Q: G is not a solvable group
    neg_q = False
    try:
        if hasattr(G, 'is_solvable'):
            val = G.is_solvable
            q = val() if callable(val) else val
            neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: M is a maximal subgroup of G",
    "H_2: M is an abelian group",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2