import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, N1, N2 = witness
        else:
            G = witness.G
            N1 = witness.N1
            N2 = witness.N2
    except Exception:
        return [False, False, False, False]

    def is_dp_nonabelian_simple(grp):
        if hasattr(grp, 'is_isomorphic_to_direct_product_of_nonabelian_simple_groups'):
            val = grp.is_isomorphic_to_direct_product_of_nonabelian_simple_groups
            return bool(val() if callable(val) else val)
        try:
            if grp.order() == 1:
                return True
            if not grp.is_perfect:
                return False
            if grp.center().order() > 1:
                return False
            return True
        except Exception:
            return False

    # H_1: G is isomorphic to a direct product of non-abelian simple groups
    try:
        h1 = is_dp_nonabelian_simple(G)
    except Exception:
        h1 = False

    # H_2: N_1 is a normal subgroup of G
    try:
        if hasattr(N1, 'is_normal'):
            val = N1.is_normal(G)
            h2 = bool(val() if callable(val) else val)
        elif hasattr(N1, 'is_normal_subgroup'):
            val = N1.is_normal_subgroup(G)
            h2 = bool(val() if callable(val) else val)
        else:
            h2 = N1.is_subgroup(G) and all((g * h * ~g) in N1 for g in G.generators for h in N1.generators)
    except Exception:
        h2 = False

    # H_3: N_2 is a normal subgroup of G
    try:
        if hasattr(N2, 'is_normal'):
            val = N2.is_normal(G)
            h3 = bool(val() if callable(val) else val)
        elif hasattr(N2, 'is_normal_subgroup'):
            val = N2.is_normal_subgroup(G)
            h3 = bool(val() if callable(val) else val)
        else:
            h3 = N2.is_subgroup(G) and all((g * h * ~g) in N2 for g in G.generators for h in N2.generators)
    except Exception:
        h3 = False

    # neg_Q: The intersection N_1 \cap N_2 is neither the trivial subgroup nor isomorphic to a direct product of non-abelian simple groups
    try:
        int_N1_N2 = None
        if hasattr(G, 'intersection'):
            int_N1_N2 = G.intersection(N1, N2)
        elif hasattr(N1, 'intersect'):
            val = N1.intersect(N2)
            int_N1_N2 = val() if callable(val) else val
        elif hasattr(N1, 'intersection'):
            val = N1.intersection(N2)
            int_N1_N2 = val() if callable(val) else val
        else:
            # Fallback for SymPy PermutationGroup
            elements = set(N1.generate_dimino()) & set(N2.generate_dimino())
            int_N1_N2 = PermutationGroup(list(elements))
            
        if int_N1_N2 is not None:
            if hasattr(int_N1_N2, 'order'):
                order = int_N1_N2.order()
            else:
                order = len(list(int_N1_N2.generate_dimino()))
                
            is_trivial = (order == 1)
            is_dp = is_dp_nonabelian_simple(int_N1_N2)
            
            neg_q = not (is_trivial or is_dp)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is isomorphic to a direct product of non-abelian simple groups",
    "H_2: N_1 is a normal subgroup of G",
    "H_3: N_2 is a normal subgroup of G",
    "¬Q: The intersection N_1 \\cap N_2 is neither the trivial subgroup nor isomorphic to a direct product of non-abelian simple groups"
]

N_HYP = 3
NEG_Q_INDEX = 3