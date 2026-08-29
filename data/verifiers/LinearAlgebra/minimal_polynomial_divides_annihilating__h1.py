import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        A, m, q = witness
    except Exception:
        return [False, False, False]
        
    try:
        free_symbols = m.free_symbols | q.free_symbols
        if len(free_symbols) == 1:
            var = list(free_symbols)[0]
        elif len(free_symbols) == 0:
            var = sympy.Symbol('x')
        else:
            if sympy.Symbol('x') in free_symbols:
                var = sympy.Symbol('x')
            else:
                var = list(free_symbols)[0]
    except Exception:
        return [False, False, False]

    try:
        minpoly = A.minpoly(var)
        h1 = (sympy.simplify(sympy.expand(m - minpoly)) == 0)
    except Exception:
        h1 = False

    try:
        q_poly = sympy.Poly(q, var)
        q_A = sympy.zeros(A.rows, A.cols)
        for power, coeff in enumerate(reversed(q_poly.all_coeffs())):
            q_A += coeff * (A ** power)
        q_A = sympy.simplify(q_A)
        h2 = (q_A.is_zero_matrix == True)
    except Exception:
        h2 = False

    try:
        q_poly = sympy.Poly(q, var)
        F = q_poly.domain
        if hasattr(F, 'get_field'):
            F = F.get_field()
        
        m_poly = sympy.Poly(m, var)
        m_in_F = True
        for c in m_poly.coeffs():
            try:
                F.from_sympy(c)
            except Exception:
                m_in_F = False
                break
                
        if not m_in_F:
            divides = False
        else:
            rem = sympy.rem(q, m, var)
            rem_poly = sympy.Poly(rem, var)
            divides = (rem_poly.is_zero == True)
            
        neg_q = not divides
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: m is the minimal polynomial of A",
    "H_2: q(A) is the zero matrix",
    "¬Q: m does not divide q"
]

N_HYP = 2
NEG_Q_INDEX = 2