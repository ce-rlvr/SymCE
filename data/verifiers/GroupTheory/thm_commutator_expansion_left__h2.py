import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    h1 = False
    elements = []
    try:
        if hasattr(witness, 'elements'):
            elements = list(witness.elements)
            h1 = True
        elif isinstance(witness, (list, tuple, set)):
            elements = list(witness)
            h1 = True
            
        if h1 and len(elements) > 0:
            _ = elements[0] * elements[0]
            _ = elements[0]**-1
        elif h1:
            h1 = False
    except Exception:
        h1 = False

    neg_q = False
    try:
        if h1:
            for x in elements:
                for y in elements:
                    for z in elements:
                        xy = x * y
                        lhs = xy * z * (xy**-1) * (z**-1)
                        
                        comm_xz = x * z * (x**-1) * (z**-1)
                        comm_yz = y * z * (y**-1) * (z**-1)
                        
                        rhs = (y**-1) * comm_xz * y * comm_yz
                        
                        if lhs != rhs:
                            neg_q = True
                            break
                    if neg_q:
                        break
                if neg_q:
                    break
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "neg_Q: The commutator identity fails"
]

N_HYP = 1
NEG_Q_INDEX = 1