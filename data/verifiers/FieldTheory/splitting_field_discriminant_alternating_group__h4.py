import sympy
from sympy import Poly, Rational
from sympy.abc import x
import math

S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    h3 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            f_expr = witness.get('f', witness.get('f(x)', None))
            D_val = witness.get('D', None)
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                f_expr, D_val = witness
            elif len(witness) >= 4:
                _, f_expr, _, D_val = witness[:4]
            else:
                f_expr, D_val = witness[0], witness[-1]
        else:
            f_expr = witness
            D_val = 1
            
        if hasattr(f_expr, "free_symbols") and f_expr.free_symbols:
            var = list(f_expr.free_symbols)[0]
        else:
            var = x
            
        f = Poly(f_expr, var)
        
        h1 = True
        h2 = bool(f.degree() >= 1 and f.is_squarefree)
        h3 = True
        
        disc = f.discriminant()
        
        def is_sq(val):
            try:
                v = Rational(val)
                if v < 0:
                    return False
                return (math.isqrt(v.p)**2 == v.p) and (math.isqrt(v.q)**2 == v.q)
            except Exception:
                return False
                
        galois_in_An = is_sq(disc)
        D_is_square = is_sq(D_val)
        
        neg_q = bool(galois_in_An != D_is_square)
        
    except Exception:
        pass
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = ['H_1: F is a field', 'H_2: f is separable', 'H_3: E is splitting field', 'not Q: Gal not in An']
N_HYP = 3
NEG_Q_INDEX = 3