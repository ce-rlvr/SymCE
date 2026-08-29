import sympy as sp
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools

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
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            n, P, alpha = witness
        else:
            n = witness['n']
            P = witness['P']
            alpha = witness['alpha']
    except Exception:
        return [False, False, False, False, False]

    try:
        h1 = isinstance(n, int) and n >= 1
    except Exception:
        h1 = False

    try:
        xs = sp.symbols(f'x1:{n+1}')
        h2 = alpha.free_symbols.issubset(set(xs))
    except Exception:
        h2 = False

    try:
        vars_P = P.free_symbols - set(xs)
        T_var = list(vars_P)[0] if len(vars_P) == 1 else sp.Symbol('T')
        P_poly = sp.Poly(P, T_var)
        coeffs = P_poly.coeffs()
        h3 = True
        for c in coeffs:
            if not c.free_symbols.issubset(set(xs)):
                h3 = False
                break
            for i in range(n-1):
                swapped = c.subs({xs[i]: xs[i+1], xs[i+1]: xs[i]})
                if sp.simplify(c - swapped) != 0:
                    h3 = False
                    break
            if not h3:
                break
    except Exception:
        h3 = False

    try:
        is_root = sp.simplify(P.subs(T_var, alpha)) == 0
        orbit = set()
        for p in itertools.permutations(xs):
            sub_dict = dict(zip(xs, p))
            val = sp.simplify(alpha.subs(sub_dict))
            orbit.add(val)
        h4 = is_root and sp.degree(P, T_var) == len(orbit)
    except Exception:
        h4 = False

    try:
        orbit_roots = 0
        for b in orbit:
            if sp.simplify(P.subs(T_var, b)) == 0:
                orbit_roots += 1
        neg_q = orbit_roots < sp.degree(P, T_var)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 1 (x_1, ..., x_n are algebraically independent variables)",
    "H_2: alpha is in K = F(x_1, ..., x_n)",
    "H_3: P is a polynomial in T over E = F(s_1, ..., s_n)",
    "H_4: P is irreducible over E and P(alpha) == 0",
    "¬Q: P does not split completely in K (K is not a normal extension of E)"
]

N_HYP = 4
NEG_Q_INDEX = 4