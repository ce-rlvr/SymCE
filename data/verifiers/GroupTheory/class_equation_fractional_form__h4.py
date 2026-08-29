import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import Rational

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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            k = witness.get('k')
            reps = witness.get('reps')
            if reps is None and k is not None:
                reps = [witness[f'x_{i}'] for i in range(1, int(k) + 1)]
        else:
            G = witness[0]
            k = witness[1]
            if len(witness) == 3 and isinstance(witness[2], (list, tuple, set)):
                reps = list(witness[2])
            else:
                reps = list(witness[2:])
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        elements = list(G.generate())
        h1 = (len(elements) == G.order()) and (G.order() > 0)
    except Exception:
        h1 = False

    # H_2: k is the number of distinct conjugacy classes of G
    try:
        if not h1:
            h2 = False
        else:
            classes = set()
            for x in elements:
                c = frozenset(g * x * ~g for g in elements)
                classes.add(c)
            h2 = (k == len(classes))
    except Exception:
        h2 = False

    # H_3: x_1, ..., x_k are representatives of the k distinct conjugacy classes of G
    try:
        if not h1 or not h2:
            h3 = False
        else:
            if len(reps) != k:
                h3 = False
            else:
                rep_classes = set()
                for x in reps:
                    if x not in elements:
                        raise ValueError("Representative not in group")
                    c = frozenset(g * x * ~g for g in elements)
                    rep_classes.add(c)
                h3 = (rep_classes == classes)
    except Exception:
        h3 = False

    # ¬Q: \sum_{i=1}^k \frac{1}{|C_G(x_i)|} != 1
    try:
        if not h1:
            neg_q = False
        else:
            sum_inv_C = 0
            for x in reps:
                # C_G(x) is the centralizer of x in G
                C_G_x_len = sum(1 for g in elements if g * x == x * g)
                sum_inv_C += Rational(1, C_G_x_len)
            neg_q = (sum_inv_C != 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: k is the number of distinct conjugacy classes of G",
    "H_3: x_1, ..., x_k are representatives of the k distinct conjugacy classes of G",
    "¬Q: sum_{i=1}^k 1/|C_G(x_i)| != 1"
]

N_HYP = 3
NEG_Q_INDEX = 3