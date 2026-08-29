import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Rational, Integer
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
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
        neg_q = False
        if isinstance(witness, int):
            if witness <= 1:
                neg_q = True
            else:
                neg_q = not sympy.isprime(witness)
        elif isinstance(witness, str):
            w = witness.replace(' ', '')
            if w.startswith('Z/') and w.endswith('Z'):
                num_str = w[2:-1]
                if num_str.isdigit():
                    n = int(num_str)
                    neg_q = not sympy.isprime(n) if n > 1 else True
            elif w.startswith('Z') and w[1:].isdigit():
                n = int(w[1:])
                neg_q = not sympy.isprime(n) if n > 1 else True
        elif isinstance(witness, tuple) and len(witness) == 3 and isinstance(witness[0], (list, tuple)):
            elements, add, mul = witness
            n = len(elements)
            zero = None
            for i in range(n):
                if all(add[i][j] == j for j in range(n)):
                    zero = i
                    break
            if zero is not None:
                has_zero_div = False
                for i in range(n):
                    if i == zero: continue
                    for j in range(n):
                        if j == zero: continue
                        if mul[i][j] == zero:
                            has_zero_div = True
                            break
                    if has_zero_div:
                        break
                neg_q = has_zero_div
        else:
            if hasattr(witness, 'is_domain'):
                neg_q = not witness.is_domain
            elif hasattr(witness, 'is_Domain'):
                neg_q = not witness.is_Domain
    except Exception:
        neg_q = False

    return [bool(neg_q)]

CONDITION_LABELS = [
    "not Q: R is not an integral domain"
]

N_HYP = 0
NEG_Q_INDEX = 0