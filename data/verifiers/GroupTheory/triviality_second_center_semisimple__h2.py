import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    try:
        normals = witness.normal_subgroups()
        h1 = True
        w_order = witness.order()
        for N in normals:
            has_comp = False
            n_order = N.order()
            for M in normals:
                m_order = M.order()
                if n_order * m_order == w_order:
                    if N.intersect(M).order() == 1:
                        has_comp = True
                        break
            if not has_comp:
                h1 = False
                break
    except Exception:
        h1 = False

    try:
        try:
            c_order = witness.center().order()
        except Exception:
            gens = witness.generators
            c_order = 0
            for g in witness.elements:
                if all(g * h == h * g for h in gens):
                    c_order += 1
        neg_q = c_order > 1
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a semisimple finite group",
    "¬Q: Z_2(G) is not the trivial subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1