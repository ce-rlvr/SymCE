import sympy
from sympy import eye, zeros
from sympy.abc import x, y, z
import math
import itertools
import functools

# Top-level setup
Z2 = sympy.GF(2)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    n = None
    elements = None
    add = None
    mul = None
    zero = None

    try:
        # Parse the witness to extract n and optionally the ring R
        if isinstance(witness, int):
            n = witness
        elif hasattr(witness, 'shape') and len(witness.shape) == 2 and witness.shape[0] == witness.shape[1]:
            n = witness.shape[0]
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                if isinstance(witness[0], int):
                    n = witness[0]
                    R = witness[1]
                elif isinstance(witness[1], int):
                    n = witness[1]
                    R = witness[0]
                else:
                    n = 1
                    R = witness[0]
                
                if hasattr(R, 'elements') and hasattr(R, 'add') and hasattr(R, 'mul') and hasattr(R, 'zero'):
                    elements = R.elements
                    add = R.add
                    mul = R.mul
                    zero = R.zero
            elif len(witness) == 5:
                n, elements, add, mul, zero = witness
            elif len(witness) == 4:
                elements, add, mul, n = witness
                zero = elements[0]
        elif isinstance(witness, dict):
            n = witness.get('n', 1)
            elements = witness.get('elements', None)
            add = witness.get('add', None)
            mul = witness.get('mul', None)
            zero = witness.get('zero', None)
            
        if n is None:
            n = 1
            
        n = int(n)
    except Exception:
        return [False, False]

    # Default to GF(2) if a custom ring was not explicitly provided
    if elements is None or add is None or mul is None or zero is None:
        elements = [0, 1]
        add = lambda a, b: (a + b) % 2
        mul = lambda a, b: (a * b) % 2
        zero = 0

    # H_1: R is a Boolean ring with at least two elements
    try:
        h1 = False
        if len(elements) >= 2:
            is_br = True
            for a in elements:
                if add(a, zero) != a: is_br = False
                if add(zero, a) != a: is_br = False
                if mul(a, a) != a: is_br = False
                has_inv = False
                for b in elements:
                    if add(a, b) == zero and add(b, a) == zero:
                        has_inv = True
                        break
                if not has_inv: is_br = False
            
            if is_br:
                for a in elements:
                    for b in elements:
                        if add(a, b) != add(b, a): is_br = False
                        for c in elements:
                            if add(add(a, b), c) != add(a, add(b, c)): is_br = False
                            if mul(mul(a, b), c) != mul(a, mul(b, c)): is_br = False
                            if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): is_br = False
                            if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): is_br = False
            h1 = is_br
    except Exception:
        h1 = False

    # ¬Q: M_n(R) is a Boolean ring
    try:
        neg_q = False
        if h1:
            if n < 1:
                neg_q = False
            elif n == 1:
                # M_1(R) is isomorphic to R, which is a Boolean ring
                neg_q = True
            else:
                # For n >= 2, we check if M_n(R) is a Boolean ring.
                # We construct the matrix E_{12} which has a non-zero element at (0,1) and 0 elsewhere.
                # Its square is the zero matrix, which does not equal E_{12}, so M_n(R) is not Boolean.
                e = None
                for val in elements:
                    if val != zero:
                        e = val
                        break
                
                if e is not None:
                    A = [[zero for _ in range(n)] for _ in range(n)]
                    A[0][1] = e
                    
                    A2 = [[zero for _ in range(n)] for _ in range(n)]
                    for i in range(n):
                        for j in range(n):
                            s = zero
                            for k in range(n):
                                s = add(s, mul(A[i][k], A[k][j]))
                            A2[i][j] = s
                            
                    is_bool = True
                    for i in range(n):
                        for j in range(n):
                            if A2[i][j] != A[i][j]:
                                is_bool = False
                    neg_q = is_bool
                else:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring with at least two elements",
    "¬Q: M_n(R) is a Boolean ring"
]

N_HYP = 1
NEG_Q_INDEX = 1