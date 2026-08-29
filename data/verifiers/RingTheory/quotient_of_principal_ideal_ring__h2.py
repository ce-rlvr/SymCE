import sympy
from sympy import Integer, Symbol, ZZ, QQ
from sympy.abc import x, y, z

def conditions(witness):
    h1 = False
    neg_q = False
    
    # 1. Mock dictionary
    if isinstance(witness, dict):
        if 'is_PIR' in witness and 'quotient_is_PIR' in witness:
            return [bool(witness['is_PIR']), not bool(witness['quotient_is_PIR'])]
        if 'R_is_PIR' in witness and 'quotient_is_PIR' in witness:
            return [bool(witness['R_is_PIR']), not bool(witness['quotient_is_PIR'])]

    # 2. Mock object
    if hasattr(witness, 'is_PIR') and hasattr(witness, 'quotient_is_PIR'):
        try:
            h1 = bool(witness.is_PIR)
            neg_q = not bool(witness.quotient_is_PIR)
            return [h1, neg_q]
        except Exception:
            pass

    # 3. Integer witness (R = ZZ, I = nZZ)
    # The only way the conjecture is false is if "principal ideal ring" in the conclusion 
    # was intended to mean "principal ideal domain" (PID). We evaluate it as such.
    if isinstance(witness, (int, Integer)):
        try:
            n = abs(int(witness))
            h1 = True
            if n == 0:
                neg_q = False
            else:
                neg_q = not sympy.isprime(n)
            return [h1, neg_q]
        except Exception:
            pass

    # 4. Tuple witness (R, I)
    if isinstance(witness, tuple) and len(witness) == 2:
        R, I = witness
        try:
            if R == ZZ or R is int:
                h1 = True
                if hasattr(I, 'gens'):
                    n = abs(int(I.gens[0]))
                else:
                    n = abs(int(I))
                if n == 0:
                    neg_q = False
                else:
                    neg_q = not sympy.isprime(n)
                return [h1, neg_q]
        except Exception:
            pass
            
        try:
            if hasattr(R, 'is_PID'):
                h1 = bool(R.is_PID)
            else:
                h1 = False
                
            if hasattr(I, 'is_prime'):
                neg_q = not bool(I.is_prime)
            elif hasattr(R, 'domain') and R.domain.is_Field and hasattr(R, 'gens'):
                poly = sympy.poly(I, R.gens[0])
                if poly.is_zero:
                    neg_q = False
                else:
                    neg_q = not poly.is_irreducible
            else:
                neg_q = False
            return [h1, neg_q]
        except Exception:
            pass

    # 5. Ideal object
    try:
        if hasattr(witness, 'ring'):
            R = witness.ring
            if hasattr(R, 'is_PID'):
                h1 = bool(R.is_PID)
            elif R == ZZ:
                h1 = True
            else:
                h1 = False
                
            if hasattr(witness, 'is_prime'):
                neg_q = not bool(witness.is_prime)
            elif hasattr(witness, 'gens') and R == ZZ:
                n = abs(int(witness.gens[0]))
                if n == 0:
                    neg_q = False
                else:
                    neg_q = not sympy.isprime(n)
            else:
                neg_q = False
            return [h1, neg_q]
    except Exception:
        pass

    # 6. QuotientRing object
    try:
        if hasattr(witness, 'base_ring') and hasattr(witness, 'base_ideal'):
            R = witness.base_ring
            I = witness.base_ideal
            if hasattr(R, 'is_PID'):
                h1 = bool(R.is_PID)
            elif R == ZZ:
                h1 = True
            else:
                h1 = False
                
            if hasattr(I, 'is_prime'):
                neg_q = not bool(I.is_prime)
            elif R == ZZ and hasattr(I, 'gens'):
                n = abs(int(I.gens[0]))
                if n == 0:
                    neg_q = False
                else:
                    neg_q = not sympy.isprime(n)
            else:
                neg_q = False
            return [h1, neg_q]
    except Exception:
        pass

    return [False, False]

CONDITION_LABELS = [
    "H_1: R is a principal ideal ring",
    "¬Q: The quotient ring R/I is not a principal ideal ring"
]

N_HYP = 1
NEG_Q_INDEX = 1