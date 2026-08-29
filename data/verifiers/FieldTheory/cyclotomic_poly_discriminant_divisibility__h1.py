import sympy
from sympy import cyclotomic_poly, discriminant
from sympy.ntheory import totient
from sympy.abc import x
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness expressions
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

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: Phi_n(x) is the n-th cyclotomic polynomial over Q",
    "H_2: Delta(Phi_n) is the discriminant of Phi_n(x)",
    "¬Q: Delta(Phi_n) does not divide n^phi(n) in Z"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    P = None
    D = None
    
    # The witness can be just the integer n, or a tuple (n, Phi_n, Delta)
    if isinstance(witness, tuple) and len(witness) == 3:
        n, P, D = witness
    else:
        n = witness
        try:
            P = cyclotomic_poly(n, x)
            D = discriminant(P, x)
        except Exception:
            pass

    # H_1: Phi_n(x) is the n-th cyclotomic polynomial over Q
    try:
        h1 = (P is not None) and bool(P == cyclotomic_poly(n, x))
    except Exception:
        h1 = False

    # H_2: Delta(Phi_n) is the discriminant of Phi_n(x)
    try:
        h2 = (D is not None) and bool(D == discriminant(P, x))
    except Exception:
        h2 = False

    # ¬Q: Delta(Phi_n) does NOT divide n^phi(n) in Z
    try:
        val_n = int(n)
        val_tot = int(totient(val_n))
        val_D = int(D)
        
        if val_D == 0:
            neg_q = (val_n**val_tot != 0)
        else:
            neg_q = ((val_n**val_tot) % val_D != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]