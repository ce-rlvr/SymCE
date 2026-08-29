import sympy
import sympy.combinatorics.named_groups
import sympy.matrices
from sympy.abc import x
from sympy.polys.domains import ZZ, QQ, RR, CC, EX, FF

S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1_ok = False
    try:
        if getattr(witness, 'is_division_ring', False):
            h1_ok = True
        elif getattr(witness, 'is_Field', False):
            h1_ok = True
        elif getattr(witness, 'is_field', False):
            h1_ok = True
        elif hasattr(witness, 'poly_ring'):
            Rx = witness.poly_ring(x)
            if getattr(Rx, 'is_PID', False) or getattr(Rx, 'is_principal_ideal_domain', False):
                h1_ok = True
        elif getattr(witness, 'is_PID_poly_ring', False):
            h1_ok = True
    except Exception:
        pass

    neg_q_ok = False
    try:
        if getattr(witness, 'is_Field', False) or getattr(witness, 'is_field', False):
            neg_q_ok = False
        else:
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = ["H_1: The polynomial ring over R is a principal ideal domain", "not_Q: R is not a field"]

N_HYP = 1
NEG_Q_INDEX = 1