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

def conditions(witness):
    try:
        p, g, k = witness
    except Exception:
        return [False, False, False]

    # H_1: p is an odd prime
    try:
        h1 = sympy.isprime(p) and (p % 2 != 0)
    except Exception:
        h1 = False

    # H_2: g is a primitive root modulo p
    try:
        h2 = sympy.ntheory.is_primitive_root(g, p)
    except Exception:
        h2 = False

    # ¬Q: (g^k is a primitive root modulo p) is not equivalent to (k is coprime to p-1)
    try:
        # Evaluate P: g^k is a primitive root modulo p
        P = False
        if isinstance(k, (int, sympy.Integer)):
            try:
                val = pow(int(g), int(k), int(p))
                P = sympy.ntheory.is_primitive_root(val, p)
            except Exception:
                P = False
        
        # Evaluate Q: k is coprime to p-1
        try:
            Q = (sympy.gcd(k, p - 1) == 1)
        except Exception:
            Q = False
            
        neg_q = (P != Q)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is an odd prime",
    "H_2: g is a primitive root modulo p",
    "¬Q: (g^k is a primitive root modulo p) is not equivalent to (k is coprime to p-1)"
]

N_HYP = 2
NEG_Q_INDEX = 2