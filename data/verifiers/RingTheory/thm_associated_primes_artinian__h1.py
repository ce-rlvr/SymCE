import sympy
from sympy import abc

Z = sympy.S.Integers
Q = sympy.S.Rationals

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        # Unpack tuple if witness is provided as (Ring, Ideal)
        if isinstance(witness, tuple) and len(witness) == 2:
            ring, ideal = witness
            witness = ideal
    except Exception:
        pass

    try:
        if isinstance(witness, (int, sympy.Integer)):
            # Witness is an integer representing the ideal pZ in Z
            p = abs(int(witness))
            if p == 0:
                # (0) is a prime ideal in Z, and it IS an associated prime (Ann(1) = (0))
                h1 = True
                neg_q = False
            else:
                # (p) is a prime ideal iff p is prime
                h1 = sympy.isprime(p)
                # In the domain Z, no non-zero ideal is an associated prime
                neg_q = True
                
        elif isinstance(witness, (sympy.Poly, sympy.Expr)):
            # Witness is a polynomial representing an ideal in a polynomial ring
            poly = sympy.Poly(witness)
            if poly.is_zero:
                h1 = True
                neg_q = False
            else:
                h1 = bool(poly.is_irreducible)
                # In a polynomial domain, no non-zero principal ideal is an associated prime
                neg_q = True
                
        elif hasattr(witness, 'is_prime'):
            # Fallback for SymPy ideal objects
            h1_val = witness.is_prime
            if callable(h1_val):
                h1_val = h1_val()
            if h1_val is not None:
                h1 = bool(h1_val)
            
            is_z = False
            if hasattr(witness, 'is_zero'):
                is_z_val = witness.is_zero
                if callable(is_z_val):
                    is_z_val = is_z_val()
                if is_z_val is not None:
                    is_z = bool(is_z_val)
            
            # Assuming the ring is a domain, it's an associated prime iff it's the zero ideal
            neg_q = not is_z
            
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P is a prime ideal of R",
    "¬Q: P is not an associated prime ideal of R"
]

N_HYP = 1
NEG_Q_INDEX = 1