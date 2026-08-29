import sympy as sp
import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

CONDITION_LABELS = [
    "H_1: f is a polynomial over F_q",
    "H_2: The degree of f is n >= 1",
    "¬Q: The factor ring does not have exactly q^n elements"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            q, f = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    h1 = False
    poly_f = None
    try:
        if isinstance(q, (int, sp.Integer)) and q >= 2:
            q = int(q)
            if isinstance(f, list):
                x = sp.Symbol('x')
                poly_f = sp.Poly.from_list(f, gens=x)
                if all(isinstance(c, (int, sp.Integer)) for c in f):
                    h1 = True
            else:
                x_syms = f.free_symbols if hasattr(f, 'free_symbols') else set()
                if len(x_syms) > 1:
                    h1 = False
                else:
                    x = list(x_syms)[0] if len(x_syms) == 1 else sp.Symbol('x')
                    poly_f = sp.Poly(f, x)
                    if all(c.is_integer for c in poly_f.all_coeffs()):
                        h1 = True
    except Exception:
        h1 = False

    h2 = False
    deg = -1
    coeffs_mod = []
    try:
        if h1 and poly_f is not None:
            coeffs = poly_f.all_coeffs()
            coeffs_mod = [int(c) % q for c in coeffs]
            for i, c in enumerate(coeffs_mod):
                if c != 0:
                    deg = len(coeffs_mod) - 1 - i
                    break
            if deg >= 1:
                h2 = True
    except Exception:
        h2 = False

    neg_q = False
    try:
        if h1 and h2:
            lc = 0
            for c in coeffs_mod:
                if c != 0:
                    lc = c
                    break
            if math.gcd(lc, q) != 1:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]