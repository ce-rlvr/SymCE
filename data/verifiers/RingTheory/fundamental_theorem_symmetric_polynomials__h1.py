import sympy
import itertools
from sympy import symbols, eye, zeros, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        f, vars = witness
        vars = list(vars)
    except Exception:
        return [False, False]
        
    # H1: f is a symmetric polynomial in vars
    try:
        f_exp = sympy.expand(f)
        
        def check(expr):
            if not expr.has(*vars):
                return True
            if expr in vars:
                return True
            if isinstance(expr, (sympy.Add, sympy.Mul)):
                return all(check(arg) for arg in expr.args)
            if isinstance(expr, sympy.Pow):
                base, exp = expr.args
                if not exp.has(*vars) and getattr(exp, 'is_Integer', False) and exp >= 0:
                    return check(base)
                return False
            return False
            
        is_poly = check(f_exp)
        
        is_sym = True
        for p in itertools.permutations(vars):
            sub_dict = dict(zip(vars, p))
            diff = sympy.expand(f_exp.subs(sub_dict) - f_exp)
            if diff != 0:
                is_sym = False
                break
                
        h1_ok = bool(is_poly and is_sym)
    except Exception:
        h1_ok = False
        
    # neg_Q: There does NOT exist a unique polynomial g such that f = g(e_1, ..., e_n)
    try:
        if any(not getattr(v, 'is_commutative', True) for v in vars):
            neg_q_ok = True
        elif not vars:
            neg_q_ok = False
        else:
            from sympy.polys.polyfuncs import symmetrize
            res = symmetrize(f, *vars, formal=True)
            g = res[0]
            rem = res[1]
            if rem != 0:
                neg_q_ok = True
            else:
                defs = res[2]
                g_sub = sympy.expand(g.subs(dict(defs)))
                diff = sympy.expand(g_sub - f_exp)
                if diff != 0:
                    neg_q_ok = True
                else:
                    neg_q_ok = False
    except Exception:
        neg_q_ok = True

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a symmetric polynomial in the multivariate polynomial ring",
    "¬Q: There does NOT exist a unique polynomial g such that f = g(e_1, ..., e_n)"
]

N_HYP = 1
NEG_Q_INDEX = 1