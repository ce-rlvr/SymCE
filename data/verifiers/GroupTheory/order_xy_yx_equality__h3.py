import sympy as sp
from sympy.matrices import Matrix, eye, zeros
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
    "H_2: x is an element of G",
    "H_3: the product xy has a finite order n",
    "¬Q: the product yx does not have finite order n"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 3:
            G, x, y = witness
            n_provided = None
        elif len(witness) == 4:
            G, x, y, n_provided = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: G is a group
    is_group = False
    e = None
    try:
        if isinstance(G, PermutationGroup):
            G_list = list(G.elements)
            is_group = True
            for cand in G_list:
                if all(cand * g == g and g * cand == g for g in G_list):
                    e = cand
                    break
        elif isinstance(G, (list, tuple, set)):
            G_list = list(G)
            if 0 < len(G_list) <= 100:
                identities = []
                for cand in G_list:
                    if all(cand * g == g and g * cand == g for g in G_list):
                        identities.append(cand)
                if len(identities) == 1:
                    e = identities[0]
                    closed = True
                    inverses = True
                    for g in G_list:
                        has_inv = False
                        for h in G_list:
                            if g * h not in G_list:
                                closed = False
                            if g * h == e and h * g == e:
                                has_inv = True
                        if not has_inv:
                            inverses = False
                    if closed and inverses:
                        is_group = True
    except Exception:
        pass

    # H2: x is an element of G
    is_x_in_G = False
    try:
        if is_group:
            for g in G_list:
                if x == g:
                    is_x_in_G = True
                    break
    except Exception:
        pass

    # H3: the product xy has a finite order n
    xy_has_finite_order = False
    n = None
    try:
        if is_group and is_x_in_G:
            xy = x * y
            if n_provided is not None:
                n_val = int(n_provided)
                if n_val >= 1:
                    val = xy
                    is_exact = True
                    for k in range(1, n_val):
                        if val == e:
                            is_exact = False
                            break
                        val = val * xy
                    if is_exact and val == e:
                        xy_has_finite_order = True
                        n = n_val
            else:
                val = xy
                for k in range(1, 100):
                    if val == e:
                        xy_has_finite_order = True
                        n = k
                        break
                    val = val * xy
    except Exception:
        pass

    # neg_Q: the product yx does not have finite order n
    yx_not_order_n = False
    if xy_has_finite_order and n is not None:
        try:
            yx = y * x
            val = yx
            is_exact = True
            for k in range(1, n):
                if val == e:
                    is_exact = False
                    break
                val = val * yx
            if not (is_exact and val == e):
                yx_not_order_n = True
        except Exception:
            yx_not_order_n = True

    return [is_group, is_x_in_G, xy_has_finite_order, yx_not_order_n]