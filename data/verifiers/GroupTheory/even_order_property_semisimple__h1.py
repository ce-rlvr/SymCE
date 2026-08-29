import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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

def conditions(witness):
    def get_order(G):
        if hasattr(G, 'order'):
            if callable(G.order):
                return G.order()
            return G.order
        raise AttributeError("No order attribute")

    def is_abelian(G):
        if hasattr(G, 'is_abelian'):
            if callable(G.is_abelian):
                return G.is_abelian()
            return G.is_abelian
        raise AttributeError("No is_abelian attribute")

    # H1: G is a semisimple group
    try:
        if hasattr(witness, 'is_semisimple'):
            val = witness.is_semisimple() if callable(witness.is_semisimple) else witness.is_semisimple
            h1 = bool(val)
        elif hasattr(witness, 'normal_subgroups'):
            h1 = True
            for N in witness.normal_subgroups():
                if get_order(N) > 1 and is_abelian(N):
                    h1 = False
                    break
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: G is a non-trivial group
    try:
        h2 = bool(get_order(witness) > 1)
    except Exception:
        h2 = False

    # neg_Q: The order of G is NOT an even integer
    try:
        o = get_order(witness)
        if o == sympy.oo or o == float('inf'):
            is_even = False
        else:
            is_even = (int(o) % 2 == 0)
        neg_q = not is_even
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a semisimple group",
    "H_2: G is a non-trivial group",
    "¬Q: The order of G is not an even integer"
]

N_HYP = 2
NEG_Q_INDEX = 2