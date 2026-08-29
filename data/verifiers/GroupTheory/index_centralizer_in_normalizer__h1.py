import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import sympy.ntheory
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, x = witness
                n_provided = False
            elif len(witness) == 3:
                G, x, n = witness
                n_provided = True
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: x is an element of G
    try:
        if hasattr(G, 'generate'):
            elements = list(G.generate())
        elif hasattr(G, 'elements'):
            elements = list(G.elements)
        else:
            elements = list(G)
        h1_ok = x in elements
    except Exception:
        h1_ok = False

    # H_2: x has finite order n
    try:
        actual_n = -1
        if hasattr(x, 'order'):
            if callable(x.order):
                actual_n = x.order()
            else:
                actual_n = x.order
        else:
            curr = x
            for i in range(1, 10000):
                is_id = False
                if hasattr(curr, 'is_Identity') and curr.is_Identity:
                    is_id = True
                elif hasattr(curr, 'shape') and len(curr.shape) == 2 and curr.shape[0] == curr.shape[1]:
                    if curr == sympy.eye(curr.shape[0]):
                        is_id = True
                if is_id:
                    actual_n = i
                    break
                curr = curr * x
        
        if n_provided:
            h2_ok = (actual_n == n) and (actual_n > 0)
        else:
            n = actual_n
            h2_ok = (n > 0)
    except Exception:
        h2_ok = False

    # neg_Q: The index of C_G(x) in N_G(x) does not divide phi(n)
    try:
        if not h2_ok:
            neg_q = False
        else:
            H_elements = []
            curr = x
            for _ in range(n):
                H_elements.append(curr)
                curr = curr * x
                
            N_size = 0
            C_size = 0
            for g in elements:
                try:
                    # check centralizer
                    if g * x == x * g:
                        C_size += 1
                        N_size += 1
                    else:
                        # check normalizer
                        try:
                            ginv = g.inv()
                        except Exception:
                            ginv = ~g
                        if (g * x * ginv) in H_elements:
                            N_size += 1
                except Exception:
                    pass
                        
            if C_size == 0:
                neg_q = True
            else:
                if N_size % C_size != 0:
                    neg_q = True
                else:
                    index = N_size // C_size
                    tot = sympy.ntheory.totient(n)
                    neg_q = (tot % index != 0)
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: x is an element of G",
    "H_2: x has finite order n",
    "¬Q: The index of C_G(x) in N_G(x) does not divide phi(n)"
]

N_HYP = 2
NEG_Q_INDEX = 2