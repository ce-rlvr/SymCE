import sympy as sp
from sympy import gcd, simplify, nsimplify, fraction, lcm, Dummy, S, Poly, solve
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import z3
import math
import itertools
import functools

# Top-level setup for standard algebra objects
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def check_system(coeffs, x_sym, y_sym):
    if all(c == 0 for c in coeffs):
        return True
        
    sols = solve(coeffs, (x_sym, y_sym), dict=True)
    if not sols:
        return False
    sol = sols[0]
    
    is_unique = True
    for var in (x_sym, y_sym):
        if var in sol:
            if sol[var].free_symbols:
                is_unique = False
                break
            
    if is_unique:
        for var in (x_sym, y_sym):
            if var in sol:
                try:
                    val = nsimplify(sol[var], rational=True)
                    if not val.is_Integer:
                        return False
                except Exception:
                    return False
        return True
        
    for c in coeffs:
        if c != 0:
            try:
                expr = nsimplify(c, rational=True)
                denoms = [fraction(val)[1] for val in expr.as_coefficients_dict().values()]
                l = 1
                for d in denoms:
                    l = lcm(l, d)
                expr_int = simplify(expr * l)
                coeffs_dict = expr_int.as_coefficients_dict()
                a = coeffs_dict.get(x_sym, 0)
                b = coeffs_dict.get(y_sym, 0)
                const = coeffs_dict.get(1, 0)
                
                if a == 0 and b == 0:
                    continue
                    
                if S(a).is_Integer and S(b).is_Integer and S(const).is_Integer:
                    g = gcd(a, b)
                    if (const % g) == 0:
                        return True
                    else:
                        return False
            except Exception:
                pass
    return False

def has_integer_solution(a, b):
    try:
        g = gcd(a, b)
    except Exception:
        return False
        
    if g == 0:
        return True
        
    x_sym = Dummy('x')
    y_sym = Dummy('y')
    
    try:
        a_norm = simplify(a / g)
        b_norm = simplify(b / g)
    except Exception:
        a_norm = a / g
        b_norm = b / g
        
    expr = a_norm * x_sym + b_norm * y_sym - 1
    free = list(expr.free_symbols - {x_sym, y_sym})
    
    if free:
        try:
            p = Poly(expr, *free)
            coeffs = p.coeffs()
            return check_system(coeffs, x_sym, y_sym)
        except Exception:
            try:
                eqs = []
                for val in [1, 2, 3]:
                    sub_dict = {f: val for f in free}
                    eqs.append(expr.subs(sub_dict))
                return check_system(eqs, x_sym, y_sym)
            except Exception:
                return False
    else:
        return check_system([expr], x_sym, y_sym)

def conditions(witness):
    try:
        a, b = witness
    except Exception:
        return [False, False]
        
    try:
        a_simp = simplify(a)
        b_simp = simplify(b)
        h1 = bool(a_simp != 0 or b_simp != 0)
    except Exception:
        h1 = False
        
    try:
        neg_q = not has_integer_solution(a, b)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are not both zero",
    "¬Q: There do not exist integers x and y such that ax + by = gcd(a, b)"
]

N_HYP = 1
NEG_Q_INDEX = 1