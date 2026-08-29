import sympy as sp
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

# Top-level setup
S3 = sp.combinatorics.named_groups.SymmetricGroup(3)
S4 = sp.combinatorics.named_groups.SymmetricGroup(4)
A4 = sp.combinatorics.named_groups.AlternatingGroup(4)
D4 = sp.combinatorics.named_groups.DihedralGroup(4)
C4 = sp.combinatorics.named_groups.CyclicGroup(4)
V4 = sp.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sp.combinatorics.named_groups.CyclicGroup(2)
Z3 = sp.combinatorics.named_groups.CyclicGroup(3)
Z4 = sp.combinatorics.named_groups.CyclicGroup(4)
Z6 = sp.combinatorics.named_groups.CyclicGroup(6)
trivial = sp.combinatorics.named_groups.CyclicGroup(1)

I2 = sp.matrices.eye(2)
I3 = sp.matrices.eye(3)
O2 = sp.matrices.zeros(2, 2)
O3 = sp.matrices.zeros(3, 3)

def conditions(witness):
    n = witness
    
    try:
        h1 = isinstance(n, (int, sp.Integer)) and not isinstance(n, bool) and n > 0
    except Exception:
        h1 = False
        
    try:
        x = sp.Symbol('x')
        divs = sp.ntheory.divisors(n)
        prod = 1
        for d in divs:
            prod *= sp.polys.cyclotomic_poly(d, x)
        
        q = sp.expand(prod) == x**n - 1
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: The polynomial x^n - 1 is NOT equal to the product of the cyclotomic polynomials Phi_d(x) over all positive integers d that divide n"
]

N_HYP = 1
NEG_Q_INDEX = 1