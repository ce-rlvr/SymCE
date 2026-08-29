import sympy
from sympy import minpoly, degree, sympify, Poly, I, sqrt, Rational, Integer, pi, E
from sympy.abc import x, y, z
import math
import itertools
import functools

# Top-level setup
# F is implicitly QQ (the rationals) unless specified otherwise.

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: E is an extension field of F",
    "H_3: alpha is an element algebraic over F",
    "not_Q: The degree of the simple extension F(alpha) over F is not equal to the degree of m(x)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            alpha, m_x = witness
        elif isinstance(witness, dict):
            alpha = witness.get('alpha', witness.get('a'))
            m_x = witness.get('m_x', witness.get('m'))
        else:
            return [False, False, False, False]
        
        if alpha is None or m_x is None:
            return [False, False, False, False]
            
        if callable(m_x):
            m_x = m_x(x)
            
        alpha = sympify(alpha)
        m_x = sympify(m_x)
    except Exception:
        return [False, False, False, False]
        
    # H_1: F is a field
    try:
        h1 = True
    except Exception:
        h1 = False
        
    # H_2: E is an extension field of F
    try:
        h2 = True
    except Exception:
        h2 = False
        
    # H_3: alpha in E is an element algebraic over F
    try:
        mp = minpoly(alpha, x)
        h3 = (mp is not None)
    except Exception:
        h3 = False
        
    # not_Q: The degree of the simple extension F(alpha) over F is not equal to the degree of m(x)
    try:
        deg_ext = degree(mp, x)
        if isinstance(m_x, Poly):
            deg_m = m_x.degree()
        else:
            deg_m = degree(m_x, x)
        neg_q = (deg_ext != deg_m)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]