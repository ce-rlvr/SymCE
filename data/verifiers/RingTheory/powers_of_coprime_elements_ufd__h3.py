import sympy
from sympy import ZZ, QQ, integer_nthroot, factor_list
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: a, b, c are non-zero elements of R",
    "H_3: n >= 2 is an integer",
    "H_4: ab = c^n",
    "¬Q: a and b are not both a unit times an n-th power"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        if len(witness) != 5:
            return [False] * 5
        R, a, b, c, n = witness
    except Exception:
        return [False] * 5
        
    # H1: R is a UFD
    try:
        h1 = False
        if hasattr(R, 'is_UFD') and R.is_UFD:
            h1 = True
        elif R in [ZZ, QQ]:
            h1 = True
    except Exception:
        h1 = False
        
    # H2: a, b, c are non-zero elements of R
    try:
        def in_R(R, val):
            try:
                if val in R:
                    return True
            except Exception:
                pass
            if hasattr(R, 'from_sympy'):
                try:
                    R.from_sympy(sympy.sympify(val))
                    return True
                except Exception:
                    return False
            return False

        def is_nonzero(R, val):
            if val == 0: return False
            if hasattr(R, 'zero') and val == R.zero: return False
            return True

        h2 = in_R(R, a) and in_R(R, b) and in_R(R, c) and is_nonzero(R, a) and is_nonzero(R, b) and is_nonzero(R, c)
    except Exception:
        h2 = False
        
    # H3: n >= 2 is an integer
    try:
        h3 = isinstance(n, int) and n >= 2
    except Exception:
        h3 = False
        
    # H4: ab = c^n
    try:
        h4 = False
        if hasattr(R, 'mul') and hasattr(R, 'pow') and hasattr(R, 'from_sympy'):
            try:
                a_R = R.from_sympy(sympy.sympify(a)) if not a in R else a
                b_R = R.from_sympy(sympy.sympify(b)) if not b in R else b
                c_R = R.from_sympy(sympy.sympify(c)) if not c in R else c
                if R.mul(a_R, b_R) == R.pow(c_R, n):
                    h4 = True
            except Exception:
                pass
        if not h4:
            diff = sympy.sympify(a) * sympy.sympify(b) - sympy.sympify(c) ** n
            h4 = (sympy.simplify(diff) == 0)
    except Exception:
        h4 = False
        
    # neg_Q: not (a = u x^n and b = v y^n)
    try:
        def is_unit_times_nth_power(R, val, n):
            if R == ZZ:
                return integer_nthroot(abs(int(val)), int(n))[1]
            if R == QQ:
                return True
                
            if hasattr(R, 'to_sympy'):
                try:
                    expr = R.to_sympy(val)
                except Exception:
                    expr = sympy.sympify(val)
            else:
                expr = sympy.sympify(val)
                
            if hasattr(R, 'domain'):
                base_ring = R.domain
                if base_ring == QQ:
                    if isinstance(expr, (int, float)) or (hasattr(expr, 'is_Rational') and expr.is_Rational):
                        return True
                elif base_ring == ZZ:
                    if isinstance(expr, int) or (hasattr(expr, 'is_Integer') and expr.is_Integer):
                        return integer_nthroot(abs(int(expr)), int(n))[1]
            else:
                if isinstance(expr, int) or (hasattr(expr, 'is_Integer') and expr.is_Integer):
                    return integer_nthroot(abs(int(expr)), int(n))[1]
                if hasattr(expr, 'is_Rational') and expr.is_Rational:
                    return True
            
            try:
                coeff, factors = factor_list(expr)
            except Exception:
                if hasattr(R, 'domain') and R.domain == QQ:
                    return True
                return integer_nthroot(abs(int(expr)), int(n))[1]
                
            for base, exp in factors:
                if exp % n != 0:
                    return False
                    
            if hasattr(R, 'domain'):
                base_ring = R.domain
                if base_ring == ZZ:
                    return integer_nthroot(abs(int(coeff)), int(n))[1]
                elif base_ring == QQ:
                    return True
            else:
                if hasattr(coeff, 'is_Integer') and coeff.is_Integer:
                    return integer_nthroot(abs(int(coeff)), int(n))[1]
                elif hasattr(coeff, 'is_Rational') and coeff.is_Rational:
                    return True
            return False

        a_is_nth = is_unit_times_nth_power(R, a, n)
        b_is_nth = is_unit_times_nth_power(R, b, n)
        
        neg_q = not (a_is_nth and b_is_nth)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]