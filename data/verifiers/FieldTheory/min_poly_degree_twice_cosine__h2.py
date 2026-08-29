import sympy
import sympy.combinatorics.named_groups as named_groups
import sympy.matrices
import sympy.ntheory
from sympy.abc import x

# Top-level setup
S3 = named_groups.SymmetricGroup(3)
S4 = named_groups.SymmetricGroup(4)
A4 = named_groups.AlternatingGroup(4)
D4 = named_groups.DihedralGroup(4)
C4 = named_groups.CyclicGroup(4)
Z2 = named_groups.CyclicGroup(2)
Z3 = named_groups.CyclicGroup(3)
Z4 = named_groups.CyclicGroup(4)
Z6 = named_groups.CyclicGroup(6)
trivial = named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: n is an integer such that n >= 3",
    "¬Q: The degree of the minimal polynomial of 2*cos(2*pi/n) over Q is not phi(n)/2"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        n_sym = sympy.sympify(witness)
        h1 = bool(n_sym.is_integer and n_sym >= 3)
    except Exception:
        h1 = False

    try:
        n_sym = sympy.sympify(witness)
        val = 2 * sympy.cos(2 * sympy.pi / n_sym)
        mp = sympy.minpoly(val, x)
        deg = sympy.degree(mp, x)
        expected = sympy.Rational(sympy.totient(n_sym), 2)
        neg_q = bool(deg != expected)
    except Exception:
        neg_q = False

    return [h1, neg_q]