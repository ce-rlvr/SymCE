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
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            d = witness.get('degree', witness.get('d'))
            s = witness.get('separable_degree', witness.get('s'))
            i = witness.get('inseparable_degree', witness.get('i'))
        elif hasattr(witness, 'degree') and hasattr(witness, 'separable_degree'):
            d = witness.degree
            s = witness.separable_degree
            i = witness.inseparable_degree
        else:
            d, s, i = witness
            
        neg_q = bool(d != s * i)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = ["not Q: degree of extension is not equal to separable times inseparable degree"]

N_HYP = 0
NEG_Q_INDEX = 0