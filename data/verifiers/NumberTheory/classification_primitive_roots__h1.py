import sympy
from sympy.ntheory import totient, factorint
import math

# Top-level setup
# No named bindings needed for Number Theory

def is_int_like(val):
    if isinstance(val, int):
        return True
    if hasattr(val, 'is_integer'):
        if callable(val.is_integer):
            return val.is_integer()
        else:
            return bool(val.is_integer)
    return False

def is_in_primitive_root_set(m):
    if m in (1, 2, 4):
        return True
    if m <= 0:
        return False
    if m % 2 == 0:
        m_test = m // 2
    else:
        m_test = m
    if m_test % 2 == 0 or m_test == 1:
        return False
    factors = factorint(m_test)
    if len(factors) == 1:
        p = list(factors.keys())[0]
        if p % 2 == 1:
            return True
    return False

def conditions(witness) -> list[bool]:
    try:
        if not is_int_like(witness):
            return [False]
        n = int(witness)
        
        if n == 0:
            has_prim = False
        else:
            n_abs = abs(n)
            if n_abs == 1:
                has_prim = True
            elif n_abs > 10000:
                # Fallback to the theorem for large numbers to ensure fast execution
                has_prim = is_in_primitive_root_set(n_abs)
            else:
                phi = int(totient(n_abs))
                factors = factorint(phi)
                has_prim = False
                for i in range(1, n_abs):
                    if math.gcd(i, n_abs) == 1:
                        is_prim = True
                        for q in factors.keys():
                            if pow(i, phi // q, n_abs) == 1:
                                is_prim = False
                                break
                        if is_prim:
                            has_prim = True
                            break
                            
        in_s = is_in_primitive_root_set(n)
        
        # The conclusion is an equivalence (A iff B). It fails when A != B.
        neg_q = bool(has_prim != in_s)
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: The equivalence between having a primitive root and being in the set {1, 2, 4, p^k, 2p^k} fails"
]

N_HYP = 0
NEG_Q_INDEX = 0