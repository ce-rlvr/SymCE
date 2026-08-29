import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
    Checks whether the witness is a valid counterexample to the false conjecture.
    Returns a list of booleans: [H_1_ok, H_2_ok, H_3_ok, neg_Q_ok].
    """
    try:
        # Witness can be a tuple (G, H, phi) or a Homomorphism object
        if isinstance(witness, tuple) and len(witness) == 3:
            G, H, phi = witness
        else:
            phi = witness
            G = phi.domain
            H = phi.codomain
    except Exception:
        return [False, False, False, False]

    def eval_phi(p, x):
        if isinstance(p, dict):
            return p[x]
        return p(x)

    # H_1: G is a simple group
    h1 = False
    try:
        if hasattr(G, 'is_simple') and callable(G.is_simple):
            h1 = bool(G.is_simple())
        elif hasattr(G, 'is_simple'):
            h1 = bool(G.is_simple)
        else:
            # A group is simple iff it has exactly 2 normal subgroups: the trivial group and itself
            normal_subgroups = G.normal_subgroups()
            h1 = len(normal_subgroups) == 2
    except Exception:
        h1 = False

    # H_2: ϕ: G → H is a group homomorphism
    h2 = False
    try:
        elements_G = list(G.generate())
        h2_ok = True
        for x in elements_G:
            px = eval_phi(phi, x)
            if px not in H:
                h2_ok = False
                break
        if h2_ok:
            for x in elements_G:
                for y in elements_G:
                    if eval_phi(phi, x * y) != eval_phi(phi, x) * eval_phi(phi, y):
                        h2_ok = False
                        break
                if not h2_ok:
                    break
        h2 = h2_ok
    except Exception:
        h2 = False

    # H_3: ϕ is not the trivial homomorphism
    h3 = False
    try:
        elements_G = list(G.generate())
        first_val = eval_phi(phi, elements_G[0])
        is_trivial = True
        # If all elements map to the same value, it must be the trivial homomorphism
        for x in elements_G[1:]:
            if eval_phi(phi, x) != first_val:
                is_trivial = False
                break
        h3 = not is_trivial
    except Exception:
        h3 = False

    # ¬Q: ϕ is not injective or G is not isomorphic to ϕ(G)
    # For finite groups, if ϕ is injective, it is an isomorphism onto its image.
    # Thus, the conclusion fails iff ϕ is NOT injective.
    neg_q = False
    try:
        elements_G = list(G.generate())
        images = []
        injective = True
        for x in elements_G:
            px = eval_phi(phi, x)
            if px in images:
                injective = False
                break
            images.append(px)
        
        neg_q = not injective
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a simple group",
    "H_2: ϕ: G → H is a group homomorphism",
    "H_3: ϕ is not the trivial homomorphism",
    "¬Q: ϕ is not injective or G is not isomorphic to ϕ(G)"
]

N_HYP = 3
NEG_Q_INDEX = 3