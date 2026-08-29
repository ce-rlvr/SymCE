import sympy
from sympy import Symbol, Rational
from sympy.polys.numberfields import primitive_element, minpoly
import math

x = Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        n = witness['n']
        a = witness['a']
    except (KeyError, TypeError):
        return [False, False, False, False, False]

    try:
        h1 = isinstance(n, int) and n > 0
    except Exception:
        h1 = False

    try:
        h2 = True 
    except Exception:
        h2 = False

    try:
        h3 = isinstance(a, (int, sympy.Integer, Rational)) or getattr(a, 'is_rational', False)
    except Exception:
        h3 = False

    try:
        h4 = True 
    except Exception:
        h4 = False

    try:
        poly = x**n - a
        roots = sympy.solve(poly, x)
        
        try:
            pe = primitive_element(roots, ex=False)
            if isinstance(pe, tuple):
                pe = pe[0]
            deg = sympy.degree(minpoly(pe))
            neg_q = bool((deg > n) or (deg % n != 0))
        except Exception:
            deg_a = sympy.degree(minpoly(sympy.root(a, n)))
            deg_zeta = sympy.totient(n)
            lcm_deg = (deg_a * deg_zeta) // math.gcd(deg_a, deg_zeta)
            
            if a == 1:
                is_cyclic_unit_group = (n in (1, 2, 4)) or \
                                       (len(sympy.factorint(n)) == 1 and n % 2 != 0) or \
                                       (n % 2 == 0 and len(sympy.factorint(n // 2)) == 1 and (n // 2) % 2 != 0)
                neg_q = not is_cyclic_unit_group
            else:
                neg_q = bool((lcm_deg > n) or (lcm_deg % n != 0))
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: K is a field whose characteristic does not divide n",
    "H_3: a is an element of K",
    "H_4: L is the splitting field of x^n - a over K",
    "¬Q: The Galois group of L/K is not cyclic or its order does not divide n"
]

N_HYP = 4
NEG_Q_INDEX = 4