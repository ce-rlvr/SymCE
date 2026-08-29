import sympy
from sympy import Rational
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup,
    AlternatingGroup,
    DihedralGroup,
    CyclicGroup
)

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

def get_centralizer_size(G, x):
    """Helper to compute the size of the centralizer of x in G."""
    for c in G.conjugacy_classes():
        c_list = list(c)
        if x in c_list:
            return G.order() // len(c_list)
    return None

def conditions(witness) -> list[bool]:
    # Witness can be (G, X) or (G, X, C)
    try:
        if len(witness) == 2:
            G, X = witness
            C = None
        elif len(witness) == 3:
            G, X, C = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: x_1, ..., x_k are representatives of the k distinct conjugacy classes of G
    # (Interpreted as: X is a list of k elements representing distinct conjugacy classes)
    try:
        h2 = True
        if not isinstance(X, (list, tuple)) or len(X) == 0:
            h2 = False
        else:
            for x in X:
                if x not in G:
                    h2 = False
                    break
            if h2:
                class_indices = set()
                classes = G.conjugacy_classes()
                for x in X:
                    found = False
                    for i, c in enumerate(classes):
                        if x in list(c):
                            if i in class_indices:
                                h2 = False
                            class_indices.add(i)
                            found = True
                            break
                    if not found:
                        h2 = False
                        break
    except Exception:
        h2 = False

    # H_3: C_G(x_i) is the centralizer of x_i in G
    try:
        h3 = True
        if C is not None:
            if not isinstance(C, (list, tuple)) or len(C) != len(X):
                h3 = False
            else:
                for x, c_sub in zip(X, C):
                    expected_size = get_centralizer_size(G, x)
                    if expected_size is None or c_sub.order() != expected_size:
                        h3 = False
                        break
    except Exception:
        h3 = False

    # neg_Q: \sum_{i=1}^k \frac{1}{|C_G(x_i)|} != 1
    try:
        sum_val = 0
        for x in X:
            c_size = get_centralizer_size(G, x)
            if c_size is None:
                raise ValueError("x not in any conjugacy class")
            sum_val += Rational(1, c_size)
        neg_q = (sum_val != 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: x_1, ..., x_k are representatives of distinct conjugacy classes of G",
    "H_3: C_G(x_i) is the centralizer of x_i in G",
    "¬Q: \\sum_{i=1}^k \\frac{1}{|C_G(x_i)|} \\neq 1"
]

N_HYP = 3
NEG_Q_INDEX = 3