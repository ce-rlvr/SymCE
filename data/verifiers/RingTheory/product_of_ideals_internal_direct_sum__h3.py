import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2,2)
O3 = sympy.matrices.zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 2:
            a, b = witness
            try:
                a_val = int(a)
                b_val = int(b)
                h1 = True
                h2 = True
                neg_q = (a_val * b_val) != 0
                return [h1, h2, neg_q]
            except (ValueError, TypeError):
                a_expr = sympy.sympify(a)
                b_expr = sympy.sympify(b)
                h1 = True
                h2 = True
                neg_q = sympy.expand(a_expr * b_expr) != 0
                return [h1, h2, neg_q]
        elif len(witness) == 3:
            n, I_gens, J_gens = witness
            n = int(n)
            h1 = n >= 0
            I_gens = [int(x) for x in I_gens]
            J_gens = [int(x) for x in J_gens]
            h2 = True
            neg_q = False
            if h1 and h2:
                for x in I_gens:
                    for y in J_gens:
                        prod = x * y
                        if n > 0:
                            prod = prod % n
                        if prod != 0:
                            neg_q = True
                            break
                    if neg_q:
                        break
            return [h1, h2, neg_q]
    except Exception:
        pass
    return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I and J are ideals of R",
    "¬Q: The product ideal IJ is not the zero ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2