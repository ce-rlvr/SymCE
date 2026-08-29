import sympy as sp
from sympy.abc import x, y, z, t
from sympy import eye, zeros, Rational, Integer

S3 = sp.combinatorics.SymmetricGroup(3)
S4 = sp.combinatorics.SymmetricGroup(4)
A4 = sp.combinatorics.AlternatingGroup(4)
D4 = sp.combinatorics.DihedralGroup(4)
C4 = sp.combinatorics.CyclicGroup(4)
V4 = sp.combinatorics.AlternatingGroup(4)
Z2 = sp.combinatorics.CyclicGroup(2)
Z3 = sp.combinatorics.CyclicGroup(3)
Z4 = sp.combinatorics.CyclicGroup(4)
Z6 = sp.combinatorics.CyclicGroup(6)
trivial = sp.combinatorics.CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = ['H_1: f is a non-constant monic polynomial', 'H_2: A is a finite-dimensional F-algebra', 'not Q: trace form non-degenerate iff separable is false']

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            f_expr = witness[-1]
        else:
            f_expr = witness
            
        if not isinstance(f_expr, sp.Poly):
            f = sp.Poly(f_expr, x)
        else:
            f = f_expr
            
        if f.domain.is_Ring and not f.domain.is_Field:
            try:
                f = f.set_domain(f.domain.get_field())
            except Exception:
                pass
            
        try:
            h1 = f.degree() >= 1 and f.LC() == 1
        except Exception:
            h1 = False
            
        try:
            h2 = f.domain.is_Field
        except Exception:
            h2 = False
            
        try:
            is_non_degenerate = (f.discriminant() != 0)
        except Exception:
            is_non_degenerate = False
            
        try:
            factors = f.factor_list()[1]
            is_separable = True
            for factor, mult in factors:
                deriv = factor.diff()
                if factor.gcd(deriv).degree() > 0:
                    is_separable = False
                    break
        except Exception:
            is_separable = False
            
        try:
            q = (is_non_degenerate == is_separable)
            neg_q = not q
        except Exception:
            neg_q = False
            
        return [bool(h1), bool(h2), bool(neg_q)]
    
    except Exception:
        return [False, False, False]