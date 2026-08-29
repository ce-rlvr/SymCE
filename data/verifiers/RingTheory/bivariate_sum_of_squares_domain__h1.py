import sympy
from sympy import isprime, Integer

Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z7 = 7
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, str):
            s = witness.replace('_', '')
            if s.startswith('Z') and s[1:].isdigit():
                witness = int(s[1:])
                
        if isinstance(witness, (int, Integer)):
            n = int(witness)
            if n <= 1:
                return [False, False]
            
            h1 = True
            is_domain = isprime(n)
            has_sqrt_minus_1 = any((a**2 + 1) % n == 0 for a in range(n))
            
            lhs = is_domain and not has_sqrt_minus_1
            rhs = not has_sqrt_minus_1
            neg_q = (lhs != rhs)
            
            return [h1, neg_q]
            
        elif hasattr(witness, 'is_IntegralDomain'):
            h1 = True
            is_domain = witness.is_IntegralDomain
            if is_domain is None:
                is_domain = getattr(witness, 'is_Field', False)
            
            if witness in (sympy.ZZ, sympy.QQ, sympy.RR):
                has_sqrt_minus_1 = False
            elif witness == sympy.CC:
                has_sqrt_minus_1 = True
            elif hasattr(witness, 'order'):
                q = witness.order
                has_sqrt_minus_1 = (q % 4 == 1) or (q % 2 == 0)
            else:
                has_sqrt_minus_1 = False
                
            lhs = is_domain and not has_sqrt_minus_1
            rhs = not has_sqrt_minus_1
            neg_q = (lhs != rhs)
            
            return [h1, neg_q]
            
        else:
            return [False, False]
            
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: F is a commutative ring",
    "¬Q: factor ring is an integral domain iff no a in F has a^2 = -1 FAILS"
]

N_HYP = 1
NEG_Q_INDEX = 1