import sympy
import sympy.abc
import sympy.polys
import math
import itertools
import functools

# Top-level setup
ZZ = sympy.ZZ
QQ = sympy.QQ
x = sympy.abc.x

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "H_2: d is a submultiplicative Euclidean function on R",
    "H_3: x is a non-zero non-unit in R",
    "¬Q: x is not an irreducible element in R"
]

N_HYP = 3
NEG_Q_INDEX = 3

def is_euclidean_domain(R):
    if R == sympy.ZZ:
        return True
    if hasattr(R, 'is_PID') and R.is_PID:
        return True
    if hasattr(R, 'domain') and hasattr(R, 'symbols'):
        if R.domain.is_Field and len(R.symbols) == 1:
            return True
    return False

def is_submultiplicative_euclidean_function(R, d):
    if R == sympy.ZZ:
        sample = [sympy.Integer(i) for i in range(-5, 6)]
        zero = sympy.Integer(0)
        
        # Check mapping to non-negative values
        for a in sample:
            if a != zero:
                try:
                    val = d(a)
                    if not isinstance(val, (int, sympy.Integer, float, sympy.Float)) or val < 0:
                        return False
                except Exception:
                    return False
                    
        # Check submultiplicativity: d(ab) <= d(a)d(b)
        for a in sample:
            for b in sample:
                if a != zero and b != zero:
                    try:
                        if d(a*b) > d(a) * d(b):
                            return False
                    except Exception:
                        return False
                        
        # Check Euclidean property: a = bq + r with r = 0 or d(r) < d(b)
        for a in sample:
            for b in sample:
                if b != zero:
                    found = False
                    for q in range(-15, 16):
                        r = a - b*q
                        if r == zero or (r != zero and d(r) < d(b)):
                            found = True
                            break
                    if not found:
                        return False
        return True
        
    elif hasattr(R, 'domain') and hasattr(R, 'symbols') and R.domain.is_Field and len(R.symbols) == 1:
        x_sym = R.symbols[0]
        sample_expr = [sympy.Integer(0), sympy.Integer(1), x_sym, x_sym**2 + 1, 2*x_sym - 3, -x_sym + 2]
        sample = []
        for expr in sample_expr:
            try:
                sample.append(R(expr))
            except Exception:
                sample.append(expr)
        zero = R.zero if hasattr(R, 'zero') else sympy.Integer(0)
        
        for a in sample:
            if a != zero:
                try:
                    val = d(a)
                    if not isinstance(val, (int, sympy.Integer, float, sympy.Float)) or val < 0:
                        return False
                except Exception:
                    return False
                    
        for a in sample:
            for b in sample:
                if a != zero and b != zero:
                    try:
                        if d(a*b) > d(a) * d(b):
                            return False
                    except Exception:
                        return False
                        
        for a in sample:
            for b in sample:
                if b != zero:
                    found = False
                    try:
                        q, r = R.div(a, b)
                        if r == zero or d(r) < d(b):
                            found = True
                    except Exception:
                        pass
                    if not found:
                        return False
        return True
        
    return False

def is_nonzero_nonunit(R, x):
    if R == sympy.ZZ:
        try:
            x_val = sympy.Integer(x)
            if x_val == 0:
                return False
            if abs(x_val) == 1:
                return False
            return True
        except Exception:
            return False
    elif hasattr(R, 'domain') and hasattr(R, 'symbols') and R.domain.is_Field and len(R.symbols) == 1:
        try:
            if x == R.zero or x == 0:
                return False
            
            deg = None
            if hasattr(x, 'degree') and callable(x.degree):
                try:
                    deg = x.degree()
                except Exception:
                    pass
            
            if deg is None:
                deg = sympy.degree(x, R.symbols[0])
                
            if deg <= 0:
                return False
            return True
        except Exception:
            return False
    return False

def is_irreducible(R, x):
    if R == sympy.ZZ:
        try:
            x_val = sympy.Integer(x)
            return sympy.isprime(abs(x_val))
        except Exception:
            return False
    elif hasattr(R, 'domain') and hasattr(R, 'symbols') and R.domain.is_Field and len(R.symbols) == 1:
        try:
            if hasattr(R, 'is_irreducible'):
                return R.is_irreducible(x)
            from sympy import factor
            f = factor(x)
            if f.is_Mul:
                non_const = 0
                for arg in f.args:
                    if arg.has(*R.symbols):
                        deg = sympy.degree(arg, R.symbols[0])
                        if deg > 0:
                            non_const += 1
                return non_const == 1
            return True
        except Exception:
            return False
    return False

def conditions(witness):
    if isinstance(witness, (tuple, list)) and len(witness) == 3:
        R, d, x_val = witness
    else:
        R = sympy.ZZ
        d = abs
        x_val = witness

    try:
        h1 = is_euclidean_domain(R)
    except Exception:
        h1 = False

    try:
        h2 = is_submultiplicative_euclidean_function(R, d)
    except Exception:
        h2 = False

    try:
        h3 = is_nonzero_nonunit(R, x_val)
    except Exception:
        h3 = False

    try:
        neg_q = not is_irreducible(R, x_val)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]