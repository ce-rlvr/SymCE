import sympy
from sympy import Poly, degree, factor_list, expand, rem, sympify, Expr
from sympy.polys.polytools import is_irreducible, sqf_list
from sympy.polys.rootoftools import RootOf
from sympy.polys.numberfields import primitive_element
from sympy.abc import x
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def get_f_x(witness):
    try:
        witness = sympify(witness)
    except Exception:
        pass
    if isinstance(witness, Poly):
        return witness.as_expr(), witness.gen
    elif isinstance(witness, Expr):
        free = witness.free_symbols
        if len(free) == 1:
            return witness, list(free)[0]
        elif len(free) == 0:
            return witness, x
    return None, None

def get_splitting_field_minpoly(f, x_var):
    n = degree(f, x_var)
    if n <= 0:
        return x_var
    all_roots = []
    for i in range(n):
        try:
            all_roots.append(RootOf(f, i))
        except Exception:
            pass
    if not all_roots:
        return x_var
    unique_roots = list(set(all_roots))
    if all(getattr(r, 'is_rational', False) for r in unique_roots):
        return x_var
    if len(unique_roots) == 1:
        return x_var - unique_roots[0]
    try:
        minpoly_eq = primitive_element(unique_roots, x_var)
        if isinstance(minpoly_eq, tuple):
            return minpoly_eq[0]
        return minpoly_eq
    except Exception:
        return None

def conditions(witness):
    f, x_var = get_f_x(witness)
    if f is None:
        return [False, False, False, False]
        
    try:
        is_sep = all(exp == 1 for fac, exp in sqf_list(f)[1])
        h1_ok = bool(is_irreducible(f) and is_sep)
    except Exception:
        h1_ok = False

    h2_ok = True

    try:
        if degree(f, x_var) > 8:
            h3_ok = False
        elif degree(f, x_var) <= 0:
            h3_ok = True
        else:
            g = get_splitting_field_minpoly(f, x_var)
            if g is None:
                h3_ok = False
            elif g == x_var or degree(g, x_var) <= 1:
                h3_ok = True
            else:
                r = RootOf(g, 0)
                if getattr(r, 'is_rational', False):
                    _, factors = factor_list(g)
                else:
                    _, factors = factor_list(g, extension=r)
                
                roots_polys = []
                h3_ok = True
                for fac, exp in factors:
                    poly_fac = fac.as_poly(x_var)
                    if poly_fac.degree() != 1:
                        h3_ok = False
                        break
                    poly_fac = poly_fac.monic()
                    root_expr = x_var - poly_fac.as_expr()
                    P_i_x = root_expr.subs(r, x_var)
                    roots_polys.append(P_i_x)
                    
                if h3_ok:
                    for i in range(len(roots_polys)):
                        for j in range(i + 1, len(roots_polys)):
                            P_i = roots_polys[i]
                            P_j = roots_polys[j]
                            comp1 = rem(P_i.subs(x_var, P_j), g, x_var)
                            comp2 = rem(P_j.subs(x_var, P_i), g, x_var)
                            if expand(comp1 - comp2) != 0:
                                h3_ok = False
                                break
                        if not h3_ok:
                            break
    except Exception:
        h3_ok = False

    try:
        neg_q = False
        n = degree(f, x_var)
        if 0 < n <= 8:
            for i in range(n):
                r = RootOf(f, i)
                if getattr(r, 'is_rational', False):
                    _, factors = factor_list(f)
                else:
                    _, factors = factor_list(f, extension=r)
                splits_completely = all(fac.as_poly(x_var).degree() == 1 for fac, exp in factors)
                if not splits_completely:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is an irreducible separable polynomial over K",
    "H_2: L is the splitting field of f(x) over K",
    "H_3: The Galois group Gal(L/K) is an abelian group",
    "neg_Q: There exists a root alpha of f(x) such that L is not equal to K(alpha)"
]

N_HYP = 3
NEG_Q_INDEX = 3