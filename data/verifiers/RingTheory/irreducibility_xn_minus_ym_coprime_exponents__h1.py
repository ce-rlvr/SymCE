import sympy as sp
import math

x, y = sp.symbols('x y')

def conditions(witness):
    H1 = False
    H2 = False
    neg_Q = False
    
    try:
        if isinstance(witness, tuple):
            n = witness[0]
            m = witness[1]
        else:
            n = witness.n
            m = witness.m
    except Exception:
        return [False, False, False]
        
    try:
        n_val = int(n)
        m_val = int(m)
        H1 = (n_val == n) and (m_val == m) and (n_val > 0) and (m_val > 0)
    except Exception:
        H1 = False
        
    try:
        H2 = math.gcd(int(n), int(m)) == 1
    except Exception:
        H2 = False
        
    try:
        poly = x**n_val - y**m_val
        
        P = None
        Q = None
        F = None
        if isinstance(witness, tuple):
            if len(witness) >= 4:
                P = witness[-2]
                Q = witness[-1]
            elif len(witness) == 3:
                F = witness[2]
        else:
            P = getattr(witness, 'P', None)
            Q = getattr(witness, 'Q', None)
            F = getattr(witness, 'F', None)
            
        if P is not None and Q is not None:
            if isinstance(P, sp.Poly) and isinstance(Q, sp.Poly):
                prod = P * Q
                poly_obj = sp.Poly(poly, x, y, domain=P.domain)
                if prod == poly_obj:
                    if sum(P.degree_list()) > 0 and sum(Q.degree_list()) > 0:
                        neg_Q = True
            else:
                prod = sp.expand(P * Q)
                if sp.simplify(prod - poly) == 0:
                    if (P.has(x) or P.has(y)) and (Q.has(x) or Q.has(y)):
                        neg_Q = True
        elif F is not None:
            try:
                factors = sp.factor_list(poly, domain=F)
                neg_Q = not (len(factors[1]) == 1 and factors[1][0][1] == 1)
            except Exception:
                if isinstance(F, int) and F > 1:
                    if not sp.isprime(F):
                        neg_Q = True
                elif hasattr(F, 'is_Field'):
                    neg_Q = not F.is_Field
                elif hasattr(F, 'is_domain'):
                    neg_Q = not F.is_domain
                else:
                    neg_Q = True
        else:
            factors = sp.factor_list(poly)
            neg_Q = not (len(factors[1]) == 1 and factors[1][0][1] == 1)
    except Exception:
        pass
        
    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: n and m are positive integers",
    "H_2: The greatest common divisor of n and m is 1",
    "¬Q: The polynomial x^n - y^m is reducible"
]

N_HYP = 2
NEG_Q_INDEX = 2