import sympy
from sympy.matrices import eye, zeros
import math
import itertools
import functools

class Ring:
    def __init__(self, elements, add_table, mul_table, zero):
        self.elements = list(elements)
        self.add_table = add_table
        self.mul_table = mul_table
        self.zero = zero

    def is_commutative(self):
        for a in self.elements:
            for b in self.elements:
                if self.mul_table[a][b] != self.mul_table[b][a]:
                    return False
        return True

    def has_identity(self):
        for e in self.elements:
            is_id = True
            for a in self.elements:
                if self.mul_table[e][a] != a or self.mul_table[a][e] != a:
                    is_id = False
                    break
            if is_id:
                # In an integral domain, 1 != 0
                if e != self.zero:
                    return True
        return False

    def has_no_zero_divisors(self):
        for a in self.elements:
            if a == self.zero: continue
            for b in self.elements:
                if b == self.zero: continue
                if self.mul_table[a][b] == self.zero:
                    return False
        return True

    def is_integral_domain(self):
        return self.is_commutative() and self.has_identity() and self.has_no_zero_divisors()

def make_Zn(n):
    elements = list(range(n))
    add_table = {i: {j: (i + j) % n for j in elements} for i in elements}
    mul_table = {i: {j: (i * j) % n for j in elements} for i in elements}
    return Ring(elements, add_table, mul_table, 0)

# Standard rings for witness construction
Z1 = make_Zn(1)
Z2 = make_Zn(2)
Z3 = make_Zn(3)
Z4 = make_Zn(4)
Z5 = make_Zn(5)
Z6 = make_Zn(6)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, S = witness
        else:
            R = witness
            if hasattr(R, 'elements'):
                S = [x for x in R.elements if x != R.zero]
            elif isinstance(R, str) and R == "2Z":
                S = "2Z_nonzero"
            elif hasattr(R, 'is_ring') and R.is_ring:
                S = "nonzero"
            else:
                S = None
    except Exception:
        return [False, False]

    # H_1: S is the set of all non-zero elements of R
    try:
        if hasattr(R, 'elements'):
            expected_S = [x for x in R.elements if x != R.zero]
            if isinstance(S, (list, tuple, set)):
                h1 = (len(S) == len(expected_S)) and all(x in expected_S for x in S) and all(x in S for x in expected_S)
            else:
                h1 = False
        elif isinstance(R, str) and R == "2Z":
            h1 = isinstance(S, str) and len(S) > 0
        elif hasattr(R, 'is_ring') and R.is_ring:
            h1 = (S == "nonzero")
        else:
            h1 = False
    except Exception:
        h1 = False

    # ¬Q: R is an integral domain if and only if S is closed under multiplication (must fail)
    try:
        if hasattr(R, 'elements'):
            is_idom = R.is_integral_domain()
            
            s_closed = True
            for a in S:
                for b in S:
                    if R.mul_table[a][b] not in S:
                        s_closed = False
                        break
                if not s_closed:
                    break
            
            neg_q = not (is_idom == s_closed)
        elif isinstance(R, str) and R == "2Z":
            # 2Z has no identity, so it is not an integral domain
            is_idom = False
            # The set of non-zero even integers is closed under multiplication
            s_closed = True
            neg_q = not (is_idom == s_closed)
        elif hasattr(R, 'is_ring') and R.is_ring:
            is_idom = R.is_domain
            # For SymPy rings, S is closed iff there are no zero divisors, which is true iff it's a domain
            s_closed = R.is_domain
            neg_q = not (is_idom == s_closed)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: S is the set of all non-zero elements of R",
    "¬Q: The equivalence between R being an integral domain and S being closed under multiplication fails"
]

N_HYP = 1
NEG_Q_INDEX = 1