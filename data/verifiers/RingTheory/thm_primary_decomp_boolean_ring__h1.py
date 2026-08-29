import sympy
from sympy.abc import x

# Top-level setup for potential witness expressions
Z = "Z"
QQ_x = "QQ[x]"
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    # 1. Try interpreting as an ideal in Z_m
    try:
        if isinstance(witness, tuple) and len(witness) >= 2:
            ring_name = str(witness[0])
            if ring_name.startswith("Z_"):
                m = int(ring_name[2:])
                n = int(witness[1])
                if m > 0:
                    n = n % m
                    # The ideal (n) in Z_m corresponds to the ideal (g) in Z where g = gcd(n, m)
                    g = sympy.gcd(n, m) if n != 0 else m
                    h1 = (g != 1)
                    
                    factors = sympy.factorint(g)
                    is_primary = (len(factors) == 1) and (g != 1)
                    is_maximal = sympy.isprime(g)
                    
                    neg_q = (is_primary != is_maximal)
                    return [h1, neg_q]
    except Exception:
        pass

    # 2. Try interpreting as an ideal in Z
    try:
        n = None
        if isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
        elif isinstance(witness, str):
            try:
                n = int(witness)
            except ValueError:
                pass
        elif isinstance(witness, tuple):
            if len(witness) == 1:
                n = int(witness[0])
            elif len(witness) >= 2:
                ring_name = str(witness[0])
                if ring_name in ("Z", "ZZ", "IntegerRing", "sympy.ZZ"):
                    n = int(witness[1])
                elif not ring_name.startswith("Z_") and ring_name not in ("QQ[x]", "QQ_x", "sympy.QQ"):
                    n = int(witness[1])
            
        if n is not None:
            n = abs(n)
            h1 = (n != 1)
            if n == 0:
                is_primary = True
                is_maximal = False
            else:
                factors = sympy.factorint(n)
                is_primary = (len(factors) == 1) and (n != 1)
                is_maximal = sympy.isprime(n)
                
            neg_q = (is_primary != is_maximal)
            return [h1, neg_q]
    except Exception:
        pass

    # 3. Try interpreting as an ideal in QQ[x]
    try:
        expr = None
        if isinstance(witness, sympy.Expr):
            expr = witness
        elif isinstance(witness, str):
            expr = sympy.sympify(witness)
        elif isinstance(witness, tuple):
            if len(witness) == 1:
                expr = sympy.sympify(witness[0])
            elif len(witness) >= 2:
                expr = sympy.sympify(witness[1])
                
        if expr is not None:
            if expr == 0:
                h1 = True
                is_primary = True
                is_maximal = False
            else:
                poly = sympy.poly(expr, x, domain='QQ')
                deg = poly.degree()
                h1 = (deg > 0)
                
                factors = sympy.factor_list(poly)
                is_primary = (len(factors[1]) == 1) and (deg > 0)
                is_maximal = (len(factors[1]) == 1) and (factors[1][0][1] == 1) and (deg > 0)
            
            neg_q = (is_primary != is_maximal)
            return [h1, neg_q]
    except Exception:
        pass

    return [False, False]

CONDITION_LABELS = [
    "H_1: Q is a proper ideal of R",
    "¬Q: Q is a primary ideal if and only if Q is a maximal ideal (fails)"
]

N_HYP = 1
NEG_Q_INDEX = 1