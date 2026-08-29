import sympy
from sympy import ZZ, QQ, Symbol, S
from sympy.polys.domains.ring import Ring
from sympy.polys.domains.field import Field

x = Symbol('x')

def conditions(witness):
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (R, I, J) where:
      - R is a SymPy domain (e.g., ZZ)
      - I and J are lists of generators for the ideals in R
    """
    try:
        R, I, J = witness
    except Exception:
        return [False, False, False, False]
        
    # Normalize S.Integers to the ZZ domain for consistency
    if R == S.Integers:
        R = ZZ
        
    # H_1: R is a commutative ring
    try:
        h1 = isinstance(R, Ring) or isinstance(R, Field)
        if hasattr(R, 'is_commutative'):
            h1 = h1 and R.is_commutative
    except Exception:
        h1 = False
        
    # H_2: I is an ideal of R
    try:
        if hasattr(I, 'is_Ideal') and I.is_Ideal:
            h2 = True
        else:
            h2 = isinstance(I, (list, tuple, set)) and all(e in R for e in I)
    except Exception:
        h2 = False
        
    # H_3: J is an ideal of R
    try:
        if hasattr(J, 'is_Ideal') and J.is_Ideal:
            h3 = True
        else:
            h3 = isinstance(J, (list, tuple, set)) and all(e in R for e in J)
    except Exception:
        h3 = False
        
    # ¬Q: Both I and J are invertible ideals (Conclusion fails -> at least one is not invertible)
    try:
        def is_invertible(ring, ideal):
            if hasattr(ideal, 'is_Ideal') and ideal.is_Ideal:
                if hasattr(ideal, 'is_invertible'):
                    return ideal.is_invertible
                gens = ideal.gens
            else:
                gens = ideal
                
            # An ideal is invertible if it is non-zero and satisfies invertibility conditions.
            # In Dedekind domains (like ZZ) or PIDs, any non-zero ideal is invertible.
            gens = [e for e in gens if e != ring.zero]
            if not gens:
                return False  # The zero ideal is never invertible
            if ring == ZZ:
                return True
            if hasattr(ring, 'is_Field') and ring.is_Field:
                return True
            if hasattr(ring, 'is_PID') and ring.is_PID:
                return True
            if len(gens) == 1 and hasattr(ring, 'is_Domain') and ring.is_Domain:
                return True
            raise ValueError("Cannot determine invertibility for this ideal in the given ring")
            
        inv_I = is_invertible(R, I)
        inv_J = is_invertible(R, J)
        neg_q = not (inv_I and inv_J)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "H_3: J is an ideal of R",
    "¬Q: At least one of I or J is not an invertible ideal"
]

N_HYP = 3
NEG_Q_INDEX = 3