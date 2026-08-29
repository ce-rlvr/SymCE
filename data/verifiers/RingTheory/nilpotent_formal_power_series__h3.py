import sympy
from sympy.abc import x
from sympy.ntheory import factorint

Z = sympy.S.Integers
Q = sympy.S.Rationals
R = sympy.S.Reals
C = sympy.S.Complexes

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            ring_or_n, coeffs_raw = witness
            
            if str(ring_or_n) in ['ZZ', 'QQ', 'RR', 'CC'] or ring_or_n in [sympy.S.Integers, sympy.S.Reals, sympy.S.Complexes, sympy.S.Rationals]:
                n = 0
            else:
                try:
                    n = int(ring_or_n)
                except Exception:
                    n = 0
                    
            if isinstance(coeffs_raw, list):
                coeffs = coeffs_raw
            elif isinstance(coeffs_raw, dict):
                coeffs = list(coeffs_raw.values())
            else:
                try:
                    coeffs = list(sympy.Poly(coeffs_raw, x).all_coeffs())
                except Exception:
                    coeffs = [coeffs_raw]
        elif isinstance(witness, list):
            n = 0
            coeffs = witness
        elif isinstance(witness, dict):
            n = 0
            coeffs = list(witness.values())
        else:
            n = 0
            try:
                coeffs = list(sympy.Poly(witness, x).all_coeffs())
            except Exception:
                coeffs = [witness]
                
        n = int(n)
        coeffs = [int(c) for c in coeffs]
        
        h1 = (n >= 0)
        h2 = True
        
        for c in coeffs:
            if n == 0:
                if c != 0:
                    neg_q = True
                    break
            elif n == 1:
                pass
            else:
                c_mod = c % n
                factors = factorint(n)
                is_nilp = True
                for p in factors:
                    if c_mod % p != 0:
                        is_nilp = False
                        break
                if not is_nilp:
                    neg_q = True
                    break
                    
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: f is an element of the formal power series ring over R",
    "not Q: There exists i >= 0 such that a_i is not a nilpotent element of R"
]

N_HYP = 2
NEG_Q_INDEX = 2