import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
    "H_1: A and B are groups",
    "H_2: A^Omega is the group of functions from Omega to A under pointwise multiplication",
    "¬Q: The semidirect product with the given action is not isomorphic to the unrestricted wreath product"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            B = witness.get('B')
            Omega = witness.get('Omega')
            act = witness.get('act')
        elif hasattr(witness, 'A') and hasattr(witness, 'B'):
            A = witness.A
            B = witness.B
            Omega = witness.Omega
            act = getattr(witness, 'act', None)
        else:
            if len(witness) == 4:
                A, B, Omega, act = witness
            elif len(witness) == 3:
                A, B, Omega = witness
                act = None
            else:
                return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1 = False
        if (hasattr(A, 'elements') or hasattr(A, 'generators') or hasattr(A, 'is_group') or isinstance(A, (list, tuple, set))) and \
           (hasattr(B, 'elements') or hasattr(B, 'generators') or hasattr(B, 'is_group') or isinstance(B, (list, tuple, set))):
            h1 = True
    except Exception:
        h1 = False

    try:
        h2 = hasattr(Omega, '__iter__') and not isinstance(Omega, str)
    except Exception:
        h2 = False

    neg_q = False
    try:
        if act is None:
            neg_q = True
        else:
            if hasattr(B, 'elements'):
                B_elements = list(B.elements)
            elif hasattr(B, 'generate'):
                B_elements = list(B.generate())
            else:
                B_elements = list(B)
                
            for b1 in B_elements:
                for b2 in B_elements:
                    try:
                        b1_b2_inv = (b1 * b2)**-1
                        b1_inv = b1**-1
                        b2_inv = b2**-1
                    except Exception:
                        try:
                            b1_b2_inv = ~(b1 * b2)
                            b1_inv = ~b1
                            b2_inv = ~b2
                        except Exception:
                            b1_b2_inv = (b1 * b2).inv()
                            b1_inv = b1.inv()
                            b2_inv = b2.inv()
                            
                    for w in Omega:
                        left_side = act(b1_b2_inv, w)
                        right_side = act(b2_inv, act(b1_inv, w))
                        if left_side != right_side:
                            neg_q = True
                            break
                    if neg_q: break
                if neg_q: break
    except Exception:
        neg_q = True

    return [bool(h1), bool(h2), bool(neg_q)]