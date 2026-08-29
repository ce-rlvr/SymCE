import math
import sympy
from sympy import eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_solution(a, b, m, x):
    try:
        diff = a * x - b
        
        # Check for exact zero
        if diff == 0:
            return True
        try:
            if sympy.simplify(diff) == 0:
                return True
        except Exception:
            pass
            
        if m == 0:
            return False
        try:
            if sympy.simplify(m) == 0:
                return False
        except Exception:
            pass
            
        # Handle matrices
        if isinstance(m, sympy.MatrixBase) or isinstance(diff, sympy.MatrixBase):
            if isinstance(m, sympy.MatrixBase):
                K = m.LUsolve(diff)
                for k in K:
                    k_simp = sympy.simplify(k)
                    if k_simp.is_integer:
                        continue
                    if sympy.re(k_simp).is_integer and sympy.im(k_simp).is_integer:
                        continue
                    return False
                return True
            else:
                K = diff / m
                for k in K:
                    k_simp = sympy.simplify(k)
                    if k_simp.is_integer:
                        continue
                    if sympy.re(k_simp).is_integer and sympy.im(k_simp).is_integer:
                        continue
                    return False
                return True
    except Exception:
        pass

    try:
        diff = a * x - b
        
        # For Python built-in integers
        if isinstance(diff, int) and isinstance(m, int):
            return diff % m == 0
            
        q = diff / m
        
        # For Python built-in floats and complex numbers
        if isinstance(q, complex):
            return float(q.real).is_integer() and float(q.imag).is_integer()
        if isinstance(q, float):
            return q.is_integer()
            
        # For sympy types
        q_simp = sympy.simplify(q)
        if q_simp.is_integer:
            return True
        if sympy.re(q_simp).is_integer and sympy.im(q_simp).is_integer:
            return True
            
        try:
            if float(q_simp).is_integer():
                return True
        except Exception:
            pass
            
        try:
            if complex(q_simp).real.is_integer() and complex(q_simp).imag.is_integer():
                return True
        except Exception:
            pass
            
    except Exception:
        pass

    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness['a']
            b = witness['b']
            m = witness['m']
            x = witness['x']
        else:
            a, b, m, x = witness
    except Exception:
        return [False, False]
        
    # H_1: x is an integer
    h1 = False
    try:
        if isinstance(x, int):
            h1 = True
        elif hasattr(x, 'is_integer') and x.is_integer:
            h1 = True
        elif isinstance(x, float) and x.is_integer():
            h1 = True
        else:
            h1_simp = sympy.simplify(x).is_integer
            if h1_simp is True:
                h1 = True
    except Exception:
        h1 = False

    # neg_Q: x is a solution to ax \equiv b (mod m) is NOT equivalent to x is a solution to ax \equiv b (mod |m|)
    neg_q = False
    try:
        sol_m = is_solution(a, b, m, x)
        
        try:
            abs_m = abs(m)
        except Exception:
            abs_m = sympy.Abs(m)
            
        sol_abs_m = is_solution(a, b, abs_m, x)
        
        neg_q = (sol_m != sol_abs_m)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: x is an integer",
    "¬Q: Congruence modulo m is not equivalent to congruence modulo |m|"
]

N_HYP = 1
NEG_Q_INDEX = 1