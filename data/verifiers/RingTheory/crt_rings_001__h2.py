import itertools

# Top-level setup
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z

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
    try:
        if hasattr(witness, 'elements'):
            elements = list(witness.elements)
            add = witness.add
            mul = witness.mul
            zero = witness.zero
            one = witness.one
            I = list(witness.I)
            J = list(witness.J)
        elif isinstance(witness, dict):
            elements = list(witness['elements'])
            add = witness['add']
            mul = witness['mul']
            zero = witness['zero']
            one = witness['one']
            I = list(witness['I'])
            J = list(witness['J'])
        else:
            elements = list(witness[0])
            add = witness[1]
            mul = witness[2]
            zero = witness[3]
            one = witness[4]
            I = list(witness[5])
            J = list(witness[6])
    except Exception:
        return [False, False, False]

    # H1: R is a ring with identity
    h1 = False
    try:
        if zero in elements and one in elements:
            h1 = True
            for a in elements:
                if add(a, zero) != a or add(zero, a) != a:
                    h1 = False
                    break
                if mul(a, one) != a or mul(one, a) != a:
                    h1 = False
                    break
            
            if h1:
                test_elements = elements[:30]
                for a in test_elements:
                    for b in test_elements:
                        if add(a, b) not in elements: h1 = False
                        if mul(a, b) not in elements: h1 = False
                        if add(a, b) != add(b, a): h1 = False
                        for c in test_elements:
                            if add(add(a, b), c) != add(a, add(b, c)): h1 = False
                            if mul(mul(a, b), c) != mul(a, mul(b, c)): h1 = False
                            if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): h1 = False
                            if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): h1 = False
    except Exception:
        h1 = False

    # H2: I + J = R
    h2 = False
    try:
        sum_IJ = []
        for i in I:
            for j in J:
                s = add(i, j)
                if s not in sum_IJ:
                    sum_IJ.append(s)
        
        h2 = True
        for e in elements:
            if e not in sum_IJ:
                h2 = False
                break
    except Exception:
        h2 = False

    # neg_Q: R/(I \cap J) \cong R/I \times R/J is false
    neg_q = False
    try:
        def is_two_sided_ideal(ideal):
            if zero not in ideal:
                return False
            for a in ideal:
                for b in ideal:
                    if add(a, b) not in ideal:
                        return False
                has_inv = False
                for b in ideal:
                    if add(a, b) == zero:
                        has_inv = True
                        break
                if not has_inv:
                    return False
            for r in elements:
                for a in ideal:
                    if mul(r, a) not in ideal:
                        return False
                    if mul(a, r) not in ideal:
                        return False
            return True

        # The theorem holds universally if I and J are two-sided ideals.
        # The conclusion fails (is not a valid ring isomorphism) if I or J is not a two-sided ideal.
        if not is_two_sided_ideal(I) or not is_two_sided_ideal(J):
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring with identity",
    "H_2: I + J = R",
    "¬Q: R/(I \\cap J) is not isomorphic to R/I \\times R/J"
]

N_HYP = 2
NEG_Q_INDEX = 2