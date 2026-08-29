import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup, AbelianGroup
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: G is a semisimple group",
    "H_2: G is a non-trivial group",
    "¬Q: The order of G is not an integer multiple of 60"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    def get_order(G):
        if hasattr(G, 'order'):
            ord_G = G.order
            if callable(ord_G):
                return ord_G()
            return ord_G
        return None

    # H_1: G is a semisimple group (has no non-trivial abelian normal subgroups)
    h1 = False
    try:
        if hasattr(witness, 'is_semisimple'):
            is_semi = witness.is_semisimple
            if callable(is_semi):
                is_semi = is_semi()
            h1 = bool(is_semi)
        elif hasattr(witness, 'normal_subgroups'):
            h1 = True
            for N in witness.normal_subgroups():
                n_order = get_order(N)
                if n_order is not None and n_order > 1:
                    is_ab = N.is_abelian
                    if callable(is_ab):
                        is_ab = is_ab()
                    if is_ab:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # H_2: G is a non-trivial group
    h2 = False
    try:
        ord_G = get_order(witness)
        if ord_G is not None and ord_G > 1:
            h2 = True
    except Exception:
        h2 = False

    # ¬Q: The order of G is not an integer multiple of 60
    neg_q = False
    try:
        ord_G = get_order(witness)
        if ord_G is not None:
            if ord_G == sympy.oo:
                neg_q = True
            else:
                if ord_G % 60 != 0:
                    neg_q = True
        else:
            neg_q = True
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]