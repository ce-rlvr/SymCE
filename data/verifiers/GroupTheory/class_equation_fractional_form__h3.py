import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, X = witness
                k_wit = len(X)
            elif len(witness) == 3:
                G, k_wit, X = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
        if h1:
            elements = list(G.generate())
            order = len(elements)
        else:
            elements = []
            order = 0
    except Exception:
        h1 = False
        elements = []
        order = 0

    # H2: k is the number of distinct conjugacy classes of G
    try:
        if h1:
            classes = []
            for x in elements:
                if not any(x in cl for cl in classes):
                    cl = []
                    for g in elements:
                        conj = g * x * ~g
                        if conj not in cl:
                            cl.append(conj)
                    classes.append(cl)
            k_actual = len(classes)
            h2 = (k_wit == k_actual) and (len(X) == k_wit)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: C_G(x_i) is the centralizer of x_i in G
    try:
        if h1:
            h3 = True
            for x in X:
                if not isinstance(x, Permutation) or x not in elements:
                    h3 = False
                    break
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: \sum_{i=1}^k 1/|C_G(x_i)| != 1
    try:
        if h1 and h3:
            total_cl_size = 0
            for x in X:
                cl = []
                for g in elements:
                    conj = g * x * ~g
                    if conj not in cl:
                        cl.append(conj)
                total_cl_size += len(cl)
            # Since 1/|C_G(x_i)| = |Cl(x_i)| / |G|, the sum is total_cl_size / order.
            # The sum != 1 is equivalent to total_cl_size != order.
            neg_q = (total_cl_size != order)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: k is the number of distinct conjugacy classes of G",
    "H_3: C_G(x_i) is the centralizer of x_i in G",
    "¬Q: \\sum_{i=1}^k \\frac{1}{|C_G(x_i)|} \\neq 1"
]

N_HYP = 3
NEG_Q_INDEX = 3