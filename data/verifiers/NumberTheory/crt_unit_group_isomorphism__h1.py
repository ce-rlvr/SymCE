import sympy
import math

# Top-level setup
# No special named bindings needed for this NumberTheory conjecture.

def get_prime_powers(m):
    """
    Returns a sorted list of prime power orders of the cyclic components
    of the unit group (Z/mZ)^x.
    Raises ValueError if m <= 0, as the unit group is typically considered
    undefined or empty in the context of this elementary theorem when m <= 0.
    """
    if m <= 0:
        raise ValueError("Undefined for m <= 0")
    if m == 1:
        return []
        
    factors = sympy.factorint(m)
    invs = []
    for p, k in factors.items():
        if p == 2:
            if k == 1:
                pass
            elif k == 2:
                invs.append(2)
            else:
                invs.extend([2, 2**(k-2)])
        else:
            invs.append(p**(k-1) * (p - 1))
    
    prime_powers = []
    for order in invs:
        if order == 1:
            continue
        for q, j in sympy.factorint(order).items():
            prime_powers.append(q**j)
            
    return sorted(prime_powers)

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False]
        m1, m2 = witness
    except Exception:
        return [False, False]
    
    # Hypothesis 1: gcd(m1, m2) == 1
    try:
        h1 = (math.gcd(int(m1), int(m2)) == 1)
    except Exception:
        h1 = False
        
    # Conclusion: The unit group (Z/(m1*m2)Z)^x is isomorphic to (Z/m1Z)^x x (Z/m2Z)^x
    try:
        pp_m1m2 = get_prime_powers(int(m1 * m2))
        pp_m1 = get_prime_powers(int(m1))
        pp_m2 = get_prime_powers(int(m2))
        
        pp_prod = sorted(pp_m1 + pp_m2)
        
        is_iso = (pp_m1m2 == pp_prod)
        neg_q = not is_iso
    except Exception:
        # If get_prime_powers raises ValueError (e.g., for m <= 0), the unit group
        # is undefined/empty, so the isomorphism statement fails.
        neg_q = True
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: gcd(m1, m2) = 1",
    "¬Q: The unit group (Z/(m1*m2)Z)^x is NOT isomorphic to (Z/m1Z)^x x (Z/m2Z)^x"
]

N_HYP = 1
NEG_Q_INDEX = 1