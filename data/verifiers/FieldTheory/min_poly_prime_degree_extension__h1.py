import sympy as sp
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    try:
        if not (isinstance(witness, tuple) and len(witness) == 2):
            return [False, False, False]
            
        f_expr, g_expr = witness
        
        syms = set()
        if hasattr(f_expr, 'free_symbols'):
            syms |= f_expr.free_symbols
        if hasattr(g_expr, 'free_symbols'):
            syms |= g_expr.free_symbols
            
        if len(syms) == 1:
            var = list(syms)[0]
        elif len(syms) == 0:
            var = sp.Symbol('x')
        else:
            var_sym = sp.Symbol('x')
            if var_sym in syms:
                var = var_sym
            else:
                var = list(syms)[0]
                
        f_poly = sp.Poly(f_expr, var, domain='QQ')
        g_poly = sp.Poly(g_expr, var, domain='QQ')
        
        p = f_poly.degree()
        
        h1 = sp.isprime(p)
        h2 = True
        
        vecs = []
        curr = sp.Poly(1, var, domain='QQ')
        for i in range(p + 1):
            rem = curr.rem(f_poly)
            coeffs = rem.all_coeffs()
            coeffs = coeffs[::-1]
            coeffs = coeffs + [0] * (p - len(coeffs))
            vecs.append(coeffs)
            curr = (curr * g_poly).rem(f_poly)
            
        M = sp.Matrix(vecs).T
        deg_minpoly = M.rank()
        
        neg_q = (deg_minpoly != 1) and (deg_minpoly != p)
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = ['H_1: The degree of E over F is a prime number p', 'H_2: alpha is an element of E', '\u00acQ: The degree of the minimal polynomial of alpha over F is neither 1 nor p']
N_HYP = 2
NEG_Q_INDEX = 2