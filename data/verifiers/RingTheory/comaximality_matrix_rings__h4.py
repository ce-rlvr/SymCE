import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z
from sympy.matrices import eye, zeros
import itertools
import functools
import math

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: I and J are two-sided ideals of R",
    "H_3: I + J = R",
    "¬Q: M_n(I) + M_n(J) != M_n(R)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        # Extract components from the witness
        if isinstance(witness, dict):
            R = witness['R']
            I = witness['I']
            J = witness['J']
            n = witness.get('n', 1)
            add = witness.get('add', lambda a, b: a + b)
            mul = witness.get('mul', lambda a, b: a * b)
            zero = witness.get('zero', None)
        elif isinstance(witness, tuple):
            if len(witness) == 4:
                R, I, J, n = witness
                add = lambda a, b: a + b
                mul = lambda a, b: a * b
                zero = None
            elif len(witness) == 3:
                R, I, J = witness
                n = 1
                add = lambda a, b: a + b
                mul = lambda a, b: a * b
                zero = None
            elif len(witness) == 7:
                R, add, mul, zero, I, J, n = witness
            else:
                return [False, False, False, False]
        else:
            R = witness.R
            I = witness.I
            J = witness.J
            n = getattr(witness, 'n', 1)
            add = getattr(witness, 'add', lambda a, b: a + b)
            mul = getattr(witness, 'mul', lambda a, b: a * b)
            zero = getattr(witness, 'zero', None)
            
        R = list(R)
        I = list(I)
        J = list(J)
        
        # Identify the zero element if not explicitly provided
        if zero is None:
            for z_cand in R:
                if all(add(a, z_cand) == a for a in R) and all(add(z_cand, a) == a for a in R):
                    zero = z_cand
                    break
        
        if zero is None:
            return [False, False, False, False]
            
    except Exception:
        return [False, False, False, False]

    # H_1: R is a ring
    def check_h1():
        if zero not in R: return False
        for a in R:
            if add(a, zero) != a or add(zero, a) != a: return False
            # Check existence of additive inverse
            has_inv = False
            for b in R:
                if add(a, b) == zero and add(b, a) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
            # Check closure, commutativity of addition, and associativity/distributivity
            for b in R:
                if add(a, b) not in R: return False
                if mul(a, b) not in R: return False
                if add(a, b) != add(b, a): return False
                for c in R:
                    if add(add(a, b), c) != add(a, add(b, c)): return False
                    if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                    if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
        return True

    try:
        h1 = check_h1()
    except Exception:
        h1 = False

    # H_2: I and J are two-sided ideals of R
    def check_ideal(S):
        if not S: return False
        for x in S:
            if x not in R: return False
            # Check additive inverse in S
            has_inv = False
            for y in S:
                if add(x, y) == zero and add(y, x) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            # Check closure under addition
            for y in S:
                if add(x, y) not in S: return False
            # Check absorption (two-sided)
            for r in R:
                if mul(r, x) not in S: return False
                if mul(x, r) not in S: return False
        return True

    try:
        h2 = check_ideal(I) and check_ideal(J)
    except Exception:
        h2 = False

    # H_3: I + J = R
    def check_h3():
        sums = []
        for x in I:
            for y in J:
                s = add(x, y)
                if s not in sums:
                    sums.append(s)
        for r in R:
            if r not in sums: return False
        return True

    try:
        h3 = check_h3()
    except Exception:
        h3 = False

    # ¬Q: M_n(I) + M_n(J) != M_n(R)
    # Matrix addition is entrywise. Thus, M_n(I) + M_n(J) = M_n(R) holds if and only if
    # every element in R can be written as a sum of an element in I and an element in J.
    def check_neg_q():
        if n <= 0:
            return False
        sums = []
        for x in I:
            for y in J:
                s = add(x, y)
                if s not in sums:
                    sums.append(s)
        for r in R:
            if r not in sums: return True
        return False

    try:
        neg_q = check_neg_q()
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]