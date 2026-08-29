import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference
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
    Checks if the witness is a valid counterexample to the false conjecture:
    "If G acts non-trivially on a set X, then the action is faithful."
    
    The witness can be provided in two ways:
    1. A sympy GroupHomomorphism representing the action of G on X.
    2. A tuple (G, K) where G is a PermutationGroup and K is a normal subgroup 
       representing the kernel of the action of G on some set X (e.g., G/K).
    """
    is_hom = False
    try:
        from sympy.combinatorics.homomorphisms import GroupHomomorphism
        if isinstance(witness, GroupHomomorphism):
            is_hom = True
    except Exception:
        pass

    if is_hom:
        try:
            h1 = True
        except Exception:
            h1 = False

        try:
            h2 = False
            for g in witness.domain.generators:
                img_g = witness(g)
                is_id = img_g.is_Identity
                if callable(is_id):
                    is_id = is_id()
                if not is_id:
                    h2 = True
                    break
        except Exception:
            h2 = False

        try:
            neg_q = False
            ker = witness.kernel()
            try:
                order = ker.order()
            except TypeError:
                order = ker.order
            if order > 1:
                neg_q = True
        except Exception:
            neg_q = False

        return [h1, h2, neg_q]

    # Otherwise, assume witness is (G, K) where K is the kernel of the action
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, K = witness
            h1 = isinstance(G, PermutationGroup) and isinstance(K, PermutationGroup)
            if h1:
                if not K.is_subgroup(G):
                    h1 = False
                elif not K.is_normal(G):
                    h1 = False
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        h2 = False
        if h1:
            G, K = witness
            try:
                order_G = G.order()
                order_K = K.order()
            except TypeError:
                order_G = G.order
                order_K = K.order
            # The action is trivial iff the kernel is the whole group G
            if order_K < order_G:
                h2 = True
    except Exception:
        h2 = False

    try:
        neg_q = False
        if h1:
            G, K = witness
            try:
                order_K = K.order()
            except TypeError:
                order_K = K.order
            # The action is not faithful iff the kernel is not trivial
            if order_K > 1:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G acts on a set X",
    "H_2: The action of G on X is not the trivial action",
    "¬Q: The action of G on X is not faithful (kernel is not trivial)"
]

N_HYP = 2
NEG_Q_INDEX = 2