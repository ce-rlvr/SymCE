import sympy
from sympy import Poly, ZZ, QQ, RR, CC
from sympy.ntheory import factorint
import math

def to_int(c):
    try:
        if hasattr(c, 'to_int'):
            return c.to_int()
        return int(c)
    except Exception:
        return 0

def is_unit(a, domain):
    if a == domain.zero:
        return False
    if hasattr(domain, 'is_Field') and domain.is_Field:
        return True
    if domain == ZZ:
        return a in [1, -1]
    if hasattr(domain, 'mod'):
        try:
            return math.gcd(to_int(a), int(domain.mod)) == 1
        except Exception:
            return False
    if domain in [QQ, RR, CC]:
        return True
    try:
        return domain.invert(a) is not None
    except Exception:
        pass
    return False

def is_nilpotent(c, domain):
    if c == domain.zero:
        return True
    if hasattr(domain, 'is_Field') and domain.is_Field:
        return False
    if domain == ZZ:
        return False
    if hasattr(domain, 'mod'):
        try:
            n = int(domain.mod)
            factors = factorint(n)
            val = to_int(c)
            for p in factors:
                if val % p != 0:
                    return False
            return True
        except Exception:
            return False
    return False

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            if hasattr(witness[0], 'is_Commutative'):
                domain = witness[0]
                f = witness[1]
            else:
                domain = witness[1]
                f = witness[0]
            if not isinstance(f, Poly):
                f = Poly(f, domain=domain)
        else:
            if not isinstance(witness, Poly):
                f = Poly(witness)
            else:
                f = witness
            domain = f.domain
            
        h1 = True
        if hasattr(domain, 'is_Commutative') and not domain.is_Commutative:
            h1 = False
            
        h2 = True
        
        coeffs = f.all_coeffs()
        if not coeffs:
            a0 = domain.zero
        else:
            a0 = coeffs[-1]
            
        a0_unit = is_unit(a0, domain)
        
        f_unit = a0_unit
        if f_unit:
            for c in coeffs[:-1]:
                if not is_nilpotent(c, domain):
                    f_unit = False
                    break
                    
        conclusion = (f_unit == a0_unit)
        neg_q = not conclusion
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: R power series ring is the ring of formal power series over R",
    "~Q: f(x) is a unit in the power series ring if and only if a_0 is a unit in R fails"
]

N_HYP = 2
NEG_Q_INDEX = 2