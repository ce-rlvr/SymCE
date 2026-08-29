import sympy
from sympy import Poly, Symbol, sympify, Rational
from sympy.polys.domains import GF
from sympy.polys.numberfields import primitive_element
import math
from functools import reduce

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

x, y, z = sympy.symbols('x y z')

def conditions(witness):
    f = None
    n = None
    F = None
    K_degree = None
    
    if isinstance(witness, dict):
        f = witness.get('f')
        n = witness.get('n')
        F = witness.get('F', 'QQ')
        K_degree = witness.get('K_degree')
    elif isinstance(witness, tuple):
        if len(witness) == 2:
            f, n = witness
            F = 'QQ'
        elif len(witness) == 3:
            F, f, n = witness
        elif len(witness) == 4:
            F, K, f, n = witness
            if isinstance(K, (int, sympy.Integer)):
                K_degree = int(K)
    else:
        f = getattr(witness, 'f', None)
        n = getattr(witness, 'n', None)
        F = getattr(witness, 'F', 'QQ')
        K_degree = getattr(witness, 'K_degree', None)
        
    if f is None or n is None:
        return [False, False, False]
        
    try:
        f = sympify(f)
        n = int(n)
    except Exception:
        return [False, False, False]
        
    try:
        h1 = False
        is_finite_field = False
        p = None
        if isinstance(F, str) and F in ('QQ', 'Q', 'Rationals'):
            h1 = True
        elif F == 'QQ' or F == sympy.S.Rationals or F == sympy.QQ:
            h1 = True
        elif hasattr(F, 'is_Field') and F.is_Field:
            h1 = True
            if hasattr(F, 'characteristic') and F.characteristic() > 0:
                is_finite_field = True
                p = int(F.characteristic())
        elif type(F).__name__ == 'GaloisField':
            h1 = True
            is_finite_field = True
            p = int(F.characteristic())
        elif isinstance(F, (int, sympy.Integer)) and F > 1:
            from sympy import isprime
            if isprime(F):
                h1 = True
                is_finite_field = True
                p = int(F)
        elif F is None:
            h1 = True
            F = 'QQ'
    except Exception:
        h1 = False

    try:
        h2 = False
        free_symbols = f.free_symbols
        if not free_symbols:
            actual_K_deg = 1
        else:
            var = sorted(list(free_symbols), key=lambda s: s.name)[0]
            
            if is_finite_field:
                f_poly = Poly(f, var, domain=GF(p))
                factors = f_poly.factor_list()[1]
                degs = [fac[0].degree() for fac in factors]
                def lcm(a, b):
                    return abs(a*b) // math.gcd(a, b) if a and b else 0
                actual_K_deg = reduce(lcm, degs, 1)
            else:
                f_poly = Poly(f, var)
                factors = f_poly.factor_list()[1]
                non_linear = [fac[0] for fac, _ in factors if fac.degree() > 1]
                
                if not non_linear:
                    actual_K_deg = 1
                elif len(non_linear) == 1 and non_linear[0].degree() == 2:
                    actual_K_deg = 2
                elif len(non_linear) == 1 and non_linear[0].degree() == 3:
                    disc = non_linear[0].discriminant()
                    from sympy import sqrt
                    if sqrt(disc).is_rational:
                        actual_K_deg = 3
                    else:
                        actual_K_deg = 6
                elif all(fac.degree() == 2 for fac in non_linear):
                    quad_roots = [fac.all_roots()[0] for fac in non_linear]
                    if not quad_roots:
                        actual_K_deg = 1
                    else:
                        min_poly, _ = primitive_element(quad_roots, var, ex=True)
                        actual_K_deg = min_poly.degree()
                else:
                    roots = f_poly.all_roots()
                    irr_roots = [r for r in roots if not r.is_rational]
                    if not irr_roots:
                        actual_K_deg = 1
                    else:
                        min_poly, _ = primitive_element(irr_roots, var, ex=True)
                        actual_K_deg = min_poly.degree()
                    
        if K_degree is None:
            K_degree = actual_K_deg
            h2 = True
        else:
            h2 = (int(K_degree) == actual_K_deg)
    except Exception:
        h2 = False

    try:
        neg_q = False
        if K_degree is not None and n >= 0:
            K_degree = int(K_degree)
            n_fact = math.factorial(n)
            if K_degree == 0:
                neg_q = False
            else:
                neg_q = (n_fact % K_degree != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: K is a splitting field of f(x) over F",
    "¬Q: The degree of K over F does not divide n!"
]

N_HYP = 2
NEG_Q_INDEX = 2