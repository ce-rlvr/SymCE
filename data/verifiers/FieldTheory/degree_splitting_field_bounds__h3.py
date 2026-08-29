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

# Top-level setup
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
    h1_ok = False
    h2_ok = False
    neg_q_ok = False
    
    try:
        if isinstance(witness, dict):
            h1_ok = bool(witness.get('F_is_field', True))
            n = int(witness.get('n', 1))
            h2_ok = bool(witness.get('f_is_poly', True) and n >= 1)
            k_deg = int(witness.get('K_degree', 1))
        elif isinstance(witness, (list, tuple)) and len(witness) >= 4:
            h1_ok = bool(witness[0])
            h2_ok = bool(witness[1])
            n = int(witness[2])
            k_deg = int(witness[3])
            h2_ok = h2_ok and (n >= 1)
        else:
            h1_ok = bool(getattr(witness, 'F_is_field', True))
            n = int(getattr(witness, 'n', 1))
            h2_ok = bool(getattr(witness, 'f_is_poly', True) and n >= 1)
            k_deg = int(getattr(witness, 'K_degree', 1))
            
        n_fact = math.factorial(n)
        neg_q_ok = (n_fact % k_deg != 0)
    except Exception:
        pass

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f is a polynomial over F of degree n >= 1",
    "not Q: The degree of the field extension K over F does not divide n!"
]

N_HYP = 2
NEG_Q_INDEX = 2