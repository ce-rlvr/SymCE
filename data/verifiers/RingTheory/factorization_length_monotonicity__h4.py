import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.matrices
import sympy.ntheory
from sympy.abc import *

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def is_ufd(a, b):
    if isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer)):
        return True
    if isinstance(a, sympy.Expr) and isinstance(b, sympy.Expr):
        if getattr(a, 'is_Matrix', False) or getattr(b, 'is_Matrix', False):
            return False
        return True
    return False

def is_zero(x):
    if isinstance(x, (int, sympy.Integer)):
        return x == 0
    try:
        return bool(sympy.simplify(x) == 0)
    except Exception:
        return False

def has_rational_coeffs(expr):
    if isinstance(expr, sympy.Expr):
        return any(isinstance(c, sympy.Rational) and not c.is_integer for c in expr.atoms(sympy.Rational))
    return False

def is_unit(x):
    if isinstance(x, (int, sympy.Integer)):
        return abs(x) == 1
    try:
        if hasattr(x, 'is_constant') and x.is_constant():
            if has_rational_coeffs(x):
                return not is_zero(x)
            else:
                return abs(int(x)) == 1
    except Exception:
        pass
    return False

def is_multiple(x, y):
    if is_zero(y):
        return is_zero(x)
    if isinstance(x, (int, sympy.Integer)) and isinstance(y, (int, sympy.Integer)):
        return x % y == 0
    
    try:
        q = sympy.simplify(x / y)
        num, den = sympy.fraction(q)
        if den == 1 or den == -1:
            return True
            
        if has_rational_coeffs(x) or has_rational_coeffs(y):
            if hasattr(den, 'is_constant') and den.is_constant():
                return True
                
        if hasattr(den, 'is_constant') and den.is_constant():
            try:
                return abs(int(den)) == 1
            except Exception:
                pass
    except Exception:
        pass
    return False

def factor_length(x):
    if isinstance(x, (int, sympy.Integer)):
        if x == 0: return 0
        if abs(x) == 1: return 0
        factors = sympy.ntheory.factorint(abs(x))
        return sum(factors.values())
    
    try:
        factors = sympy.factor_list(x)
        c = factors[0]
        c_len = 0
        
        if not has_rational_coeffs(x):
            if isinstance(c, (int, sympy.Integer)) and abs(c) > 1:
                c_len = sum(sympy.ntheory.factorint(abs(c)).values())
            elif hasattr(c, 'is_constant') and c.is_constant() and abs(int(c)) > 1:
                c_len = sum(sympy.ntheory.factorint(abs(int(c))).values())
                
        poly_len = sum(exp for f, exp in factors[1])
        return c_len + poly_len
    except Exception:
        try:
            val = int(x)
            if val == 0: return 0
            if abs(val) == 1: return 0
            factors = sympy.ntheory.factorint(abs(val))
            return sum(factors.values())
        except Exception:
            return 0

def conditions(witness):
    try:
        if len(witness) == 3:
            R, a, b = witness
        elif len(witness) == 2:
            a, b = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        h1 = is_ufd(a, b)
    except Exception:
        h1 = False

    try:
        h2 = not is_zero(a) and not is_unit(a) and not is_zero(b) and not is_unit(b)
    except Exception:
        h2 = False

    try:
        h3 = is_multiple(a, b) and not is_multiple(b, a)
    except Exception:
        h3 = False

    try:
        neg_q = factor_length(a) <= factor_length(b)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: a and b are non-zero, non-unit elements of R",
    "H_3: The principal ideal (a) is strictly contained in the principal ideal (b)",
    "¬Q: L(a) <= L(b)"
]

N_HYP = 3
NEG_Q_INDEX = 3