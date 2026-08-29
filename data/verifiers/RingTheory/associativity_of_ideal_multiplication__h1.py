import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            elements = list(witness['elements'])
            add = witness['add']
            neg = witness['neg']
            mul = witness['mul']
            zero = witness['zero']
            I = list(witness['I'])
            J = list(witness['J'])
            K = list(witness['K'])
        else:
            elements = list(witness.elements)
            add = witness.add
            neg = witness.neg
            mul = witness.mul
            zero = witness.zero
            I = list(witness.I)
            J = list(witness.J)
            K = list(witness.K)

        def is_ideal(S):
            S = set(S)
            if zero not in S: 
                return False
            for x in S:
                if neg(x) not in S: 
                    return False
                for y in S:
                    if add(x, y) not in S: 
                        return False
            for x in S:
                for r in elements:
                    if mul(x, r) not in S: 
                        return False
                    if mul(r, x) not in S: 
                        return False
            return True

        def ideal_mul(A, B):
            products = set()
            for a in A:
                for b in B:
                    products.add(mul(a, b))
            closure = set(products)
            closure.add(zero)
            changed = True
            while changed:
                changed = False
                new_elements = set()
                for x in closure:
                    for y in closure:
                        s = add(x, y)
                        if s not in closure and s not in new_elements:
                            new_elements.add(s)
                if new_elements:
                    closure.update(new_elements)
                    changed = True
            return frozenset(closure)

        h1 = is_ideal(I)
        h2 = is_ideal(J)
        h3 = is_ideal(K)

        IJ = ideal_mul(I, J)
        JK = ideal_mul(J, K)
        I_JK = ideal_mul(I, JK)
        IJ_K = ideal_mul(IJ, K)

        neg_q = (I_JK != IJ_K)

        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: I is a two-sided ideal of R",
    "H_2: J is a two-sided ideal of R",
    "H_3: K is a two-sided ideal of R",
    "¬Q: I(JK) != (IJ)K"
]

N_HYP = 3
NEG_Q_INDEX = 3