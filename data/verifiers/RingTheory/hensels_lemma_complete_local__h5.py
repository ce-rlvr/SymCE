import sympy as sp
from sympy.abc import x
import itertools

# Top-level setup
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

from sympy.matrices import eye, zeros
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        p = int(witness['p'])
        n = int(witness['n'])
        f_expr = witness['f']
        g_0_expr = witness['g_0']
        h_0_expr = witness['h_0']
        
        f = sp.Poly(f_expr, x)
        g_0 = sp.Poly(g_0_expr, x)
        h_0 = sp.Poly(h_0_expr, x)
    except Exception:
        return [False, False, False, False, False]

    # H1: R is a commutative Noetherian ring
    try:
        h1 = isinstance(p, int) and isinstance(n, int) and n >= 1
    except Exception:
        h1 = False

    # H2: R is a local ring with maximal ideal m and residue field k = R/m
    try:
        h2 = sp.isprime(p) and n >= 1
    except Exception:
        h2 = False

    # H3: R is complete with respect to the m-adic topology
    try:
        h3 = h1 and h2
    except Exception:
        h3 = False

    # H4: f(x) is a monic polynomial over R
    try:
        f_coeffs = [int(c) % (p**n) for c in f.all_coeffs()]
        while f_coeffs and f_coeffs[0] == 0:
            f_coeffs.pop(0)
        if not f_coeffs:
            h4 = False
        else:
            h4 = (f_coeffs[0] == 1)
    except Exception:
        h4 = False

    # neg_Q: There do NOT exist monic g, h over R such that f = g h mod p^n,
    # and g = g_0 mod p, h = h_0 mod p.
    try:
        f_coeffs = [int(c) % (p**n) for c in f.all_coeffs()]
        while f_coeffs and f_coeffs[0] == 0:
            f_coeffs.pop(0)
        if not f_coeffs:
            f_coeffs = [0]
        deg_f = len(f_coeffs) - 1
        f_reduced = sp.Poly.from_list(f_coeffs, x)

        g_0_coeffs = [int(c) % p for c in g_0.all_coeffs()]
        while g_0_coeffs and g_0_coeffs[0] == 0:
            g_0_coeffs.pop(0)
        if not g_0_coeffs:
            g_0_coeffs = [0]
        deg_g = len(g_0_coeffs) - 1
        g_0_reduced = sp.Poly.from_list(g_0_coeffs, x)

        h_0_coeffs = [int(c) % p for c in h_0.all_coeffs()]
        while h_0_coeffs and h_0_coeffs[0] == 0:
            h_0_coeffs.pop(0)
        if not h_0_coeffs:
            h_0_coeffs = [0]
        deg_h = len(h_0_coeffs) - 1
        h_0_reduced = sp.Poly.from_list(h_0_coeffs, x)

        if deg_f != deg_g + deg_h:
            neg_q = True
        else:
            def get_coeffs(poly_mod_p, deg):
                coeffs = []
                for i in range(deg):
                    c = int(poly_mod_p.nth(i)) % p
                    lifts = [c + k * p for k in range(p**(n-1))]
                    coeffs.append(lifts)
                return coeffs
                
            g_coeffs_list = get_coeffs(g_0_reduced, deg_g)
            h_coeffs_list = get_coeffs(h_0_reduced, deg_h)
            
            found = False
            for g_c in itertools.product(*g_coeffs_list):
                g_poly = sp.Poly(x**deg_g + sum(c * x**i for i, c in enumerate(g_c)), x)
                for h_c in itertools.product(*h_coeffs_list):
                    h_poly = sp.Poly(x**deg_h + sum(c * x**i for i, c in enumerate(h_c)), x)
                    
                    prod = g_poly * h_poly
                    diff = prod - f_reduced
                    
                    if all(int(c) % (p**n) == 0 for c in diff.all_coeffs()):
                        found = True
                        break
                if found:
                    break
            neg_q = not found
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: R is a local ring with maximal ideal m and residue field k = R/m",
    "H_3: R is complete with respect to the m-adic topology",
    "H_4: f(x) is a monic polynomial over R",
    "¬Q: There do not exist monic polynomials g, h over R such that f = g h and g = g_0, h = h_0 mod m"
]

N_HYP = 4
NEG_Q_INDEX = 4