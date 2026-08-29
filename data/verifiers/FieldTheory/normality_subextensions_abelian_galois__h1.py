import sympy
from sympy import Poly, factor_list, RootOf
from sympy.abc import x

# Top-level setup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
)
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_irreducible(f_expr):
    try:
        f_poly = Poly(f_expr, x, domain='QQ')
        facs = factor_list(f_poly)
        if len(facs[1]) != 1:
            return False
        return facs[1][0][1] == 1
    except Exception:
        return False

def get_automorphisms(f_expr):
    f_poly = Poly(f_expr, x, domain='QQ')
    a = RootOf(f_poly, 0)
    facs = factor_list(f_poly, extension=a)
    auts = []
    for fac, exp in facs[1]:
        fac_poly = Poly(fac, x)
        if fac_poly.degree() == 1:
            c = fac_poly.coeff_monomial(x).subs(a, x)
            d = fac_poly.coeff_monomial(1).subs(a, x)
            c_poly = Poly(c, x, domain='QQ')
            d_poly = Poly(-d, x, domain='QQ')
            if c_poly == Poly(1, x, domain='QQ'):
                g_poly = d_poly.rem(f_poly)
            else:
                c_inv = c_poly.invert(f_poly)
                g_poly = (d_poly * c_inv).rem(f_poly)
            auts.append(g_poly.as_expr())
    return auts

def is_abelian(auts, f_expr):
    f_poly = Poly(f_expr, x, domain='QQ')
    for g1 in auts:
        for g2 in auts:
            comp1 = g1.subs(x, g2)
            comp2 = g2.subs(x, g1)
            rem1 = Poly(comp1, x, domain='QQ').rem(f_poly)
            rem2 = Poly(comp2, x, domain='QQ').rem(f_poly)
            if rem1 != rem2:
                return False
    return True

def is_subfield(M_expr, L_expr):
    L_poly = Poly(L_expr, x, domain='QQ')
    a = RootOf(L_poly, 0)
    facs = factor_list(M_expr, extension=a)
    for fac, exp in facs[1]:
        if Poly(fac, x).degree() == 1:
            return True
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                L_expr, M_expr = witness
            elif len(witness) == 3:
                L_expr, M_expr, K_expr = witness
                if hasattr(K_expr, 'free_symbols') and len(K_expr.free_symbols) == 1:
                    K_expr = K_expr.subs(list(K_expr.free_symbols)[0], x)
                if K_expr != x:
                    return [False, False, False]
            else:
                return [False, False, False]
        else:
            L_expr = witness
            M_expr = witness
            
        if hasattr(L_expr, 'free_symbols') and len(L_expr.free_symbols) == 1:
            L_expr = L_expr.subs(list(L_expr.free_symbols)[0], x)
        if hasattr(M_expr, 'free_symbols') and len(M_expr.free_symbols) == 1:
            M_expr = M_expr.subs(list(M_expr.free_symbols)[0], x)
            
        if not is_irreducible(L_expr) or not is_irreducible(M_expr):
            return [False, False, False]
            
        auts_L = get_automorphisms(L_expr)
        h1 = is_abelian(auts_L, L_expr)
        
        h2 = is_subfield(M_expr, L_expr)
        
        auts_M = get_automorphisms(M_expr)
        M_poly = Poly(M_expr, x, domain='QQ')
        is_gal = (len(auts_M) == M_poly.degree())
        neg_q = not is_gal
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: Gal(L/K) is an abelian group",
    "H_2: M is an intermediate field such that K <= M <= L",
    "¬Q: M/K is not a Galois extension"
]

N_HYP = 2
NEG_Q_INDEX = 2