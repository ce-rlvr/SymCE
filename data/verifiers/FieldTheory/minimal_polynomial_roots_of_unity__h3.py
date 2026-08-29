import sympy
from sympy import simplify, I, pi, exp, Poly, Eq, cyclotomic_poly, minpoly
from sympy.abc import x
from sympy.ntheory import primefactors
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            zeta_n = witness.get('zeta_n')
            Phi_n = witness.get('Phi_n')
        else:
            n, zeta_n, Phi_n = witness
    except Exception:
        return [False, False, False]

    # H1: n is a positive integer
    try:
        n_val = int(n)
        h1 = bool(n_val == n and n_val > 0)
        n = n_val
    except Exception:
        h1 = False

    # H2: zeta_n is a primitive n-th root of unity
    try:
        if not h1:
            h2 = False
        else:
            z = sympy.sympify(zeta_n)
            is_root = simplify(z**n - 1) == 0
            is_prim = True
            for p in primefactors(n):
                if simplify(z**(n//p) - 1) == 0:
                    is_prim = False
                    break
            h2 = bool(is_root and is_prim)
    except Exception:
        h2 = False

    # neg_Q: Phi_n(x) is NOT the minimal polynomial of zeta_n over Q
    try:
        if isinstance(Phi_n, Poly):
            Phi_n_expr = Phi_n.as_expr()
        elif isinstance(Phi_n, Eq):
            Phi_n_expr = Phi_n.lhs - Phi_n.rhs
        else:
            Phi_n_expr = sympy.sympify(Phi_n)
            
        free_vars = Phi_n_expr.free_symbols
        if len(free_vars) == 1:
            var = list(free_vars)[0]
            Phi_n_expr = Phi_n_expr.subs(var, x)
            
        if h2:
            actual_minpoly = cyclotomic_poly(n, x)
        else:
            z = sympy.sympify(zeta_n)
            actual_minpoly = minpoly(z, x)
            
        diff = sympy.cancel(sympy.expand(Phi_n_expr - actual_minpoly))
        neg_q = bool(diff != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: ζ_n ∈ ℂ is a primitive n-th root of unity",
    "¬Q: Φ_n(x) is not the minimal polynomial of ζ_n over ℚ"
]

N_HYP = 2
NEG_Q_INDEX = 2