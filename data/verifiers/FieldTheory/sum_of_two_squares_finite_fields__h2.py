import sympy
from sympy import Poly
from sympy.abc import x
from sympy.polys.domains import FF
from sympy.ntheory import factorint
import itertools

CONDITION_LABELS = [
    "H_1: F_q is a finite field",
    "not Q: a is not a sum of two squares in F_q"
]
N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    if isinstance(witness, tuple) and len(witness) == 2:
        q, a = witness
    else:
        q = witness
        a = None

    try:
        q_int = int(q)
        if q_int <= 1:
            h1 = False
        else:
            factors = factorint(q_int)
            h1 = len(factors) == 1
    except Exception:
        h1 = False
        q_int = None

    neg_q = False
    try:
        if h1 and q_int is not None:
            factors = factorint(q_int)
            p = list(factors.keys())[0]
            k = factors[p]
            
            if a is None:
                neg_q = False
            else:
                if q_int <= 1000:
                    if k == 1:
                        squares = set((i**2) % p for i in range(p))
                        sums = set((s1 + s2) % p for s1 in squares for s2 in squares)
                        
                        try:
                            if isinstance(a, (int, sympy.Integer)):
                                a_val = int(a) % p
                            elif isinstance(a, sympy.Rational):
                                a_val = (a.p * pow(a.q, -1, p)) % p
                            else:
                                a_val = int(a) % p
                            neg_q = a_val not in sums
                        except Exception:
                            neg_q = True
                    else:
                        mod_poly = None
                        for coeffs in itertools.product(range(p), repeat=k):
                            poly_expr = x**k + sum(c * x**(k-1-i) for i, c in enumerate(coeffs))
                            poly = Poly(poly_expr, x, domain=FF(p))
                            if poly.is_irreducible:
                                mod_poly = poly
                                break
                        
                        if mod_poly is not None:
                            elements = []
                            for coeffs in itertools.product(range(p), repeat=k):
                                poly_expr = sum(c * x**(k-1-i) for i, c in enumerate(coeffs))
                                elements.append(Poly(poly_expr, x, domain=FF(p)))
                                
                            squares = set()
                            for elem in elements:
                                sq = (elem * elem) % mod_poly
                                coeffs = sq.all_coeffs()
                                coeffs = [int(c) % p for c in coeffs]
                                coeffs = tuple([0]*(k - len(coeffs)) + coeffs)
                                squares.add(coeffs)
                                
                            sums = set()
                            for s1 in squares:
                                for s2 in squares:
                                    s = tuple((c1 + c2) % p for c1, c2 in zip(s1, s2))
                                    sums.add(s)
                                    
                            try:
                                if isinstance(a, (int, sympy.Integer)):
                                    a_val = [0]*k
                                    a_val[-1] = int(a) % p
                                    a_val = tuple(a_val)
                                elif isinstance(a, sympy.Rational):
                                    a_val = [0]*k
                                    a_val[-1] = (a.p * pow(a.q, -1, p)) % p
                                    a_val = tuple(a_val)
                                elif isinstance(a, (tuple, list)):
                                    a_val = [int(c) % p for c in a]
                                    a_val = tuple([0]*(k - len(a_val)) + a_val)
                                else:
                                    poly_a = Poly(a, x, domain=FF(p))
                                    _, rem = poly_a.div(mod_poly)
                                    coeffs = rem.all_coeffs()
                                    coeffs = [int(c) % p for c in coeffs]
                                    a_val = tuple([0]*(k - len(coeffs)) + coeffs)
                                neg_q = a_val not in sums
                            except Exception:
                                neg_q = True
                        else:
                            neg_q = True
                else:
                    try:
                        if k == 1:
                            if isinstance(a, (int, sympy.Integer)):
                                a_val = int(a) % p
                                neg_q = False
                            elif isinstance(a, sympy.Rational):
                                a_val = (a.p * pow(a.q, -1, p)) % p
                                neg_q = False
                            else:
                                a_val = int(a) % p
                                neg_q = False
                        else:
                            if isinstance(a, (int, sympy.Integer)):
                                neg_q = False
                            elif isinstance(a, sympy.Rational):
                                a_val = (a.p * pow(a.q, -1, p)) % p
                                neg_q = False
                            elif isinstance(a, (tuple, list)):
                                a_val = [int(c) % p for c in a]
                                neg_q = False
                            else:
                                poly_a = Poly(a, x, domain=FF(p))
                                neg_q = False
                    except Exception:
                        neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]