import sympy
from sympy import S, ImageSet, FiniteSet, Lambda

# Top-level setup: named object bindings that the witness expression may reference.
Z = S.Integers
Q = S.Rationals

def extract_witness(witness):
    """
    Flexibly extract R, K, I, J from the witness.
    Supports dicts and tuples of varying lengths.
    """
    if isinstance(witness, dict):
        R = witness.get('R', S.Integers)
        K = witness.get('K', S.Rationals)
        I = witness.get('I')
        J = witness.get('J')
        return R, K, I, J
    elif isinstance(witness, (tuple, list)):
        if len(witness) >= 4:
            return witness[0], witness[1], witness[2], witness[3]
        elif len(witness) == 3:
            # Assume (R, I, J) with K implicitly Q
            return witness[0], S.Rationals, witness[1], witness[2]
        elif len(witness) == 2:
            # Assume (I, J) with R implicitly Z and K implicitly Q
            return S.Integers, S.Rationals, witness[0], witness[1]
    return None, None, None, None

def is_integral_domain(R):
    if isinstance(R, str): 
        R = R.strip().upper()
    return R in (S.Integers, S.Rationals, S.Reals, S.Complexes, 'Z', 'Q', 'R', 'C')

def is_field_of_fractions(K, R):
    if isinstance(R, str): R = R.strip().upper()
    if isinstance(K, str): K = K.strip().upper()
    
    if R in (S.Integers, 'Z') and K in (S.Rationals, 'Q'):
        return True
    if R in (S.Rationals, 'Q') and K in (S.Rationals, 'Q'):
        return True
    if R in (S.Reals, 'R') and K in (S.Reals, 'R'):
        return True
    if R in (S.Complexes, 'C') and K in (S.Complexes, 'C'):
        return True
    return False

def is_fractional_ideal(M, R):
    if isinstance(R, str):
        R = R.strip().upper()
    if isinstance(M, str):
        M = M.strip().upper()
        
    if R == S.Integers or R == 'Z':
        if M == S.Integers or M == 'Z':
            return True
        if M == S.Rationals or M == 'Q':
            return False
        if M in (S.Reals, S.Complexes) or M in ('R', 'C'):
            return False
        if isinstance(M, (set, frozenset)) and list(M) == [0]:
            return True
        if getattr(M, 'is_FiniteSet', False) and list(M) == [0]:
            return True
        if M == '0' or M == '{0}':
            return True
        if isinstance(M, ImageSet) and M.base_set == S.Integers:
            return True
    return False

def product_of_modules(I, J):
    if isinstance(I, str): I = I.strip().upper()
    if isinstance(J, str): J = J.strip().upper()
    
    if I in (S.Rationals, 'Q') and J in (S.Integers, 'Z'):
        return S.Rationals
    if I in (S.Integers, 'Z') and J in (S.Rationals, 'Q'):
        return S.Rationals
    if I in (S.Rationals, 'Q') and J in (S.Rationals, 'Q'):
        return S.Rationals
    if I in (S.Integers, 'Z') and J in (S.Integers, 'Z'):
        return S.Integers
        
    def is_zero(M):
        if isinstance(M, str) and M in ('0', '{0}'): return True
        return (isinstance(M, (set, frozenset)) and list(M) == [0]) or \
               (getattr(M, 'is_FiniteSet', False) and list(M) == [0])
               
    if is_zero(I) or is_zero(J):
        return {0}
        
    if isinstance(I, ImageSet) and I.base_set == S.Integers and J in (S.Integers, 'Z'):
        return I
    if isinstance(J, ImageSet) and J.base_set == S.Integers and I in (S.Integers, 'Z'):
        return J
        
    return None

def conditions(witness) -> list[bool]:
    R, K, I, J = extract_witness(witness)
    
    try:
        h1 = is_integral_domain(R)
    except Exception:
        h1 = False
        
    try:
        h2 = is_field_of_fractions(K, R)
    except Exception:
        h2 = False
        
    try:
        h3 = is_fractional_ideal(J, R)
    except Exception:
        h3 = False
        
    try:
        IJ = product_of_modules(I, J)
        if IJ is None:
            neg_q = False
        else:
            neg_q = not is_fractional_ideal(IJ, R)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: K is the field of fractions of R",
    "H_3: J is a fractional ideal of R",
    "¬Q: The product IJ is not a fractional ideal of R"
]

N_HYP = 3
NEG_Q_INDEX = 3