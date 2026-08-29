import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import oo, lcm

# Top-level setup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    # H_1: G is an abelian group
    try:
        if hasattr(witness, 'is_abelian'):
            is_ab = witness.is_abelian() if callable(witness.is_abelian) else witness.is_abelian
        else:
            is_ab = False
        h1_ok = bool(is_ab)
    except Exception:
        h1_ok = False

    # H_2: The exponent of G is equal to the order of G
    try:
        if hasattr(witness, 'order'):
            ordG = witness.order() if callable(witness.order) else witness.order
        else:
            ordG = len(list(witness.elements))
            
        if hasattr(witness, 'exponent'):
            exp = witness.exponent() if callable(witness.exponent) else witness.exponent
        else:
            if ordG == oo:
                exp = oo
            else:
                exp = 1
                for g in witness.elements:
                    exp = lcm(exp, g.order())
                
        h2_ok = (exp == ordG)
    except Exception:
        h2_ok = False

    # ¬Q: G is not a cyclic group
    try:
        if hasattr(witness, 'is_cyclic'):
            is_cyc = witness.is_cyclic() if callable(witness.is_cyclic) else witness.is_cyclic
        elif hasattr(witness, 'elements'):
            if hasattr(witness, 'order'):
                ordG_q = witness.order() if callable(witness.order) else witness.order
            else:
                ordG_q = len(list(witness.elements))
                
            if ordG_q == oo:
                is_cyc = False
            else:
                is_cyc = any(g.order() == ordG_q for g in witness.elements)
        else:
            is_cyc = True
        neg_q = not bool(is_cyc)
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "H_2: The exponent of G is equal to the order of G",
    "¬Q: G is not a cyclic group"
]

N_HYP = 2
NEG_Q_INDEX = 2