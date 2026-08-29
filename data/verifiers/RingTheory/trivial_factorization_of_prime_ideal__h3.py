import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

# Top-level setup for potential witness references
ZZ = sympy.ZZ
QQ = sympy.QQ
Z = sympy.ZZ
Q = sympy.QQ

def get_val(witness, key, idx, default=None):
    """Helper to extract values from various witness formats (dict, object, tuple)."""
    if isinstance(witness, dict):
        if key in witness:
            return witness[key]
        if default is not None:
            return default
        raise ValueError(f"Key {key} not found")
        
    if hasattr(witness, key):
        return getattr(witness, key)
        
    if isinstance(witness, (tuple, list)):
        if len(witness) == 3:
            # Assume format is (P, I, J)
            if key == 'R': return default if default is not None else ZZ
            if key == 'P': return witness[0]
            if key == 'I': return witness[1]
            if key == 'J': return witness[2]
        elif len(witness) >= 4:
            # Assume format is (R, P, I, J)
            if len(witness) > idx:
                return witness[idx]
                
    if default is not None:
        return default
        
    raise ValueError(f"Could not extract {key}")

def conditions(witness) -> list[bool]:
    # H_1: R is a commutative ring
    h1 = False
    try:
        if callable(getattr(witness, "is_commutative_ring", None)):
            h1 = bool(witness.is_commutative_ring())
        else:
            R = get_val(witness, 'R', 0, ZZ)
            if hasattr(R, 'is_commutative'):
                h1 = bool(R.is_commutative)
            elif R == 'Z' or R == ZZ or R == QQ:
                h1 = True
            else:
                h1 = True  # Assume commutative if not explicitly specified but valid
    except Exception:
        pass

    # H_2: P is a prime ideal of R
    h2 = False
    try:
        if callable(getattr(witness, "is_prime_ideal", None)):
            h2 = bool(witness.is_prime_ideal())
        else:
            P = get_val(witness, 'P', 1)
            if hasattr(P, 'is_prime_ideal'):
                if callable(P.is_prime_ideal):
                    h2 = bool(P.is_prime_ideal())
                else:
                    h2 = bool(P.is_prime_ideal)
            elif hasattr(P, 'is_prime'):
                if callable(P.is_prime):
                    h2 = bool(P.is_prime())
                else:
                    h2 = bool(P.is_prime)
            else:
                try:
                    h2 = sympy.isprime(abs(P))
                except Exception:
                    h2 = sympy.isprime(P)
    except Exception:
        pass

    # H_3: The product ideal IJ is equal to P
    h3 = False
    try:
        if callable(getattr(witness, "is_product_ideal_equal", None)):
            h3 = bool(witness.is_product_ideal_equal())
        else:
            P = get_val(witness, 'P', 1)
            I = get_val(witness, 'I', 2)
            J = get_val(witness, 'J', 3)
            
            prod = I * J
            if prod == P:
                h3 = True
            elif hasattr(prod, 'equals') and callable(prod.equals) and prod.equals(P):
                h3 = True
            else:
                try:
                    if abs(prod) == abs(P):
                        h3 = True
                except Exception:
                    pass
                if not h3:
                    try:
                        if sympy.simplify(prod - P) == 0:
                            h3 = True
                        elif sympy.simplify(prod + P) == 0:
                            h3 = True
                    except Exception:
                        pass
    except Exception:
        pass

    # ¬Q: I != P and J != P
    neg_q = False
    try:
        if callable(getattr(witness, "neg_q", None)):
            neg_q = bool(witness.neg_q())
        elif callable(getattr(witness, "conclusion_fails", None)):
            neg_q = bool(witness.conclusion_fails())
        else:
            P = get_val(witness, 'P', 1)
            I = get_val(witness, 'I', 2)
            J = get_val(witness, 'J', 3)
            
            def equals_P(X, P_val):
                try:
                    if X == P_val: return True
                except Exception:
                    pass
                try:
                    if hasattr(X, 'equals') and callable(X.equals) and X.equals(P_val): return True
                except Exception:
                    pass
                try:
                    if abs(X) == abs(P_val): return True
                except Exception:
                    pass
                try:
                    if sympy.simplify(X - P_val) == 0: return True
                    if sympy.simplify(X + P_val) == 0: return True
                except Exception:
                    pass
                return False
            
            neg_q = not (equals_P(I, P) or equals_P(J, P))
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: P is a prime ideal of R",
    "H_3: The product ideal IJ is equal to P",
    "¬Q: I != P and J != P"
]

N_HYP = 3
NEG_Q_INDEX = 3