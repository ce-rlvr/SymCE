import sympy
from sympy import symbols, Poly
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 3:
            domain, polys, f = witness
        elif len(witness) == 2:
            domain = sympy.ZZ
            polys, f = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    if not isinstance(polys, (list, tuple)) or len(polys) < 2:
        return [False, False, False]
        
    try:
        free_symbols = set()
        for p in polys:
            free_symbols.update(sympy.sympify(p).free_symbols)
        if len(free_symbols) > 1:
            return [False, False, False]
        elif len(free_symbols) == 0:
            var = sympy.Symbol('x')
        else:
            var = list(free_symbols)[0]
    except Exception:
        return [False, False, False]

    h1_ok = True
    try:
        poly_list = []
        for p in polys:
            poly_p = sympy.Poly(p, var, domain=domain)
            if poly_p.degree() < 1:
                h1_ok = False
                break
            poly_list.append(poly_p)
                
        if h1_ok:
            for i in range(len(poly_list)):
                for j in range(i+1, len(poly_list)):
                    g_poly = poly_list[i].gcd(poly_list[j])
                    if g_poly.degree() != 0:
                        h1_ok = False
                        break
                    c = g_poly.LC()
                    try:
                        domain.exquo(domain.one, c)
                    except Exception:
                        h1_ok = False
                        break
                if not h1_ok:
                    break
    except Exception:
        h1_ok = False

    h2_ok = False
    try:
        prod = sympy.S.One
        for p in polys:
            prod *= sympy.sympify(p)
        if sympy.simplify(sympy.sympify(f) - prod) == 0:
            h2_ok = True
    except Exception:
        h2_ok = False

    neg_q_ok = False
    try:
        all_comaximal = True
        for i in range(len(polys)):
            for j in range(i+1, len(polys)):
                comax = False
                try:
                    gb = sympy.groebner([polys[i], polys[j]], var, domain=domain)
                    for basis_elem in gb:
                        poly_b = sympy.Poly(basis_elem, var, domain=domain)
                        if poly_b.degree() == 0:
                            c = poly_b.LC()
                            try:
                                domain.exquo(domain.one, c)
                                comax = True
                                break
                            except Exception:
                                pass
                except Exception:
                    pass
                
                if not comax:
                    try:
                        res = sympy.resultant(polys[i], polys[j], var)
                        poly_res = sympy.Poly(res, var, domain=domain)
                        domain.exquo(domain.one, poly_res.LC())
                        comax = True
                    except Exception:
                        pass
                
                if not comax:
                    all_comaximal = False
                    break
            if not all_comaximal:
                break
        neg_q_ok = not all_comaximal
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f_i are pairwise coprime non-constant polynomials",
    "H_2: f is the product of f_i",
    "neg_Q: quotient ring is not isomorphic to the direct product"
]

N_HYP = 2
NEG_Q_INDEX = 2