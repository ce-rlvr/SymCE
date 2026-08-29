import sympy
from sympy import Poly
from sympy.abc import x, y, z
from sympy import Rational, Integer
from sympy.polys.domains import ZZ, QQ, RR, CC

def conditions(witness):
    H1 = False
    neg_Q = False
    
    try:
        if isinstance(witness, (list, set, tuple)):
            is_valid_S = True
            polys = []
            
            for p in witness:
                try:
                    poly = Poly(p)
                    if len(poly.free_symbols) > 1:
                        is_valid_S = False
                        break
                    polys.append(poly)
                except Exception:
                    is_valid_S = False
                    break
            
            if is_valid_S:
                H1 = True
                
                domain_is_field = True
                has_zero = False
                
                domains = set(poly.domain for poly in polys)
                if len(domains) == 1:
                    domain = domains.pop()
                    if not getattr(domain, 'is_Field', False):
                        domain_is_field = False
                elif len(domains) > 1:
                    domain_is_field = False
                        
                for poly in polys:
                    if poly.is_zero:
                        has_zero = True
                        
                if not domain_is_field or has_zero:
                    neg_Q = True
    except Exception:
        pass
        
    return [H1, neg_Q]

CONDITION_LABELS = [
    "H_1: S is a set of univariate polynomials over F",
    "¬Q: The conclusion fails"
]

N_HYP = 1
NEG_Q_INDEX = 1