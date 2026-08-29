import sympy
from sympy.abc import x

CONDITION_LABELS = [
    'H_1: phi is an F-algebra automorphism of the polynomial ring',
    'not Q: phi is not of the form ax + b'
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1 = False
    neg_q = False
    try:
        m = None
        P = None
        if isinstance(witness, dict):
            m = int(witness.get('m', 0))
            P = witness.get('P', None)
        elif isinstance(witness, (list, tuple)) and len(witness) >= 2:
            m = int(witness[0])
            P = witness[1]
        elif hasattr(witness, 'm') and hasattr(witness, 'P'):
            m = int(witness.m)
            P = witness.P
        elif isinstance(witness, sympy.Poly):
            P = witness
            domain = witness.domain
            if hasattr(domain, 'mod'):
                m = int(domain.mod)
            elif hasattr(domain, 'order'):
                m = int(domain.order)
            else:
                m = 0
        else:
            return [False, False]
            
        if m is None or m < 2 or P is None:
            return [False, False]
            
        if not isinstance(P, sympy.Expr) and not isinstance(P, sympy.Poly):
            P = sympy.sympify(P)
            
        if isinstance(P, sympy.Poly):
            P_poly = P
        else:
            P_poly = sympy.Poly(P, x)
            
        coeffs = P_poly.all_coeffs()
        
        coeffs_int = []
        for c in coeffs:
            if hasattr(c, 'rep'):
                val = int(c.rep)
            else:
                val = int(c)
            coeffs_int.append(val % m)
            
        coeffs_int.reverse()
        
        while len(coeffs_int) < 2:
            coeffs_int.append(0)
            
        a1 = coeffs_int[1]
        
        if sympy.gcd(a1, m) == 1:
            primes = list(sympy.ntheory.factorint(m).keys())
            is_auto = True
            for i in range(2, len(coeffs_int)):
                for p in primes:
                    if coeffs_int[i] % p != 0:
                        is_auto = False
                        break
                if not is_auto:
                    break
            h1 = is_auto
            
        is_linear = True
        for i in range(2, len(coeffs_int)):
            if coeffs_int[i] % m != 0:
                is_linear = False
                break
                
        neg_q = not is_linear
        
    except Exception:
        pass
        
    return [h1, neg_q]