import sympy
from sympy import Poly, roots, sympify, QQ, minpoly, degree
from sympy.abc import x
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def in_field(expr, gens):
    expr = sympify(expr)
    if expr.is_Rational:
        return True
    
    clean_gens = []
    for g in gens:
        g_sym = sympify(g)
        if not g_sym.is_Rational:
            clean_gens.append(g_sym)
            
    unique_gens = []
    for g in clean_gens:
        if g not in unique_gens:
            unique_gens.append(g)
            
    if not unique_gens:
        domain = QQ
    else:
        domain = QQ.algebraic_field(*unique_gens)
        
    try:
        mp = minpoly(expr, x, domain=domain)
        return degree(mp, x) == 1
    except Exception:
        return False

def conditions(witness):
    if isinstance(witness, dict):
        F_gens = witness.get('F', [])
        E_gens = witness.get('E', [])
        K_gens = witness.get('K', [])
        f = witness.get('f', None)
    else:
        try:
            F_gens, E_gens, K_gens, f = witness
        except Exception:
            return [False, False, False, False]

    try:
        h1 = isinstance(F_gens, list)
    except Exception:
        h1 = False
        
    try:
        p = Poly(f, x)
        coeffs = p.coeffs()
        h2 = all(in_field(c, F_gens) for c in coeffs)
    except Exception:
        h2 = False
        
    try:
        rts = roots(f, x)
        if sum(rts.values()) != p.degree():
            h3 = False
        else:
            root_list = list(rts.keys())
            roots_in_K = all(in_field(r, K_gens) for r in root_list)
            F_in_K = all(in_field(g, K_gens) for g in F_gens)
            K_in_F_roots = all(in_field(g, F_gens + root_list) for g in K_gens)
            h3 = roots_in_K and F_in_K and K_in_F_roots
    except Exception:
        h3 = False
        
    try:
        f_in_E = all(in_field(c, E_gens) for c in coeffs)
        E_in_K = all(in_field(g, K_gens) for g in E_gens)
        roots_in_K_E = all(in_field(r, K_gens) for r in root_list)
        K_in_E_roots = all(in_field(g, E_gens + root_list) for g in K_gens)
        
        is_splitting_field_over_E = f_in_E and E_in_K and roots_in_K_E and K_in_E_roots
        neg_q = not is_splitting_field_over_E
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f is a polynomial over F",
    "H_3: K is a splitting field of f over F",
    "not Q: K is not a splitting field of f viewed as a polynomial over E"
]

N_HYP = 3
NEG_Q_INDEX = 3