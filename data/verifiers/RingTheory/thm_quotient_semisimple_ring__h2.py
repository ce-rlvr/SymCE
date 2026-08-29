import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z
from sympy.ntheory import factorint

def is_square_free(n):
    if n == 0:
        return True
    factors = factorint(abs(n))
    return all(exp == 1 for exp in factors.values())

def evaluate_witness(witness):
    R_is_semisimple = False
    quotient_is_semisimple = True
    
    try:
        # Case 1: witness is a single integer (representing R=ZZ, I=n*ZZ)
        if isinstance(witness, int) or (hasattr(witness, 'is_Integer') and witness.is_Integer):
            n = abs(int(witness))
            R_is_semisimple = True
            quotient_is_semisimple = is_square_free(n)
            return R_is_semisimple, quotient_is_semisimple
            
        # Case 2: witness is a tuple (R, I)
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            R, I = witness
            
            if R == ZZ or str(R) in ('ZZ', 'Integers'):
                R_is_semisimple = True
                if isinstance(I, int) or (hasattr(I, 'is_Integer') and I.is_Integer):
                    n = abs(int(I))
                    quotient_is_semisimple = is_square_free(n)
                elif hasattr(I, 'gen'):
                    n = abs(int(I.gen))
                    quotient_is_semisimple = is_square_free(n)
                else:
                    n = abs(int(I))
                    quotient_is_semisimple = is_square_free(n)
                return R_is_semisimple, quotient_is_semisimple
                
            if R == QQ or str(R) in ('QQ', 'Rationals'):
                R_is_semisimple = True
                quotient_is_semisimple = True
                return R_is_semisimple, quotient_is_semisimple
                
            # Polynomial rings over fields are Jacobson semisimple
            if hasattr(R, 'is_PolynomialRing') or 'Poly' in str(type(R)):
                R_is_semisimple = True
                try:
                    from sympy import sqf_list
                    factors = sqf_list(I)[1]
                    quotient_is_semisimple = all(p == 1 for f, p in factors)
                except Exception:
                    quotient_is_semisimple = True
                return R_is_semisimple, quotient_is_semisimple

        # Case 3: witness is a sympy expression (representing R=k[x], I=(witness))
        if hasattr(witness, 'free_symbols') and witness.free_symbols:
            from sympy import sqf_list
            try:
                factors = sqf_list(witness)[1]
                quotient_is_semisimple = all(p == 1 for f, p in factors)
                R_is_semisimple = True
                return R_is_semisimple, quotient_is_semisimple
            except Exception:
                pass

    except Exception:
        pass
        
    return R_is_semisimple, quotient_is_semisimple

def conditions(witness) -> list[bool]:
    try:
        R_is_semisimple, quotient_is_semisimple = evaluate_witness(witness)
    except Exception:
        R_is_semisimple = False
        quotient_is_semisimple = True

    return [R_is_semisimple, not quotient_is_semisimple]

CONDITION_LABELS = [
    "H_1: R is a semisimple ring",
    "¬Q: The quotient ring R/I is not a semisimple ring"
]

N_HYP = 1
NEG_Q_INDEX = 1