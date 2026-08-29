import sympy
from sympy import eye, zeros
from sympy.abc import x, y, z
import itertools
import math

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 4:
                n, add_table, mul_table, I = witness
                elements = list(range(n))
                def add(a, b): return add_table[a][b]
                def mul(a, b): return mul_table[a][b]
            elif len(witness) == 2:
                R, I = witness
                if isinstance(R, list):
                    elements = R
                    def add(a, b): return a + b
                    def mul(a, b): return a * b
                else:
                    elements = R.elements
                    add = R.add
                    mul = R.mul
            else:
                return [False, False]
        elif isinstance(witness, dict):
            if 'n' in witness:
                n = witness['n']
                add_table = witness['add_table']
                mul_table = witness['mul_table']
                I = witness['I']
                elements = list(range(n))
                def add(a, b): return add_table[a][b]
                def mul(a, b): return mul_table[a][b]
            else:
                R = witness['R']
                I = witness['I']
                if isinstance(R, list):
                    elements = R
                    def add(a, b): return a + b
                    def mul(a, b): return a * b
                else:
                    elements = R.elements
                    add = R.add
                    mul = R.mul
        else:
            R = witness.R
            I = witness.I
            elements = R.elements
            add = R.add
            mul = R.mul

        I = list(I)

        def contains(lst, item):
            for e in lst:
                try:
                    if e == item:
                        return True
                except Exception:
                    pass
            return False

        # Check closure
        for a in elements:
            for b in elements:
                if not contains(elements, add(a, b)): return [False, False]
                if not contains(elements, mul(a, b)): return [False, False]

        # Find zero
        zeros_list = []
        for c in elements:
            if all(add(c, a) == a and add(a, c) == a for a in elements):
                zeros_list.append(c)
        if not zeros_list:
            return [False, False]
        zero = zeros_list[0]

        # Check inverses
        for a in elements:
            if not any(add(a, b) == zero and add(b, a) == zero for b in elements):
                return [False, False]

        # Check associativity and commutativity
        for a in elements:
            for b in elements:
                if add(a, b) != add(b, a): return [False, False]
                for c in elements:
                    if add(add(a, b), c) != add(a, add(b, c)): return [False, False]
                    if mul(mul(a, b), c) != mul(a, mul(b, c)): return [False, False]
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return [False, False]
                    if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return [False, False]

        # Check if R is von Neumann regular
        is_vnr = True
        for a in elements:
            found = False
            for b in elements:
                if mul(mul(a, b), a) == a:
                    found = True
                    break
            if not found:
                is_vnr = False
                break

        h1 = is_vnr

        # Check if I is an ideal
        is_ideal = True
        if not I:
            is_ideal = False
        else:
            for i_elem in I:
                if not contains(elements, i_elem):
                    is_ideal = False
                    break
            if is_ideal:
                for a in I:
                    for b in I:
                        neg_b = None
                        for c in elements:
                            if add(b, c) == zero and add(c, b) == zero:
                                neg_b = c
                                break
                        if neg_b is None or not contains(I, add(a, neg_b)):
                            is_ideal = False
                for i_elem in I:
                    for r in elements:
                        if not contains(I, mul(i_elem, r)):
                            is_ideal = False
                        if not contains(I, mul(r, i_elem)):
                            is_ideal = False

        # If I is an ideal, R/I is a valid quotient ring and is guaranteed to be von Neumann regular.
        # If I is not an ideal, R/I is not a valid quotient ring, hence the conclusion fails.
        neg_q = not is_ideal

        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a von Neumann regular ring",
    "¬Q: The quotient ring R/I is not a von Neumann regular ring"
]

N_HYP = 1
NEG_Q_INDEX = 1