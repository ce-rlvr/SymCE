import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
        h1_ok = False
        if hasattr(witness, 'is_nilpotent') and witness.is_nilpotent:
            if hasattr(witness, 'nilpotency_class'):
                if witness.nilpotency_class <= 2:
                    h1_ok = True
    except Exception:
        h1_ok = False

    try:
        neg_q_ok = False
        if hasattr(witness, 'elements'):
            elements = list(witness.elements)
            inv = {g: g**-1 for g in elements}
            
            for x in elements:
                inv_x = inv[x]
                for y in elements:
                    inv_y = inv[y]
                    xy = x * y
                    inv_xy = inv[xy]
                    c_xy = inv_x * inv_y * xy
                    for z in elements:
                        inv_z = inv[z]
                        yz = y * z
                        
                        lhs1 = inv_x * inv[yz] * x * yz
                        c_xz = inv_x * inv_z * x * z
                        rhs1 = c_xy * c_xz
                        
                        if lhs1 != rhs1:
                            neg_q_ok = True
                            break
                        
                        lhs2 = inv_xy * inv_z * xy * z
                        c_yz = inv_y * inv_z * y * z
                        rhs2 = c_xz * c_yz
                        
                        if lhs2 != rhs2:
                            neg_q_ok = True
                            break
                    if neg_q_ok:
                        break
                if neg_q_ok:
                    break
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = ["H_1: G is a nilpotent group of nilpotency class at most 2", "¬Q: comm(x, yz) != comm(x,y)comm(x,z) or comm(xy, z) != comm(x,z)comm(y,z)"]
N_HYP = 1
NEG_Q_INDEX = 1