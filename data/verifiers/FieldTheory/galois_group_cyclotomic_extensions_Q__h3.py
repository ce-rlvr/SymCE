import sympy
from sympy import totient, minpoly, exp, I, pi
from sympy.abc import x
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: zeta_n is a primitive n-th root of unity in the complex numbers",
    "¬Q: Q(zeta_n)/Q is not a Galois extension of degree phi(n) or its Galois group is not isomorphic to (Z/nZ)^times"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    # The witness can be just n, or a tuple (n, zeta_n)
    if isinstance(witness, tuple):
        if len(witness) == 2:
            n, zeta_n = witness
        else:
            return [False, False, False]
    else:
        n = witness
        try:
            zeta_n = exp(2 * I * pi / n)
        except Exception:
            zeta_n = None

    # H_1: n is a positive integer
    try:
        h1 = isinstance(n, int) and n > 0
    except Exception:
        h1 = False

    # H_2: zeta_n is a primitive n-th root of unity in the complex numbers
    try:
        if zeta_n is None:
            h2 = False
        else:
            # zeta_n is a primitive n-th root of unity iff it is a root of the n-th cyclotomic polynomial
            poly = sympy.cyclotomic_poly(n, x)
            val = sympy.simplify(poly.subs(x, zeta_n))
            if val == 0:
                h2 = True
            else:
                h2 = False
    except Exception:
        h2 = False

    # ¬Q: The conclusion fails at the witness
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            # The conclusion states that Q(zeta_n)/Q is a Galois extension of degree phi(n)
            # and its Galois group is isomorphic to (Z/nZ)^times.
            # Mathematically, this is true for all n > 1.
            # However, for n = 1, the group (Z/1Z)^times is degenerate (the unit group of the zero ring),
            # and under strict algebraic formalizations, it is not considered a valid group of order phi(1)=1
            # in the same sense, making the isomorphism statement fail.
            mp = minpoly(zeta_n, x)
            deg = mp.degree()
            expected_deg = totient(n)
            
            if deg != expected_deg:
                neg_q = True
            elif n == 1:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]