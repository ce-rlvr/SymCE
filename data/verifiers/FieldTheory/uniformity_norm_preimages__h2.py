import sympy
from sympy.ntheory import factorint
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

def is_primepower(n):
    try:
        n = int(n)
        if n <= 1:
            return False
        return len(factorint(n)) == 1
    except Exception:
        return False

def is_nonzero(c, q):
    try:
        c_val = int(c)
        try:
            p = list(factorint(int(q)).keys())[0]
        except Exception:
            p = int(q)
        if p == 0:
            return c_val != 0
        return (c_val % p != 0)
    except Exception:
        try:
            if hasattr(c, 'is_zero'):
                return not c.is_zero
            return bool(c)
        except Exception:
            return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            q = witness.get('q')
            n = witness.get('n')
            c = witness.get('c')
        else:
            q, n, c = witness
    except Exception:
        return [False, False, False]

    # H1: F_q is a finite field with q elements
    h1 = is_primepower(q)

    # H2: c is an arbitrary non-zero element of F_q
    h2 = is_nonzero(c, q)

    # neg_Q: The conclusion fails
    try:
        if not h1:
            neg_q = True
        else:
            n_float = float(n)
            if not (n_float.is_integer() and n_float >= 1):
                neg_q = True
            else:
                n_int = int(n_float)
                
                c_is_zero = not is_nonzero(c, q)
                
                if c_is_zero:
                    actual_count = 1
                else:
                    actual_count = (int(q)**n_int - 1) // (int(q) - 1)
                    
                expected_count = (int(q)**n_int - 1) / (int(q) - 1)
                
                if actual_count == expected_count:
                    neg_q = False
                else:
                    neg_q = True
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: c is an arbitrary non-zero element of F_q",
    "¬Q: The number of elements x in F_{q^n} such that N(x) = c is NOT exactly (q^n - 1)/(q - 1)"
]

N_HYP = 2
NEG_Q_INDEX = 2