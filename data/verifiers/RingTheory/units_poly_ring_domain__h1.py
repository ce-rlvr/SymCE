import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import is_square_free

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

ZZ = sympy.S.Integers
QQ = sympy.S.Rationals
RR = sympy.S.Reals
CC = sympy.S.Complexes

def parse_witness(witness):
    if isinstance(witness, bool):
        return witness
    if isinstance(witness, (int, float)):
        return int(witness)
    if hasattr(witness, 'is_Integer') and witness.is_Integer:
        return int(witness)
    if hasattr(witness, 'order') and witness.__class__.__name__ == 'CyclicGroup':
        return int(witness.order())
    if isinstance(witness, str):
        s = witness.strip().replace(' ', '')
        if s.startswith('Z/') and s.endswith('Z'):
            try:
                return int(s[2:-1])
            except ValueError:
                pass
        if s.startswith('Z_'):
            try:
                return int(s[2:])
            except ValueError:
                pass
    return witness

def conditions(witness) -> list[bool]:
    w = parse_witness(witness)
    
    try:
        if isinstance(w, int) and not isinstance(w, bool):
            h1_ok = (w >= 2)
        elif w in (ZZ, QQ, RR, CC):
            h1_ok = True
        elif hasattr(w, 'get_ring'):
            h1_ok = True
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    try:
        if isinstance(w, int) and not isinstance(w, bool):
            neg_q_ok = not is_square_free(w)
        elif w in (ZZ, QQ, RR, CC):
            neg_q_ok = False
        elif hasattr(w, 'get_ring'):
            neg_q_ok = False
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = ["H_1: R is a valid ring", "¬Q: The group of units of the polynomial ring is not equal to the group of units of R"]
N_HYP = 1
NEG_Q_INDEX = 1