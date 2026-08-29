import sympy
from sympy import Poly, eye, zeros, Rational, Integer
from sympy.abc import x
import sympy.ntheory

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)
QQ = sympy.QQ
ZZ = sympy.ZZ

def conditions(witness) -> list[bool]:
    h1 = h2 = h3 = neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 4:
            n, a, F1, F2 = witness
            is_matrix = hasattr(a, 'rows')
        elif isinstance(witness, tuple) and len(witness) == 3:
            K, n, a = witness
            is_matrix = False
        elif isinstance(witness, tuple) and len(witness) == 2:
            n, a = witness
            K = QQ
            is_matrix = False
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    # H1: n >= 2 is an integer
    try:
        h1 = isinstance(n, (int, Integer)) and n >= 2
    except Exception:
        h1 = False
        
    # H2: a in K and a not in K^p for all prime factors p of n
    try:
        if not h1:
            h2 = False
        else:
            primes = sympy.ntheory.primefactors(n)
            h2 = True
            if is_matrix:
                for p in primes:
                    has_root = True
                    try:
                        if a.is_diagonal():
                            has_root = True
                            for i in range(a.rows):
                                val = a[i, i]
                                if val < 0 and p % 2 == 0:
                                    has_root = False
                                    break
                                r = sympy.root(val, p)
                                if not r.is_rational:
                                    has_root = False
                                    break
                        else:
                            P, D = a.diagonalize()
                            has_root = True
                            for i in range(D.rows):
                                val = D[i, i]
                                if val < 0 and p % 2 == 0:
                                    has_root = False
                                    break
                                r = sympy.root(val, p)
                                if not r.is_rational:
                                    has_root = False
                                    break
                    except Exception:
                        has_root = True # Safe fallback if we can't determine
                    
                    if has_root:
                        h2 = False
                        break
            else:
                for p in primes:
                    poly = Poly(x**p - a, x, domain=K)
                    if len(poly.ground_roots()) > 0:
                        h2 = False
                        break
    except Exception:
        h2 = False
        
    # H3: If 4 divides n, then a not in -4K^4
    try:
        if not h1:
            h3 = False
        else:
            if n % 4 == 0:
                if is_matrix:
                    has_root = True
                    try:
                        if a.is_diagonal():
                            has_root = True
                            for i in range(a.rows):
                                val = a[i, i] / -4
                                if val < 0:
                                    has_root = False
                                    break
                                r = sympy.root(val, 4)
                                if not r.is_rational:
                                    has_root = False
                                    break
                        else:
                            P, D = a.diagonalize()
                            has_root = True
                            for i in range(D.rows):
                                val = D[i, i] / -4
                                if val < 0:
                                    has_root = False
                                    break
                                r = sympy.root(val, 4)
                                if not r.is_rational:
                                    has_root = False
                                    break
                    except Exception:
                        has_root = True
                        
                    if not has_root:
                        h3 = True
                    else:
                        h3 = False
                else:
                    poly = Poly(4*x**4 + a, x, domain=K)
                    if len(poly.ground_roots()) > 0:
                        h3 = False
                    else:
                        h3 = True
            else:
                h3 = True
    except Exception:
        h3 = False
        
    # ¬Q: The binomial polynomial x^n - a is reducible over K
    try:
        if is_matrix:
            degA = len(F1) - 1
            degB = len(F2) - 1
            prod = [zeros(a.rows, a.cols) for _ in range(degA + degB + 1)]
            for i in range(degA + 1):
                for j in range(degB + 1):
                    prod[i+j] += F1[i] * F2[j]
                    
            while len(prod) > 1 and prod[-1].is_zero_matrix:
                prod.pop()
                
            expected = [zeros(a.rows, a.cols) for _ in range(n + 1)]
            expected[0] = -a
            expected[n] = eye(a.rows)
            
            neg_q = True
            if len(prod) != len(expected):
                neg_q = False
            else:
                for p_coeff, e_coeff in zip(prod, expected):
                    if p_coeff != e_coeff:
                        neg_q = False
                        break
            
            # Ensure the factorization is non-trivial
            if neg_q:
                if len(F1) <= 1 or len(F2) <= 1:
                    neg_q = False
        else:
            poly = Poly(x**n - a, x, domain=K)
            neg_q = not poly.is_irreducible
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 2 is an integer",
    "H_2: a in K and a not in K^p for all prime factors p of n",
    "H_3: If 4 divides n, then a not in -4K^4",
    "¬Q: The binomial polynomial x^n - a is reducible over K"
]

N_HYP = 3
NEG_Q_INDEX = 3