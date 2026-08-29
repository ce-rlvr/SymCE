import sympy
from sympy import Poly, Expr, factor_list
from sympy.abc import x
from sympy.ntheory import factorint

from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

from sympy.matrices import eye, zeros
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

N_HYP = 3
NEG_Q_INDEX = 3

CONDITION_LABELS = [
    "H_1: R is a UFD",
    "H_2: f is a non-constant polynomial over R",
    "H_3: f is reducible over F",
    "neg_Q: f is not reducible over R"
]

def conditions(witness) -> list[bool]:
    try:
        domain_R = None
        if isinstance(witness, tuple) and len(witness) == 2:
            d_obj, w_obj = witness
            d_str = str(d_obj)
            if 'ZZ' in d_str or 'Integer' in d_str or d_str == 'Z':
                domain_R = 'ZZ'
            elif 'QQ' in d_str or 'Rational' in d_str or d_str == 'Q':
                domain_R = 'QQ'
            witness = w_obj

        if isinstance(witness, Poly):
            poly_f = witness
            f_expr = witness.as_expr()
            if not poly_f.gens:
                return [False, False, False, False]
            var = poly_f.gens[0]
        elif isinstance(witness, Expr):
            f_expr = witness
            free_symbols = f_expr.free_symbols
            if len(free_symbols) != 1:
                return [False, False, False, False]
            var = list(free_symbols)[0]
            poly_f = Poly(f_expr, var)
        else:
            return [False, False, False, False]
            
        coeffs = poly_f.coeffs()
        if domain_R is None:
            if all(c.is_integer for c in coeffs):
                domain_R = 'ZZ'
            elif all(c.is_rational for c in coeffs):
                domain_R = 'QQ'
            else:
                return [False, False, False, False]
        else:
            if domain_R == 'ZZ' and not all(c.is_integer for c in coeffs):
                return [False, False, False, False]
            if domain_R == 'QQ' and not all(c.is_rational for c in coeffs):
                return [False, False, False, False]
            
        h1 = True
        h2 = bool(poly_f.degree() >= 1)
        
        fact_QQ = factor_list(f_expr, var, domain='QQ')
        num_factors_QQ = sum(mult for factor, mult in fact_QQ[1] if factor.as_poly(var).degree() >= 1)
        h3 = bool(num_factors_QQ > 1)
        
        if domain_R == 'ZZ':
            fact_ZZ = factor_list(f_expr, var, domain='ZZ')
            content = abs(fact_ZZ[0])
            if content == 0:
                num_factors_R = 0
            else:
                num_factors_R = sum(factorint(content).values()) + sum(mult for factor, mult in fact_ZZ[1] if factor.as_poly(var).degree() >= 1)
        else:
            num_factors_R = num_factors_QQ
            
        q = bool(num_factors_R > 1)
        neg_q = not q
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]