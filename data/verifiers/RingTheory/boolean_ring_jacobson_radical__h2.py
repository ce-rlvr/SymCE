import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for standard algebra objects
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

def conditions(witness) -> list[bool]:
    try:
        R, J = witness
    except Exception:
        return [False, False, False]

    # H_1: R is a Boolean ring
    try:
        elements = list(R.elements)
        zero = R.zero
        add = R.add
        mul = R.mul

        h1 = True
        if zero not in elements:
            h1 = False
        else:
            # Check identity
            for a in elements:
                if add(a, zero) != a or add(zero, a) != a:
                    h1 = False
                    break
            
            # Check inverses
            if h1:
                neg = {}
                for a in elements:
                    has_inv = False
                    for b in elements:
                        if add(a, b) == zero and add(b, a) == zero:
                            has_inv = True
                            neg[a] = b
                            break
                    if not has_inv:
                        h1 = False
                        break
            
            # Check associativity and commutativity of addition
            if h1:
                for a in elements:
                    for b in elements:
                        if add(a, b) != add(b, a):
                            h1 = False
                            break
                        for c in elements:
                            if add(add(a, b), c) != add(a, add(b, c)):
                                h1 = False
                                break
                        if not h1: break
                    if not h1: break
            
            # Check associativity of multiplication
            if h1:
                for a in elements:
                    for b in elements:
                        for c in elements:
                            if mul(mul(a, b), c) != mul(a, mul(b, c)):
                                h1 = False
                                break
                        if not h1: break
                    if not h1: break
            
            # Check distributivity
            if h1:
                for a in elements:
                    for b in elements:
                        for c in elements:
                            if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)):
                                h1 = False
                                break
                            if mul(add(a, b), c) != add(mul(a, c), mul(b, c)):
                                h1 = False
                                break
                        if not h1: break
                    if not h1: break
            
            # Check Boolean property (idempotence)
            if h1:
                for a in elements:
                    if mul(a, a) != a:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # H_2: J is the Jacobson radical of R
    try:
        elements = list(R.elements)
        zero = R.zero
        add = R.add
        mul = R.mul

        neg = {}
        for a in elements:
            for b in elements:
                if add(a, b) == zero and add(b, a) == zero:
                    neg[a] = b
                    break

        expected_J = []
        for x in elements:
            is_in_J = True
            for y in elements:
                xy = mul(x, y)
                is_qr = False
                for z in elements:
                    xyz = mul(xy, z)
                    if xyz in neg:
                        minus_xyz = neg[xyz]
                        term = add(add(xy, z), minus_xyz)
                        if term == zero:
                            is_qr = True
                            break
                if not is_qr:
                    is_in_J = False
                    break
            if is_in_J:
                expected_J.append(x)

        J_list = list(J)
        if len(J_list) != len(expected_J):
            h2 = False
        else:
            h2 = True
            for x in J_list:
                if x not in expected_J:
                    h2 = False
                    break
            if h2:
                for x in expected_J:
                    if x not in J_list:
                        h2 = False
                        break
    except Exception:
        h2 = False

    # ¬Q: J is not {0}
    try:
        J_list = list(J)
        if len(J_list) == 1 and J_list[0] == R.zero:
            neg_q = False
        else:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: J is the Jacobson radical of R",
    "¬Q: J is not {0}"
]

N_HYP = 2
NEG_Q_INDEX = 2