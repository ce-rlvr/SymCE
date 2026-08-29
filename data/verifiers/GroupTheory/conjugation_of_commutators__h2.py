import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.named_groups import AbelianGroup
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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
    if isinstance(witness, tuple) and len(witness) == 4:
        G, g, x, y = witness
        try:
            elements = list(G.elements)
            h1 = hasattr(G, 'elements') and (g in elements) and (x in elements) and (y in elements)
        except Exception:
            h1 = False
        
        try:
            comm_xy_1 = x * y * (x**-1) * (y**-1)
            left_1 = g * comm_xy_1 * (g**-1)
            gxg = g * x * (g**-1)
            gyg = g * y * (g**-1)
            right_1 = gxg * gyg * (gxg**-1) * (gyg**-1)
            
            comm_xy_2 = (x**-1) * (y**-1) * x * y
            left_2 = g * comm_xy_2 * (g**-1)
            right_2 = (gxg**-1) * (gyg**-1) * gxg * gyg
            
            neg_q = (left_1 != right_1) or (left_2 != right_2)
        except Exception:
            neg_q = False
        return [h1, neg_q]
    else:
        G = witness
        try:
            h1 = hasattr(G, 'elements')
        except Exception:
            h1 = False

        neg_q = False
        try:
            if h1:
                elements = list(G.elements)
                for g in elements:
                    for x in elements:
                        for y in elements:
                            comm_xy_1 = x * y * (x**-1) * (y**-1)
                            left_1 = g * comm_xy_1 * (g**-1)
                            gxg = g * x * (g**-1)
                            gyg = g * y * (g**-1)
                            right_1 = gxg * gyg * (gxg**-1) * (gyg**-1)
                            
                            comm_xy_2 = (x**-1) * (y**-1) * x * y
                            left_2 = g * comm_xy_2 * (g**-1)
                            right_2 = (gxg**-1) * (gyg**-1) * gxg * gyg
                            
                            if (left_1 != right_1) or (left_2 != right_2):
                                neg_q = True
                                break
                        if neg_q: break
                    if neg_q: break
        except Exception:
            neg_q = False

        return [h1, neg_q]

CONDITION_LABELS = ["H_1: G is a group", "¬Q: Conjugate of commutator is not equal to commutator of conjugates"]
N_HYP = 1
NEG_Q_INDEX = 1