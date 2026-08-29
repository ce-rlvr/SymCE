import sympy
from sympy import ZZ, QQ, Symbol, S

# Top-level setup for witness expressions
x = Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "In a reduced commutative ring, every ideal is the zero ideal."
    
    The witness should be a tuple (R, I) where:
      - R is a SymPy domain or set representing a reduced commutative ring (e.g., ZZ).
      - I is an ideal represented by a list of generators, a single generator, or a SymPy Ideal object.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    try:
        # H_1: R is a reduced commutative ring
        # We accept standard integral domains and fields, which are reduced and commutative.
        if R in (S.Integers, S.Rationals, S.Reals, S.Complexes, ZZ, QQ):
            h1 = True
        elif getattr(R, 'is_Field', False) or getattr(R, 'is_domain', False):
            h1 = True
        else:
            name = type(R).__name__
            h1 = ('Ring' in name or 'Field' in name or 'Domain' in name)
    except Exception:
        h1 = False
        
    try:
        # H_2: I is an ideal of R
        if hasattr(I, 'gens'):
            gens = I.gens
        elif isinstance(I, (list, tuple, set)):
            gens = I
        else:
            gens = [I]
            
        if hasattr(I, 'ring'):
            h2 = bool(I.ring == R)
        else:
            h2 = all(e in R for e in gens)
    except Exception:
        h2 = False
        
    try:
        # ¬Q: The ideal I is not the zero ideal
        if hasattr(I, 'gens'):
            gens = I.gens
        elif isinstance(I, (list, tuple, set)):
            gens = I
        else:
            gens = [I]
            
        zero = getattr(R, 'zero', 0)
        neg_q = any(e != zero for e in gens)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a reduced commutative ring",
    "H_2: I is an ideal of R",
    "¬Q: The ideal I is not the zero ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2