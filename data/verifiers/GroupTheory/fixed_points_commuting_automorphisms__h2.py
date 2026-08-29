import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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
    "H_1: G is a group",
    "H_2: \\alpha(\\beta(x)) = \\beta(\\alpha(x)) for all x \\in G",
    "H_3: F_\\alpha is the set of all x \\in G such that \\alpha(x) = x",
    "¬Q: There exists y \\in F_\\alpha such that \\beta(y) \\notin F_\\alpha"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if len(witness) == 4:
            G, alpha, beta, F_alpha = witness
        elif len(witness) == 3:
            G, alpha, beta = witness
            F_alpha = None
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: G is a group
    try:
        if isinstance(G, PermutationGroup):
            h1_ok = True
            elements = list(G.elements)
        elif hasattr(G, 'is_group') and getattr(G, 'is_group'):
            h1_ok = True
            elements = list(G.elements) if hasattr(G, 'elements') else list(G)
        elif hasattr(G, 'elements') and hasattr(G, 'identity'):
            h1_ok = True
            elements = list(G.elements)
        else:
            h1_ok = False
            elements = []
    except Exception:
        h1_ok = False
        elements = []

    def apply_fn(f, x):
        if isinstance(f, dict):
            return f[x]
        return f(x)

    # H2: \alpha(\beta(x)) = \beta(\alpha(x)) for all x \in G
    try:
        h2_ok = True
        for x in elements:
            if apply_fn(alpha, apply_fn(beta, x)) != apply_fn(beta, apply_fn(alpha, x)):
                h2_ok = False
                break
    except Exception:
        h2_ok = False

    # H3: F_\alpha is the set of all x \in G such that \alpha(x) = x
    try:
        expected_F_alpha = set()
        for x in elements:
            if apply_fn(alpha, x) == x:
                expected_F_alpha.add(x)
        
        if F_alpha is not None:
            h3_ok = set(F_alpha) == expected_F_alpha
        else:
            h3_ok = True
    except Exception:
        h3_ok = False
        expected_F_alpha = set()

    # ¬Q: There exists y \in F_\alpha such that \beta(y) \notin F_\alpha
    try:
        neg_q = False
        for y in expected_F_alpha:
            by = apply_fn(beta, y)
            if by not in expected_F_alpha:
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, neg_q]