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
            vals = list(witness.values())
            M_K_s = witness.get('M_K_s', witness.get('MK', vals[0] if len(vals) > 0 else None))
            M_L_s = witness.get('M_L_s', witness.get('ML', vals[1] if len(vals) > 1 else None))
            L_K_s = witness.get('L_K_s', witness.get('LK', vals[2] if len(vals) > 2 else None))
        elif hasattr(witness, 'M_K_s'):
            M_K_s = witness.M_K_s
            M_L_s = witness.M_L_s
            L_K_s = witness.L_K_s
        else:
            M_K_s, M_L_s, L_K_s = witness
            
        neg_Q = bool(M_K_s != M_L_s * L_K_s)
    except Exception:
        neg_Q = False
        
    return [neg_Q]

CONDITION_LABELS = ["not Q: M_K_s != M_L_s * L_K_s"]

N_HYP = 0
NEG_Q_INDEX = 0